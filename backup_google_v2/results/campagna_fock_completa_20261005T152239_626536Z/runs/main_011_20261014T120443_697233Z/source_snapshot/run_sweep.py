#!/usr/bin/env python3
"""Reoptimize a duration/filter campaign; never interpret failure as a speed limit."""
import argparse
from copy import deepcopy
import csv
from datetime import datetime,timezone
import json
import math
from pathlib import Path
from qoc.config import load_config
from qoc.pipeline import run_experiment
from qoc.storage import save_json


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config",required=True,type=Path)
    timing = p.add_mutually_exclusive_group(required=True)
    timing.add_argument("--durations",type=float,nargs="+",help="Durate T esplicite")
    timing.add_argument("--factors-taus",type=int,nargs="+",help="Multipli interi positivi di tau_s")
    p.add_argument("--cutoffs",type=float,nargs="+")
    p.add_argument("--output",type=Path,default=Path(__file__).resolve().parent/"results")
    p.add_argument("--no-plots",action="store_true")
    args = p.parse_args()
    cfg = load_config(args.config)
    durations = args.durations or [factor*cfg.tau_s for factor in args.factors_taus]
    if any(not math.isfinite(x) or x<=0 for x in durations+(args.cutoffs or [])):
        p.error("Durate e tagli devono essere finiti e positivi")
    destination = args.output/("sweep_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ"))
    destination.mkdir(parents=True)
    dt = cfg.duration/cfg.intervals
    node_step = cfg.duration/(cfg.control.nodes-1)
    rows = []
    save_json(destination/"campaign.json",{"base_config":cfg.to_dict(),"durations":durations,
        "factors_taus":args.factors_taus,"tau_s":cfg.tau_s,
        "cutoffs":args.cutoffs,"resolution_policy":"keep propagation and command spacing no larger than base configuration; independent restarts"})
    for index,duration in enumerate(durations):
        for cutoff in args.cutoffs or [cfg.control.filter_cutoff]:
            trial = deepcopy(cfg)
            trial.name = f"{cfg.name}_T{duration:g}_wc{cutoff}"
            trial.duration = duration
            trial.factor_taus = args.factors_taus[index] if args.factors_taus else None
            trial.intervals = max(2,math.ceil(duration/dt))
            trial.control.nodes = min(trial.intervals+1,max(3,math.ceil(duration/node_step)+1))
            trial.control.filter_cutoff = cutoff
            run = run_experiment(trial,destination,plots=not args.no_plots)
            summary = json.loads((run/"summary.json").read_text())
            for case in summary["cases"]:
                best = next(x for x in case["seeds"] if x["seed"]==case["selected_seed"])
                rows.append({"duration":duration,"filter_cutoff":cutoff,"case":case["name"],
                    "best_continuous_probability":best["metrics"]["target_probability"],
                    "numerically_valid":best["validation"]["passed"],"goal_reached":best["metrics"]["goal_reached"],
                    "mean_probability":case["statistics"]["probability_mean"],"run":str(run)})
            with (destination/"sweep.csv").open("w",newline="") as f:
                w = csv.DictWriter(f,fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(rows)
    print(destination/"sweep.csv")


if __name__=="__main__":
    main()
