"""
run_crab_2q.py
==============
CRAB (Chopped Random Basis) optimization for nonclassical state generation
in a cavity + 2 qubit system (ultrastrong coupling regime).

This script:
  1. Builds the two-qubit system (operators, Hamiltonians)
  2. Defines the target state and cost function
  3. Runs the CRAB optimizer with two independent control drives
  4. Visualizes: control pulses, ⟨n⟩(t), Wigner functions, FFT spectrum

Usage:
    python run_crab_2q.py
    
    (run from the Stage_twoqubits directory with the appropriate
     Python environment that has qutip, numpy, matplotlib installed)
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from qutip import sesolve, expect, ptrace, fidelity, wigner

# ── Ensure this directory is on the path ──
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from two_qubit_system import (
    build_two_qubit_system,
    target_fock_2q,
    target_squeezed_2q,
    target_cat_2q,
    make_crab_cost_cavity,
    compute_control_cost,
    db_to_r,
)
from crab_optimizer import CRABOptimizer

# ── Matplotlib settings ──
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.size": 14,
})

# ====================================================================
# 1.  Physical parameters
# ====================================================================
dim = 30             # cavity Fock-space truncation
omega_c = 1.0        # cavity frequency (energy unit)
g1 = 0.3             # coupling qubit 1  (USC regime: g/ω_c = 0.3)
g2 = 0.3             # coupling qubit 2

tau_s = np.pi / (2 * g1)       # characteristic timescale (half vacuum Rabi)
T = 20 * tau_s                 # total evolution time
Nt = 400                       # number of time slots
tlist = np.linspace(0, T, Nt)

# CRAB specific
num_freqs = 20                 # Fourier components per control
omega_bases = [2.0, 2.0]       # base drive amplitude for each qubit

# ====================================================================
# 2.  Build the system
# ====================================================================
sys2q = build_two_qubit_system(dim=dim, omega_c=omega_c, g1=g1, g2=g2)

print(f"Hilbert space dimension: {sys2q.H0.shape[0]}")
print(f"Number of controls: {len(sys2q.H_controls)}")

# ====================================================================
# 3.  Define target state
# ====================================================================
# ---- Target: Fock state |n⟩ of the cavity ----
n_target = 6
target_state = target_fock_2q(dim, n_target, trace_over_qubits=True)

# ---- Alternative targets (uncomment to use) ----
# r_dB = 3.0
# r = db_to_r(r_dB)
# target_state = target_squeezed_2q(dim, r, theta=np.pi/4, trace_over_qubits=True)

# alpha = 2.0
# target_state = target_cat_2q(dim, alpha, trace_over_qubits=True)

# ====================================================================
# 4.  Build cost function
# ====================================================================
cost_fn = make_crab_cost_cavity(target_state)

# ====================================================================
# 5.  Create optimizer and run
# ====================================================================
optimizer = CRABOptimizer(
    H_drift=sys2q.H0,
    H_controls=sys2q.H_controls,   # [H1_ctrl, H2_ctrl]
    T=T,
    num_tslots=Nt,
    num_freqs=num_freqs,
    omega_bases=omega_bases,
    freq_range=(0, 3 * omega_c),
    basis_type="uniform",
    seed=None,
)

print("\n--- Starting CRAB optimization ---")
result = optimizer.optimize(
    psi0=sys2q.psi0_ket,
    cost_function=cost_fn,
    max_iter=None,          # Nelder-Mead default
    method="Nelder-Mead",
)

# ====================================================================
# 6.  Post-processing
# ====================================================================
# Extract optimized pulses
control_q1 = result.control_pulses[0]  # drive on qubit 1
control_q2 = result.control_pulses[1]  # drive on qubit 2

# Re-run evolution with optimal controls
H_total = [sys2q.H0,
           [sys2q.H_controls[0], control_q1],
           [sys2q.H_controls[1], control_q2]]

result_evol = sesolve(H_total, sys2q.psi0_ket, tlist)
states = result_evol.states

# Final fidelity
final_cav = ptrace(states[-1], 0)
F_final = fidelity(target_state, final_cav)
print(f"\nFinal fidelity (cavity): {F_final:.6f}")

# Mean photon number
n_expect = [expect(sys2q.n_tot, psi) for psi in states]

# Control cost
dt = tlist[1] - tlist[0]
C2 = compute_control_cost([control_q1, control_q2], dt)
print(f"Control cost C²: {C2:.2f}")

# ====================================================================
# 7.  Plots
# ====================================================================
# ---- Mean photon number ⟨n⟩(t) ----
plt.figure(figsize=(7, 4))
plt.plot(tlist / tau_s, n_expect, "crimson", lw=2)
plt.xlabel(r"$t / \tau_s$")
plt.ylabel(r"$\langle n \rangle$")
plt.title(f"Mean photon number  (F = {F_final:.4f})")
plt.grid(True)
plt.tight_layout()
plt.savefig("crab_2q_nmean.pdf", dpi=300)
plt.show()

# ---- Control drives ----
fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
axes[0].plot(tlist / tau_s, control_q1, "darkgreen", lw=2)
axes[0].set_ylabel(r"$\Omega_{D1}(t) / \omega_c$")
axes[0].set_title("Drive qubit 1")
axes[0].grid(True)

axes[1].plot(tlist / tau_s, control_q2, "navy", lw=2)
axes[1].set_xlabel(r"$t / \tau_s$")
axes[1].set_ylabel(r"$\Omega_{D2}(t) / \omega_c$")
axes[1].set_title("Drive qubit 2")
axes[1].grid(True)
fig.tight_layout()
plt.savefig("crab_2q_drives.pdf", dpi=300)
plt.show()

# ---- Wigner functions ----
xvec = np.linspace(-5, 5, 200)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Target
if target_state.isket:
    w_target = wigner(target_state, xvec, xvec)
else:
    w_target = wigner(target_state, xvec, xvec)
axes[0].contourf(xvec, xvec, w_target, 100, cmap="RdBu_r")
axes[0].set_title("Target Wigner")
axes[0].set_xlabel("x")
axes[0].set_ylabel("p")

# Optimized
w_final = wigner(final_cav, xvec, xvec)
im = axes[1].contourf(xvec, xvec, w_final, 100, cmap="RdBu_r")
axes[1].set_title("Optimized Wigner")
axes[1].set_xlabel("x")
fig.colorbar(im, ax=axes[1])
fig.tight_layout()
plt.savefig("crab_2q_wigner.pdf", dpi=300)
plt.show()

# ---- FFT of the control drives ----
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for idx, (ctrl, ax, label) in enumerate(zip(
    [control_q1, control_q2], axes, ["Qubit 1", "Qubit 2"]
)):
    ctrl_centered = ctrl - np.mean(ctrl)
    fft_vals = np.fft.fft(ctrl_centered)
    freqs = np.fft.fftfreq(len(ctrl_centered), d=dt)
    mask = freqs >= 0
    ax.plot(freqs[mask] * (2 * np.pi), np.abs(fft_vals[mask]))
    ax.axvline(2 * omega_c, color="red", ls="--", label=r"$2\omega_c$")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Amplitude")
    ax.set_title(f"FFT — {label}")
    ax.legend()
    ax.grid(True)
fig.tight_layout()
plt.savefig("crab_2q_fft.pdf", dpi=300)
plt.show()

print("\nDone. All figures saved.")
