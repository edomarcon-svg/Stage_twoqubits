#!/usr/bin/env python3
"""Run or resume a multi-target campaign, with a pilot before the main comparison."""
import argparse
import json
from pathlib import Path
from qoc.campaign import load_campaign, campaign_plan, plan_counts, run_campaign


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config",type=Path,help="Campaign JSON/JSONC")
    parser.add_argument("--resume",type=Path,help="Saved campaign directory")
    parser.add_argument("--output",type=Path,help="Base output directory")
    parser.add_argument("--validate-config",action="store_true",help="Print plan and counts; no optimization")
    parser.add_argument("--pilot-only",action="store_true",help="Run pilot and save decision; resume later for main campaign")
    parser.add_argument("--no-plots",action="store_true")
    args = parser.parse_args()
    if not args.config and not args.resume: parser.error("Supply --config or --resume")
    spec = load_campaign(args.config or args.resume/"campaign.json")
    jobs = campaign_plan(spec)
    if args.validate_config:
        from qoc.config import from_dict
        from qoc.models import build_model
        seen = set()
        for job in jobs:
            cfg = from_dict(job["config"])
            for case in cfg.cases:
                key = json.dumps([cfg.target.__dict__,case.__dict__,cfg.dimension,cfg.initial_state,cfg.parity_reduction],sort_keys=True)
                if key not in seen: build_model(cfg,case);seen.add(key)
        print(json.dumps({"name":spec["name"],"counts":plan_counts(jobs),"experiments":[{
            "id":j["id"],"stage":j["stage"],"target":j["config"]["target"],"factor_taus":j["config"]["factor_taus"],
            "cutoff":j["config"]["control"]["filter_cutoff"],"intervals":j["config"]["intervals"],
            "nodes":j["config"]["control"]["nodes"]} for j in jobs]},indent=2))
        return
    root = run_campaign(spec,args.output,args.resume,not args.no_plots,args.pilot_only)
    print(f"Report: {root/'report.html'}")
    if json.loads((root/"state.json").read_text())["state"] == "pilot_failed":
        raise SystemExit(2)


if __name__ == "__main__": main()
