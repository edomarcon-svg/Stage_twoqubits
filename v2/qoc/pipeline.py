"""Resumable multi-seed experiments. Workers only write their own seed folder."""
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import time
import numpy as np
from threadpoolctl import threadpool_limits
from .config import from_dict
from .models import build_model
from .controls import Signal
from .propagation import Objective, continuous_evolution
from .metrics import state_metrics
from .optimizers import crab, grape
from .validation import validate_waveform
from .storage import SCHEMA_VERSION, prepare_run, save_json
from .reporting import write_reports


def save_arrays(path, **arrays):
    path = Path(path)
    tmp = path.with_suffix(".tmp")
    with tmp.open("wb") as f:
        np.savez_compressed(f,**arrays)
    os.replace(tmp,path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_checkpoint(folder, name):
    folder = Path(folder)
    path = folder/(name+".json")
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    arrays = folder/data["array_file"]
    if not arrays.exists() or hashlib.sha256(arrays.read_bytes()).hexdigest()!=data["array_sha256"]:
        raise ValueError(f"Corrupt checkpoint: {folder}/{name}")
    return data


def _crab_worker(args):
    raw, index, seed, folder = args
    cfg = from_dict(raw)
    case = cfg.cases[index]
    path = Path(folder)
    path.mkdir(parents=True,exist_ok=True)
    with threadpool_limits(limits=cfg.optimization.blas_threads):
        model = build_model(cfg,case)
        signal = Signal(cfg.duration,cfg.control.nodes,cfg.control.filter_cutoff)
        result = crab(Objective(model,signal,cfg),seed)
    digest = save_arrays(path/"crab.npz",nodes=result.nodes,parameters=result.parameters,
        frequencies=result.frequencies,history=result.history,state=result.state)
    data = {"schema_version":SCHEMA_VERSION,**result.metadata,"array_file":"crab.npz","array_sha256":digest}
    save_json(path/"crab.json",data)
    return data


def _refine_worker(args):
    raw,index,seed,folder = args
    cfg = from_dict(raw)
    case = cfg.cases[index]
    path = Path(folder)
    source = load_checkpoint(path,"crab")
    if source is None:
        raise ValueError("CRAB checkpoint missing")
    with np.load(path/"crab.npz",allow_pickle=False) as saved:
        initial = saved["nodes"]
        crab_arrays = {"crab_"+k:saved[k] for k in saved.files}
    t0 = time.perf_counter()
    with threadpool_limits(limits=cfg.optimization.blas_threads):
        model = build_model(cfg,case)
        signal = Signal(cfg.duration,cfg.control.nodes,cfg.control.filter_cutoff)
        result = grape(Objective(model,signal,cfg),initial)
        checked,arrays = validate_waveform(cfg,case,model,signal,result.nodes)
    arrays.update(crab_arrays)
    arrays["grape_history"] = result.history
    arrays["grape_midpoint_state"] = result.state
    digest = save_arrays(path/"arrays.npz",**arrays)
    data = {"schema_version":SCHEMA_VERSION,"case":case.name,"seed":seed,
        "crab":source,"grape":result.metadata,**checked,"array_file":"arrays.npz","array_sha256":digest,
        "elapsed_refinement_validation_seconds":time.perf_counter()-t0,
        "hilbert_dimension_full":model.dimension*2**model.nqubits,
        "hilbert_dimension_used":len(model.initial),"initial_parity":model.initial_parity}
    save_json(path/"result.json",data)
    return data


def _dispatch(worker, jobs, workers):
    if workers==1:
        for job in jobs:
            yield worker(job)
    else:
        # Spawn avoids inheriting BLAS thread pools and works from the standalone CLI.
        with ProcessPoolExecutor(max_workers=min(workers,len(jobs)),mp_context=multiprocessing.get_context("spawn")) as pool:
            futures = {pool.submit(worker,job):job for job in jobs}
            for future in as_completed(futures):
                yield future.result()


def run_experiment(cfg, destination=None, resume=None, plots=True):
    cfg.validate()
    # Fail impossible targets before starting any expensive optimization.
    for case in cfg.cases:
        build_model(cfg,case)
    root = prepare_run(cfg,destination,resume)
    print(f"Run: {root}",flush=True)
    summary = {"schema_version":SCHEMA_VERSION,"experiment":cfg.name,"cases":[],"complete":False}
    save_json(root/"status.json",{"state":"running"})
    try:
        for index,case in enumerate(cfg.cases):
            case_folder = root/case.name
            case_folder.mkdir(exist_ok=True)
            baseline = load_checkpoint(case_folder,"baseline")
            if baseline is None:
                with threadpool_limits(limits=cfg.optimization.blas_threads):
                    model = build_model(cfg,case)
                    signal = Signal(cfg.duration,cfg.control.nodes,cfg.control.filter_cutoff)
                    zero_nodes = np.zeros((model.ncontrols,cfg.control.nodes))
                    ts = np.linspace(0,cfg.duration,cfg.validation.trajectory_points)
                    baseline_states = continuous_evolution(model,signal,zero_nodes,ts,cfg.validation.atol,cfg.validation.rtol)
                    baseline_metrics = state_metrics(model,baseline_states[-1])
                checksum = save_arrays(case_folder/"baseline.npz",times=ts,states_reduced=baseline_states,
                    parity_indices=model.indices,state_final_full=model.expand(baseline_states[-1]))
                baseline = {"metrics":baseline_metrics,"description":"No modulation; same interacting model and initial preparation",
                    "array_file":"baseline.npz","array_sha256":checksum}
                save_json(case_folder/"baseline.json",baseline)
            seeds = cfg.optimization.seeds
            folders = {s:case_folder/f"seed_{s}" for s in seeds}
            crab_results = {}
            jobs = []
            for seed in seeds:
                done = load_checkpoint(folders[seed],"crab")
                if done is None:
                    jobs.append((cfg.to_dict(),index,seed,str(folders[seed])))
                else:
                    crab_results[seed] = done
            if jobs:
                for result in _dispatch(_crab_worker,jobs,cfg.optimization.workers):
                    crab_results[result["seed"]] = result
                    print(f"{case.name} CRAB seed {result['seed']}: P={result['target_probability']:.6f}, nfev={result['evaluations']}",flush=True)
            ranked = sorted(seeds,key=lambda s:(crab_results[s]["cost"],s))
            chosen = ranked if cfg.optimization.refine_top is None else ranked[:cfg.optimization.refine_top]
            completed = {}
            jobs = []
            for seed in chosen:
                done = load_checkpoint(folders[seed],"result")
                if done is None:
                    jobs.append((cfg.to_dict(),index,seed,str(folders[seed])))
                else:
                    completed[seed] = done
            if jobs:
                for result in _dispatch(_refine_worker,jobs,cfg.optimization.workers):
                    completed[result["seed"]] = result
                    print(f"{case.name} GRAPE seed {result['seed']}: P continuo={result['metrics']['target_probability']:.6f}, validato={result['validation']['passed']}",flush=True)
            items = []
            for seed in sorted(chosen):
                item = dict(completed[seed])
                item["folder"] = str(folders[seed].relative_to(root))
                items.append(item)
            eligible = [x for x in items if x["validation"]["passed"]]
            selected = min(eligible or items,key=lambda x:(x["metrics"]["continuous_objective"],x["seed"]))
            probabilities = np.array([x["metrics"]["target_probability"] for x in items])
            stats = {"count":len(items),"probability_mean":float(np.mean(probabilities)),
                "probability_std_population":float(np.std(probabilities)),"probability_median":float(np.median(probabilities)),
                "probability_min":float(np.min(probabilities)),"probability_max":float(np.max(probabilities)),
                "numerically_valid_count":len(eligible),
                "validated_goal_count":sum(x["metrics"]["goal_reached"] for x in eligible),
                "selection_bias_top_only":cfg.optimization.refine_top is not None and cfg.optimization.refine_top<len(seeds)}
            summary["cases"].append({"name":case.name,"statistics":stats,"selected_seed":selected["seed"],
                "baseline":baseline,"all_crab":[crab_results[s] for s in seeds],"seeds":items})
            save_json(root/"summary.json",summary)
        summary["complete"] = True
        save_json(root/"summary.json",summary)
        write_reports(root,make_figures=plots)
        save_json(root/"status.json",{"state":"complete","all_selected_numerically_valid":all(
            next(s for s in c["seeds"] if s["seed"]==c["selected_seed"])["validation"]["passed"] for c in summary["cases"])})
    except BaseException as exc:
        save_json(root/"status.json",{"state":"interrupted" if isinstance(exc,KeyboardInterrupt) else "failed",
                  "exception":type(exc).__name__,"message":str(exc)})
        raise
    return root
