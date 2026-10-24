"""
one_qubit_system.py
===================
Kernel module for a single-mode cavity coupled to ONE qubit
in the ultrastrong coupling (USC) regime, as formulated in the paper:
"Deterministic generation of nonclassical cavity states via dynamical Casimir effect".

Hilbert space:  H_cav ⊗ H_q   (dim × 2)

Hamiltonian:
    H_S(t) = H_R + H_D(t)
    H_R    = ω_c a†a + (ω_q/2) σ_z + g (a + a†) σ_x
    H_D(t) = (Ω_D(t)/2) σ_z

In QuTiP representation (with bare qubit energy absorbed into the control drive):
    H0 = ω_c (n_tot + 0.5 * identity) + g * (a + a†) ⊗ σ_x
    H1 = -0.5 * σ_z  (control Hamiltonian for Ω_D(t))

Provides:
  - Factory function `build_one_qubit_system`
  - Target-state constructors (Fock, squeezed, cat)
  - Cost functions compatible with both CRAB and GRAPE optimizers
  - Utility functions (cost calculation, dB to r conversion)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Callable
import numpy as np
from qutip import (
    Qobj, basis, destroy, qeye, tensor, sigmaz, sigmax, sigmay,
    squeeze, coherent, ket2dm, fidelity, ptrace, wigner,
)


# ====================================================================
# System dataclass — holds every operator the scripts and notebooks need
# ====================================================================
@dataclass
class OneQubitSystem:
    """
    Container for all operators and Hamiltonians of the
    cavity + 1-qubit system.
    """
    # --- physical parameters ---
    dim: int                  # cavity Fock-space truncation
    omega_c: float            # cavity frequency
    g: float                  # light-matter coupling strength

    # --- bare operators (tensored to full Hilbert space H_cav ⊗ H_q) ---
    a_tot: Qobj = field(repr=False, default=None)       # cavity annihilation: a ⊗ I_q
    n_tot: Qobj = field(repr=False, default=None)       # photon number: a†a ⊗ I_q
    identity: Qobj = field(repr=False, default=None)    # full identity: I_c ⊗ I_q

    sz: Qobj = field(repr=False, default=None)          # σ_z qubit: I_c ⊗ σ_z
    sx: Qobj = field(repr=False, default=None)          # σ_x qubit: I_c ⊗ σ_x
    sy: Qobj = field(repr=False, default=None)          # σ_y qubit: I_c ⊗ σ_y

    x_couple: Qobj = field(repr=False, default=None)    # (a + a†) ⊗ σ_x

    # --- Hamiltonians ---
    H0: Qobj = field(repr=False, default=None)          # drift Hamiltonian
    H_controls: list = field(repr=False, default=None)  # [H1_ctrl]

    # --- initial state ---
    psi0_ket: Qobj = field(repr=False, default=None)    # |0,g⟩ (ket)
    psi0_dm: Qobj = field(repr=False, default=None)     # |0,g⟩⟨0,g| (density matrix)


# ====================================================================
# Factory — build the full 1-qubit system
# ====================================================================
def build_one_qubit_system(
    dim: int = 30,
    omega_c: float = 1.0,
    g: float = 0.3,
) -> OneQubitSystem:
    """
    Build every operator and Hamiltonian for a cavity + 1-qubit system.

    Parameters
    ----------
    dim : int
        Truncation dimension of the cavity Fock space.
    omega_c : float
        Cavity angular frequency (sets the energy scale; typically = 1.0).
    g : float
        Light–matter coupling strength (regime USC: g/ω_c ≳ 0.1, paper uses g = 0.3).

    Returns
    -------
    OneQubitSystem
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

    # ---- full-space operators (cavity ⊗ qubit) ----
    a_tot = tensor(a, I_q)
    n_tot = tensor(n_op, I_q)
    identity = tensor(I_c, I_q)

    # Pauli matrices in the full Hilbert space
    sz = tensor(I_c, sigmaz())
    sx = tensor(I_c, sigmax())
    sy = tensor(I_c, sigmay())

    # Cavity–qubit coupling operator: (a + a†) ⊗ σ_x
    x_couple = tensor(x_op, sigmax())

    # ---- Drift Hamiltonian H0 ----
    # H0 = ω_c (a†a + 1/2) + g (a + a†) σ_x
    # Note: the bare qubit energy (ω_q/2)σ_z is absorbed into
    # the control drive Ω_D(t) as in the paper and optimal control formulation,
    # where H1 = -0.5 * sz acts as the control Hamiltonian.
    H0 = omega_c * (n_tot + 0.5 * identity) + g * x_couple

    # ---- Control Hamiltonian ----
    # H_D(t) = (Ω_D(t)/2) * σ_z^{paper} = -0.5 * Ω_D(t) * σ_z^{qutip}
    H1 = -0.5 * sz
    H_controls = [H1]

    # ---- Initial state |0⟩|g⟩ ----
    psi0_ket = tensor(basis(dim, 0), basis(2, 0))
    psi0_dm = ket2dm(psi0_ket)

    return OneQubitSystem(
        dim=dim, omega_c=omega_c, g=g,
        a_tot=a_tot, n_tot=n_tot, identity=identity,
        sz=sz, sx=sx, sy=sy,
        x_couple=x_couple,
        H0=H0, H_controls=H_controls,
        psi0_ket=psi0_ket, psi0_dm=psi0_dm,
    )


# ====================================================================
# Target-state constructors
# ====================================================================

def target_fock_1q(dim: int, n: int, trace_over_qubit: bool = True) -> Qobj:
    """
    Fock state |n⟩ of the cavity.

    Parameters
    ----------
    dim : int
        Cavity truncation.
    n : int
        Target photon number.
    trace_over_qubit : bool
        If True, return the *reduced* cavity ket |n⟩ (dim-dimensional).
        If False, return the target observable |n⟩⟨n| ⊗ I_2 for the full system.
    """
    if trace_over_qubit:
        return basis(dim, n)
    else:
        return tensor(ket2dm(basis(dim, n)), qeye(2))


def target_squeezed_1q(dim: int, r: float, theta: float = 0.0,
                       trace_over_qubit: bool = True) -> Qobj:
    """
    Squeezed vacuum state of the cavity S(r, θ)|0⟩.

    Parameters
    ----------
    dim : int
        Cavity truncation.
    r : float
        Squeezing parameter (linear scale).
    theta : float
        Squeezing angle.
    trace_over_qubit : bool
        If True, return cavity ket.
        If False, return full-space density matrix observable.
    """
    squeezed_ket = squeeze(dim, r * np.exp(1j * theta)) * basis(dim, 0)
    if trace_over_qubit:
        return squeezed_ket
    else:
        rho = ket2dm(squeezed_ket)
        return tensor(rho, qeye(2))


def target_cat_1q(dim: int, alpha: float = 2.0,
                  trace_over_qubit: bool = True) -> Qobj:
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
    trace_over_qubit : bool
        If True, return cavity ket.
        If False, return full-space density matrix observable.
    """
    cat_a = coherent(dim, alpha)
    cat_ma = coherent(dim, -alpha)
    cat_ia = coherent(dim, 1j * alpha)
    cat_mia = coherent(dim, -1j * alpha)

    C_plus = (cat_a + cat_ma).unit()
    Ci_plus = (cat_ia + cat_mia).unit()

    cat_state = (C_plus - Ci_plus).unit()

    if trace_over_qubit:
        return cat_state
    else:
        rho = ket2dm(cat_state)
        return tensor(rho, qeye(2))


# ====================================================================
# Cost functions for CRAB optimizer
# ====================================================================

def make_crab_cost_cavity(target_cav_ket: Qobj):
    """
    Build a CRAB-compatible cost function that measures the infidelity
    of the *cavity* reduced state w.r.t. a target cavity ket:
        C = 1 - F(target, Tr_q[|ψ_final⟩⟨ψ_final|])
    """
    def cost(final_state, pulses):
        # ptrace over qubit (index 1) → cavity density matrix
        rho_cav = ptrace(final_state, 0)
        return 1.0 - fidelity(target_cav_ket, rho_cav)
    return cost


def make_crab_cost_full(target_dm: Qobj):
    """
    Build a CRAB-compatible cost function for the *full* system state.
    """
    def cost(final_state, pulses):
        if final_state.isket:
            rho = ket2dm(final_state)
        else:
            rho = final_state
        return 1.0 - fidelity(target_dm, rho)
    return cost


# ====================================================================
# GRAPE target-state builders (density matrices in full Hilbert space)
# ====================================================================

def grape_target_fock_1q(dim: int, n: int, ground_qubit: bool = False) -> Qobj:
    """
    GRAPE target operator for cavity Fock state |n⟩.

    Parameters
    ----------
    dim : int
        Cavity truncation.
    n : int
        Target photon number.
    ground_qubit : bool
        If False (default, trace-preserving observable):
            O_target = |n⟩⟨n| ⊗ I_2
            Tr[O ρ] = ⟨n|ρ_cav|n⟩ ∈ [0, 1].
        If True, the qubit must also be in |g⟩ at t=T:
            ρ_target = |n,g⟩⟨n,g|
    """
    if ground_qubit:
        target_ket = tensor(basis(dim, n), basis(2, 0))
        return ket2dm(target_ket)
    else:
        rho_cav = ket2dm(basis(dim, n))
        return tensor(rho_cav, qeye(2))


def grape_target_squeezed_1q(dim: int, r: float, theta: float = 0.0,
                             ground_qubit: bool = False) -> Qobj:
    """
    GRAPE target operator for cavity squeezed vacuum.
    """
    squeezed_ket = squeeze(dim, r * np.exp(1j * theta)) * basis(dim, 0)
    if ground_qubit:
        target_ket = tensor(squeezed_ket, basis(2, 0))
        return ket2dm(target_ket)
    else:
        rho_cav = ket2dm(squeezed_ket)
        return tensor(rho_cav, qeye(2))


def grape_target_cat_1q(dim: int, alpha: float = 2.0,
                        ground_qubit: bool = False) -> Qobj:
    """
    GRAPE target operator for cavity cat-state superposition.
    """
    cat_ket = target_cat_1q(dim, alpha, trace_over_qubit=True)
    if ground_qubit:
        target_ket = tensor(cat_ket, basis(2, 0))
        return ket2dm(target_ket)
    else:
        rho_cav = ket2dm(cat_ket)
        return tensor(rho_cav, qeye(2))


# ====================================================================
# Utility functions
# ====================================================================

def compute_control_cost(pulses: List[np.ndarray], dt: float) -> float:
    """
    Compute the control energy cost C² = ∫₀ᵀ ||H_D(s)||² ds,
    approximated as Σ_k Σ_t pulse_k(t)² · dt.
    
    This matches Eq. (4) of the paper.
    """
    cost = 0.0
    for pulse in pulses:
        cost += np.sum(pulse ** 2) * dt
    return cost


def db_to_r(rdB: float) -> float:
    """Convert squeezing in dB to the linear squeezing parameter r."""
    return rdB / (20.0 * np.log10(np.e))
