"""Create an MP4 of the saved cat 2Q GRAPE run, with physical substeps."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import numpy as np
from scipy.sparse.linalg import expm_multiply
from qutip import Qobj, wigner
from two_qubit_system import build_two_qubit_system, target_cat_2q


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "visualizzazioni/cat_2q"
    meta = json.loads((out / "provenienza.json").read_text())
    with np.load(meta["source"]) as data:
        controls = data["ctrl_grape"].copy()
        dim = int(data["dim"])
        alpha = float(data["target_param"])
        tau = float(data["tau_s"])
    system = build_two_qubit_system(dim, meta["omega_c"], meta["g1"], meta["g2"])
    h0 = system.H0.to("CSR").data.as_scipy()
    hc = [op.to("CSR").data.as_scipy() for op in system.H_controls]
    # Resolve each original constant pulse into four exact unitary substeps.
    # No interpolation of images or states and no new optimization.
    dt = meta["time_step"] / 4
    psi = system.psi0_ket.full().ravel()
    states = [psi.copy()]
    for values in controls.T:
        h = h0 + sum(u * op for u, op in zip(values, hc))
        chunk = expm_multiply(-1j*h, psi, start=0, stop=4*dt, num=5)
        states.extend(chunk[1:].copy())
        psi = chunk[-1]
    states = np.asarray(states)
    amplitudes = states.reshape(-1, dim, 4)
    rho = amplitudes @ amplitudes.conj().transpose(0, 2, 1)
    populations = np.sum(abs(amplitudes)**2, axis=1)
    photons = np.diagonal(rho, axis1=1, axis2=2).real
    purity = np.einsum("tij,tji->t", rho, rho).real
    target = target_cat_2q(dim, alpha).full().ravel()
    probability = np.einsum("i,tij,j->t", target.conj(), rho, target).real
    assert abs(np.sqrt(probability[-1])-meta["saved_root_fidelity"]) < 1e-6
    assert np.max(abs(np.sum(abs(states)**2, axis=1)-1)) < 1e-8
    times = np.arange(len(states))*dt/tau
    grid = np.linspace(-5, 5, 101)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100, facecolor="#f8fafc")
    gs = fig.add_gridspec(3, 2, width_ratios=[1.3, 1], left=.065, right=.96,
                          top=.84, bottom=.13, wspace=.32, hspace=.68)
    axw = fig.add_subplot(gs[:, 0])
    imp = axw.imshow(wigner(Qobj(rho[0]), grid, grid), extent=[-5, 5, -5, 5],
                     origin="lower", cmap="RdBu_r", vmin=-1/np.pi, vmax=1/np.pi)
    axw.set(xlabel="Quadratura x", ylabel="Quadratura p", title="Stato quantistico della cavità")
    fig.colorbar(imp, ax=axw, shrink=.7, pad=.025, label="Wigner")
    axn = fig.add_subplot(gs[0, 1])
    bars_n = axn.bar(np.arange(dim), photons[0], color="#7c3aed", width=.8)
    axn.set(xlim=(-.7, 15.7), ylim=(0, 1.03), ylabel="Probabilità", title="Fotoni nella cavità", xlabel="n")
    axn.set_xticks(np.arange(0, 16, 2))
    axq = fig.add_subplot(gs[1, 1])
    bars_q = axq.bar(["gg", "ge", "eg", "ee"], populations[0],
                      color=["#2563eb", "#f59e0b", "#10b981", "#ef4444"])
    axq.set(ylim=(0, 1.03), ylabel="Probabilità", title="Stati dei due qubit · g: fondamentale, e: eccitato")
    axp = fig.add_subplot(gs[2, 1])
    axp.plot(times, probability, color="#2563eb", alpha=.18)
    axp.plot(times, purity, color="#ea580c", alpha=.18)
    lp, = axp.plot([], [], color="#2563eb", label="Target")
    lu, = axp.plot([], [], color="#ea580c", label="Purezza")
    cursor = axp.axvline(0, color="#475569", lw=1)
    axp.set(xlim=(0, times[-1]), ylim=(0, 1.03), xlabel="Tempo t/τs")
    axp.legend(loc="upper left", ncol=2, fontsize=9)
    fig.text(.065, .94, "Dal vuoto a uno stato cat", fontsize=24, weight="bold", color="#0f172a")
    fig.text(.065, .89, "Cavità + 2 qubit  •  Evoluzione dagli impulsi GRAPE salvati", fontsize=13, color="#475569")
    clock = fig.text(.96, .94, "", ha="right", fontsize=18, color="#0f172a")
    status = fig.text(.065, .065, "", fontsize=12, color="#0f172a")
    fig.text(.065, .025, "Blu nella Wigner: valori negativi. Tempo della v1 riprodotto: finale 15,10 τs. Livelli mostrati: n ≤ 15.",
             fontsize=9, color="#64748b")
    movie = out / "evoluzione_cat_2q.mp4"
    writer = FFMpegWriter(fps=20, codec="libopenh264", bitrate=2400,
                         extra_args=["-pix_fmt", "yuv420p", "-movflags", "+faststart"])
    with writer.saving(fig, str(movie), dpi=100):
        for i in range(len(states)):
            imp.set_data(wigner(Qobj(rho[i]), grid, grid))
            for bar, value in zip(bars_n, photons[i]):
                bar.set_height(value)
            for bar, value in zip(bars_q, populations[i]):
                bar.set_height(value)
            lp.set_data(times[:i+1], probability[:i+1])
            lu.set_data(times[:i+1], purity[:i+1])
            cursor.set_xdata([times[i], times[i]])
            clock.set_text(f"t / τs = {times[i]:05.2f}")
            status.set_text(f"Probabilità del target: {100*probability[i]:5.1f}%     |     Purezza: {purity[i]:.3f}     |     Fotoni medi: {photons[i] @ np.arange(dim):.2f}")
            writer.grab_frame()
            if i in [0, len(states)//2, len(states)-1]:
                fig.savefig(out / f"video_frame_{i:04d}.png", dpi=100)
            if i % 100 == 0:
                print(f"Frame {i}/{len(states)-1}", flush=True)
        for _ in range(40):
            writer.grab_frame()
    plt.close(fig)
    print(movie, flush=True)


if __name__ == "__main__":
    main()
