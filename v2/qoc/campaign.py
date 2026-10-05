"""Multi-target campaigns: fixed plan, paired random restarts and resumable children."""
from copy import deepcopy
import csv
import html
import json
import math
from pathlib import Path
import numpy as np
from .config import from_dict, _without_json_comments
from .models import build_model
from .pipeline import run_experiment
from .storage import prepare_run, save_json


def _keys(data, allowed, required=()):
    if not isinstance(data,dict) or set(data)-set(allowed) or set(required)-set(data):
        raise ValueError(f"Invalid campaign fields; allowed={sorted(allowed)}, required={list(required)}")


def _merge(base, update):
    result = deepcopy(base)
    for key,value in update.items():
        if isinstance(value,dict) and isinstance(result.get(key),dict):
            result[key] = _merge(result[key],value)
        else:
            result[key] = deepcopy(value)
    return result


def load_campaign(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    spec = json.loads(_without_json_comments(text) if path.suffix == ".jsonc" else text)
    def resolve(value):
        if isinstance(value,dict):
            for warm in value.get("warm_starts",[]):
                warm["path"] = str((path.parent/warm["path"]).resolve())
            for child in value.values(): resolve(child)
        elif isinstance(value,list):
            for child in value: resolve(child)
    resolve(spec)
    campaign_plan(spec)
    return spec


def campaign_plan(spec):
    _keys(spec,{"name","base","blocks","pilot"},{"name","base","blocks"})
    if not isinstance(spec["name"],str) or not spec["name"] or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in spec["name"]):
        raise ValueError("Campaign name must be a safe nonempty identifier")
    base = from_dict(spec["base"])
    dt = base.duration/base.intervals
    dh = base.duration/(base.control.nodes-1)
    jobs = []
    names = set()
    def add(stage,block,target,factor,cutoff,case_names,optimization=None,profile=None):
        if isinstance(factor,bool) or not isinstance(factor,int) or factor < 1:
            raise ValueError("factors_taus must be positive integers")
        if cutoff is not None and (isinstance(cutoff,bool) or not isinstance(cutoff,(int,float)) or not math.isfinite(cutoff) or cutoff <= 0):
            raise ValueError("cutoff must be positive or null (no filter)")
        raw = base.to_dict()
        raw["target"] = deepcopy(target)
        raw["factor_taus"] = factor
        duration = factor*base.tau_s
        raw["intervals"] = max(2,math.ceil(duration/dt-1e-10))
        raw["control"]["nodes"] = max(3,math.ceil(duration/dh-1e-10)+1)
        raw["control"]["filter_cutoff"] = cutoff
        raw["validation"]["trajectory_points"] = max(3,math.ceil((base.validation.trajectory_points-1)*duration/base.duration-1e-10)+1)
        if not case_names or len(set(case_names)) != len(case_names) or set(case_names)-{c.name for c in base.cases}:
            raise ValueError("Unknown, duplicate or empty campaign cases")
        raw["cases"] = [c for c in raw["cases"] if c["name"] in case_names]
        raw["optimization"] = _merge(raw["optimization"],optimization or {})
        if stage == "pilot":
            raw["optimization"]["warm_starts"] = []
        else:
            raw["optimization"]["warm_starts"] = [w for w in raw["optimization"]["warm_starts"] if w["case"] in case_names]
        raw["name"] = f"{stage}_{len(jobs):03d}"
        cfg = from_dict(raw)
        jobs.append({"id":raw["name"],"stage":stage,"block":block,"profile":profile,"config":cfg.to_dict()})
    pilot = spec.get("pilot",{})
    if pilot:
        _keys(pilot,{"enabled","cases","target","factor_taus","filter_cutoff","seeds","profiles","budgets","minimum_probability_gain"},
            {"enabled","cases","target","factor_taus","filter_cutoff","seeds","profiles","budgets"})
        if not isinstance(pilot["enabled"],bool): raise ValueError("pilot.enabled must be boolean")
        if pilot.get("minimum_probability_gain",1e-6) < 0: raise ValueError("minimum_probability_gain must be nonnegative")
        _keys(pilot["budgets"],{"crab_max_evaluations","grape_max_iterations","grape_max_evaluations"})
        profile_names = set()
        if not pilot["profiles"]: raise ValueError("Pilot profiles cannot be empty")
        for profile in pilot["profiles"]:
            _keys(profile,{"name","optimization"},{"name","optimization"})
            if not isinstance(profile["name"],str) or not profile["name"] or profile["name"] in profile_names:
                raise ValueError("Pilot profile names must be nonempty and unique")
            profile_names.add(profile["name"])
            _keys(profile["optimization"],{"objective","objective_scale","root_epsilon","crab_initial_std","ftol","gtol"})
            if pilot["enabled"]:
                opt = _merge(profile["optimization"],pilot["budgets"])
                opt["seeds"] = pilot["seeds"]
                opt["refine_top"] = None
                add("pilot","pilot",pilot["target"],pilot["factor_taus"],pilot["filter_cutoff"],pilot["cases"],opt,profile["name"])
    if not isinstance(spec["blocks"],list) or not spec["blocks"]: raise ValueError("blocks must be nonempty")
    for block in spec["blocks"]:
        _keys(block,{"name","enabled","targets","factors_taus","cutoffs","cases","optimization"},
            {"name","targets","factors_taus","cutoffs"})
        if not isinstance(block["name"],str) or not block["name"] or block["name"] in names: raise ValueError("Block names must be unique")
        names.add(block["name"])
        if not isinstance(block.get("enabled",True),bool): raise ValueError("block.enabled must be boolean")
        if not all(isinstance(block[k],list) and block[k] for k in ["targets","factors_taus","cutoffs"]):
            raise ValueError("Each block requires nonempty targets, factors_taus and cutoffs")
        if not block.get("enabled",True): continue
        for target in block["targets"]:
            for factor in block["factors_taus"]:
                for cutoff in block["cutoffs"]:
                    add("main",block["name"],target,factor,cutoff,block.get("cases",[c.name for c in base.cases]),block.get("optimization"))
    if not any(j["stage"] == "main" for j in jobs): raise ValueError("No enabled main experiments")
    # Pilot and production draws must not be reused for selecting and assessing a profile.
    pilot_seeds = set(pilot.get("seeds",[])) if pilot.get("enabled") else set()
    if any(pilot_seeds & set(j["config"]["optimization"]["seeds"]) for j in jobs if j["stage"] == "main"):
        raise ValueError("Use disjoint seeds for pilot selection and main campaign")
    return jobs


def plan_counts(jobs):
    result = {}
    for stage in ["pilot","main"]:
        subset = [j for j in jobs if j["stage"] == stage]
        result[stage] = {"experiments":len(subset),
            "random_pipelines":sum(len(j["config"]["cases"])*len(j["config"]["optimization"]["seeds"]) for j in subset),
            "warm_starts":sum(len(j["config"]["optimization"]["warm_starts"]) for j in subset)}
    return result


def select_profile(spec, summaries):
    """Select on pilot cases only; no main-run outcomes enter the selection."""
    pilot = spec["pilot"]
    scores = []
    for profile in pilot["profiles"]:
        summary = summaries[profile["name"]]
        values, gains, viable = [], [], True
        for case in summary["cases"]:
            items = case["seeds"]
            values.append(float(np.median([x["metrics"]["target_probability"] if x["validation"]["passed"] else 0. for x in items])))
            gain = max(x["metrics"]["target_probability"] - x["crab"]["initial_probability"] for x in items)
            gains.append(gain)
            viable &= any(x["validation"]["passed"] and (x["metrics"]["goal_reached"] or (
                x["metrics"]["target_probability"]-x["crab"]["initial_probability"] >= pilot.get("minimum_probability_gain",1e-6)
                and len(x["grape"].get("accepted_iterations",[])) > 0)) for x in items)
        scores.append({"profile":profile["name"],"viable":bool(viable),
            "mean_of_case_median_valid_probability":float(np.mean(values)),"case_probability_gains":gains})
    eligible = [s for s in scores if s["viable"]]
    selected = max(eligible,key=lambda s:s["mean_of_case_median_valid_probability"]) if eligible else None
    return {"selected_profile":selected["profile"] if selected else None,"scores":scores,
        "criterion":"Mean of per-case median validated probability; invalid draws count as zero. Require a validated improving GRAPE attempt (or goal reached) in every pilot case. Main seeds are disjoint."}


def write_campaign_report(root, spec, jobs, state):
    rows, experiments = [], []
    for job in jobs:
        entry = state["jobs"].get(job["id"],{})
        if not entry.get("run"): continue
        run = root/entry["run"]
        if not (run/"summary.json").exists(): continue
        summary = json.loads((run/"summary.json").read_text())
        cfg = json.loads((run/"config.json").read_text())
        for case in summary["cases"]:
            shared = {"stage":job["stage"],"block":job["block"],"profile":entry.get("profile",job["profile"]),
                "target":json.dumps(cfg["target"],sort_keys=True),"factor_taus":cfg["factor_taus"],
                "duration":cfg["duration"],"filter_cutoff":cfg["control"]["filter_cutoff"],"case":case["name"],
                "run":str(run.relative_to(root)),"objective":cfg["optimization"]["objective"],
                "crab_initial_std":cfg["optimization"]["crab_initial_std"]}
            experiments.append({**shared,**case["statistics"]})
            for item in case["seeds"] + case.get("warm_starts",[]):
                m,v,g,c,a = (item[k] for k in ["metrics","validation","grape","crab","actuator"])
                rows.append({**shared,"seed":item["seed"],"cohort":item.get("cohort","random"),
                    "P":m["target_probability"],"F_root":m["fidelity_root"],"valid":v["passed"],
                    "goal":m["goal_reached"],"validated_goal":v["passed"] and m["goal_reached"],
                    "P_initial":c.get("initial_probability"),"P_crab":c["target_probability"],
                    "crab_gain":c.get("probability_gain"),"grape_gain":g.get("probability_gain"),
                    "grape_iterations":g["iterations"],"stop_reason":g["message"],
                    "initial_projected_gradient":g.get("initial_gradient",{}).get("projected_gradient_max"),
                    "final_projected_gradient":g.get("final_gradient",{}).get("projected_gradient_max"),
                    "max_mean_photons":m.get("max_mean_photons_preparation"),
                    "max_edge_population":v["max_edge_population"],"max_norm_error":v["max_norm_error"],
                    "dimension_trace_distance":v["dimension_cavity_trace_distance"],
                    "hold_P_min":(item.get("hold_summary") or {}).get("minimum_target_probability"),
                    "hold_P_final":(item.get("hold_metrics") or {}).get("target_probability"),
                    "fluence":a["modulation_fluence_total"],"slew":a["slew_worst_channel"],
                    "omega99":a["omega_99_worst_channel"],"spectral_power_above_threshold":a.get("ac_power_fraction_above_threshold_worst"),
                    "spectral_threshold":cfg["validation"]["spectral_threshold"],
                    "crab_seconds":c["elapsed_seconds"],"refinement_validation_seconds":item["elapsed_refinement_validation_seconds"],
                    "folder":str((run/item["folder"]).relative_to(root))})
    for name,records in [("seeds.csv",rows),("summary.csv",experiments)]:
        temp = root/(name+".tmp")
        with temp.open("w",newline="",encoding="utf-8") as f:
            writer = csv.DictWriter(f,fieldnames=list(records[0]) if records else ["stage"])
            writer.writeheader();writer.writerows(records)
        temp.replace(root/name)
    save_json(root/"summary.json",{"state":state["state"],"counts":plan_counts(jobs),"experiments":experiments})
    body = ["<h1>Campagna multi-target</h1>",f"<p>Stato: {html.escape(state['state'])}</p>",
        "<p>Statistiche su partenze casuali; warm start separati in seeds.csv. Pilot escluso dal confronto principale. Mancato successo non dimostra un limite fisico.</p>",
        "<p><a href='summary.csv'>Statistiche</a> · <a href='seeds.csv'>Tutti i tentativi e diagnostiche</a> · <a href='campaign.json'>Configurazione</a> · <a href='state.json'>Stato e ripresa</a></p>"]
    if (root/"pilot_selection.json").exists():
        body.append("<p><a href='pilot_selection.json'>Confronto e selezione del collaudo</a></p>")
    body.append("<table><tr><th>Fase</th><th>Target</th><th>T/τs</th><th>Filtro</th><th>Sistema</th><th>P mediana</th><th>Successi validati</th><th>Report</th></tr>")
    for row in experiments:
        label = json.loads(row["target"])
        values = [row["stage"],f"{label['kind']} {label['value']}",row["factor_taus"],row["filter_cutoff"],row["case"],f"{row['probability_median']:.6g}",f"{row['validated_goal_count']}/{row['count']}"]
        body.append("<tr>"+"".join(f"<td>{html.escape(str(x))}</td>" for x in values)+f"<td><a href='{html.escape(row['run'],quote=True)}/report.html'>Apri</a></td></tr>")
    body.append("</table>")
    (root/"report.html").write_text("<!doctype html><html lang='it'><meta charset='utf-8'><title>Campagna QOC</title><style>body{font:16px system-ui;margin:30px}td,th{padding:8px;border:1px solid #ccc}table{border-collapse:collapse}</style><body>"+"\n".join(body)+"</body></html>")


def run_campaign(spec, destination=None, resume=None, plots=True, pilot_only=False):
    jobs = campaign_plan(spec)
    base = from_dict(spec["base"]);base.name = spec["name"]
    # Preflight every distinct target/case, including parity constraints.
    checked = set()
    for job in jobs:
        cfg = from_dict(job["config"])
        for case in cfg.cases:
            key = json.dumps([cfg.target.__dict__,case.__dict__,cfg.initial_state,cfg.dimension,cfg.parity_reduction],sort_keys=True)
            if key not in checked:
                build_model(cfg,case);checked.add(key)
    root = prepare_run(base,destination,resume)
    print(f"Campaign: {root}",flush=True)
    if resume:
        if json.loads((root/"campaign.json").read_text()) != spec:
            raise ValueError("Resume refused: campaign configuration differs")
        state = json.loads((root/"state.json").read_text())
    else:
        save_json(root/"campaign.json",spec)
        save_json(root/"plan.json",jobs)
        state = {"state":"running","jobs":{}}
    state.pop("error",None)
    save_json(root/"state.json",state)
    selected = None
    summaries = {}
    try:
        for job in jobs:
            if job["stage"] == "main" and spec.get("pilot",{}).get("enabled") and selected is None:
                decision = select_profile(spec,summaries)
                save_json(root/"pilot_selection.json",decision)
                selected = decision["selected_profile"]
                if selected is None:
                    state["state"] = "pilot_failed"
                    print("Pilot did not produce a validated improving attempt in every diagnostic case; main campaign not started. Inspect pilot_selection.json.",flush=True)
                    break
                if pilot_only:
                    state["state"] = "pilot_complete"
                    break
            if job["stage"] == "main" and pilot_only:
                state["state"] = "pilot_complete"
                break
            cfg = from_dict(job["config"])
            if selected and job["stage"] == "main":
                profile = next(p for p in spec["pilot"]["profiles"] if p["name"] == selected)
                raw = cfg.to_dict();raw["optimization"] = _merge(raw["optimization"],profile["optimization"])
                cfg = from_dict(raw)
            entry = state["jobs"].setdefault(job["id"],{})
            if "run" in entry:
                run = prepare_run(cfg,resume=root/entry["run"])
            else:
                run = prepare_run(cfg,root/"runs")
                entry.update(run=str(run.relative_to(root)),profile=selected if job["stage"] == "main" else job["profile"],state="pending")
                save_json(root/"state.json",state)
            entry["state"] = "running"
            state["state"] = "running"
            save_json(root/"state.json",state)
            # run_experiment verifies every checkpoint, and regenerates summaries on resume.
            run_experiment(cfg,resume=run,plots=plots)
            entry["state"] = "complete"
            if job["stage"] == "pilot": summaries[job["profile"]] = json.loads((run/"summary.json").read_text())
            save_json(root/"state.json",state)
            write_campaign_report(root,spec,jobs,state)
        else:
            state["state"] = "complete"
    except BaseException as exc:
        state["state"] = "interrupted" if isinstance(exc,KeyboardInterrupt) else "failed"
        state["error"] = {"type":type(exc).__name__,"message":str(exc)}
        raise
    finally:
        save_json(root/"state.json",state)
        write_campaign_report(root,spec,jobs,state)
    return root
