"""End-to-end file/CLI tests, including relocation and interrupted-run recovery."""
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from qoc.config import Experiment,Case,Target,load_config
from qoc.pipeline import run_experiment,load_checkpoint
from qoc.storage import prepare_run
from qoc.reporting import write_reports


def tiny():
    cfg=Experiment(name="integration",dimension=4,duration=.4,intervals=12,target=Target("fock",0))
    cfg.cases=[Case("1q",[0.],[2.])]
    cfg.control.nodes=4
    cfg.optimization.seeds=[0]
    cfg.optimization.frequencies=1
    cfg.optimization.crab_max_evaluations=4
    cfg.optimization.grape_max_iterations=2
    cfg.optimization.grape_max_evaluations=3
    cfg.validation.edge_levels=1
    cfg.validation.dimension_increment=3
    cfg.validation.trajectory_points=9
    cfg.validation.phase_grid_points=31
    return cfg.validate()


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.base=Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_tiny(self):
        with redirect_stdout(io.StringIO()):
            return run_experiment(tiny(),self.base,plots=False)

    def test_complete_pipeline_and_report_only(self):
        root=self.run_tiny()
        summary=json.loads((root/"summary.json").read_text())
        self.assertTrue(summary["complete"])
        seed=summary["cases"][0]["seeds"][0]
        self.assertTrue(seed["validation"]["passed"])
        self.assertTrue(seed["metrics"]["goal_reached"])
        self.assertTrue((root/"source_snapshot"/"qoc"/"propagation.py").exists())
        self.assertTrue((root/"source_snapshot"/"resolved_config.json").exists())
        with np.load(root/seed["folder"]/"arrays.npz",allow_pickle=False) as data:
            self.assertEqual(data["states_reduced"].shape[0],9)
            self.assertAlmostEqual(data["times"][-1],.4)
        write_reports(root,make_figures=False)
        self.assertNotIn("<img",(root/"report.html").read_text())
        self.assertTrue((root/"summary.csv").exists())

    def test_resume_preserves_completed_arrays(self):
        root=self.run_tiny();path=root/"1q"/"seed_0"/"arrays.npz"
        stamp=path.stat().st_mtime_ns;content=path.read_bytes()
        with redirect_stdout(io.StringIO()):
            resumed=run_experiment(load_config(root/"config.json"),resume=root,plots=False)
        self.assertEqual(resumed,root)
        self.assertEqual(path.stat().st_mtime_ns,stamp)
        self.assertEqual(path.read_bytes(),content)

    def test_partial_resume_from_crab(self):
        root=self.run_tiny();seed=root/"1q"/"seed_0"
        crab_stamp=(seed/"crab.npz").stat().st_mtime_ns
        (seed/"result.json").unlink()
        (seed/"arrays.npz").unlink()
        with redirect_stdout(io.StringIO()):
            run_experiment(tiny(),resume=root,plots=False)
        self.assertTrue((seed/"result.json").exists())
        self.assertEqual((seed/"crab.npz").stat().st_mtime_ns,crab_stamp)

    def test_corrupt_checkpoint_is_rejected(self):
        root=self.run_tiny();seed=root/"1q"/"seed_0"
        (seed/"arrays.npz").write_bytes(b"corrupted")
        with self.assertRaises(ValueError):load_checkpoint(seed,"result")

    def test_resume_rejects_config_or_code_change(self):
        root=self.run_tiny();cfg=tiny();cfg.duration=.8
        with self.assertRaises(ValueError):prepare_run(cfg,resume=root)
        with patch("qoc.storage.source_hashes",return_value={"changed":"hash"}):
            with self.assertRaises(ValueError):prepare_run(tiny(),resume=root)

    def test_analysis_handles_partial_summary(self):
        root=self.run_tiny()
        (root/"summary.json").write_text(json.dumps({"cases":[],"complete":False}))
        script=Path(__file__).resolve().parents[1]/"analyze_run.py"
        args=[sys.executable,str(script),str(root),"--case","1q","--cutoffs","2"]
        unavailable=subprocess.run(args,capture_output=True,text=True,timeout=30)
        self.assertEqual(unavailable.returncode,2)
        self.assertIn("non ancora presente",unavailable.stderr)
        explicit=subprocess.run(args+["--seed","0"],capture_output=True,text=True,timeout=30)
        self.assertEqual(explicit.returncode,0,explicit.stderr)

    def test_standalone_copy_cli(self):
        source=Path(__file__).resolve().parents[1]
        app=self.base/"unrelated_project";app.mkdir()
        shutil.copytree(source/"qoc",app/"qoc",ignore=shutil.ignore_patterns("__pycache__"))
        for name in ["run_simulation.py","run_sweep.py","analyze_run.py","requirements.txt","requirements-tested.txt","pyproject.toml"]:
            shutil.copy2(source/name,app/name)
        config=app/"config.json";config.write_text(json.dumps(tiny().to_dict()))
        env=dict(os.environ);env.pop("PYTHONPATH",None)
        env["OPENBLAS_NUM_THREADS"]="1";env["OMP_NUM_THREADS"]="1"
        run=subprocess.run([sys.executable,str(app/"run_simulation.py"),"--config",str(config),"--output",str(app/"runs"),"--no-plots"],
            cwd=self.base,env=env,capture_output=True,text=True,timeout=30)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
        summaries=list((app/"runs").glob("*/summary.json"))
        self.assertEqual(len(summaries),1)
        self.assertTrue(json.loads(summaries[0].read_text())["complete"])


if __name__=="__main__":
    unittest.main()
