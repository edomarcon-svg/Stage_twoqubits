"""Rabi models with explicit bare frequencies, total parity and ket propagation."""
from dataclasses import dataclass
import numpy as np
import qutip as qt
from .config import Experiment, Case, Target


def cavity_target(dim: int, target: Target) -> np.ndarray:
    if target.kind == "fock":
        ket = qt.basis(dim, int(target.value))
    elif target.kind == "squeezed":
        r = target.value if target.squeezing_unit == "r" else target.value * np.log(10) / 20
        ket = qt.squeeze(dim, r * np.exp(1j * target.theta)) * qt.basis(dim, 0)
    elif target.kind == "cat":
        # Analytic projection of the four-component cat: only n = 2 mod 4.
        # Log coefficients avoid cancellation for small alpha and overflow for large alpha.
        from scipy.special import gammaln
        ns = np.arange(2, dim, 4)
        logs = ns * np.log(target.value) - .5 * gammaln(ns + 1)
        vec = np.zeros(dim, complex)
        vec[ns] = np.exp(logs - np.max(logs))
        return vec / np.linalg.norm(vec)
    else:
        raise ValueError(f"Unknown target {target.kind}")
    return ket.full().ravel()


@dataclass
class Model:
    dimension: int
    nqubits: int
    drift: np.ndarray
    controls: np.ndarray
    initial: np.ndarray
    target_operator: np.ndarray
    target_cavity: np.ndarray
    indices: np.ndarray
    initial_parity: int
    physical_map: np.ndarray
    bare_frequencies: np.ndarray
    full_drift: qt.Qobj
    full_controls: list

    @property
    def ncontrols(self):
        return len(self.controls)

    def expand(self, state):
        state = np.asarray(state)
        out = np.zeros((self.dimension * 2**self.nqubits,), complex)
        out[self.indices] = state
        return out

    def full_ket(self, state):
        return qt.Qobj(self.expand(state), dims=[[self.dimension] + [2]*self.nqubits, [1]*(self.nqubits+1)])

    def cavity_density(self, state):
        c = self.expand(state).reshape(self.dimension, 2**self.nqubits)
        return c @ c.conj().T


def build_model(cfg: Experiment, case: Case, dimension=None) -> Model:
    dim = cfg.dimension if dimension is None else dimension
    nq = len(case.couplings)
    ident = [qt.qeye(dim)] + [qt.qeye(2) for _ in range(nq)]
    a = qt.tensor(qt.destroy(dim), *ident[1:])
    def spin(op, j):
        ops = ident.copy()
        ops[j+1] = op
        return qt.tensor(*ops)
    zs = [spin(qt.sigmaz(), j) for j in range(nq)]
    xs = [spin(qt.sigmax(), j) for j in range(nq)]
    h = cfg.omega_c * a.dag() * a  # Irrelevant zero-point energy omitted.
    for j, g in enumerate(case.couplings):
        h += -.5 * case.qubit_frequencies[j] * zs[j] + g * (a + a.dag()) * xs[j]
    if case.direct_exchange:
        ys = [spin(qt.sigmay(), j) for j in range(nq)]
        h += case.direct_exchange * (xs[0]*xs[1] + ys[0]*ys[1])
    physical_map = np.eye(nq) if case.control == "independent" else np.ones((nq, 1))
    controls = [sum((-.5 * physical_map[j,k] * zs[j] for j in range(nq))) for k in range(physical_map.shape[1])]
    full_dim = dim * 2**nq
    cavity_numbers = np.repeat(np.arange(dim), 2**nq)
    bit_counts = np.tile([int(i).bit_count() for i in range(2**nq)], dim)
    parity = (-1.)**(cavity_numbers + bit_counts)
    if cfg.initial_state == "bare":
        psi = np.zeros(full_dim, complex)
        psi[0] = 1
        sign = 1
    else:
        # Diagonalize each parity block separately to avoid mixed-parity eigenvectors
        # at degeneracies. The selected state is the actual minimum-energy block.
        candidates = []
        for sign in [1, -1]:
            ids = np.flatnonzero(parity == sign)
            e, v = np.linalg.eigh(h.full()[np.ix_(ids, ids)])
            candidates.append((e[0], sign, ids, v[:,0]))
        _, sign, ids, vec = min(candidates, key=lambda x: x[0])
        psi = np.zeros(full_dim, complex)
        psi[ids] = vec
    idx = np.flatnonzero(parity == sign) if cfg.parity_reduction else np.arange(full_dim)
    target = cavity_target(dim, cfg.target)
    qtarget = np.eye(2**nq)
    if cfg.target.reset_qubits:
        qtarget *= 0
        qtarget[0,0] = 1
    observable = np.kron(np.outer(target, target.conj()), qtarget)
    if np.linalg.norm(observable[np.ix_(np.flatnonzero(parity == sign), np.flatnonzero(parity == sign))]) < 1e-12:
        raise ValueError("Target is forbidden in the initial total-parity sector with this qubit-reset constraint")
    return Model(dim, nq, h.full()[np.ix_(idx,idx)],
                 np.array([c.full()[np.ix_(idx,idx)] for c in controls]), psi[idx],
                 observable[np.ix_(idx,idx)], target, idx, int(sign), physical_map,
                 np.asarray(case.qubit_frequencies), h, controls)
