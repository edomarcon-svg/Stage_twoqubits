#!/usr/bin/env python3
"""Independent analyses of saved optimized waveforms, without reoptimization."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits
from qoc.config import load_config
from qoc.storage import save_json, provenance
from qoc.pipeline import load_checkpoint, save_arrays
from qoc.robustness import filter_scan, static_noise_ensemble
from qoc.dissipation import dressed_bath_evolution


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run",type=Path)
    p.add_argument("--case",required=True)
    p.add_argument("--seed",type=int,help="Default: seed selezionato dal report")
    p.add_argument("--cutoffs",type=float,nargs="+",help="Tagli passa-basso positivi da testare sullo stesso comando")
    p.add_argument("--noise-samples",type=int,default=0)
    p.add_argument("--noise-seed",type=int,default=1234)
    p.add_argument("--gain-std",type=float,default=0.)
    p.add_argument("--detuning-std",type=float,default=0.)
    p.add_argument("--coupling-relative-std",type=float,default=0.)
    p.add_argument("--bath",action="store_true",help="Analisi approssimata Bloch-Redfield dressed; costo elevato")
    p.add_argument("--cavity-strength",type=float,default=0.)
    p.add_argument("--qubit-strength",type=float,default=0.)
    p.add_argument("--dephasing-strength",type=float,default=0.)
    p.add_argument("--bath-cutoff",type=float,default=10.)
    p.add_argument("--temperature",type=float,default=0.)
    args = p.parse_args()
    if args.noise_samples<0:
        p.error("noise-samples deve essere nonnegativo")
    if not (args.cutoffs or args.noise_samples or args.bath):
        p.error("Specificare --cutoffs, --noise-samples oppure --bath")
    cfg = load_config(args.run/"config.json")
    cases = {c.name:c for c in cfg.cases}
    if args.case not in cases:
        p.error("Caso inesistente")
    case = cases[args.case]
    summary_path = args.run/"summary.json"
    summary = json.loads(summary_path.read_text()) if summary_path.exists() else {"cases":[]}
    selected = next((c for c in summary["cases"] if c["name"]==args.case),None)
    if args.seed is None and selected is None:
        p.error("Caso non ancora presente nel riepilogo: attendere la fine della run oppure specificare --seed per un checkpoint già completo")
    seed = selected["selected_seed"] if args.seed is None else args.seed
    folder = args.run/args.case/f"seed_{seed}"
    checkpoint = load_checkpoint(folder,"result")
    if checkpoint is None:
        p.error("Seed raffinato non disponibile")
    with np.load(folder/"arrays.npz",allow_pickle=False) as d:
        nodes = d["command_modulation"]
    out = args.run/"analyses"/datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    out.mkdir(parents=True)
    data = {"case":args.case,"seed":seed,"source_array_sha256":checkpoint["array_sha256"],
        "nominal_validation_passed":checkpoint["validation"]["passed"],
        "analysis_provenance":provenance(cfg),"perturbations_numerically_revalidated":False}
    with threadpool_limits(limits=cfg.optimization.blas_threads):
        if args.cutoffs:
            data["filter_scan"] = filter_scan(cfg,case,nodes,args.cutoffs)
        if args.noise_samples:
            data["noise"] = static_noise_ensemble(cfg,case,nodes,args.noise_samples,args.noise_seed,
                args.gain_std,args.detuning_std,args.coupling_relative_std)
        if args.bath:
            data["bath"],arrays = dressed_bath_evolution(cfg,case,nodes,args.cavity_strength,args.qubit_strength,
                args.dephasing_strength,args.bath_cutoff,args.temperature)
            save_arrays(out/"bath.npz",**arrays)
    save_json(out/"analysis.json",data)
    print(out/"analysis.json")


if __name__=="__main__":
    main()
