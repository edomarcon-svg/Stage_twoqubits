"""
run_grape_2q.py
===============
GRAPE (Gradient Ascent Pulse Engineering) optimization for nonclassical
state generation in a cavity + 2 qubit system (USC regime).

This script:
  1. Builds the two-qubit system
  2. Defines the target state (density matrix in full Hilbert space)
  3. Optionally loads CRAB results as initial guess
  4. Runs GRAPE optimization (gradient ascent or L-BFGS-B)
  5. Optionally smooths the result via interpolation
  6. Visualizes: control pulses, ⟨n⟩(t), Wigner functions, FFT

Usage:
    python run_grape_2q.py

    (run from the Stage_twoqubits directory with the appropriate
     Python environment that has qutip, numpy, matplotlib installed)
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from qutip import expect, ptrace, fidelity, wigner, ket2dm

# ── Ensure this directory is on the path ──
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from two_qubit_system import (
    build_two_qubit_system,
    grape_target_fock_2q,
    grape_target_squeezed_2q,
    grape_target_cat_2q,
    target_fock_2q,
    compute_control_cost,
    db_to_r,
)
from grape_optimizer import GRAPEOptimizer, GRAPEResult

# ── Matplotlib settings ──
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.size": 14,
})

# ====================================================================
# 1.  Physical parameters
# ====================================================================
dim = 30              # cavity truncation
omega_c = 1.0         # cavity frequency
g1 = 0.3              # coupling qubit 1
g2 = 0.3              # coupling qubit 2
omega_base = 2.0      # base drive amplitude for both qubits

tau_s = np.pi / (2 * g1)
T = 20 * tau_s
Nt = 300              # GRAPE time slots

# ====================================================================
# 2.  Build the system
# ====================================================================
sys2q = build_two_qubit_system(dim=dim, omega_c=omega_c, g1=g1, g2=g2)

print(f"Hilbert space dimension: {sys2q.H0.shape[0]}")
print(f"Number of controls: {len(sys2q.H_controls)}")

# ====================================================================
# 3.  Target state (full density matrix for GRAPE)
# ====================================================================
n_target = 6

# GRAPE needs a density matrix in the full Hilbert space
target_dm = grape_target_fock_2q(dim, n_target)

# Also keep the cavity ket for fidelity evaluation
target_cav_ket = target_fock_2q(dim, n_target, trace_over_qubits=True)

# ---- Alternatives (uncomment to use) ----
# r_dB = 3.0; r = db_to_r(r_dB)
# target_dm = grape_target_squeezed_2q(dim, r, theta=np.pi/4)
# target_cav_ket = target_squeezed_2q(dim, r, theta=np.pi/4, trace_over_qubits=True)

# alpha = 2.0
# target_dm = grape_target_cat_2q(dim, alpha)
# target_cav_ket = target_cat_2q(dim, alpha, trace_over_qubits=True)

# ====================================================================
# 4.  Initial state (density matrix for GRAPE)
# ====================================================================
psi0_dm = sys2q.psi0_dm

# ====================================================================
# 5.  GRAPE optimization
# ====================================================================
optimizer = GRAPEOptimizer(
    H_drift=sys2q.H0,
    H_controls=sys2q.H_controls,    # [H1_ctrl, H2_ctrl]
    T=T,
    num_tslots=Nt,
    omega_bases=[omega_base, omega_base],
    epsilon=1e-1,
    seed=None,
)

# ---- Method A: Gradient Ascent ----
# result = optimizer.optimize_gradient_ascent(
#     psi0=psi0_dm,
#     target_state=target_dm,
#     max_iter=1000,
#     goal=0.99,
# )

# ---- Method B: L-BFGS-B (recommended) ----
print("\n--- Starting GRAPE (L-BFGS-B) optimization ---")
result = optimizer.optimize_minimize(
    psi0=psi0_dm,
    target_state=target_dm,
    max_iter=500,
    amp_bound=(0.5, 3.0),
    # initial_guess=[crab_pulse_q1, crab_pulse_q2],   # uncomment to warm-start
)

print(f"\nGRAPE final fidelity (full DM): {result.final_fidelity:.6f}")
print(f"GRAPE converged: {result.success}")
print(f"GRAPE message: {result.message}")

# ====================================================================
# 6.  Post-processing
# ====================================================================
control_q1 = result.control_pulses[0]
control_q2 = result.control_pulses[1]
tlist = np.linspace(0, T, Nt)

# Forward propagation with optimized pulses
states = optimizer.forward_propagation(result.control_pulses, psi0_dm)

# Cavity fidelity
final_cav = ptrace(states[-1], 0)
F_cav = fidelity(target_cav_ket, final_cav)
print(f"Cavity fidelity: {F_cav:.6f}")

# Mean photon number
n_expect = [expect(sys2q.n_tot, rho) for rho in states]

# Control cost
dt = tlist[1] - tlist[0]
C2 = compute_control_cost([control_q1, control_q2], dt)
print(f"Control cost C²: {C2:.2f}")

# ====================================================================
# 7.  (Optional) Interpolation smoothing
# ====================================================================
SMOOTH = True  # set to True to apply interpolation

if SMOOTH:
    Nt_fine = 2 * Nt
    tlist_fine = np.linspace(0, T, Nt_fine)

    cs_q1 = PchipInterpolator(tlist, control_q1)
    cs_q2 = PchipInterpolator(tlist, control_q2)

    control_q1_smooth = cs_q1(tlist_fine)
    control_q2_smooth = cs_q2(tlist_fine)

    # Rebuild optimizer at finer resolution for verification
    optimizer_fine = GRAPEOptimizer(
        H_drift=sys2q.H0,
        H_controls=sys2q.H_controls,
        T=T,
        num_tslots=Nt_fine,
        omega_bases=[omega_base, omega_base],
        epsilon=1e-1,
    )

    states_smooth = optimizer_fine.forward_propagation(
        [control_q1_smooth, control_q2_smooth], psi0_dm
    )

    final_cav_smooth = ptrace(states_smooth[-1], 0)
    F_smooth = fidelity(target_cav_ket, final_cav_smooth)
    print(f"\nSmoothed cavity fidelity: {F_smooth:.6f}")

    # Use smoothed data for plots
    plot_tlist = tlist_fine
    plot_ctrl_q1 = control_q1_smooth
    plot_ctrl_q2 = control_q2_smooth
    plot_states = states_smooth
    plot_F = F_smooth
    n_expect_plot = [expect(sys2q.n_tot, rho) for rho in states_smooth]
else:
    plot_tlist = tlist
    plot_ctrl_q1 = control_q1
    plot_ctrl_q2 = control_q2
    plot_states = states
    plot_F = F_cav
    n_expect_plot = n_expect

# ====================================================================
# 8.  Plots
# ====================================================================
# ---- Mean photon number ----
plt.figure(figsize=(7, 4))
plt.plot(plot_tlist / tau_s, n_expect_plot[1:], "crimson", lw=2)
plt.xlabel(r"$t / \tau_s$")
plt.ylabel(r"$\langle n \rangle$")
plt.title(f"Mean photon number  (F = {plot_F:.4f})")
plt.grid(True)
plt.tight_layout()
plt.savefig("grape_2q_nmean.pdf", dpi=300)
plt.show()

# ---- Control drives ----
fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
step_kw = dict(where="post") if not SMOOTH else {}
plot_fn = axes[0].step if not SMOOTH else axes[0].plot

plot_fn_0 = axes[0].step if not SMOOTH else axes[0].plot
plot_fn_1 = axes[1].step if not SMOOTH else axes[1].plot

plot_fn_0(plot_tlist / tau_s, plot_ctrl_q1, color="darkgreen", lw=2, **step_kw)
axes[0].set_ylabel(r"$\Omega_{D1}(t) / \omega_c$")
axes[0].set_title("Drive qubit 1")
axes[0].grid(True)

plot_fn_1(plot_tlist / tau_s, plot_ctrl_q2, color="navy", lw=2, **step_kw)
axes[1].set_xlabel(r"$t / \tau_s$")
axes[1].set_ylabel(r"$\Omega_{D2}(t) / \omega_c$")
axes[1].set_title("Drive qubit 2")
axes[1].grid(True)
fig.tight_layout()
plt.savefig("grape_2q_drives.pdf", dpi=300)
plt.show()

# ---- Wigner functions ----
xvec = np.linspace(-5, 5, 200)
final_cav_plot = ptrace(plot_states[-1], 0)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

w_target = wigner(target_cav_ket, xvec, xvec)
axes[0].contourf(xvec, xvec, w_target, 100, cmap="RdBu_r")
axes[0].set_title("Target Wigner")
axes[0].set_xlabel("x")
axes[0].set_ylabel("p")

w_final = wigner(final_cav_plot, xvec, xvec)
im = axes[1].contourf(xvec, xvec, w_final, 100, cmap="RdBu_r")
axes[1].set_title("Optimized Wigner")
axes[1].set_xlabel("x")
fig.colorbar(im, ax=axes[1])
fig.tight_layout()
plt.savefig("grape_2q_wigner.pdf", dpi=300)
plt.show()

# ---- FFT ----
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
dt_plot = plot_tlist[1] - plot_tlist[0]
for ctrl, ax, label in zip(
    [plot_ctrl_q1, plot_ctrl_q2], axes, ["Qubit 1", "Qubit 2"]
):
    ctrl_c = ctrl - np.mean(ctrl)
    fft_v = np.fft.fft(ctrl_c)
    freqs = np.fft.fftfreq(len(ctrl_c), d=dt_plot)
    mask = freqs >= 0
    ax.plot(freqs[mask] * (2 * np.pi), np.abs(fft_v[mask]))
    ax.axvline(2 * omega_c, color="red", ls="--", label=r"$2\omega_c$")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Amplitude")
    ax.set_title(f"FFT — {label}")
    ax.legend()
    ax.grid(True)
fig.tight_layout()
plt.savefig("grape_2q_fft.pdf", dpi=300)
plt.show()

print("\nDone. All figures saved.")
