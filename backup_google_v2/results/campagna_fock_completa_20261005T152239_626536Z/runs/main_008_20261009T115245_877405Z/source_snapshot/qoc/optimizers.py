"""CRAB and GRAPE on the same command nodes, bounds and hardware model."""
from dataclasses import dataclass
import time
import numpy as np
from scipy.optimize import minimize
from .controls import feasible_nodes, logical_bounds, slew_constraint


@dataclass
class OptimizationResult:
    nodes: np.ndarray
    cost: float
    target_probability: float
    state: np.ndarray
    metadata: dict
    history: np.ndarray
    parameters: np.ndarray | None = None
    frequencies: np.ndarray | None = None
    diagnostics: list | None = None


def crab(objective, seed):
    cfg = objective.cfg
    model = objective.model
    opt = cfg.optimization
    rng = np.random.default_rng(seed)
    freqs = rng.uniform(*opt.frequency_range, size=(model.ncontrols,opt.frequencies))
    times = objective.signal.times
    envelope = np.sin(np.pi*times/cfg.duration)**2
    sine = np.sin(freqs[:,:,None]*times)
    cosine = np.cos(freqs[:,:,None]*times)
    lo, hi = logical_bounds(model, cfg.control)
    def construct(params):
        p = params.reshape(model.ncontrols,2,opt.frequencies)
        raw = np.einsum("kf,kfn->kn",p[:,0],sine)+np.einsum("kf,kfn->kn",p[:,1],cosine)
        return feasible_nodes(raw*envelope, lo, hi, cfg.control.max_slew, objective.signal.h)
    history = []
    best = [float("inf"), None]
    def fun(params):
        cost, _, _ = objective.evaluate_nodes(construct(params))
        history.append(cost)
        if cost < best[0]:
            best[:] = [cost, params.copy()]
        return cost
    initial_std = opt.crab_initial_std if opt.crab_initial_std is not None else .15/np.sqrt(opt.frequencies)
    x0 = rng.normal(0, initial_std, size=model.ncontrols*2*opt.frequencies)
    initial_probability = objective.evaluate_nodes(construct(x0))[1]
    t0 = time.perf_counter()
    res = minimize(fun, x0, method="Nelder-Mead", options={"maxfev":opt.crab_max_evaluations,
                   "maxiter":opt.crab_max_evaluations, "xatol":1e-7, "fatol":opt.ftol, "adaptive":True})
    params = best[1]
    nodes = construct(params)
    cost, prob, state = objective.evaluate_nodes(nodes)
    meta = {"algorithm":"CRAB/Nelder-Mead", "seed":seed, "success":bool(res.success),
            "message":str(res.message), "iterations":int(res.nit), "evaluations":int(res.nfev),
            "elapsed_seconds":time.perf_counter()-t0, "cost":cost, "target_probability":prob,
            "fidelity_root":float(np.sqrt(np.clip(prob,0,1))),
            "initial_probability":initial_probability, "probability_gain":prob-initial_probability,
            "initial_std":initial_std, "objective":opt.objective, "objective_scale":opt.objective_scale}
    return OptimizationResult(nodes, cost, prob, state, meta, np.asarray(history), params, freqs)


def grape(objective, initial_nodes):
    cfg = objective.cfg
    opt = cfg.optimization
    lo, hi = logical_bounds(objective.model, cfg.control)
    bounds = [(lo[k],hi[k]) for k in range(objective.model.ncontrols) for _ in range(objective.signal.nodes-2)]
    x0 = initial_nodes[:,1:-1].ravel().copy()
    history = []
    best = [float("inf"), x0.copy()]
    cached = [None,None]
    count = 0
    diagnostics = []
    accepted_iterations = []
    previous = [x0.copy()]
    lower, upper = np.asarray(bounds).T
    def gradient_info(x, gradient):
        projected = x - np.clip(x - gradient, lower, upper)
        return {"gradient_max":float(np.max(abs(gradient))),
                "projected_gradient_max":float(np.max(abs(projected)))}
    def callback(x):
        # SciPy calls this after an accepted iterate; fun is normally cached.
        value, gradient = fun(x)
        accepted_iterations.append({"iteration":len(accepted_iterations)+1,
            "cost":float(value), "target_probability":float(objective.last_probability),
            "command_step_max":float(np.max(abs(x-previous[0]))), **gradient_info(x,gradient)})
        previous[0] = x.copy()
    class BudgetExceeded(Exception):
        pass
    def feasible(x):
        nodes = objective.unpack(x)
        tol = 1e-9
        if np.any(nodes < lo[:,None]-tol) or np.any(nodes > hi[:,None]+tol):
            return False
        return cfg.control.max_slew is None or np.max(abs(np.diff(nodes,axis=1)))/objective.signal.h <= cfg.control.max_slew+tol
    def fun(x):
        nonlocal count
        if cached[0] is not None and np.array_equal(x,cached[0]):
            return cached[1]
        if count >= opt.grape_max_evaluations:
            raise BudgetExceeded()
        out = objective(x)
        count += 1
        history.append(out[0])
        diagnostics.append({"evaluation":count,"cost":float(out[0]),
            "target_probability":float(objective.last_probability), **gradient_info(x,out[1])})
        if feasible(x) and out[0] < best[0]:
            best[:] = [out[0],x.copy()]
        cached[:] = [x.copy(),out]
        return out
    method = "L-BFGS-B" if cfg.control.max_slew is None else "SLSQP"
    kwargs = {}
    options = {"maxiter":opt.grape_max_iterations,"ftol":opt.ftol}
    if method == "L-BFGS-B":
        options.update(gtol=opt.gtol,maxfun=opt.grape_max_evaluations,maxls=30)
    else:
        kwargs["constraints"] = [slew_constraint(objective.model.ncontrols, objective.signal.nodes, objective.signal.h, cfg.control.max_slew)]
    t0 = time.perf_counter()
    try:
        res = minimize(fun, x0, jac=True, method=method, bounds=bounds, options=options, callback=callback, **kwargs)
        success, message, nit = bool(res.success), str(res.message), int(res.nit)
    except BudgetExceeded:
        success, message, nit = False,"Explicit objective-evaluation budget exhausted",None
    # Retain the best feasible waveform, including the initial CRAB waveform.
    nodes = objective.unpack(best[1])
    cost, prob, state = objective.evaluate_nodes(nodes)
    _, final_grad = objective.evaluate_nodes(nodes, gradient=True)
    meta = {"algorithm":"GRAPE/"+method,"success":success,"message":message,
            "iterations":nit,"evaluations":count,"elapsed_seconds":time.perf_counter()-t0,
            "cost":cost,"target_probability":prob,"fidelity_root":float(np.sqrt(np.clip(prob,0,1))),
            "objective":opt.objective,"objective_scale":opt.objective_scale,
            "initial_probability":diagnostics[0]["target_probability"],
            "probability_gain":prob-diagnostics[0]["target_probability"],
            "initial_gradient":{k:diagnostics[0][k] for k in ["gradient_max","projected_gradient_max"]},
            "final_gradient":gradient_info(best[1],final_grad),
            "projected_gradient_scope":"box bounds only; slew constraints excluded",
            "accepted_iterations":accepted_iterations,
            "extra_final_gradient_evaluations":1}
    return OptimizationResult(nodes,cost,prob,state,meta,np.asarray(history),diagnostics=diagnostics)
