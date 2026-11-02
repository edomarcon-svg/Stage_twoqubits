"""Campaign restart, pilot isolation, exact root gradients and waveform imports."""
from copy import deepcopy
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from qoc.config import from_dict, load_config
from qoc.campaign import campaign_plan, plan_counts, load_campaign, run_campaign, select_profile
from qoc.models import build_model
from qoc.controls import Signal
from qoc.propagation import Objective
from qoc.optimizers import grape
from qoc.pipeline import run_experiment
from qoc.metrics import actuator_metrics, initial_state_metrics
from qoc.robustness import initial_state_analysis
from qoc.warm_start import import_nodes
from test_pipeline import tiny
from test_numerics import small_config


def tiny_campaign():
    cfg = tiny()
    cfg.tau_s_coupling = np.pi/(2*cfg.duration)
    cfg.validation.hold_time = .1
    cfg.validation.hold_points = 5
    return {"name":"test_campaign","base":cfg.to_dict(),"pilot":{
        "enabled":True,"cases":["1q"],"target":{"kind":"fock","value":0},
        "factor_taus":1,"filter_cutoff":3.,"seeds":[100],
        "profiles":[{"name":name,"optimization":{"objective":name,"crab_initial_std":.1}}
                    for name in ["probability","root"]],
        "budgets":{"crab_max_evaluations":4,"grape_max_iterations":2,"grape_max_evaluations":3}},
        "blocks":[{"name":"main","targets":[{"kind":"fock","value":0},{"kind":"fock","value":2}],
            "factors_taus":[1,2],"cutoffs":[3.,None]}]}


class CampaignTests(unittest.TestCase):
    def test_production_plan(self):
        spec = load_campaign(Path(__file__).resolve().parents[1]/"configurazione_campagna.jsonc")
        jobs = campaign_plan(spec)
        counts = plan_counts(jobs)
        self.assertEqual(counts["main"]["experiments"],44)
        self.assertEqual(counts["main"]["random_pipelines"],1056)
        self.assertEqual(counts["pilot"]["random_pipelines"],0)
        ground_jobs = [j for j in jobs if j["config"]["initial_state"] == "ground"]
        self.assertEqual(len(ground_jobs),7)
        for job in jobs:
            cfg = job["config"]
            self.assertEqual([c["name"] for c in cfg["cases"]],["1q","2q_common","2q_independent"])
            self.assertEqual(cfg["intervals"],cfg["factor_taus"]*100)
            self.assertEqual(cfg["optimization"]["crab_intervals"],cfg["factor_taus"]*25)
            self.assertEqual(cfg["control"]["nodes"],cfg["factor_taus"]*10+1)
            self.assertEqual(cfg["optimization"]["grape_stop_probability"],0.99995)
            expected_dim = 60 if cfg["target"]["kind"] == "fock" else 48
            self.assertEqual(cfg["dimension"],expected_dim)
        spec["pilot"]["enabled"] = True
        self.assertEqual(plan_counts(campaign_plan(spec))["pilot"]["random_pipelines"],16)

    def test_bad_campaign_fails_before_execution(self):
        for mutate in [lambda s:s["blocks"][0].update(factors_taus=[0]),
                       lambda s:s["blocks"][0].update(cutoffs=[-1]),
                       lambda s:s["blocks"][0].update(cases=["missing"]),
                       lambda s:s["blocks"][0].update(control={"total_frequency_bounds":[1.,3.]},controls=[{"max_slew":1.}]),
                       lambda s:s["blocks"][0].update(controls=[]),
                       lambda s:s["blocks"][0].update(control={"filter_cutoff":2.}),
                       lambda s:s["blocks"][0].update(initial_state="invalid"),
                       lambda s:s["pilot"].update(seeds=[0]),
                       lambda s:s["base"]["optimization"].update(objective="typo")]:
            spec=tiny_campaign();mutate(spec)
            with self.assertRaises(ValueError): campaign_plan(spec)

    def test_block_controls_list_and_initial_state(self):
        spec=tiny_campaign()
        spec["pilot"]["enabled"]=False
        spec["blocks"]=[{
            "name":"bounds_and_slew_scan",
            "initial_state":"ground",
            "targets":[{"kind":"fock","value":0}],
            "factors_taus":[1],
            "cutoffs":[2.,None],
            "controls":[
                {"total_frequency_bounds":[1.0,3.0],"slew_weight":1e-4},
                {"total_frequency_bounds":[1.25,2.75],"max_slew":1.5}
            ]
        }]
        jobs=campaign_plan(spec)
        self.assertEqual(len(jobs),4)
        self.assertEqual(jobs[0]["config"]["initial_state"],"ground")
        self.assertEqual(jobs[0]["config"]["control"]["total_frequency_bounds"],[1.0,3.0])
        self.assertEqual(jobs[0]["config"]["control"]["slew_weight"],1e-4)
        self.assertEqual(jobs[1]["config"]["control"]["total_frequency_bounds"],[1.25,2.75])
        self.assertEqual(jobs[1]["config"]["control"]["max_slew"],1.5)

    def test_pilot_selection_rejects_stagnation(self):
        spec=tiny_campaign()
        item={"metrics":{"target_probability":1e-10,"goal_reached":False},"validation":{"passed":True},
              "crab":{"initial_probability":1e-10},"grape":{"accepted_iterations":[]}}
        summaries={p["name"]:{"cases":[{"seeds":[deepcopy(item)]}]} for p in spec["pilot"]["profiles"]}
        self.assertIsNone(select_profile(spec,summaries)["selected_profile"])
        item=deepcopy(item);item["metrics"]["target_probability"]=.5;item["grape"]["accepted_iterations"]=[{}]
        summaries["root"]["cases"][0]["seeds"]=[item]
        self.assertEqual(select_profile(spec,summaries)["selected_profile"],"root")

    def test_campaign_pilot_then_resume_and_interruption(self):
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            spec=tiny_campaign()
            root=run_campaign(spec,tmp,plots=False,pilot_only=True)
            self.assertEqual(json.loads((root/"state.json").read_text())["state"],"pilot_complete")
            stamps={p:p.stat().st_mtime_ns for p in root.glob("runs/*/*/seed_*/arrays.npz")}
            real=run_experiment
            calls=[0]
            def interrupt(cfg,*args,**kwargs):
                calls[0]+=1
                if calls[0]==4: raise KeyboardInterrupt()
                return real(cfg,*args,**kwargs)
            with patch("qoc.campaign.run_experiment",side_effect=interrupt):
                with self.assertRaises(KeyboardInterrupt):run_campaign(spec,resume=root,plots=False)
            self.assertEqual(json.loads((root/"state.json").read_text())["state"],"interrupted")
            run_campaign(spec,resume=root,plots=False)
            self.assertEqual(json.loads((root/"state.json").read_text())["state"],"complete")
            for path,stamp in stamps.items():self.assertEqual(path.stat().st_mtime_ns,stamp)
            self.assertTrue((root/"seeds.csv").exists())
            # Configuration/source checks cannot be bypassed by a complete manifest.
            changed=deepcopy(spec);changed["blocks"][0]["factors_taus"]=[1]
            with self.assertRaises(ValueError):run_campaign(changed,resume=root,plots=False)


class NewNumericsTests(unittest.TestCase):
    def test_root_gradient_matches_finite_differences_with_penalties(self):
        for filtered in [None,3.]:
            cfg=small_config(2);cfg.optimization.objective="root";cfg.optimization.objective_scale=4.
            cfg.control.filter_cutoff=filtered;cfg.control.fluence_weight=.01;cfg.control.slew_weight=.002
            model=build_model(cfg,cfg.cases[0]);signal=Signal(cfg.duration,cfg.control.nodes,filtered)
            obj=Objective(model,signal,cfg)
            x=np.random.default_rng(4).normal(0,.1,obj.nfree)
            _,grad=obj(x);eps=1e-5
            numeric=[]
            for i in range(len(x)):
                step=np.zeros_like(x);step[i]=eps
                numeric.append((obj(x+step)[0]-obj(x-step)[0])/(2*eps))
            np.testing.assert_allclose(grad,numeric,atol=2e-8,rtol=2e-5)

    def test_root_zero_overlap_is_finite_and_diagnostics_are_saved(self):
        cfg=tiny();cfg.target.value=2;cfg.optimization.objective="root"
        model=build_model(cfg,cfg.cases[0]);signal=Signal(cfg.duration,cfg.control.nodes,3.)
        obj=Objective(model,signal,cfg);result=grape(obj,np.zeros((1,4)))
        self.assertTrue(np.isfinite(result.cost))
        self.assertEqual(result.metadata["initial_gradient"]["projected_gradient_max"],0.)
        self.assertEqual(result.diagnostics[0]["target_probability"],0.)

    def test_spectral_fraction_above_threshold(self):
        cfg=small_config();model=build_model(cfg,cfg.cases[0]);signal=Signal(20,401,None)
        high=np.sin(6*signal.times)[None,:];low=np.sin(.6*signal.times)[None,:]
        act_hi=actuator_metrics(model,signal,high)
        act_lo=actuator_metrics(model,signal,low)
        self.assertGreater(act_hi["ac_power_fraction_above_threshold_worst"],.95)
        self.assertLess(act_lo["ac_power_fraction_above_threshold_worst"],.02)
        self.assertAlmostEqual(act_hi["c2_paper_total"],0.5*act_hi["modulation_fluence_total"])
        self.assertAlmostEqual(act_hi["c2_paper_max_channel"],0.5*act_hi["modulation_fluence_max_channel"])
        self.assertIsNone(act_hi["ac_power_fraction_above_cutoff_worst"])
        signal_filt=Signal(20,401,2.0)
        act_filt=actuator_metrics(model,signal_filt,high)
        self.assertIsNotNone(act_filt["ac_power_fraction_above_cutoff_worst"])
        self.assertIn("slew_rms_worst_channel",act_filt)
        self.assertIn("command_slew_worst_channel",act_filt)

    def test_initial_state_analysis_bare_vs_ground(self):
        cfg=small_config(2)
        case=cfg.cases[0]
        nodes=np.zeros((2,cfg.control.nodes))
        ia=initial_state_analysis(cfg,case,nodes)
        self.assertLess(ia["bare_ground_overlap_probability"],1.0)
        self.assertGreater(ia["bare_ground_overlap_probability"],0.9)
        self.assertLess(ia["dressed_energy_shift"],0.0)
        self.assertGreater(ia["ground_virtual_photons"],0.0)
        self.assertEqual(ia["bare"]["initial"]["bare_vacuum_probability"],1.0)

    def test_crab_intervals_and_grape_stop_probability(self):
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            cfg=tiny()
            cfg.optimization.crab_intervals=4
            cfg.optimization.grape_stop_probability=0.5
            cfg.optimization.grape_max_iterations=50
            cfg.optimization.grape_max_evaluations=100
            root=run_experiment(cfg,tmp,plots=False)
            summary=json.loads((root/"summary.json").read_text())["cases"][0]
            seed=summary["seeds"][0]
            self.assertEqual(seed["crab"]["intervals"],4)
            self.assertEqual(seed["grape"]["stop_probability_threshold"],0.5)
            self.assertTrue(seed["grape"]["stop_probability_active"])
            self.assertIn("c2_paper_total",seed["actuator"])
            self.assertIn("c2_paper_max_channel",seed["actuator"])
            self.assertIn("c2_paper_total_median",summary["statistics"])
            self.assertIn("c2_paper_max_channel_median",summary["statistics"])
            self.assertIn("slew_median",summary["statistics"])
            self.assertIn("omega99_median",summary["statistics"])
            # When slew_weight > 0, early stopping on probability alone is disabled so GRAPE can smooth the pulse.
            cfg.control.slew_weight=1e-3
            model=build_model(cfg,cfg.cases[0]);sig=Signal(cfg.duration,cfg.control.nodes,3.)
            res=grape(Objective(model,sig,cfg),np.zeros((1,cfg.control.nodes)))
            self.assertFalse(res.metadata["stop_probability_active"])

    def test_legacy_import_and_separate_warm_statistics(self):
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            path=Path(tmp)/"old.npz"
            np.savez(path,tlist_fine=np.linspace(0,.4,20),ctrl_smooth=np.full((1,20),2.))
            cfg=tiny();spec={"name":"old","case":"1q","path":str(path),"format":"legacy_smooth"}
            cfg.optimization.warm_starts=[spec]
            root=run_experiment(cfg,tmp,plots=False)
            summary=json.loads((root/"summary.json").read_text())["cases"][0]
            self.assertEqual(summary["statistics"]["count"],1)
            self.assertEqual(len(summary["warm_starts"]),1)
            self.assertEqual(summary["warm_starts"][0]["cohort"],"warm_start")
            path.unlink() # A resume must use the immutable input snapshot.
            run_experiment(cfg,resume=root,plots=False)
            arrays=np.load(root/"1q"/"seed_0"/"arrays.npz")
            self.assertIn("photon_populations",arrays.files)
            self.assertIn("grape_diagnostics",arrays.files)

    def test_import_rejects_duration_mismatch_and_records_adjustment(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"old.npz"
            np.savez(path,tlist_crab=[0,1,2],ctrl_crab=[[2,7,2]])
            cfg=tiny();model=build_model(cfg,cfg.cases[0]);signal=Signal(.4,4,None)
            spec={"path":str(path),"format":"legacy_crab"}
            with self.assertRaisesRegex(ValueError,"duration"):import_nodes(spec,model,signal,cfg.control)
            spec["rescale_time"]=True
            nodes,meta=import_nodes(spec,model,signal,cfg.control)
            self.assertLessEqual(nodes.max()+2,3)
            self.assertGreater(meta["max_feasibility_adjustment"],0)


if __name__ == "__main__":unittest.main()
