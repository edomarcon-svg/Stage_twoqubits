"""Import explicit saved commands, never silently interpret modulation as frequency."""
import hashlib
from pathlib import Path
import numpy as np
from .controls import feasible_nodes, logical_bounds


def import_nodes(spec, model, signal, control):
    path = Path(spec["path"])
    with np.load(path, allow_pickle=False) as data:
        if spec["format"] == "v2":
            times = data["command_times"]
            # Physical channels allow common -> independent transfer.
            physical = data["physical_command_modulation"] if "physical_command_modulation" in data else data["command_modulation"]
        else:
            stage = spec["format"].removeprefix("legacy_")
            times = data["tlist_fine" if stage == "smooth" else "tlist_"+stage]
            total = np.atleast_2d(data["ctrl_"+stage])
            if total.shape[0] != model.nqubits:
                raise ValueError("Legacy warm start must have the same physical channel count")
            physical = total - model.bare_frequencies[:, None]
        times = np.asarray(times, float)
        physical = np.atleast_2d(np.asarray(physical, float))
    if times.ndim != 1 or len(times) < 2 or physical.shape[1] != len(times) or not np.all(np.isfinite(times)) or not np.all(np.isfinite(physical)) or np.any(np.diff(times) <= 0) or abs(times[0]) > 1e-12:
        raise ValueError("Invalid warm-start time grid or controls")
    source_duration = float(times[-1])
    if not np.isclose(source_duration, signal.duration, rtol=1e-10, atol=1e-12):
        if not spec.get("rescale_time",False):
            raise ValueError("Warm-start duration differs; explicitly set rescale_time to stretch the command")
        times = times * signal.duration/source_duration
    if physical.shape[0] == 1 and model.nqubits == 2:
        physical = np.repeat(physical,2,axis=0)
    if physical.shape[0] != model.nqubits:
        raise ValueError("Warm-start physical channel count does not match model")
    if model.ncontrols == 1 and model.nqubits == 2 and not np.allclose(physical[0],physical[1],rtol=1e-8,atol=1e-10):
        raise ValueError("Unequal independent controls cannot be silently mapped to common control")
    raw = np.array([np.interp(signal.times,times,row) for row in physical[:model.ncontrols]])
    lo,hi = logical_bounds(model,control)
    nodes = feasible_nodes(raw,lo,hi,control.max_slew,signal.h)
    return nodes, {"source_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
        "source_duration":source_duration,"format":spec["format"],
        "rescale_time":spec.get("rescale_time",False),
        "max_feasibility_adjustment":float(np.max(abs(nodes-raw)))}
