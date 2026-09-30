"""
run_full_pipeline_1q.py
=======================
Full hybrid optimal-control pipeline for the cavity + 1 qubit system:

    CRAB (multi-seed, parallel) → best-pick → GRAPE refinement → Interpolation

Reproduces the procedure described in the paper for the one-qubit case.

Supports cross-platform multiprocessing (Linux, Windows, macOS).

Usage:
    python run_full_pipeline_1q.py
"""

import sys
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from qutip import sesolve, expect, ptrace, fidelity, wigner, ket2dm

# ── Ensure project root is in sys.path for worker processes on all OS ──
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from one_qubit_system import (
    build_one_qubit_system,
    target_fock_1q,
    grape_target_fock_1q,
    make_crab_cost_cavity,
    compute_control_cost,
)
from crab_optimizer import CRABOptimizer
from grape_optimizer import GRAPEOptimizer

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
dim = 40
omega_c = 1.0
g = 0.3
tau_s = np.pi / (2 * g)
T = 20 * tau_s
omega_bases = [2.0]

# --- CRAB stage ---
CRAB_NUM_SEEDS = 10        # number of independent CRAB runs
CRAB_NT = 400              # CRAB time slots
CRAB_NUM_FREQS = 20        # Fourier components per control
CRAB_MAX_ITER = None       # Nelder-Mead default (None = auto/unlimited)
CRAB_METHOD = "Nelder-Mead"

# --- GRAPE stage ---
GRAPE_NT = 300             # GRAPE time slots
GRAPE_MAX_ITER = 500
GRAPE_AMP_BOUND = (0.5, 3.0)

# --- Interpolation stage ---
INTERP_NT = 600            # fine time grid for final smoothing

# --- Target ---
n_target = 10

# --- Output ---
output_dir = f"results_1q_pipeline_n{n_target}"


# ====================================================================
# Top-level Worker for Parallel CRAB (Cross-platform)
# ====================================================================
def _crab_worker(args):
    """
    Top-level worker function executed across processes.
    Reconstructs the system locally to ensure 100% compatibility with
    the 'spawn' start method used on Windows and macOS.
    """
    (seed, dim_, omega_c_, g_, n_target_, T_, Nt_, num_freqs_, omega_bases_, max_iter_, method_) = args

    # Ensure project directory is in path inside spawned worker
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    from one_qubit_system import build_one_qubit_system, target_fock_1q, make_crab_cost_cavity, compute_control_cost
    from crab_optimizer import CRABOptimizer
    from qutip import ptrace, fidelity

    t0 = time.time()
    sys1q_worker = build_one_qubit_system(dim=dim_, omega_c=omega_c_, g=g_)
    target_cav_worker = target_fock_1q(dim_, n_target_, trace_over_qubit=True)
    cost_fn_worker = make_crab_cost_cavity(target_cav_worker)

    opt = CRABOptimizer(
        H_drift=sys1q_worker.H0,
        H_controls=sys1q_worker.H_controls,
        T=T_,
        num_tslots=Nt_,
        num_freqs=num_freqs_,
        omega_bases=omega_bases_,
        freq_range=(0, 3 * omega_c_),
        basis_type="uniform",
        seed=seed,
    )

    res = opt.optimize(
        psi0=sys1q_worker.psi0_ket,
        cost_function=cost_fn_worker,
        max_iter=max_iter_,
        method=method_,
    )

    rho_cav = ptrace(res.final_state, 0)
    F = float(fidelity(target_cav_worker, rho_cav))
    dt_crab = T_ / (Nt_ - 1)
    C2 = float(compute_control_cost(res.control_pulses, dt_crab))
    elapsed = time.time() - t0

    return {
        "seed": seed,
        "fidelity": F,
        "cost": C2,
        "control_pulses": res.control_pulses,
        "final_state": res.final_state,
        "elapsed": elapsed,
        "message": res.message,
    }


# ====================================================================
# Main Workflow
# ====================================================================
def main():
    t_pipeline_start = time.time()
    os.makedirs(output_dir, exist_ok=True)

    # Build system for main process
    sys1q = build_one_qubit_system(dim=dim, omega_c=omega_c, g=g)
    target_cav_ket = target_fock_1q(dim, n_target, trace_over_qubit=True)
    target_dm = grape_target_fock_1q(dim, n_target, ground_qubit=False)
    psi0_dm = sys1q.psi0_dm

    print("=" * 65)
    print(f"  FULL PIPELINE — target |n={n_target}⟩, 1 qubit")
    print(f"  Hilbert space dimension: {sys1q.H0.shape[0]} (dim={dim} × 2)")
    print(f"  T = {T:.2f}  ({T/tau_s:.1f} τ_s)")
    print("=" * 65)

    # ----------------------------------------------------------------
    # Stage 1: Parallel Multi-Seed CRAB Optimization
    # ----------------------------------------------------------------
    cpu_count = os.cpu_count() or 1
    # Leave 1 core for OS responsiveness, min 1 worker
    n_workers = min(CRAB_NUM_SEEDS, max(1, cpu_count - 1))

    print("\n" + "=" * 65)
    print(f"  STAGE 1: Parallel CRAB optimization ({CRAB_NUM_SEEDS} seeds)")
    print(f"  Allocated workers: {n_workers} (detected {cpu_count} CPU cores)")
    print("=" * 65)

    tlist_crab = np.linspace(0, T, CRAB_NT)
    t_start_crab = time.time()

    task_args = [
        (seed, dim, omega_c, g, n_target, T, CRAB_NT, CRAB_NUM_FREQS, omega_bases, CRAB_MAX_ITER, CRAB_METHOD)
        for seed in range(CRAB_NUM_SEEDS)
    ]

    crab_results = []
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        future_to_seed = {executor.submit(_crab_worker, arg): arg[0] for arg in task_args}
        completed = 0
        for future in as_completed(future_to_seed):
            completed += 1
            res_dict = future.result()
            crab_results.append(res_dict)
            print(f"  [{completed:>2d}/{CRAB_NUM_SEEDS}] Seed {res_dict['seed'] + 1:>2d} finished | "
                  f"Fidelity: {res_dict['fidelity']:.6f} | "
                  f"Cost C²: {res_dict['cost']:7.2f} | "
                  f"Time: {res_dict['elapsed']:.1f}s")

    total_crab_time = time.time() - t_start_crab
    print(f"\nAll {CRAB_NUM_SEEDS} seeds completed in parallel in {total_crab_time:.1f}s (~{total_crab_time/60:.1f} min)")

    # Sort results by seed order for deterministic reporting
    crab_results.sort(key=lambda r: r["seed"])

    fidelities = [r["fidelity"] for r in crab_results]
    costs = [r["cost"] for r in crab_results]

    print(f"\nCRAB Summary ({CRAB_NUM_SEEDS} seeds):")
    print(f"  Mean fidelity: {np.mean(fidelities):.6f} ± {np.std(fidelities):.6f}")
    print(f"  Mean cost C²:  {np.mean(costs):.2f} ± {np.std(costs):.2f}")

    # Pick the best seed
    best_idx = int(np.argmax(fidelities))
    best_crab = crab_results[best_idx]
    print(f"\n  >>> BEST SEED: Seed {best_crab['seed'] + 1} (F = {best_crab['fidelity']:.6f}, C² = {best_crab['cost']:.2f}) <<<")

    best_pulses_crab = best_crab["control_pulses"]

    # ----------------------------------------------------------------
    # Stage 2: GRAPE Refinement (L-BFGS-B)
    # ----------------------------------------------------------------
    print("\n" + "=" * 65)
    print("  STAGE 2: GRAPE refinement (L-BFGS-B with bounds)")
    print("=" * 65)

    tlist_grape = np.linspace(0, T, GRAPE_NT)
    dt_grape = tlist_grape[1] - tlist_grape[0]

    optimizer_grape = GRAPEOptimizer(
        H_drift=sys1q.H0,
        H_controls=sys1q.H_controls,
        T=T,
        num_tslots=GRAPE_NT,
        omega_bases=omega_bases,
        seed=None,
    )

    print(f"Running GRAPE with warm-start from best CRAB seed (max_iter={GRAPE_MAX_ITER})...")
    t0 = time.time()
    result_grape = optimizer_grape.optimize_minimize(
        psi0=psi0_dm,
        target_state=target_dm,
        max_iter=GRAPE_MAX_ITER,
        amp_bound=GRAPE_AMP_BOUND,
        initial_guess=best_pulses_crab,
    )
    elapsed_grape = time.time() - t0

    states_grape = optimizer_grape.forward_propagation(result_grape.control_pulses, psi0_dm)
    rho_cav_grape = ptrace(states_grape[-1], 0)
    F_grape = float(fidelity(target_cav_ket, rho_cav_grape))
    C2_grape = float(compute_control_cost(result_grape.control_pulses, dt_grape))

    print(f"  GRAPE fidelity: {F_grape:.6f}")
    print(f"  GRAPE cost C²:  {C2_grape:.2f}")
    print(f"  GRAPE time:     {elapsed_grape:.1f}s")
    print(f"  GRAPE message:  {result_grape.message}")

    # ----------------------------------------------------------------
    # Stage 3: PCHIP Interpolation Smoothing
    # ----------------------------------------------------------------
    print("\n" + "=" * 65)
    print("  STAGE 3: Interpolation smoothing (PCHIP)")
    print("=" * 65)

    tlist_fine = np.linspace(0, T, INTERP_NT)
    dt_fine = tlist_fine[1] - tlist_fine[0]

    ctrl_q1_grape = result_grape.control_pulses[0]

    cs_q1 = PchipInterpolator(tlist_grape, ctrl_q1_grape)
    ctrl_q1_smooth = cs_q1(tlist_fine)

    optimizer_fine = GRAPEOptimizer(
        H_drift=sys1q.H0,
        H_controls=sys1q.H_controls,
        T=T,
        num_tslots=INTERP_NT,
        omega_bases=omega_bases,
    )

    states_smooth = optimizer_fine.forward_propagation([ctrl_q1_smooth], sys1q.psi0_dm)
    rho_cav_smooth = ptrace(states_smooth[-1], 0)
    F_smooth = float(fidelity(target_cav_ket, rho_cav_smooth))
    C2_smooth = float(compute_control_cost([ctrl_q1_smooth], dt_fine))

    print(f"  Smoothed fidelity: {F_smooth:.6f}")
    print(f"  Smoothed cost C²:  {C2_smooth:.2f}")

    total_pipeline_time = time.time() - t_pipeline_start

    # ----------------------------------------------------------------
    # Final Summary Table
    # ----------------------------------------------------------------
    print("\n" + "=" * 65)
    print("  FINAL PIPELINE SUMMARY (1 QUBIT)")
    print("=" * 65)
    print(f"  {'Stage':<25s}  {'Fidelity':>12s}  {'Cost C²':>12s}")
    print(f"  {'-'*25}  {'-'*12}  {'-'*12}")
    print(f"  {'CRAB (best seed)':<25s}  {best_crab['fidelity']:12.6f}  {best_crab['cost']:12.2f}")
    print(f"  {'GRAPE (L-BFGS-B)':<25s}  {F_grape:12.6f}  {C2_grape:12.2f}")
    print(f"  {'PCHIP Smoothed':<25s}  {F_smooth:12.6f}  {C2_smooth:12.2f}")
    print("=" * 65)
    print(f"  Total pipeline time: {total_pipeline_time:.1f}s (~{total_pipeline_time/60:.1f} min)")
    print("=" * 65)

    # ----------------------------------------------------------------
    # Save Results
    # ----------------------------------------------------------------
    results_path = os.path.join(output_dir, "results.npz")
    np.savez(
        results_path,
        tlist_crab=tlist_crab,
        tlist_grape=tlist_grape,
        tlist_fine=tlist_fine,
        ctrl_q1_crab=best_pulses_crab[0],
        ctrl_q1_grape=ctrl_q1_grape,
        ctrl_q1_smooth=ctrl_q1_smooth,
        ctrl_q_crab=best_pulses_crab[0],
        ctrl_q_grape=ctrl_q1_grape,
        ctrl_q_smooth=ctrl_q1_smooth,
        fidelity_crab=best_crab["fidelity"],
        fidelity_grape=F_grape,
        fidelity_smooth=F_smooth,
        cost_crab=best_crab["cost"],
        cost_grape=C2_grape,
        cost_smooth=C2_smooth,
        all_fidelities=fidelities,
        all_costs=costs,
        elapsed_crab=total_crab_time,
        elapsed_grape=elapsed_grape,
        elapsed_total=total_pipeline_time,
    )
    print(f"\nAll data saved to {results_path}")

    # ----------------------------------------------------------------
    # Plots Generation (PDFs)
    # ----------------------------------------------------------------
    n_expect = [expect(sys1q.n_tot, rho) for rho in states_smooth]

    # 1. Mean photon number
    plt.figure(figsize=(7, 4))
    plt.plot(tlist_fine / tau_s, n_expect[1:], "crimson", lw=2)
    plt.axhline(n_target, color="gray", ls="--", label=f"Target n={n_target}")
    plt.xlabel(r"$t / \tau_s$")
    plt.ylabel(r"$\langle n \rangle$")
    plt.title(f"Pipeline 1Q — Mean photon number  (F = {F_smooth:.4f})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "nmean.pdf"), dpi=300)
    plt.close()

    # 2. Control drives comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    # CRAB Q1
    axes[0].plot(tlist_crab / tau_s, best_pulses_crab[0], "darkgreen", lw=1.5)
    axes[0].set_title(f"CRAB — Qubit 1  (F={best_crab['fidelity']:.4f})")
    axes[0].set_xlabel(r"$t/\tau_s$")
    axes[0].set_ylabel(r"$\Omega_D(t)/\omega_c$")
    axes[0].grid(True, alpha=0.3)
    # Smoothed Q1
    axes[1].plot(tlist_fine / tau_s, ctrl_q1_smooth, "darkgreen", lw=1.8)
    axes[1].set_title(f"Smoothed (GRAPE + PCHIP) — Qubit 1  (F={F_smooth:.4f})")
    axes[1].set_xlabel(r"$t/\tau_s$")
    axes[1].set_ylabel(r"$\Omega_D(t)/\omega_c$")
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "drives_comparison.pdf"), dpi=300)
    plt.close()

    # 3. Wigner functions
    xvec = np.linspace(-5, 5, 200)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    w_target = wigner(target_cav_ket, xvec, xvec)
    axes[0].contourf(xvec, xvec, w_target, 100, cmap="RdBu_r")
    axes[0].set_title(f"Target Wigner (|n={n_target}⟩)")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("p")

    w_final = wigner(rho_cav_smooth, xvec, xvec)
    im = axes[1].contourf(xvec, xvec, w_final, 100, cmap="RdBu_r")
    axes[1].set_title(f"Optimized Wigner (F={F_smooth:.4f})")
    axes[1].set_xlabel("x")
    fig.colorbar(im, ax=axes[1])
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "wigner.pdf"), dpi=300)
    plt.close()

    # 4. FFT spectrum
    fig, ax = plt.subplots(figsize=(7, 4))
    ctrl_c = ctrl_q1_smooth - np.mean(ctrl_q1_smooth)
    fft_v = np.fft.fft(ctrl_c)
    freqs = np.fft.fftfreq(len(ctrl_c), d=dt_fine)
    mask = freqs >= 0
    ax.plot(freqs[mask] * (2 * np.pi), np.abs(fft_v[mask]), "darkgreen", lw=1.5)
    ax.axvline(2 * omega_c, color="red", ls="--", label=r"$2\omega_c$")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Amplitude")
    ax.set_title("FFT — Qubit 1")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "fft.pdf"), dpi=300)
    plt.close()

    print(f"All figures saved to {output_dir}/ (.pdf)")
    print("Pipeline complete successfully.")


if __name__ == "__main__":
    main()
