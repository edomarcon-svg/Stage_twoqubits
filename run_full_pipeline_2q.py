"""
run_full_pipeline_2q.py
=======================
Full hybrid optimal-control pipeline for the cavity + 2 qubit system:

    CRAB (multi-seed) → best-pick → GRAPE refinement → Interpolation

Reproduces the procedure described in the paper for the one-qubit case,
now extended to two independently controlled qubits.

Usage:
    python run_full_pipeline_2q.py
"""

import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from qutip import sesolve, expect, ptrace, fidelity, wigner, ket2dm

# ── Ensure this directory is on the path ──
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from two_qubit_system import (
    build_two_qubit_system,
    target_fock_2q,
    grape_target_fock_2q,
    make_crab_cost_cavity,
    compute_control_cost,
)
from crab_optimizer import CRABOptimizer, CRABResult
from grape_optimizer import GRAPEOptimizer, GRAPEResult

plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 14,
})

# ====================================================================
# Configuration
# ====================================================================
# --- Physics ---
dim = 30
omega_c = 1.0
g1 = 0.3
g2 = 0.3
tau_s = np.pi / (2 * g1)
T = 20 * tau_s
omega_bases = [2.0, 2.0]

# --- CRAB stage ---
CRAB_NUM_SEEDS = 10       # number of independent CRAB runs
CRAB_NT = 400             # CRAB time slots
CRAB_NUM_FREQS = 20       # Fourier components per control
CRAB_MAX_ITER = None       # Nelder-Mead default (None = auto)
CRAB_METHOD = "Nelder-Mead"

# --- GRAPE stage ---
GRAPE_NT = 300             # GRAPE time slots (can differ from CRAB)
GRAPE_MAX_ITER = 500
GRAPE_AMP_BOUND = (0.5, 3.0)

# --- Interpolation stage ---
INTERP_NT = 600            # fine time grid for final smoothing

# --- Target ---
n_target = 6

# --- Output ---
output_dir = f"results_2q_pipeline_n{n_target}"
os.makedirs(output_dir, exist_ok=True)

# ====================================================================
# Build system
# ====================================================================
sys2q = build_two_qubit_system(dim=dim, omega_c=omega_c, g1=g1, g2=g2)
target_cav_ket = target_fock_2q(dim, n_target, trace_over_qubits=True)
target_dm = grape_target_fock_2q(dim, n_target)
cost_fn = make_crab_cost_cavity(target_cav_ket)
psi0_dm = sys2q.psi0_dm
psi0_ket = sys2q.psi0_ket

print("=" * 60)
print(f"  FULL PIPELINE — target |n={n_target}⟩, 2 qubits")
print(f"  Hilbert space: {sys2q.H0.shape[0]}")
print(f"  T = {T:.2f}  ({T/tau_s:.1f} τ_s)")
print("=" * 60)

# ====================================================================
# Stage 1: Multi-seed CRAB
# ====================================================================
print("\n" + "=" * 60)
print("  STAGE 1: CRAB optimization ({} seeds)".format(CRAB_NUM_SEEDS))
print("=" * 60)

tlist_crab = np.linspace(0, T, CRAB_NT)
dt_crab = tlist_crab[1] - tlist_crab[0]

crab_results = []

for seed in range(CRAB_NUM_SEEDS):
    print(f"\n--- CRAB seed {seed + 1}/{CRAB_NUM_SEEDS} ---")
    t0 = time.time()

    optimizer_crab = CRABOptimizer(
        H_drift=sys2q.H0,
        H_controls=sys2q.H_controls,
        T=T,
        num_tslots=CRAB_NT,
        num_freqs=CRAB_NUM_FREQS,
        omega_bases=omega_bases,
        freq_range=(0, 3 * omega_c),
        basis_type="uniform",
        seed=seed,
    )

    res = optimizer_crab.optimize(
        psi0=psi0_ket,
        cost_function=cost_fn,
        max_iter=CRAB_MAX_ITER,
        method=CRAB_METHOD,
    )

    # Evaluate cavity fidelity
    rho_cav = ptrace(res.final_state, 0)
    F = fidelity(target_cav_ket, rho_cav)
    C2 = compute_control_cost(res.control_pulses, dt_crab)
    elapsed = time.time() - t0

    crab_results.append({
        "seed": seed,
        "fidelity": F,
        "cost": C2,
        "result": res,
        "time": elapsed,
    })

    print(f"  Fidelity: {F:.6f}  |  Cost: {C2:.2f}  |  Time: {elapsed:.1f}s")

# Summary
fidelities = [r["fidelity"] for r in crab_results]
costs = [r["cost"] for r in crab_results]
print(f"\nCRAB summary:")
print(f"  Mean fidelity: {np.mean(fidelities):.6f} ± {np.std(fidelities):.6f}")
print(f"  Mean cost:     {np.mean(costs):.2f} ± {np.std(costs):.2f}")

# Pick best
best_idx = int(np.argmax(fidelities))
best_crab = crab_results[best_idx]
print(f"  Best seed: {best_crab['seed']}  (F = {best_crab['fidelity']:.6f})")

best_pulses_crab = best_crab["result"].control_pulses

# ====================================================================
# Stage 2: GRAPE refinement
# ====================================================================
print("\n" + "=" * 60)
print("  STAGE 2: GRAPE refinement (L-BFGS-B)")
print("=" * 60)

tlist_grape = np.linspace(0, T, GRAPE_NT)

optimizer_grape = GRAPEOptimizer(
    H_drift=sys2q.H0,
    H_controls=sys2q.H_controls,
    T=T,
    num_tslots=GRAPE_NT,
    omega_bases=omega_bases,
    epsilon=1e-1,
    seed=None,
)

print("Running GRAPE with CRAB warm-start...")
t0 = time.time()
result_grape = optimizer_grape.optimize_minimize(
    psi0=psi0_dm,
    target_state=target_dm,
    max_iter=GRAPE_MAX_ITER,
    amp_bound=GRAPE_AMP_BOUND,
    initial_guess=best_pulses_crab,
)
elapsed_grape = time.time() - t0

# Evaluate GRAPE result
states_grape = optimizer_grape.forward_propagation(
    result_grape.control_pulses, psi0_dm
)
F_grape = fidelity(target_cav_ket, ptrace(states_grape[-1], 0))
C2_grape = compute_control_cost(result_grape.control_pulses, tlist_grape[1] - tlist_grape[0])

print(f"  GRAPE fidelity: {F_grape:.6f}")
print(f"  GRAPE cost:     {C2_grape:.2f}")
print(f"  GRAPE time:     {elapsed_grape:.1f}s")

# ====================================================================
# Stage 3: Interpolation smoothing
# ====================================================================
print("\n" + "=" * 60)
print("  STAGE 3: Interpolation smoothing")
print("=" * 60)

tlist_fine = np.linspace(0, T, INTERP_NT)

ctrl_q1_grape = result_grape.control_pulses[0]
ctrl_q2_grape = result_grape.control_pulses[1]

cs_q1 = PchipInterpolator(tlist_grape, ctrl_q1_grape)
cs_q2 = PchipInterpolator(tlist_grape, ctrl_q2_grape)

ctrl_q1_smooth = cs_q1(tlist_fine)
ctrl_q2_smooth = cs_q2(tlist_fine)

# Verify fidelity after smoothing
optimizer_fine = GRAPEOptimizer(
    H_drift=sys2q.H0,
    H_controls=sys2q.H_controls,
    T=T,
    num_tslots=INTERP_NT,
    omega_bases=omega_bases,
    epsilon=1e-1,
)

states_smooth = optimizer_fine.forward_propagation(
    [ctrl_q1_smooth, ctrl_q2_smooth], psi0_dm
)
F_smooth = fidelity(target_cav_ket, ptrace(states_smooth[-1], 0))
C2_smooth = compute_control_cost(
    [ctrl_q1_smooth, ctrl_q2_smooth], tlist_fine[1] - tlist_fine[0]
)

print(f"  Smoothed fidelity: {F_smooth:.6f}")
print(f"  Smoothed cost:     {C2_smooth:.2f}")

# ====================================================================
# Final summary
# ====================================================================
print("\n" + "=" * 60)
print("  FINAL SUMMARY")
print("=" * 60)
print(f"  {'Stage':<25s}  {'Fidelity':>10s}  {'Cost C²':>10s}")
print(f"  {'-'*25}  {'-'*10}  {'-'*10}")
print(f"  {'CRAB (best seed)':<25s}  {best_crab['fidelity']:10.6f}  {best_crab['cost']:10.2f}")
print(f"  {'GRAPE (L-BFGS-B)':<25s}  {F_grape:10.6f}  {C2_grape:10.2f}")
print(f"  {'Interpolated':<25s}  {F_smooth:10.6f}  {C2_smooth:10.2f}")

# ====================================================================
# Save results
# ====================================================================
np.savez(
    os.path.join(output_dir, "results.npz"),
    tlist_crab=tlist_crab,
    tlist_grape=tlist_grape,
    tlist_fine=tlist_fine,
    ctrl_q1_crab=best_pulses_crab[0],
    ctrl_q2_crab=best_pulses_crab[1],
    ctrl_q1_grape=ctrl_q1_grape,
    ctrl_q2_grape=ctrl_q2_grape,
    ctrl_q1_smooth=ctrl_q1_smooth,
    ctrl_q2_smooth=ctrl_q2_smooth,
    fidelity_crab=best_crab["fidelity"],
    fidelity_grape=F_grape,
    fidelity_smooth=F_smooth,
    cost_crab=best_crab["cost"],
    cost_grape=C2_grape,
    cost_smooth=C2_smooth,
)
print(f"\nResults saved to {output_dir}/results.npz")

# ====================================================================
# Plots
# ====================================================================
n_expect = [expect(sys2q.n_tot, rho) for rho in states_smooth]

# ---- Mean photon number ----
plt.figure(figsize=(7, 4))
plt.plot(tlist_fine / tau_s, n_expect[1:], "crimson", lw=2)
plt.xlabel(r"$t / \tau_s$")
plt.ylabel(r"$\langle n \rangle$")
plt.title(f"Pipeline — Mean photon number  (F = {F_smooth:.4f})")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "nmean.pdf"), dpi=300)
plt.show()

# ---- Control drives (all stages) ----
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
# CRAB
axes[0, 0].plot(tlist_crab / tau_s, best_pulses_crab[0], "darkgreen", lw=1.5)
axes[0, 0].set_title(f"CRAB — Q1  (F={best_crab['fidelity']:.4f})")
axes[0, 0].set_ylabel(r"$\Omega_{D1}/\omega_c$")
axes[0, 0].grid(True)

axes[1, 0].plot(tlist_crab / tau_s, best_pulses_crab[1], "navy", lw=1.5)
axes[1, 0].set_title("CRAB — Q2")
axes[1, 0].set_xlabel(r"$t/\tau_s$")
axes[1, 0].set_ylabel(r"$\Omega_{D2}/\omega_c$")
axes[1, 0].grid(True)

# Smoothed
axes[0, 1].plot(tlist_fine / tau_s, ctrl_q1_smooth, "darkgreen", lw=1.5)
axes[0, 1].set_title(f"Smoothed — Q1  (F={F_smooth:.4f})")
axes[0, 1].grid(True)

axes[1, 1].plot(tlist_fine / tau_s, ctrl_q2_smooth, "navy", lw=1.5)
axes[1, 1].set_title("Smoothed — Q2")
axes[1, 1].set_xlabel(r"$t/\tau_s$")
axes[1, 1].grid(True)

fig.tight_layout()
plt.savefig(os.path.join(output_dir, "drives_comparison.pdf"), dpi=300)
plt.show()

# ---- Wigner functions ----
xvec = np.linspace(-5, 5, 200)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

w_target = wigner(target_cav_ket, xvec, xvec)
axes[0].contourf(xvec, xvec, w_target, 100, cmap="RdBu_r")
axes[0].set_title("Target Wigner")
axes[0].set_xlabel("x")
axes[0].set_ylabel("p")

final_cav = ptrace(states_smooth[-1], 0)
w_final = wigner(final_cav, xvec, xvec)
im = axes[1].contourf(xvec, xvec, w_final, 100, cmap="RdBu_r")
axes[1].set_title(f"Optimized Wigner (F={F_smooth:.4f})")
axes[1].set_xlabel("x")
fig.colorbar(im, ax=axes[1])
fig.tight_layout()
plt.savefig(os.path.join(output_dir, "wigner.pdf"), dpi=300)
plt.show()

# ---- FFT ----
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
dt_fine = tlist_fine[1] - tlist_fine[0]
for ctrl, ax, label in zip(
    [ctrl_q1_smooth, ctrl_q2_smooth], axes, ["Qubit 1", "Qubit 2"]
):
    ctrl_c = ctrl - np.mean(ctrl)
    fft_v = np.fft.fft(ctrl_c)
    freqs = np.fft.fftfreq(len(ctrl_c), d=dt_fine)
    mask = freqs >= 0
    ax.plot(freqs[mask] * (2 * np.pi), np.abs(fft_v[mask]))
    ax.axvline(2 * omega_c, color="red", ls="--", label=r"$2\omega_c$")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Amplitude")
    ax.set_title(f"FFT — {label}")
    ax.legend()
    ax.grid(True)
fig.tight_layout()
plt.savefig(os.path.join(output_dir, "fft.pdf"), dpi=300)
plt.show()

print(f"\nAll figures saved to {output_dir}/")
print("Pipeline complete.")
