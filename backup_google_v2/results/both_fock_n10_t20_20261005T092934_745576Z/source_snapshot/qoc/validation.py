"""Every reported final result is checked with independent continuous dynamics."""
import numpy as np
from .models import build_model
from .propagation import continuous_evolution, propagate_midpoint
from .metrics import state_metrics, actuator_metrics, phase_space
from .controls import logical_bounds


def validate_waveform(cfg, case, model, signal, nodes):
    v = cfg.validation
    times = np.linspace(0,cfg.duration,v.trajectory_points)
    if v.hold_time:
        times = np.r_[times,np.linspace(cfg.duration,cfg.duration+v.hold_time,101)[1:]]
    states = continuous_evolution(model,signal,nodes,times,v.atol,v.rtol)
    final = states[v.trajectory_points-1]
    metrics = state_metrics(model,final)
    act = actuator_metrics(model,signal,nodes)
    ntraj, purity, edges, cavity_fidelity, qpop, singlet = [], [], [], [], [], []
    for state in states:
        full = model.expand(state).reshape(model.dimension,-1)
        rho = full@full.conj().T
        pops = np.diag(rho).real
        ntraj.append(float(pops@np.arange(model.dimension)))
        edges.append(float(sum(pops[-v.edge_levels:])))
        purity.append(float(np.trace(rho@rho).real))
        cavity_fidelity.append(float(np.sqrt(max(0,np.vdot(model.target_cavity,rho@model.target_cavity).real))))
        qrho = full.T@full.conj()
        qpop.append(np.diag(qrho).real)
        if model.nqubits==2:
            s = np.array([0,1,-1,0])/np.sqrt(2)
            singlet.append(float(np.vdot(s,qrho@s).real))
    norm_error = float(np.max(abs(np.sum(abs(states)**2,axis=1)-1)))
    probs = []
    for intervals in [cfg.intervals,2*cfg.intervals]:
        tm = (np.arange(intervals)+.5)*cfg.duration/intervals
        prob,_ = propagate_midpoint(model,signal.values(nodes,tm),cfg.duration)
        probs.append(prob)
    tight_state = continuous_evolution(model,signal,nodes,[0,cfg.duration],v.atol/10,v.rtol/10,signal.h/16)[-1]
    tight_p = float(np.vdot(tight_state,model.target_operator@tight_state).real)
    large = build_model(cfg,case,dimension=cfg.dimension+v.dimension_increment)
    large_states = continuous_evolution(large,signal,nodes,np.linspace(0,cfg.duration,v.trajectory_points),v.atol,v.rtol)
    large_metrics = state_metrics(large,large_states[-1])
    target_padded = np.pad(model.target_cavity,(0,v.dimension_increment))
    target_discrepancy = float(max(0,1-abs(np.vdot(target_padded,large.target_cavity))**2))
    # Compare the whole cavity state, not just its overlap with one target.
    rho = model.cavity_density(final)
    large_rho = large.cavity_density(large_states[-1])
    rho_padded = np.pad(rho,((0,v.dimension_increment),(0,v.dimension_increment)))
    cavity_trace_distance = float(.5*np.sum(abs(np.linalg.eigvalsh(rho_padded-large_rho))))
    init_small = np.pad(model.expand(model.initial),(0,v.dimension_increment*2**model.nqubits))
    initial_discrepancy = float(max(0,1-abs(np.vdot(init_small,large.expand(large.initial)))**2))
    initial_dim_parity_match = model.initial_parity == large.initial_parity
    # Target and initial state constructors must converge as well as dynamics.
    root = metrics["fidelity_root"]
    mid_error = abs(root-np.sqrt(np.clip(probs[0],0,1)))
    refined_error = abs(root-np.sqrt(np.clip(probs[1],0,1)))
    ode_error = abs(root-np.sqrt(np.clip(tight_p,0,1)))
    dim_error = abs(root-large_metrics["fidelity_root"])
    lo,hi = logical_bounds(model,cfg.control)
    bound_ok = bool(np.all(nodes>=lo[:,None]-1e-9) and np.all(nodes<=hi[:,None]+1e-9))
    slew_ok = cfg.control.max_slew is None or float(np.max(abs(np.diff(nodes,axis=1)))/signal.h)<=cfg.control.max_slew+1e-8
    endpoint_ok = bool(np.max(abs(nodes[:,[0,-1]]))<1e-12)
    checks = {
        "time_grid":bool(mid_error<=v.fidelity_tolerance and refined_error<=v.fidelity_tolerance),
        "ode_tolerance":bool(ode_error<=v.fidelity_tolerance/10),
        "dimension":bool(dim_error<=v.truncation_tolerance and cavity_trace_distance<=v.truncation_tolerance),
        "target_construction":bool(target_discrepancy<=v.truncation_tolerance),
        "initial_construction":bool(initial_discrepancy<=v.truncation_tolerance and initial_dim_parity_match),
        "edge_population":bool(max(edges)<=v.edge_tolerance),
        "norm":bool(norm_error<=max(1e-7,100*v.atol)),
        "parity":bool(metrics["parity_error"]<=max(1e-7,100*v.atol)),
        "command_bounds":bound_ok,"command_slew":bool(slew_ok),"command_endpoints":endpoint_ok,
    }
    diagnostics = {"passed":all(checks.values()),"checks":checks,
        "midpoint_fidelity_error":float(mid_error),"double_intervals_fidelity_error":float(refined_error),
        "tighter_ode_fidelity_error":float(ode_error),"dimension_fidelity_error":float(dim_error),
        "dimension_cavity_trace_distance":cavity_trace_distance,"target_truncation_error":target_discrepancy,
        "initial_truncation_error":initial_discrepancy,"max_edge_population":max(edges),
        "max_norm_error":norm_error,"larger_dimension":large.dimension,
        "larger_dimension_metrics":large_metrics}
    grid,wigner,wmetrics = phase_space(model,rho,v.phase_grid_points)
    metrics.update(wmetrics)
    # Continuous cost uses continuous-state overlap and a dense quadrature of the
    # actual delivered modulation, with the same physical-channel normalization.
    metrics["continuous_objective"] = float(1-metrics["target_probability"] +
        cfg.control.fluence_weight*act["modulation_fluence_total"]/cfg.duration +
        cfg.control.slew_weight*sum(x["slew_rms"]**2 for x in act["channels"]))
    metrics["goal_reached"] = bool(metrics["target_probability"]>=cfg.target_probability_goal)
    hold = state_metrics(model,states[-1]) if v.hold_time else None
    arrays = {"command_times":signal.times,"command_modulation":nodes,
        "physical_command_modulation":model.physical_map@nodes,
        "times":times,"delivered_modulation":signal.values(nodes,times),
        "physical_delivered_modulation":model.physical_map@signal.values(nodes,times),
        "physical_total_frequency":model.bare_frequencies[:,None]+model.physical_map@signal.values(nodes,times),
        "states_reduced":states,"parity_indices":model.indices,"state_final_full":model.expand(final),
        "rho_cavity_final":rho,"target_cavity":model.target_cavity,"mean_photons":np.asarray(ntraj),
        "purity":np.asarray(purity),"edge_population":np.asarray(edges),
        "cavity_fidelity_root":np.asarray(cavity_fidelity),"qubit_basis_populations":np.asarray(qpop),
        "wigner_grid":grid,"wigner_final":wigner,"photon_distribution":np.diag(rho).real,
        "singlet_population":np.asarray(singlet)}
    return {"metrics":metrics,"actuator":act,"validation":diagnostics,"hold_metrics":hold},arrays
