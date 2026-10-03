"""Post-optimization sensitivity: actual transfer response and quasi-static errors."""
from copy import deepcopy
import numpy as np
from .controls import Signal
from .models import build_model
from .propagation import continuous_evolution
from .metrics import state_metrics


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
