"""Linear control nodes followed by an optional causal first-order actuator.

The exact linear transfer map permits differentiation through the hardware model.
Nodes describe MODULATION around the bare qubit frequency, not total frequency.
The command is zero before 0 and after T; the filter starts in equilibrium.
"""
import numpy as np
from scipy.optimize import LinearConstraint


class Signal:
    def __init__(self, duration, nodes, cutoff=None):
        self.duration = float(duration)
        self.nodes = int(nodes)
        self.times = np.linspace(0, duration, nodes)
        self.cutoff = cutoff
        self.h = self.times[1] - self.times[0]

    @staticmethod
    def _factors(cutoff, s):
        z = cutoff*s
        one_minus_e = -np.expm1(-z)
        # s - (1-exp(-w*s))/w; stable even near t=0.
        ramp = s*(z/2-z*z/6+z**3/24-z**4/120) if abs(z) < 1e-4 else s-one_minus_e/cutoff
        return 1-one_minus_e, one_minus_e, ramp

    def matrix(self, times, derivative=False):
        ts = np.asarray(times, float).ravel()
        eye = np.eye(self.nodes)
        rows = np.zeros((len(ts), self.nodes))
        if self.cutoff is not None:
            response_nodes = np.zeros_like(eye)
            e, om, ramp = self._factors(self.cutoff, self.h)
            for i in range(self.nodes-1):
                response_nodes[i+1] = e*response_nodes[i] + om*eye[i] + ramp*(eye[i+1]-eye[i])/self.h
        for k, t in enumerate(ts):
            if t < 0:
                continue
            if t >= self.duration:
                if self.cutoff is not None:
                    rows[k] = np.exp(-self.cutoff*(t-self.duration))*response_nodes[-1]
                    if derivative:
                        rows[k] *= -self.cutoff
                continue
            i = min(int(t/self.h), self.nodes-2)
            s = t-self.times[i]
            command = eye[i] + s/self.h*(eye[i+1]-eye[i])
            if self.cutoff is None:
                rows[k] = (eye[i+1]-eye[i])/self.h if derivative else command
            else:
                e, om, ramp = self._factors(self.cutoff, s)
                delivered = e*response_nodes[i] + om*eye[i] + ramp*(eye[i+1]-eye[i])/self.h
                rows[k] = self.cutoff*(command-delivered) if derivative else delivered
        return rows

    def values(self, node_values, times):
        return np.asarray(node_values) @ self.matrix(times).T

    def callback(self, node_values):
        # Cache interval response once: callbacks must not build transfer matrices.
        node_values = np.asarray(node_values)
        filtered_nodes = self.values(node_values, self.times)
        def evaluate(t):
            if t < 0:
                return np.zeros(len(node_values))
            if t >= self.duration:
                return np.zeros(len(node_values)) if self.cutoff is None else filtered_nodes[:,-1]*np.exp(-self.cutoff*(t-self.duration))
            i = min(int(t/self.h), self.nodes-2)
            s = t-self.times[i]
            slope = (node_values[:,i+1]-node_values[:,i])/self.h
            if self.cutoff is None:
                return node_values[:,i]+s*slope
            e, om, ramp = self._factors(self.cutoff, s)
            return e*filtered_nodes[:,i]+om*node_values[:,i]+ramp*slope
        return evaluate


def logical_bounds(model, control):
    lo, hi = control.total_frequency_bounds
    lower = np.array([max(lo-model.bare_frequencies[j] for j in np.flatnonzero(model.physical_map[:,k])) for k in range(model.ncontrols)])
    upper = np.array([min(hi-model.bare_frequencies[j] for j in np.flatnonzero(model.physical_map[:,k])) for k in range(model.ncontrols)])
    return lower, upper


def feasible_nodes(raw, lower, upper, max_slew, h):
    """Scale each CRAB waveform into the same convex admissible set as GRAPE."""
    out = np.asarray(raw, float).copy()
    out[:,[0,-1]] = 0
    for k, v in enumerate(out):
        scale = 1.
        if v.max() > upper[k]:
            scale = min(scale, upper[k]/v.max())
        if v.min() < lower[k]:
            scale = min(scale, lower[k]/v.min())
        if max_slew is not None and np.max(abs(np.diff(v))) > max_slew*h:
            scale = min(scale, max_slew*h/np.max(abs(np.diff(v))))
        out[k] *= scale
    return out


def slew_constraint(ncontrols, nnodes, h, limit):
    diff = np.diff(np.eye(nnodes), axis=0)[:,1:-1] / h
    matrix = np.kron(np.eye(ncontrols), diff)
    return LinearConstraint(matrix, -limit, limit)
