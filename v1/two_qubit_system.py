"""
two_qubit_system.py
====================
Kernel module for a single-mode cavity coupled to TWO qubits
in the ultrastrong coupling (USC) regime.

Hilbert space:  H_cav ⊗ H_q1 ⊗ H_q2   (dim × 2 × 2)

Provides:
  - Factory function to build all operators and Hamiltonians
  - Target-state constructors (Fock, squeezed, cat, Bell)
  - Cost functions compatible with both CRAB and GRAPE optimizers
"""

from dataclasses import dataclass, field
from typing import List, Optional, Callable
import numpy as np
from qutip import (
    Qobj, basis, destroy, qeye, tensor, sigmaz, sigmax, sigmay,
    squeeze, coherent, ket2dm, fidelity, ptrace, wigner,
)


# ====================================================================
# System dataclass — holds every operator the scripts will ever need
# ====================================================================
@dataclass
class TwoQubitSystem:
    """
    Container for all operators and Hamiltonians of the
    cavity + 2-qubit system.
    """
    # --- physical parameters ---
    dim: int                  # cavity Fock-space truncation
    omega_c: float            # cavity frequency
    g1: float                 # coupling strength qubit 1
    g2: float                 # coupling strength qubit 2

    # --- bare operators (already tensored to full Hilbert space) ---
    a_tot: Qobj = field(repr=False, default=None)       # cavity annihilation
    n_tot: Qobj = field(repr=False, default=None)       # photon number
    identity: Qobj = field(repr=False, default=None)    # full identity

    sz1: Qobj = field(repr=False, default=None)         # σ_z qubit 1
    sz2: Qobj = field(repr=False, default=None)         # σ_z qubit 2
    sx1: Qobj = field(repr=False, default=None)         # σ_x qubit 1
    sx2: Qobj = field(repr=False, default=None)         # σ_x qubit 2

    x_couple1: Qobj = field(repr=False, default=None)   # (a + a†) ⊗ σ_x1
    x_couple2: Qobj = field(repr=False, default=None)   # (a + a†) ⊗ σ_x2

    # --- Hamiltonians ---
    H0: Qobj = field(repr=False, default=None)          # drift
    H_controls: list = field(repr=False, default=None)  # [H_ctrl1, H_ctrl2]

    # --- initial state ---
    psi0_ket: Qobj = field(repr=False, default=None)    # |0,g,g⟩  (ket)
    psi0_dm: Qobj = field(repr=False, default=None)     # |0,g,g⟩⟨0,g,g|


# ====================================================================
# Factory — build the full system
# ====================================================================
def build_two_qubit_system(
    dim: int = 30,
    omega_c: float = 1.0,
    g1: float = 0.3,
    g2: float = 0.3,
) -> TwoQubitSystem:
    """
    Build every operator and Hamiltonian for a cavity + 2-qubit system.

    Parameters
    ----------
    dim : int
        Truncation dimension of the cavity Fock space.
    omega_c : float
        Cavity angular frequency (sets the energy scale; typically = 1).
    g1 : float
        Light–matter coupling strength for qubit 1.
    g2 : float
        Light–matter coupling strength for qubit 2.

    Returns
    -------
    TwoQubitSystem
        Fully populated container with operators, Hamiltonians,
        and initial state.
    """
    # ---- identity operators for each subsystem ----
    I_c = qeye(dim)       # cavity identity
    I_q = qeye(2)         # single-qubit identity

    # ---- bare cavity operators ----
    a = destroy(dim)
    n_op = a.dag() * a
    x_op = a + a.dag()    # position quadrature (a + a†)

    # ---- full-space operators  (cavity ⊗ qubit1 ⊗ qubit2) ----
    a_tot = tensor(a, I_q, I_q)
    n_tot = tensor(n_op, I_q, I_q)
    identity = tensor(I_c, I_q, I_q)

    # Pauli matrices in the full Hilbert space
    sz1 = tensor(I_c, sigmaz(), I_q)
    sz2 = tensor(I_c, I_q, sigmaz())
    sx1 = tensor(I_c, sigmax(), I_q)
    sx2 = tensor(I_c, I_q, sigmax())

    # Cavity–qubit coupling operators: (a + a†) σ_x_k
    x_couple1 = tensor(x_op, sigmax(), I_q)
    x_couple2 = tensor(x_op, I_q, sigmax())

    # ---- Drift Hamiltonian H0 ----
    # H0 = ω_c (a†a + 1/2) + g1 (a+a†)σ_x1 + g2 (a+a†)σ_x2
    # Note: the bare qubit energies (ω_q/2)σ_z are absorbed into
    # the control drives Ω_D(t) as in the original 1-qubit code,
    # where H1 = -0.5 σ_z acts as the control Hamiltonian.
    H0 = omega_c * (n_tot + 0.5 * identity) + g1 * x_couple1 + g2 * x_couple2

    # ---- Control Hamiltonians ----
    H1 = -0.5 * sz1   # drive on qubit 1
    H2 = -0.5 * sz2   # drive on qubit 2
    H_controls = [H1, H2]

    # ---- Initial state |0⟩|g⟩|g⟩ ----
    psi0_ket = tensor(basis(dim, 0), basis(2, 0), basis(2, 0))
    psi0_dm = ket2dm(psi0_ket)

    return TwoQubitSystem(
        dim=dim, omega_c=omega_c, g1=g1, g2=g2,
        a_tot=a_tot, n_tot=n_tot, identity=identity,
        sz1=sz1, sz2=sz2, sx1=sx1, sx2=sx2,
        x_couple1=x_couple1, x_couple2=x_couple2,
        H0=H0, H_controls=H_controls,
        psi0_ket=psi0_ket, psi0_dm=psi0_dm,
    )


# ====================================================================
# Target-state constructors
# ====================================================================

def target_fock_2q(dim: int, n: int, trace_over_qubits: bool = True) -> Qobj:
    """
    Fock state |n⟩ of the cavity with both qubits in the ground state.

    Parameters
    ----------
    dim : int
        Cavity truncation.
    n : int
        Target photon number.
    trace_over_qubits : bool
        If True, return the *reduced* cavity density matrix/ket ρ_cav = |n⟩
        (useful for CRAB cost).
        If False, return the target observable |n⟩⟨n| ⊗ I_2 ⊗ I_2
        (useful for GRAPE cost, expectation value Tr[O ρ] ∈ [0, 1]).
    """
    if trace_over_qubits:
        # Pure cavity state only
        return basis(dim, n)   # ket
    else:
        # Target observable for the cavity subsystem (trace-preserving: Tr[O ρ] = ⟨n|ρ_cav|n⟩)
        return tensor(ket2dm(basis(dim, n)), qeye(2), qeye(2))


def target_squeezed_2q(dim: int, r: float, theta: float = 0.0,
                       trace_over_qubits: bool = True) -> Qobj:
    """
    Squeezed vacuum state of the cavity.

    Parameters
    ----------
    dim : int
        Cavity truncation.
    r : float
        Squeezing parameter (linear, not dB).
    theta : float
        Squeezing angle.
    trace_over_qubits : bool
        If True, return ket of cavity only.
        If False, return target observable for full system.
    """
    squeezed_ket = squeeze(dim, r * np.exp(1j * theta)) * basis(dim, 0)
    if trace_over_qubits:
        return squeezed_ket
    else:
        rho = ket2dm(squeezed_ket)
        return tensor(rho, qeye(2), qeye(2))


def target_cat_2q(dim: int, alpha: float = 2.0,
                  trace_over_qubits: bool = True) -> Qobj:
    """
    Superposition of Schrödinger-cat states:
        |ψ⟩ ∝ C+_α − C+_{iα}
    as defined in the paper, Eq. (B4).

    Parameters
    ----------
    dim : int
        Cavity truncation.
    alpha : float
        Coherent-state amplitude.
    trace_over_qubits : bool
        If True, return ket of cavity only.
        If False, return target observable for full system.
    """
    cat_a = coherent(dim, alpha)
    cat_ma = coherent(dim, -alpha)
    cat_ia = coherent(dim, 1j * alpha)
    cat_mia = coherent(dim, -1j * alpha)

    C_plus = (cat_a + cat_ma).unit()
    Ci_plus = (cat_ia + cat_mia).unit()

    cat_state = (C_plus - Ci_plus).unit()

    if trace_over_qubits:
        return cat_state
    else:
        rho = ket2dm(cat_state)
        return tensor(rho, qeye(2), qeye(2))


def target_bell_2q(dim: int, n_cav: int = 0,
                   bell_type: str = "phi_plus") -> Qobj:
    """
    Bell state of the two qubits with the cavity in Fock state |n_cav⟩.

    Parameters
    ----------
    dim : int
        Cavity truncation.
    n_cav : int
        Number of photons in the cavity.
    bell_type : str
        One of: 'phi_plus'  = (|gg⟩ + |ee⟩) / √2
                'phi_minus' = (|gg⟩ - |ee⟩) / √2
                'psi_plus'  = (|ge⟩ + |eg⟩) / √2
                'psi_minus' = (|ge⟩ - |eg⟩) / √2

    Returns
    -------
    Qobj
        Full-system density matrix.
    """
    g = basis(2, 0)
    e = basis(2, 1)
    cav = basis(dim, n_cav)

    if bell_type == "phi_plus":
        qubit_state = (tensor(g, g) + tensor(e, e)).unit()
    elif bell_type == "phi_minus":
        qubit_state = (tensor(g, g) - tensor(e, e)).unit()
    elif bell_type == "psi_plus":
        qubit_state = (tensor(g, e) + tensor(e, g)).unit()
    elif bell_type == "psi_minus":
        qubit_state = (tensor(g, e) - tensor(e, g)).unit()
    else:
        raise ValueError(f"Unknown bell_type: {bell_type}")

    full_state = tensor(cav, qubit_state)
    return ket2dm(full_state)


# ====================================================================
# Cost functions for CRAB optimizer
# ====================================================================
# CRAB cost functions receive (final_state: Qobj, pulses: list[np.ndarray])
# and must return a scalar.

def make_crab_cost_cavity(target_cav_ket: Qobj):
    """
    Build a CRAB-compatible cost function that measures the infidelity
    of the *cavity* reduced state w.r.t. a target cavity ket.

    The final_state from sesolve is a ket in the full Hilbert space;
    we trace over both qubits (subsystems 1 and 2) to get the
    cavity density matrix.
    """
    def cost(final_state, pulses):
        # ptrace over qubits (indices 1,2) → cavity density matrix
        rho_cav = ptrace(final_state, 0)
        return 1.0 - fidelity(target_cav_ket, rho_cav)
    return cost


def make_crab_cost_full(target_dm: Qobj):
    """
    Build a CRAB-compatible cost function that measures infidelity
    of the *full* system state (cavity + 2 qubits) w.r.t. a target
    density matrix.
    """
    def cost(final_state, pulses):
        if final_state.isket:
            rho = ket2dm(final_state)
        else:
            rho = final_state
        return 1.0 - fidelity(target_dm, rho)
    return cost


def make_crab_cost_qubits(target_qubit_dm: Qobj):
    """
    Build a CRAB-compatible cost function for the qubit subsystem only.
    Traces over the cavity (subsystem 0) to get the 2-qubit density matrix.
    """
    def cost(final_state, pulses):
        rho_qubits = ptrace(final_state, [1, 2])
        return 1.0 - fidelity(target_qubit_dm, rho_qubits)
    return cost


# ====================================================================
# GRAPE target-state builders (density matrices in full Hilbert space)
# ====================================================================

def grape_target_fock_2q(dim: int, n: int, ground_qubits: bool = False) -> Qobj:
    """
    GRAPE target operator for cavity Fock state |n⟩.

    Parameters
    ----------
    dim : int
        Cavity truncation.
    n : int
        Target photon number.
    ground_qubits : bool
        If False (default, trace-insensitive), the target observable is:
            O_target = |n⟩⟨n| ⊗ I_2 ⊗ I_2
        Its expectation value Tr[O ρ] equals the cavity fidelity ⟨n|ρ_cav|n⟩ ∈ [0, 1].
        If True, both qubits are required to be in |g, g⟩ at t=T:
            ρ_target = |n,g,g⟩⟨n,g,g|
        whose overlap with ρ(T) is ⟨n,g,g|ρ|n,g,g⟩ ∈ [0, 1].
    """
    if ground_qubits:
        target_ket = tensor(basis(dim, n), basis(2, 0), basis(2, 0))
        return ket2dm(target_ket)
    else:
        rho_cav = ket2dm(basis(dim, n))
        return tensor(rho_cav, qeye(2), qeye(2))


def grape_target_squeezed_2q(dim: int, r: float, theta: float = 0.0,
                             ground_qubits: bool = False) -> Qobj:
    """
    GRAPE target operator for cavity squeezed vacuum.
    """
    squeezed_ket = squeeze(dim, r * np.exp(1j * theta)) * basis(dim, 0)
    if ground_qubits:
        target_ket = tensor(squeezed_ket, basis(2, 0), basis(2, 0))
        return ket2dm(target_ket)
    else:
        rho_cav = ket2dm(squeezed_ket)
        return tensor(rho_cav, qeye(2), qeye(2))


def grape_target_cat_2q(dim: int, alpha: float = 2.0,
                        ground_qubits: bool = False) -> Qobj:
    """
    GRAPE target operator for cavity cat-state superposition.
    """
    cat_ket = target_cat_2q(dim, alpha, trace_over_qubits=True)
    if ground_qubits:
        target_ket = tensor(cat_ket, basis(2, 0), basis(2, 0))
        return ket2dm(target_ket)
    else:
        rho_cav = ket2dm(cat_ket)
        return tensor(rho_cav, qeye(2), qeye(2))


# ====================================================================
# Utility functions
# ====================================================================

def compute_control_cost(pulses: List[np.ndarray], dt: float) -> float:
    """
    Compute the control cost C² = ∫₀ᵀ ||H_D(s)||² ds,
    approximated as Σ_k Σ_t pulse_k(t)² · dt.
    
    This is the Frobenius-norm-based cost from Eq. (4) of the paper.
    """
    cost = 0.0
    for pulse in pulses:
        cost += np.sum(pulse ** 2) * dt
    return cost


def db_to_r(rdB: float) -> float:
    """Convert squeezing in dB to the linear squeezing parameter r."""
    return rdB / (20.0 * np.log10(np.e))
