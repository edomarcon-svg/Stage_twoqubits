"""Ket propagators and exact derivatives of each finite-time exponential."""
import numpy as np
import qutip as qt


def propagate_midpoint(model, amplitudes, duration, gradient=False, intervals=None):
    """N amplitudes -> exactly N intervals of duration T/N.

    The exponential and its derivative are exact for each constant interval.
    Approximating a continuous signal by its midpoint values is a separate,
    explicitly validated time-discretization approximation.
    """
    amplitudes = np.asarray(amplitudes)
    n = amplitudes.shape[1]
    dt = duration/n
    psi = model.initial.copy()
    states = [psi] if gradient else None
    eigensystems = [] if gradient else None
    for t in range(n):
        h = model.drift + np.einsum("k,kij->ij", amplitudes[:,t], model.controls)
        energy, v = np.linalg.eigh(h)
        phases = np.exp(-1j*dt*energy)
        psi = v @ (phases*(v.conj().T @ psi))
        if gradient:
            eigensystems.append((energy, v, phases))
            states.append(psi)
    probability = float(np.vdot(psi, model.target_operator @ psi).real)
    if not gradient:
        return probability, psi
    adjoint = model.target_operator @ psi
    deriv = np.zeros_like(amplitudes, dtype=float)
    for t in range(n-1, -1, -1):
        energy, v, phases = eigensystems[t]
        before = v.conj().T @ states[t]
        after = v.conj().T @ adjoint
        differences = energy[:,None]-energy[None,:]
        means = (energy[:,None]+energy[None,:])/2
        # Divided differences of exp(-i dt H), including degenerate eigenvalues.
        frechet_factor = -1j*dt*np.exp(-1j*dt*means)*np.sinc(dt*differences/(2*np.pi))
        for k, hc in enumerate(model.controls):
            hc_eigen = v.conj().T @ hc @ v
            deriv[k,t] = 2*np.vdot(after, (frechet_factor*hc_eigen) @ before).real
        adjoint = v @ (phases.conj()*after)
    return probability, psi, deriv


def continuous_evolution(model, signal, nodes, times, atol=1e-10, rtol=1e-10, max_step=None):
    """Independent ODE propagation of the exact continuous actuator response."""
    fn = signal.callback(nodes)
    def coefficient(k):
        def value(t):
            return float(fn(t)[k])
        return value
    h = [qt.Qobj(model.drift)] + [[qt.Qobj(hc), coefficient(k)] for k,hc in enumerate(model.controls)]
    options = {"atol":atol, "rtol":rtol, "nsteps":1000000,
               "max_step":signal.h/8 if max_step is None else max_step,
               "normalize_output":False, "store_states":True}
    result = qt.sesolve(h, qt.Qobj(model.initial), np.asarray(times), options=options)
    return np.array([x.full().ravel() for x in result.states])


class Objective:
    def __init__(self, model, signal, cfg):
        self.model = model
        self.signal = signal
        self.cfg = cfg
        self.midpoints = (np.arange(cfg.intervals)+.5)*cfg.duration/cfg.intervals
        self.transfer = signal.matrix(self.midpoints)
        self.derivative_transfer = signal.matrix(self.midpoints, derivative=True)
        self.nfree = model.ncontrols*(signal.nodes-2)

    def unpack(self, flat):
        nodes = np.zeros((self.model.ncontrols, self.signal.nodes))
        nodes[:,1:-1] = np.asarray(flat).reshape(self.model.ncontrols,-1)
        return nodes

    def evaluate_nodes(self, nodes, gradient=False):
        amplitudes = nodes @ self.transfer.T
        out = propagate_midpoint(self.model, amplitudes, self.cfg.duration, gradient)
        probability, state = out[:2]
        physical = self.model.physical_map @ amplitudes
        rates = self.model.physical_map @ nodes @ self.derivative_transfer.T
        u = self.cfg.control
        # Time-averaged square modulation and slew, summed over PHYSICAL channels.
        penalty = u.fluence_weight*np.mean(np.sum(physical**2,axis=0)) + u.slew_weight*np.mean(np.sum(rates**2,axis=0))
        cost = 1-probability+penalty
        if not gradient:
            return float(cost), probability, state
        grad_nodes = -out[2] @ self.transfer
        grad_nodes += 2*u.fluence_weight/self.cfg.intervals * (self.model.physical_map.T @ physical) @ self.transfer
        grad_nodes += 2*u.slew_weight/self.cfg.intervals * (self.model.physical_map.T @ rates) @ self.derivative_transfer
        return float(cost), grad_nodes[:,1:-1].ravel()

    def __call__(self, flat):
        return self.evaluate_nodes(self.unpack(flat), gradient=True)
