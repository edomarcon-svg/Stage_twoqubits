"""Post-optimization sensitivity: actual transfer response and quasi-static errors."""
from copy import deepcopy
import numpy as np
from .controls import Signal
from .models import build_model
from .propagation import continuous_evolution
from .metrics import state_metrics, initial_state_metrics


def initial_state_analysis(cfg, case, nodes):
    """Compare bare |0,g...> and dressed ground |E0> initial states and cross-evaluate a pulse."""
    signal = Signal(cfg.duration,cfg.control.nodes,cfg.control.filter_cutoff)
    results = {}
    models = {}
    for kind in ["bare", "ground"]:
        trial_cfg = deepcopy(cfg)
        trial_cfg.initial_state = kind
        m = build_model(trial_cfg, case)
        models[kind] = m
        final = continuous_evolution(m, signal, nodes, [0, cfg.duration], cfg.validation.atol, cfg.validation.rtol)[-1]
        results[kind] = {
            "initial": initial_state_metrics(m),
            "final": state_metrics(m, final)
        }
    bare_full = models["bare"].expand(models["bare"].initial)
    ground_full = models["ground"].expand(models["ground"].initial)
    overlap = float(abs(np.vdot(bare_full, ground_full))**2)
    return {
        "nominal_initial_state": cfg.initial_state,
        "bare_ground_overlap_probability": overlap,
        "dressed_energy_shift": float(results["ground"]["initial"]["drift_energy"] - results["bare"]["initial"]["drift_energy"]),
        "ground_virtual_photons": float(results["ground"]["initial"]["mean_photons"]),
        "ground_cavity_purity": float(results["ground"]["initial"]["purity"]),
        "bare": results["bare"],
        "ground": results["ground"],
        "target_probability_bare": float(results["bare"]["final"]["target_probability"]),
        "target_probability_ground": float(results["ground"]["final"]["target_probability"]),
        "target_probability_difference_ground_minus_bare": float(
            results["ground"]["final"]["target_probability"] - results["bare"]["final"]["target_probability"]
        )
    }


def filter_scan(cfg, case, nodes, cutoffs):
    model = build_model(cfg,case)
    output = []
    for cutoff in cutoffs:
        if cutoff is not None and (not np.isfinite(cutoff) or cutoff<=0):
            raise ValueError("Filter cutoffs must be positive or null")
        signal = Signal(cfg.duration,cfg.control.nodes,cutoff)
        final = continuous_evolution(model,signal,nodes,[0,cfg.duration],cfg.validation.atol,cfg.validation.rtol)[-1]
        output.append({"cutoff":cutoff,**state_metrics(model,final)})
    return output


def static_noise_ensemble(cfg, case, nodes, samples, seed=1234, gain_std=0., detuning_std=0., coupling_relative_std=0.):
    if samples<1 or min(gain_std,detuning_std,coupling_relative_std)<0:
        raise ValueError("samples >= 1 and nonnegative standard deviations required")
    rng = np.random.default_rng(seed)
    output = []
    signal = Signal(cfg.duration,cfg.control.nodes,cfg.control.filter_cutoff)
    # Real actuators fluctuate independently even if their nominal command is common.
    nominal = build_model(cfg,case)
    physical_nodes = nominal.physical_map@nodes
    for i in range(samples):
        perturbed = deepcopy(case)
        perturbed.control = "independent"
        nq = len(case.couplings)
        gains = 1+rng.normal(0,gain_std,nq)
        detunings = rng.normal(0,detuning_std,nq)
        coupling_factors = 1+rng.normal(0,coupling_relative_std,nq)
        perturbed.qubit_frequencies = (np.array(case.qubit_frequencies)+detunings).tolist()
        perturbed.couplings = (np.array(case.couplings)*coupling_factors).tolist()
        model = build_model(cfg,perturbed)
        # Keep the nominal initial preparation fixed; noise affects the dynamics.
        # If parity sectors differ, use a full-space model rather than projecting away state.
        if model.initial_parity!=nominal.initial_parity:
            full_cfg = deepcopy(cfg)
            full_cfg.parity_reduction = False
            model = build_model(full_cfg,perturbed)
        model.initial = nominal.expand(nominal.initial)[model.indices]
        model.initial_parity = nominal.initial_parity
        noisy_nodes = gains[:,None]*physical_nodes
        final = continuous_evolution(model,signal,noisy_nodes,[0,cfg.duration],cfg.validation.atol,cfg.validation.rtol)[-1]
        ts = np.linspace(0,cfg.duration,cfg.validation.trajectory_points)
        total = np.array(perturbed.qubit_frequencies)[:,None]+signal.values(noisy_nodes,ts)
        lo,hi = cfg.control.total_frequency_bounds
        output.append({"sample":i,"gains":gains.tolist(),"detunings":detunings.tolist(),
            "coupling_factors":coupling_factors.tolist(),"bounds_exceeded":bool(np.any(total<lo)|np.any(total>hi)),
            **state_metrics(model,final)})
    ps = np.array([x["target_probability"] for x in output])
    return {"noise_model":"independent quasi-static Gaussian gain/detuning/coupling errors; fixed nominal preparation",
        "random_seed":seed,"gain_std":gain_std,"detuning_std":detuning_std,"coupling_relative_std":coupling_relative_std,
        "probability_mean":float(ps.mean()),"probability_std_population":float(ps.std()),
        "probability_quantiles_05_50_95":np.quantile(ps,[.05,.5,.95]).tolist(),
        "goal_fraction":float(np.mean(ps>=cfg.target_probability_goal)),"samples":output}
