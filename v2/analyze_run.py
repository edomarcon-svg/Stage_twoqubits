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
from qoc.robustness import filter_scan, static_noise_ensemble, initial_state_analysis
from qoc.dissipation import dressed_bath_evolution


def _analyze_seed(cfg, case, seed, folder, args):
    checkpoint = load_checkpoint(folder,"result")
    if checkpoint is None:
        raise ValueError(f"Seed raffinato non disponibile: {folder}")
    with np.load(folder/"arrays.npz",allow_pickle=False) as d:
        nodes = d["command_modulation"]
    item = {"case":case.name,"seed":seed,"source_array_sha256":checkpoint["array_sha256"],
        "nominal_validation_passed":checkpoint["validation"]["passed"],
        "analysis_provenance":provenance(cfg),"perturbations_numerically_revalidated":False}
    arrays = None
    if args.cutoffs:
        item["filter_scan"] = filter_scan(cfg,case,nodes,args.cutoffs)
    if args.initial_state_check:
        item["initial_state_analysis"] = initial_state_analysis(cfg,case,nodes)
    if args.noise_samples:
        item["noise"] = static_noise_ensemble(cfg,case,nodes,args.noise_samples,args.noise_seed,
            args.gain_std,args.detuning_std,args.coupling_relative_std)
    if args.bath:
        item["bath"],arrays = dressed_bath_evolution(cfg,case,nodes,args.cavity_strength,args.qubit_strength,
            args.dephasing_strength,args.bath_cutoff,args.temperature)
    return item, arrays


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run",type=Path)
    p.add_argument("--case",help="Caso da analizzare (se omesso con --all-cases o --all-seeds, analizza tutti i casi)")
    p.add_argument("--all-cases",action="store_true",help="Analizza tutti i casi presenti nella run")
    p.add_argument("--seed",type=int,help="Default: seed selezionato dal report")
    p.add_argument("--all-seeds",action="store_true",help="Analizza tutti i seed completati per ciascun caso e calcola le mediane")
    p.add_argument("--cutoffs",type=float,nargs="+",help="Tagli passa-basso positivi da testare sullo stesso comando")
    p.add_argument("--initial-state-check",action="store_true",help="Confronta stato iniziale bare vs ground vestito e valuta l'impulso su entrambi")
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
    if not (args.cutoffs or args.initial_state_check or args.noise_samples or args.bath):
        p.error("Specificare --cutoffs, --initial-state-check, --noise-samples oppure --bath")
    if not args.case and not args.all_cases and not args.all_seeds:
        p.error("Specificare --case <nome> oppure --all-cases / --all-seeds")
    if args.seed is not None and args.all_seeds:
        p.error("Non specificare contemporaneamente --seed e --all-seeds")
    cfg = load_config(args.run/"config.json")
    cases = {c.name:c for c in cfg.cases}
    if args.case and args.case not in cases:
        p.error("Caso inesistente")
    summary_path = args.run/"summary.json"
    summary = json.loads(summary_path.read_text()) if summary_path.exists() else {"cases":[]}
    out = args.run/"analyses"/datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    # Modalità singola classica (retrocompatibile al 100%)
    if args.case and not args.all_cases and not args.all_seeds:
        case = cases[args.case]
        selected = next((c for c in summary["cases"] if c["name"]==args.case),None)
        if args.seed is None and selected is None:
            p.error("Caso non ancora presente nel riepilogo: attendere la fine della run oppure specificare --seed per un checkpoint già completo")
        seed = selected["selected_seed"] if args.seed is None else args.seed
        folder = args.run/args.case/f"seed_{seed}"
        if load_checkpoint(folder,"result") is None:
            p.error("Seed raffinato non disponibile")
        out.mkdir(parents=True)
        with threadpool_limits(limits=cfg.optimization.blas_threads):
            data, arrays = _analyze_seed(cfg, case, seed, folder, args)
            if arrays is not None:
                save_arrays(out/"bath.npz",**arrays)
        save_json(out/"analysis.json",data)
        print(out/"analysis.json")
        return
    # Modalità batch (multi-caso e/o multi-seed)
    target_cases = [cases[args.case]] if args.case else list(cfg.cases)
    out.mkdir(parents=True)
    batch_results = []
    filter_summary = []
    initial_state_summary = []
    with threadpool_limits(limits=cfg.optimization.blas_threads):
        for case in target_cases:
            selected = next((c for c in summary["cases"] if c["name"]==case.name),None)
            if args.all_seeds:
                seeds = cfg.optimization.seeds
            else:
                if args.seed is None and selected is None:
                    p.error(f"Caso {case.name} non ancora presente nel riepilogo")
                seeds = [selected["selected_seed"] if args.seed is None else args.seed]
            case_items = []
            for seed in seeds:
                folder = args.run/case.name/f"seed_{seed}"
                if load_checkpoint(folder,"result") is None:
                    p.error(f"Seed raffinato non disponibile: {case.name}/seed_{seed}")
                item, arrays = _analyze_seed(cfg, case, seed, folder, args)
                if arrays is not None:
                    save_arrays(out/f"bath_{case.name}_seed_{seed}.npz",**arrays)
                case_items.append(item)
            batch_results.append({"case":case.name,"seeds":case_items})
            if args.cutoffs:
                for idx, cutoff in enumerate(args.cutoffs):
                    ps = np.array([it["filter_scan"][idx]["target_probability"] for it in case_items])
                    filter_summary.append({
                        "case":case.name,"cutoff":cutoff,"count":len(ps),
                        "probability_median":float(np.median(ps)),
                        "probability_mean":float(np.mean(ps)),
                        "probability_min":float(np.min(ps)),
                        "probability_max":float(np.max(ps)),
                        "probability_q25":float(np.quantile(ps,.25)),
                        "probability_q75":float(np.quantile(ps,.75)),
                        "goal_count":int(np.sum(ps >= cfg.target_probability_goal))
                    })
            if args.initial_state_check:
                p_bare = np.array([it["initial_state_analysis"]["target_probability_bare"] for it in case_items])
                p_ground = np.array([it["initial_state_analysis"]["target_probability_ground"] for it in case_items])
                first_ia = case_items[0]["initial_state_analysis"]
                initial_state_summary.append({
                    "case":case.name,"count":len(case_items),
                    "nominal_initial_state":cfg.initial_state,
                    "bare_ground_overlap_probability":first_ia["bare_ground_overlap_probability"],
                    "dressed_energy_shift":first_ia["dressed_energy_shift"],
                    "ground_virtual_photons":first_ia["ground_virtual_photons"],
                    "ground_cavity_purity":first_ia["ground_cavity_purity"],
                    "probability_bare_median":float(np.median(p_bare)),
                    "probability_ground_median":float(np.median(p_ground)),
                    "probability_difference_median":float(np.median(p_ground - p_bare)),
                    "goal_count_bare":int(np.sum(p_bare >= cfg.target_probability_goal)),
                    "goal_count_ground":int(np.sum(p_ground >= cfg.target_probability_goal))
                })
    payload = {"mode":"batch","analysis_provenance":provenance(cfg),
        "perturbations_numerically_revalidated":False,"cases":batch_results,
        "filter_scan_summary":filter_summary,"initial_state_summary":initial_state_summary}
    save_json(out/"analysis.json",payload)
    print(out/"analysis.json")


if __name__=="__main__":
    main()
