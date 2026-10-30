"""Replay saved 2Q cat pulses with the original v1 time-step convention.

No optimization is performed. Physical parameters must match the run report.
The v1 propagator applies N steps of T/(N-1); plot the actual propagated time.
"""
import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse.linalg import expm_multiply
from qutip import Qobj, wigner
from two_qubit_system import build_two_qubit_system, target_cat_2q


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stage", choices=["grape", "smooth"], default="grape")
    parser.add_argument("--omega-c", type=float, default=1.)
    parser.add_argument("--g1", type=float, default=.3)
    parser.add_argument("--g2", type=float, default=.3)
    args = parser.parse_args()
    path = args.run / "results.npz"
    with np.load(path, allow_pickle=False) as data:
        if str(data["system_type"]) != "2q" or str(data["target_type"]) != "cat":
            raise ValueError("This example supports the v1 2Q cat runs only")
        dim = int(data["dim"])
        alpha = float(data["target_param"])
        T, tau = float(data["T"]), float(data["tau_s"])
        controls = data[f"ctrl_{args.stage}"].copy()
        reference = float(data[f"fidelity_{args.stage}"])
    system = build_two_qubit_system(dim, args.omega_c, args.g1, args.g2)
    nsteps = controls.shape[1]
    dt = T / (nsteps - 1)
    times = np.arange(nsteps + 1) * dt
    psi = system.psi0_ket.full().ravel()
    states = [psi.copy()]
    h0 = system.H0.to("CSR").data.as_scipy()
    hc = [h.to("CSR").data.as_scipy() for h in system.H_controls]
    for values in controls.T:
        h = h0 + sum(u * op for u, op in zip(values, hc))
        psi = expm_multiply(-1j * dt * h, psi)
        states.append(psi.copy())
    states = np.asarray(states)
    amplitudes = states.reshape(-1, dim, 4)
    rho = amplitudes @ amplitudes.conj().transpose(0, 2, 1)
    populations = np.sum(abs(amplitudes)**2, axis=1)
    photons = np.diagonal(rho, axis1=1, axis2=2).real
    purity = np.einsum("tij,tji->t", rho, rho).real
    target = target_cat_2q(dim, alpha).full().ravel()
    probability = np.einsum("i,tij,j->t", target.conj(), rho, target).real
    final_fidelity = np.sqrt(max(0., probability[-1]))
    norm_error = float(np.max(abs(np.sum(abs(states)**2, axis=1) - 1)))
    if abs(final_fidelity-reference) > 1e-6 or norm_error > 1e-8:
        raise ValueError(f"Replay does not match: F={final_fidelity}, saved={reference}, norm={norm_error}")
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    grid = np.linspace(-5, 5, 151)
    selected = np.rint(np.linspace(0, nsteps, 7)).astype(int)
    images = [wigner(Qobj(rho[i]), grid, grid) for i in selected]
    images.append(wigner(Qobj(target), grid, grid))
    limit = max(float(np.max(abs(w))) for w in images)
    fig, axes = plt.subplots(2, 4, figsize=(14, 7), layout="constrained")
    for j, (ax, values) in enumerate(zip(axes.flat, images)):
        im = ax.imshow(values, extent=[-5, 5, -5, 5], origin="lower",
                       cmap="RdBu_r", vmin=-limit, vmax=limit)
        ax.set(xlabel="Quadratura x", ylabel="Quadratura p")
        ax.set_title(f"t/τs = {times[selected[j]]/tau:.2f}" if j < 7 else "Target cat, α = 2")
    fig.colorbar(im, ax=axes, shrink=.85, label="Wigner W(x,p)")
    fig.suptitle(f"Cavità + 2 qubit · evoluzione con impulsi {args.stage.upper()} salvati", fontsize=17)
    fig.savefig(out / "wigner_evoluzione.png", dpi=160)
    fig.savefig(out / "wigner_evoluzione.pdf")
    plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), layout="constrained")
    t = times/tau
    ax = axes[0, 0]
    mesh = ax.pcolormesh(t, np.arange(dim), photons.T, shading="auto", cmap="magma", vmin=0, vmax=1)
    ax.set(title="Come si popolano i livelli della cavità", ylabel="Numero di fotoni n")
    fig.colorbar(mesh, ax=ax, label="P(n)")
    ax = axes[0, 1]
    for k, label in enumerate(["gg", "ge", "eg", "ee"]):
        ax.plot(t, populations[:, k], label=label)
    ax.set(title="Popolazioni congiunte dei qubit", ylabel="Probabilità", ylim=(-.03, 1.03))
    ax.legend(ncol=4)
    ax = axes[1, 0]
    ax.plot(t, probability, label="Probabilità del target cat")
    ax.plot(t, purity, label="Purezza della cavità")
    ax.set(title="Preparazione e correlazioni con i qubit", ylabel="Valore", ylim=(-.03, 1.03))
    ax.legend()
    ax = axes[1, 1]
    ax.plot(t, photons @ np.arange(dim), color="tab:purple")
    ax.set(title="Eccitazione della cavità", ylabel="Numero medio di fotoni")
    for ax in axes.flat:
        ax.set_xlabel("Tempo t/τs")
    fig.suptitle("Dinamica ricostruita dalla run cat 2Q", fontsize=17)
    fig.savefig(out / "osservabili.png", dpi=160)
    fig.savefig(out / "osservabili.pdf")
    plt.close(fig)
    meta = dict(source=str(path.resolve()), source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                stage=args.stage, omega_c=args.omega_c, g1=args.g1, g2=args.g2,
                nominal_T=T, actual_final_time=float(times[-1]), time_step=dt,
                time_convention="Original v1: N steps of T/(N-1), including last control sample",
                saved_root_fidelity=reference, reconstructed_root_fidelity=float(final_fidelity),
                final_target_probability=float(probability[-1]), maximum_norm_error=norm_error,
                final_cavity_purity=float(purity[-1]), minimum_cavity_purity=float(purity.min()))
    (out / "provenienza.json").write_text(json.dumps(meta, indent=2)+"\n")
    np.savez_compressed(out / "traiettoria.npz", times=times, states=states,
                        cavity_purity=purity, target_probability=probability,
                        photon_populations=photons, qubit_populations=populations)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
