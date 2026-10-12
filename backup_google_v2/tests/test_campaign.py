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
from qoc.metrics import actuator_metrics
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
        self.assertEqual(counts["main"]["random_pipelines"],320)
        self.assertEqual(counts["pilot"]["random_pipelines"],16)
        for job in jobs:
            cfg = job["config"]
            self.assertEqual(cfg["intervals"],cfg["factor_taus"]*100)
            self.assertEqual(cfg["control"]["nodes"],cfg["factor_taus"]*10+1)
            self.assertEqual(cfg["dimension"],60)
        spec["blocks"][-1]["enabled"] = True
        self.assertEqual(plan_counts(campaign_plan(spec))["main"]["random_pipelines"],480)

    def test_bad_campaign_fails_before_execution(self):
        for mutate in [lambda s:s["blocks"][0].update(factors_taus=[0]),
                       lambda s:s["blocks"][0].update(cutoffs=[-1]),
                       lambda s:s["blocks"][0].update(cases=["missing"]),
                       lambda s:s["pilot"].update(seeds=[0]),
                       lambda s:s["base"]["optimization"].update(objective="typo")]:
            spec=tiny_campaign();mutate(spec)
            with self.assertRaises(ValueError): campaign_plan(spec)

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
        hi=actuator_metrics(model,signal,high)["ac_power_fraction_above_threshold_worst"]
        lo=actuator_metrics(model,signal,low)["ac_power_fraction_above_threshold_worst"]
        self.assertGreater(hi,.95);self.assertLess(lo,.02)

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
