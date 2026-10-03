"""Physical and numerical regression tests independent of optimizer success."""
from copy import deepcopy
from types import SimpleNamespace
import unittest
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp
import qutip as qt
from qoc.config import Experiment,Case,Target,from_dict
from qoc.models import build_model,cavity_target
from qoc.controls import Signal,logical_bounds,feasible_nodes,slew_constraint
from qoc.propagation import Objective,propagate_midpoint,continuous_evolution
from qoc.metrics import state_metrics,actuator_metrics
from qoc.optimizers import crab,grape
from qoc.validation import validate_waveform
from qoc.robustness import filter_scan,static_noise_ensemble
from qoc.dissipation import ohmic_spectrum,dressed_bath_evolution


def small_config(nq=1):
    cfg = Experiment(dimension=6,duration=2.,intervals=40)
    cfg.cases = [Case("test",[.3]*nq,[2.]*nq)]
    cfg.target = Target("fock",2)
    cfg.control.nodes = 6
    cfg.validation.dimension_increment = 4
    cfg.validation.trajectory_points = 31
    cfg.validation.phase_grid_points = 41
    cfg.validation.edge_levels = 2
    cfg.optimization.seeds = [3]
    cfg.optimization.frequencies = 2
    cfg.optimization.crab_max_evaluations = 18
    cfg.optimization.grape_max_iterations = 3
    cfg.optimization.grape_max_evaluations = 6
    return cfg.validate()


class ConfigurationTests(unittest.TestCase):
    def test_round_trip(self):
        cfg = small_config()
        self.assertEqual(cfg.to_dict(),from_dict(cfg.to_dict()).to_dict())

    def test_unknown_field(self):
        with self.assertRaises(ValueError):
            from_dict({"duraton":1})

    def test_invalid_fock(self):
        for value in [-1,1.2,99]:
            cfg=small_config();cfg.target.value=value
            with self.assertRaises(ValueError):cfg.validate()

    def test_invalid_types_and_infinities(self):
        for value in [3.5,True]:
            cfg=small_config();cfg.control.nodes=value
            with self.assertRaises(ValueError):cfg.validate()
        cfg=small_config();cfg.duration=float("inf")
        with self.assertRaises(ValueError):cfg.validate()

    def test_bounds_and_baseline(self):
        cfg=small_config();cfg.cases[0].qubit_frequencies=[4.]
        with self.assertRaises(ValueError):cfg.validate()

    def test_dB_conversion(self):
        a=cavity_target(30,Target("squeezed",3.,.2,"dB"))
        b=cavity_target(30,Target("squeezed",3*np.log(10)/20,.2,"r"))
        np.testing.assert_allclose(a,b,atol=1e-14)

    def test_cat_components_and_small_alpha(self):
        for alpha in [1e-8,2.,5.]:
            target=cavity_target(60,Target("cat",alpha))
            self.assertAlmostEqual(np.linalg.norm(target),1)
            self.assertEqual(np.sum(abs(target[np.arange(60)%4!=2])**2),0.)
        a=2.;dim=40
        reference=(qt.coherent(dim,a)+qt.coherent(dim,-a)-qt.coherent(dim,1j*a)-qt.coherent(dim,-1j*a)).unit().full().ravel()
        self.assertGreater(abs(np.vdot(reference,cavity_target(dim,Target("cat",a))))**2,1-1e-12)


class ModelTests(unittest.TestCase):
    def test_differential_control_accesses_singlet(self):
        cfg=small_config(2);model=build_model(cfg,cfg.cases[0])
        _,common=propagate_midpoint(model,np.zeros((2,30)),2.)
        _,differential=propagate_midpoint(model,np.tile(np.array([[.4],[-.4]]),(1,30)),2.)
        self.assertLess(state_metrics(model,common)["singlet_population"],1e-12)
        self.assertGreater(state_metrics(model,differential)["singlet_population"],1e-6)

    def test_hermiticity_and_parity(self):
        cfg=small_config(2);cfg.parity_reduction=False;cfg.cases[0].direct_exchange=.1
        model=build_model(cfg,cfg.cases[0])
        par=np.diag((-1.)**(np.repeat(np.arange(6),4)+np.tile([0,1,1,2],6)))
        for h in [model.drift,*model.controls]:
            np.testing.assert_allclose(h,h.conj().T,atol=1e-14)
            np.testing.assert_allclose(h@par,par@h,atol=1e-14)

    def test_parity_reduction_matches_full(self):
        cfg=small_config(2);case=cfg.cases[0]
        reduced=build_model(cfg,case)
        cfg.parity_reduction=False;full=build_model(cfg,case)
        u=np.random.default_rng(8).uniform(-.4,.4,(2,19))
        pr,vr=propagate_midpoint(reduced,u,cfg.duration)
        pf,vf=propagate_midpoint(full,u,cfg.duration)
        np.testing.assert_allclose(reduced.expand(vr),vf,atol=1e-12)
        self.assertAlmostEqual(pr,pf,places=12)

    def test_zero_coupling_no_photons(self):
        cfg=small_config(2);cfg.cases[0].couplings=[0.,0.]
        model=build_model(cfg,cfg.cases[0]);u=np.ones((2,20))*.4
        _,state=propagate_midpoint(model,u,cfg.duration)
        self.assertAlmostEqual(state_metrics(model,state)["mean_photons"],0.,places=12)

    def test_second_decoupled_qubit_matches_one(self):
        cfg=small_config();one=build_model(cfg,cfg.cases[0])
        two=build_model(cfg,Case("2q",[.3,0.],[2.,2.]))
        u=np.sin(np.linspace(0,2,30))[None,:]*.2
        _,v1=propagate_midpoint(one,u,2.)
        _,v2=propagate_midpoint(two,np.vstack([u,u*.6]),2.)
        np.testing.assert_allclose(one.cavity_density(v1),two.cavity_density(v2),atol=1e-12)

    def test_common_matches_equal_independent(self):
        cfg=small_config(2);case=cfg.cases[0]
        independent=build_model(cfg,case)
        common_case=deepcopy(case);common_case.control="common"
        common=build_model(cfg,common_case)
        u=np.sin(np.linspace(0,3,25))[None,:]*.3
        p1,v1=propagate_midpoint(common,u,2.)
        p2,v2=propagate_midpoint(independent,np.vstack([u,u]),2.)
        np.testing.assert_allclose(v1,v2,atol=1e-12)
        self.assertAlmostEqual(p1,p2,places=12)

    def test_odd_fock_allowed_without_reset(self):
        cfg=small_config();cfg.target.value=1
        model=build_model(cfg,cfg.cases[0])
        probability,_=propagate_midpoint(model,np.zeros((1,20)),.5)
        self.assertGreater(probability,1e-4)
        cfg.target.reset_qubits=True
        with self.assertRaises(ValueError):build_model(cfg,cfg.cases[0])

    def test_ground_state_is_eigenstate(self):
        cfg=small_config(2);cfg.initial_state="ground"
        model=build_model(cfg,cfg.cases[0])
        energy=np.vdot(model.initial,model.drift@model.initial)
        np.testing.assert_allclose(model.drift@model.initial,energy*model.initial,atol=1e-12)

    def test_fidelity_conventions(self):
        cfg=small_config();model=build_model(cfg,cfg.cases[0])
        _,state=propagate_midpoint(model,np.zeros((1,15)),1.)
        m=state_metrics(model,state)
        self.assertAlmostEqual(m["fidelity_root"]**2,m["target_probability"],places=13)
        qf=qt.fidelity(qt.Qobj(model.target_cavity),qt.Qobj(model.cavity_density(state)))
        self.assertAlmostEqual(qf,m["cavity_fidelity_root"],places=7)


class SignalTests(unittest.TestCase):
    def test_linear_callback_and_map(self):
        u=np.array([[0.,1.,-.2,0.]])
        for cutoff in [None,.01,3.,100.]:
            s=Signal(3,4,cutoff);t=np.linspace(0,4,101)
            expected=s.values(u,t)
            actual=np.array([s.callback(u)(x) for x in t]).T
            np.testing.assert_allclose(actual,expected,atol=1e-13)

    def test_filtered_signal_against_independent_ode(self):
        u=np.array([[0.,.7,-.3,0.]])
        s=Signal(3,4,2.1);ts=np.linspace(0,4,201)
        def fun(t,y):
            command=np.interp(t,s.times,u[0],left=0,right=0)
            return 2.1*(command-y)
        sol=solve_ivp(fun,[0,4],[0.],t_eval=ts,atol=1e-11,rtol=1e-11,max_step=.005)
        np.testing.assert_allclose(s.values(u,ts),sol.y,atol=2e-9)

    def test_transfer_derivative(self):
        s=Signal(2,6,3);u=np.array([[0,.3,-.2,.4,.1,0.]])
        ts=np.array([.15,.55,1.25,1.8,2.1]);eps=1e-6
        finite=(s.values(u,ts+eps)-s.values(u,ts-eps))/(2*eps)
        exact=u@s.matrix(ts,True).T
        np.testing.assert_allclose(exact,finite,atol=1e-9)

    def test_crab_feasibility(self):
        raw=np.random.default_rng(1).normal(size=(2,10))*8
        v=feasible_nodes(raw,np.array([-1.,-.5]),np.array([.4,.8]),.7,.2)
        self.assertTrue(np.all(v>=[[-1.],[-.5]]))
        self.assertTrue(np.all(v<=[[.4],[.8]]))
        self.assertLessEqual(abs(np.diff(v)).max()/.2,.7+1e-12)
        np.testing.assert_array_equal(v[:,[0,-1]],0)

    def test_common_bounds_intersection(self):
        cfg=small_config(2);case=cfg.cases[0];case.control="common";case.qubit_frequencies=[1.,2.5]
        lo,hi=logical_bounds(build_model(cfg,case),cfg.control)
        np.testing.assert_allclose(lo,[-.5]);np.testing.assert_allclose(hi,[.5])

    def test_filter_retains_terminal_tail(self):
        s=Signal(2,3,1.);u=np.array([[0,1.,0.]])
        y=s.values(u,[2.,3.])[0]
        self.assertGreater(y[0],0)
        self.assertAlmostEqual(y[1]/y[0],np.exp(-1),places=12)


class GradientTests(unittest.TestCase):
    def test_duration_exactly_T(self):
        model=SimpleNamespace(initial=np.array([1,0],complex),drift=.5*np.array([[0,1],[1,0]]),
            controls=np.zeros((1,2,2)),target_operator=np.diag([0,1]))
        for n in [2,9,37]:
            p,v=propagate_midpoint(model,np.zeros((1,n)),1.3)
            self.assertAlmostEqual(p,np.sin(1.3/2)**2,places=13)

    def test_propagation_against_scipy_expm(self):
        cfg=small_config();model=build_model(cfg,cfg.cases[0]);u=np.ones((1,7))*.2
        _,v=propagate_midpoint(model,u,1.1)
        reference=expm(-1j*1.1*(model.drift+.2*model.controls[0]))@model.initial
        np.testing.assert_allclose(v,reference,atol=1e-12)

    def check_gradient(self,nq,common,filtered,regularization,slew=False):
        cfg=small_config(nq);cfg.intervals=7;cfg.control.nodes=5
        cfg.cases[0].control="common" if common else "independent"
        cfg.control.filter_cutoff=2. if filtered else None
        if regularization:
            cfg.control.fluence_weight=.03;cfg.control.slew_weight=.02
        model=build_model(cfg,cfg.cases[0]);s=Signal(cfg.duration,cfg.control.nodes,cfg.control.filter_cutoff)
        obj=Objective(model,s,cfg);x=np.random.default_rng(42).uniform(-.3,.3,obj.nfree)
        f,g=obj(x);eps=1e-6;numeric=np.zeros_like(g)
        for j in range(len(x)):
            a=x.copy();b=x.copy();a[j]+=eps;b[j]-=eps
            numeric[j]=(obj.evaluate_nodes(obj.unpack(a))[0]-obj.evaluate_nodes(obj.unpack(b))[0])/(2*eps)
        np.testing.assert_allclose(g,numeric,rtol=2e-5,atol=2e-9)

    def test_gradient_one_qubit_unfiltered(self):self.check_gradient(1,False,False,False)
    def test_gradient_two_qubits_filtered(self):self.check_gradient(2,False,True,False)
    def test_gradient_common_regularized(self):self.check_gradient(2,True,True,True)

    def test_gradient_degenerate_hamiltonian(self):
        # At H=0 all eigenvalues coincide; the Frechet derivative still exists.
        model=SimpleNamespace(initial=np.array([1,1j])/np.sqrt(2),drift=np.zeros((2,2)),
            controls=np.array([[[0,1],[1,0]]]),target_operator=np.diag([1,0]))
        p,v,g=propagate_midpoint(model,np.zeros((1,3)),.7,True)
        self.assertTrue(np.isfinite(g).all())
        eps=1e-6;u=np.zeros((1,3));u[0,1]=eps
        pp,_=propagate_midpoint(model,u,.7);pm,_=propagate_midpoint(model,-u,.7)
        self.assertAlmostEqual(g[0,1],(pp-pm)/(2*eps),places=8)

    def test_midpoint_converges_to_continuous(self):
        cfg=small_config();model=build_model(cfg,cfg.cases[0]);s=Signal(2,6,3.)
        nodes=np.array([[0,.3,-.2,.4,.1,0.]])
        ref=continuous_evolution(model,s,nodes,[0,2],1e-12,1e-12)[-1]
        errors=[]
        for n in [20,80]:
            _,v=propagate_midpoint(model,s.values(nodes,(np.arange(n)+.5)*2/n),2)
            errors.append(np.linalg.norm(v-ref))
        self.assertLess(errors[1],errors[0]/8)


class OptimizationValidationTests(unittest.TestCase):
    def test_crab_budget_and_reproducibility(self):
        cfg=small_config();model=build_model(cfg,cfg.cases[0]);obj=Objective(model,Signal(2,6,3),cfg)
        a=crab(obj,9);b=crab(obj,9)
        self.assertLessEqual(a.metadata["evaluations"],cfg.optimization.crab_max_evaluations)
        np.testing.assert_array_equal(a.nodes,b.nodes)
        np.testing.assert_array_equal(a.frequencies,b.frequencies)

    def test_grape_keeps_best_and_respects_budget(self):
        cfg=small_config();model=build_model(cfg,cfg.cases[0]);obj=Objective(model,Signal(2,6,3),cfg)
        initial=np.zeros((1,6));before=obj.evaluate_nodes(initial)[0]
        result=grape(obj,initial)
        self.assertLessEqual(result.cost,before+1e-12)
        self.assertLessEqual(result.metadata["evaluations"],6)

    def test_slsqp_slew_bound(self):
        cfg=small_config();cfg.control.max_slew=.1;model=build_model(cfg,cfg.cases[0]);obj=Objective(model,Signal(2,6,3),cfg)
        result=grape(obj,np.zeros((1,6)))
        self.assertLessEqual(abs(np.diff(result.nodes)).max()/.4,.1+1e-8)

    def test_stationary_vacuum_validation(self):
        cfg=small_config();cfg.cases[0].couplings=[0.];cfg.target.value=0
        model=build_model(cfg,cfg.cases[0]);signal=Signal(2,6,3.)
        result,arrays=validate_waveform(cfg,cfg.cases[0],model,signal,np.zeros((1,6)))
        self.assertTrue(result["validation"]["passed"])
        self.assertTrue(result["metrics"]["goal_reached"])
        self.assertAlmostEqual(arrays["times"][-1],2.)
        self.assertAlmostEqual(result["metrics"]["minimum_quadrature_variance"],.5)

    def test_bad_time_grid_is_not_validated(self):
        cfg=small_config();cfg.intervals=2;cfg.control.nodes=3;cfg.validation.fidelity_tolerance=1e-7
        model=build_model(cfg,cfg.cases[0]);signal=Signal(2,3,3.)
        result,_=validate_waveform(cfg,cfg.cases[0],model,signal,np.array([[0,1.,0]]))
        self.assertFalse(result["validation"]["checks"]["time_grid"])

    def test_cost_counts_all_physical_channels(self):
        cfg=small_config(2);cfg.cases[0].control="common";model=build_model(cfg,cfg.cases[0]);signal=Signal(2,6,None)
        m=actuator_metrics(model,signal,np.array([[0,.3,.3,.3,.3,0.]]),points=501)
        self.assertAlmostEqual(m["modulation_fluence_total"],2*m["modulation_fluence_max_channel"])

    def test_zero_noise_and_nominal_filter(self):
        cfg=small_config();case=cfg.cases[0];nodes=np.array([[0,.3,.2,-.3,.1,0.]])
        baseline=filter_scan(cfg,case,nodes,[3.])[0]["target_probability"]
        noise=static_noise_ensemble(cfg,case,nodes,2)
        self.assertAlmostEqual(noise["probability_mean"],baseline,places=12)
        self.assertEqual(noise["probability_std_population"],0)


class DissipationTests(unittest.TestCase):
    def test_zero_bath_matches_unitary_driven_evolution(self):
        cfg=small_config();cfg.dimension=3;cfg.validation.edge_levels=1;cfg.duration=.3
        cfg.validation.trajectory_points=9;cfg.target.value=0
        nodes=np.array([[0,.1,-.2,.3,.1,0.]])
        meta,arrays=dressed_bath_evolution(cfg,cfg.cases[0],nodes)
        model=build_model(cfg,cfg.cases[0]);signal=Signal(cfg.duration,6,3.)
        v=continuous_evolution(model,signal,nodes,[0,cfg.duration])[-1]
        v=model.expand(v)
        np.testing.assert_allclose(arrays["rho_full_final"],np.outer(v,v.conj()),atol=1e-7)

    def test_detailed_balance(self):
        f=ohmic_spectrum(.1,10.,.3)
        for w in [.2,1.,3.]:
            self.assertAlmostEqual(f(-w)/f(w),np.exp(-w/.3),places=12)
        self.assertEqual(ohmic_spectrum(.1,10.,0.)(-1.),0)

    def test_zero_temperature_ground_not_heated(self):
        cfg=small_config();cfg.dimension=3;cfg.validation.edge_levels=1;cfg.duration=.2
        cfg.initial_state="ground";cfg.validation.trajectory_points=5;cfg.target.value=0
        meta,arrays=dressed_bath_evolution(cfg,cfg.cases[0],np.zeros((1,6)),.01,.01,.01)
        model=build_model(cfg,cfg.cases[0])
        psi=model.expand(model.initial)
        np.testing.assert_allclose(arrays["rho_full_final"],np.outer(psi,psi.conj()),atol=2e-7)
        self.assertTrue(meta["basic_density_checks_passed"])


if __name__=="__main__":
    unittest.main()
