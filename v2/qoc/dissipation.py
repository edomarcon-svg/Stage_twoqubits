"""Optional dressed, time-dependent Bloch-Redfield analysis using QuTiP.

This is a weak-bath, Markov/secular approximation, not a universal USC bath model.
Fast driving may invalidate its assumptions. It is deliberately separate from
the validated UNITARY optimizer and must be calibrated against the experiment.
"""
from copy import deepcopy
import numpy as np
import qutip as qt
from .models import build_model
from .controls import Signal


def ohmic_spectrum(strength, cutoff, temperature):
    if strength<0 or cutoff<=0 or temperature<0 or not np.isfinite([strength,cutoff,temperature]).all():
        raise ValueError("Require finite strength>=0, cutoff>0, temperature>=0")
    def spectrum(w):
        w = float(w)
        if abs(w)<1e-12:
            return strength*temperature
        scale = strength*abs(w)*np.exp(-abs(w)/cutoff)
        if temperature==0:
            return scale if w>0 else 0.
        x = abs(w)/temperature
        occupation = 0. if x>700 else 1/np.expm1(x)
        return scale*((occupation+1) if w>0 else occupation)
    return spectrum


def dressed_bath_evolution(cfg, case, nodes, cavity_strength=0., qubit_strength=0., dephasing_strength=0.,
                          bath_cutoff=10., temperature=0., secular_cutoff=1e-8):
    if secular_cutoff<=0:
        raise ValueError("A positive secular cutoff is required")
    for s in [cavity_strength,qubit_strength,dephasing_strength]:
        ohmic_spectrum(s,bath_cutoff,temperature)
    full_cfg = deepcopy(cfg)
    full_cfg.parity_reduction = False  # Dissipation can change total parity.
    model = build_model(full_cfg,case)
    signal = Signal(cfg.duration,cfg.control.nodes,cfg.control.filter_cutoff)
    evaluate = signal.callback(nodes)
    def coefficient(k):
        def value(t):
            return float(evaluate(t)[k])
        return value
    h = [model.full_drift]+[[hc,coefficient(k)] for k,hc in enumerate(model.full_controls)]
    ident = [qt.qeye(model.dimension)]+[qt.qeye(2)]*model.nqubits
    a = qt.tensor(qt.destroy(model.dimension),*ident[1:])
    baths = []
    if cavity_strength:
        baths.append((a+a.dag(),ohmic_spectrum(cavity_strength,bath_cutoff,temperature)))
    for j in range(model.nqubits):
        for op,strength in [(qt.sigmax(),qubit_strength),(qt.sigmaz(),dephasing_strength)]:
            if strength:
                ops = ident.copy()
                ops[j+1] = op
                baths.append((qt.tensor(*ops),ohmic_spectrum(strength,bath_cutoff,temperature)))
    times = np.linspace(0,cfg.duration,cfg.validation.trajectory_points)
    psi0 = model.full_ket(model.initial)
    options = {"atol":cfg.validation.atol,"rtol":cfg.validation.rtol,"max_step":signal.h/8,
               "nsteps":1000000,"normalize_output":False,"store_states":True}
    result = qt.brmesolve(h,psi0.proj(),times,a_ops=baths,sec_cutoff=secular_cutoff,options=options)
    rho = result.states[-1]
    rho_c = rho.ptrace(0).full()
    probability = float(np.trace(model.target_operator@rho.full()).real)
    traces = [float(abs(x.tr()-1)) for x in result.states]
    minimum_eigenvalue = min(float(np.linalg.eigvalsh(x.full()).min()) for x in result.states)
    target_probability = float(np.vdot(model.target_cavity,rho_c@model.target_cavity).real)
    metadata = {"model":"time-dependent dressed Bloch-Redfield with secular cutoff",
        "limitations":"Weak-bath and Markov/secular assumptions require physical justification, especially under fast driving; not an open-system optimal-control result.",
        "cavity_strength":cavity_strength,"qubit_strength":qubit_strength,"dephasing_strength":dephasing_strength,
        "bath_cutoff":bath_cutoff,"temperature":temperature,"secular_cutoff":secular_cutoff,
        "target_probability":probability,"fidelity_root":float(np.sqrt(np.clip(probability,0,1))),
        "cavity_target_probability":target_probability,"purity_cavity":float(np.trace(rho_c@rho_c).real),
        "max_trace_error":max(traces),"minimum_density_eigenvalue":minimum_eigenvalue,
        "basic_density_checks_passed":bool(max(traces)<1e-7 and minimum_eigenvalue>-1e-7),
        "dimension_and_bath_approximation_validated":False}
    return metadata,{"times":times,"rho_full_final":rho.full(),"rho_cavity_final":rho_c,
        "mean_photons":np.array(qt.expect(a.dag()*a,result.states))}
