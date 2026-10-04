"""The editable configuration must remain complete and usable by the real CLI."""
from dataclasses import fields
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from qoc.config import (Case, Control, Experiment, Optimization, Target, Validation,
                        _without_json_comments, load_config)


ROOT = Path(__file__).resolve().parents[1]


class CommentedConfigTests(unittest.TestCase):
    def test_editable_file_covers_every_field_and_matches_smoke(self):
        path = ROOT / "configurazione.jsonc"
        raw = json.loads(_without_json_comments(path.read_text()))
        # Duration is derived from factor_taus, not a second editable time input.
        self.assertEqual(set(raw), {f.name for f in fields(Experiment)} - {"duration"})
        self.assertIsInstance(raw["factor_taus"], int)
        self.assertGreater(raw["factor_taus"], 0)
        for key, cls in [("target", Target), ("control", Control),
                         ("optimization", Optimization), ("validation", Validation)]:
            self.assertEqual(set(raw[key]), {f.name for f in fields(cls)})
        for case in raw["cases"]:
            self.assertEqual(set(case), {f.name for f in fields(Case)})
        editable = load_config(path).to_dict()
        smoke = load_config(ROOT / "configs" / "smoke.json").to_dict()
        editable["name"] = smoke["name"]
        editable["duration"] = smoke["duration"]
        editable["factor_taus"] = smoke["factor_taus"]
        self.assertEqual(editable, smoke)

    def test_comments_preserve_strings_and_positions(self):
        value = 'https://example.org/a/*b*/\\escaped"//still-a-string'
        text = '{/* prima\nseconda */ "name": ' + json.dumps(value) + ', // dopo\n"dimension": 14}'
        cleaned = _without_json_comments(text)
        self.assertEqual(len(cleaned), len(text))
        self.assertEqual([i for i, c in enumerate(cleaned) if c == '\n'],
                         [i for i, c in enumerate(text) if c == '\n'])
        self.assertEqual(json.loads(cleaned), {"name": value, "dimension": 14})

    def test_unclosed_comment_rejected(self):
        with self.assertRaisesRegex(json.JSONDecodeError, "Unterminated"):
            _without_json_comments('{"name": "ok"} /* unfinished')

    def test_json_stays_strict_and_jsonc_stays_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            plain = folder / "config.json"
            plain.write_text('// comment\n{}')
            with self.assertRaises(json.JSONDecodeError):
                load_config(plain)
            commented = folder / "config.jsonc"
            for text, error in [('// comment\n{"duraton": 1}', ValueError),
                                ('{"duration": -1} // comment', ValueError),
                                ('{"duration": 1,}', json.JSONDecodeError)]:
                commented.write_text(text)
                with self.assertRaises(error):
                    load_config(commented)

    def test_commented_cli_roundtrip_and_resume(self):
        cfg = load_config(ROOT / "configurazione.jsonc")
        cfg.name = "commented_integration"
        cfg.dimension = 4
        cfg.duration = .4
        cfg.factor_taus = 1
        cfg.tau_s_coupling = 3.141592653589793 / .8
        cfg.intervals = 12
        cfg.cases = [Case("1q", [0.], [2.])]
        cfg.target.value = 0
        cfg.control.nodes = 4
        cfg.optimization.seeds = [0]
        cfg.optimization.frequencies = 1
        cfg.optimization.crab_max_evaluations = 4
        cfg.optimization.grape_max_iterations = 2
        cfg.optimization.grape_max_evaluations = 3
        cfg.validation.edge_levels = 1
        cfg.validation.trajectory_points = 9
        cfg.validation.phase_grid_points = 21
        cfg.validate()
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / "config.jsonc"
            source.write_text('// Editable input\n' + json.dumps(cfg.to_dict()))
            cli = [sys.executable, str(ROOT / "run_simulation.py")]
            result = subprocess.run(cli + ["--config", str(source), "--output", str(folder / "runs"), "--no-plots"],
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            run = next((folder / "runs").iterdir())
            self.assertEqual(load_config(run / "config.json").to_dict(), cfg.to_dict())
            checkpoint = run / "1q" / "seed_0" / "arrays.npz"
            stamp = checkpoint.stat().st_mtime_ns
            resumed = subprocess.run(cli + ["--resume", str(run), "--no-plots"],
                                     capture_output=True, text=True, timeout=60)
            self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
            self.assertEqual(checkpoint.stat().st_mtime_ns, stamp)


if __name__ == "__main__":
    unittest.main()
