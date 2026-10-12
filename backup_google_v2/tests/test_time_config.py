"""Physical time, integer tau_s factors and CLI/sweep overrides stay consistent."""
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from qoc.config import Case, from_dict
import run_sweep


ROOT = Path(__file__).resolve().parents[1]


class TimeConfigTests(unittest.TestCase):
    def test_factor_reference_and_roundtrip(self):
        cfg = from_dict({"factor_taus": 20, "tau_s_coupling": .3, "duration": 1})
        self.assertAlmostEqual(cfg.duration, 104.71975511965978)
        self.assertEqual(from_dict(cfg.to_dict()).to_dict(), cfg.to_dict())
        cfg.cases = [Case("normalized", [.3 / math.sqrt(2)] * 2, [2., 2.])]
        cfg.validate()
        self.assertAlmostEqual(cfg.duration, 20 * math.pi / .6)
        cfg.factor_taus = 10
        cfg.validate()
        self.assertAlmostEqual(cfg.duration, 52.35987755982989)
        self.assertEqual(from_dict({"duration": 3}).duration, 3)

    def test_invalid_factors_and_reference(self):
        for factor in [0, -1, 1.5, True, "20", 20.0]:
            with self.subTest(factor=factor), self.assertRaises(ValueError):
                from_dict({"factor_taus": factor})
        for coupling in [0, -1, float("inf"), float("nan"), True, "0.3"]:
            with self.subTest(coupling=coupling), self.assertRaises(ValueError):
                from_dict({"tau_s_coupling": coupling})

    def test_cli_overrides_and_case_selection(self):
        cli = [sys.executable, str(ROOT / "run_simulation.py"), "--config",
               str(ROOT / "configurazione.jsonc"), "--validate-config", "--case", "2q_common"]
        for flags, factor, duration in [(["--duration", "2"], None, 2),
                                        (["--factor-taus", "10", "--tau-s-coupling", "0.6"], 10, 10*math.pi/1.2)]:
            result = subprocess.run(cli + flags, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            cfg = json.loads(result.stdout)
            self.assertEqual(cfg["factor_taus"], factor)
            self.assertAlmostEqual(cfg["duration"], duration)
        bad = subprocess.run(cli + ["--duration", "2", "--factor-taus", "3"], capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)

    def test_sweep_factors_and_explicit_time_do_not_conflict(self):
        for flags, expected_factors, durations in [(["--factors-taus", "1", "2"], [1, 2], [math.pi/.6, 2*math.pi/.6]),
                                                   (["--durations", "2", "3"], [None, None], [2, 3])]:
            with tempfile.TemporaryDirectory() as tmp:
                observed = []

                def fake_run(cfg, destination, plots):
                    cfg.validate()
                    observed.append((cfg.factor_taus, cfg.duration))
                    root = Path(destination) / str(len(observed))
                    root.mkdir()
                    summary = {"cases": [{"name": "test", "selected_seed": 0,
                        "seeds": [{"seed": 0, "metrics": {"target_probability": 1., "goal_reached": True},
                                   "validation": {"passed": True}}],
                        "statistics": {"probability_mean": 1.}}]}
                    (root / "summary.json").write_text(json.dumps(summary))
                    return root

                argv = ["run_sweep.py", "--config", str(ROOT / "configurazione.jsonc"), "--output", tmp] + flags
                with patch.object(sys, "argv", argv), patch.object(run_sweep, "run_experiment", side_effect=fake_run):
                    run_sweep.main()
                self.assertEqual([item[0] for item in observed], expected_factors)
                for actual, expected in zip(observed, durations):
                    self.assertAlmostEqual(actual[1], expected)


if __name__ == "__main__":
    unittest.main()
