from pathlib import Path
import csv
import shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10.5,
    "axes.titlesize": 11,
    "axes.labelsize": 10.5,
    "legend.fontsize": 9,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "figure.dpi": 220,
})

ROOT = Path("/home/edo_laptop/Desktop/Stage_twoqubits")
CAMP = ROOT / "backup_google_v2/results/campagna_fock_completa_20261005T152239_626536Z"
OUT = ROOT / "report_relatrice/figure"
OUT.mkdir(parents=True, exist_ok=True)

CASES = [
    ("1q", "1Q\n(g=0.3)"),
    ("2q_common", "2Q com.\n(g=0.3)"),
    ("2q_independent", "2Q ind.\n(g=0.3)"),
    ("2q_normalized_common", "2Q norm. com.\n(g=0.3/√2)"),
    ("2q_normalized_independent", "2Q norm. ind.\n(g=0.3/√2)"),
]
COLORS = {
    "1q": "#1f77b4",
    "2q_common": "#ff7f0e",
    "2q_independent": "#2ca02c",
    "2q_normalized_common": "#9467bd",
    "2q_normalized_independent": "#d62728",
}

summary_rows = list(csv.DictReader(open(CAMP / "summary.csv")))

# ---------------------------------------------------------
# FIGURA 1: Panoramica Fock n=2, 6, 10 a T=10 vs T=20 tau_s
# ---------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.8), sharey=True)

configs_grid = [
    (axes[0], "10", "Durata breve: $T = 10\\,\\tau_s$ (filtro $\\omega_c=3.0$)", [
        ("main_004", "Fock $|2\\rangle$"),
        ("main_006", "Fock $|6\\rangle$"),
        ("main_008", "Fock $|10\\rangle$"),
    ]),
    (axes[1], "20", "Durata standard: $T = 20\\,\\tau_s$ (filtro $\\omega_c=3.0$)", [
        ("main_005", "Fock $|2\\rangle$"),
        ("main_007", "Fock $|6\\rangle$"),
        ("main_009", "Fock $|10\\rangle$"),
    ]),
]

for ax, taus_str, title, blocks in configs_grid:
    x = np.arange(len(blocks))
    width = 0.15
    for idx, (case_key, case_label) in enumerate(CASES):
        medians = []
        q25s = []
        q75s = []
        valid_counts = []
        for job_prefix, _ in blocks:
            row = next(
                r for r in summary_rows
                if r["run"].startswith(f"runs/{job_prefix}") and r["case"] == case_key
            )
            med = float(row["probability_median"])
            q25 = float(row["probability_q25"])
            q75 = float(row["probability_q75"])
            vc = int(row["validated_goal_count"])
            medians.append(med)
            q25s.append(med - q25)
            q75s.append(q75 - med)
            valid_counts.append(vc)

        pos = x + (idx - 2) * width
        bars = ax.bar(
            pos,
            medians,
            width=width * 0.92,
            color=COLORS[case_key],
            alpha=0.88,
            label=case_label.replace("\n", " "),
            edgecolor="black",
            linewidth=0.5,
        )
        ax.errorbar(
            pos,
            medians,
            yerr=[q25s, q75s],
            fmt="none",
            ecolor="black",
            elinewidth=1.0,
            capsize=2.5,
        )
        for b, vc, med in zip(bars, valid_counts, medians):
            y_txt = min(med + 0.03, 1.03) if med < 0.92 else 0.91
            txt_color = "black" if med < 0.92 else "white"
            ax.text(
                b.get_x() + b.get_width() / 2,
                y_txt,
                f"{vc}/8",
                ha="center",
                va="bottom" if med < 0.92 else "center",
                fontsize=7.5,
                fontweight="bold",
                color=txt_color,
                rotation=90 if med < 0.92 else 0,
            )

    ax.axhline(0.99, color="crimson", linestyle="--", linewidth=1.1, label="Soglia $P=0.99$")
    ax.set_xticks(x)
    ax.set_xticklabels([b[1] for b in blocks])
    ax.set_ylim(0.0, 1.09)
    ax.set_title(title)
    ax.grid(axis="y", linestyle=":", alpha=0.6)

axes[0].set_ylabel("Probabilità target continua $P_{\\mathrm{target}}$ (mediana e quartili)")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=6, bbox_to_anchor=(0.5, 1.03), frameon=False)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(OUT / "fig1_panoramica_campagna.pdf")
fig.savefig(OUT / "fig1_panoramica_campagna.png")
plt.close(fig)

# ---------------------------------------------------------
# FIGURA 2: Confronto Fock 10 a T=10 tau_s CON vs SENZA filtro (main_008 vs main_010)
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.5, 4.6))

x = np.arange(len(CASES))
width = 0.34

for i, (job_prefix, label_mode, hatch_style, alpha_val) in enumerate([
    ("main_008", "Con filtro passa-basso ($\\omega_c = 3.0$) — main_008", "", 0.85),
    ("main_010", "Senza filtro ($\\omega_c = \\mathrm{null}$) — main_010", "//", 0.55),
]):
    medians, mins, maxs, vcounts = [], [], [], []
    for case_key, _ in CASES:
        row = next(
            r for r in summary_rows
            if r["run"].startswith(f"runs/{job_prefix}") and r["case"] == case_key
        )
        med = float(row["probability_median"])
        pmin = float(row["probability_min"])
        pmax = float(row["probability_max"])
        vc = int(row["validated_goal_count"])
        medians.append(med)
        mins.append(med - pmin)
        maxs.append(pmax - med)
        vcounts.append(vc)

    pos = x + (i - 0.5) * width
    bars = ax.bar(
        pos,
        medians,
        width=width * 0.92,
        color=[COLORS[c[0]] for c in CASES],
        alpha=alpha_val,
        hatch=hatch_style,
        edgecolor="black",
        linewidth=0.8,
        label=label_mode,
    )
    ax.errorbar(
        pos,
        medians,
        yerr=[mins, maxs],
        fmt="o",
        color="black",
        markersize=3.5,
        elinewidth=1.1,
        capsize=3,
    )
    for b, vc, pmax in zip(bars, vcounts, np.array(medians) + np.array(maxs)):
        ax.text(
            b.get_x() + b.get_width() / 2,
            min(pmax + 0.025, 1.035),
            f"valid: {vc}/8",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold" if vc > 0 else "normal",
        )

ax.axhline(0.99, color="crimson", linestyle="--", linewidth=1.2, label="Soglia $P_{\\mathrm{target}} = 0.99$")
ax.set_xticks(x)
ax.set_xticklabels([c[1] for c in CASES])
ax.set_ylim(0.0, 1.11)
ax.set_ylabel("Probabilità target $P_{\\mathrm{target}}$ (mediana e min–max su 8 seed)")
ax.set_title("Fock $|n=10\\rangle$ a durata breve $T = 10\\,\\tau_s$: effetto del filtro e dell'accoppiamento")
ax.grid(axis="y", linestyle=":", alpha=0.6)
ax.legend(loc="lower right", frameon=True)
fig.tight_layout()
fig.savefig(OUT / "fig2_fock10_t10_filtro_vs_nofiltro.pdf")
fig.savefig(OUT / "fig2_fock10_t10_filtro_vs_nofiltro.png")
plt.close(fig)

# ---------------------------------------------------------
# FIGURA 3: Confronto diretto P_target tra v1 (post-PCHIP) e v2 (propagazione continua)
# ---------------------------------------------------------
fig, ax2 = plt.subplots(figsize=(8.2, 4.3))
comp_labels = [
    "Fock $|6\\rangle$, $20\\tau_s$\n(2Q indep.)",
    "Fock $|10\\rangle$, $20\\tau_s$\n(2Q indep.)",
    "Fock $|10\\rangle$, $10\\tau_s$\n(1Q)",
    "Fock $|10\\rangle$, $10\\tau_s$\n(2Q indep.)",
]
v1_p = [0.990824**2, 0.987673**2, 0.839708**2, 0.962247**2]
v2_filt_p = [0.999996, 0.999994, 0.310186, 0.940965]
v2_nofilt_p = [np.nan, 0.999979, 0.635531, 0.999937]

xc = np.arange(len(comp_labels))
w2 = 0.25
b_v1 = ax2.bar(xc - w2, v1_p, width=w2, color="#7f7f7f", edgecolor="black", label="v1 (best seed, post-PCHIP, no filtro)")
b_v2f = ax2.bar(xc, v2_filt_p, width=w2, color="#1f77b4", edgecolor="black", label="v2 con filtro $\\omega_c=3.0$ (mediana 8 seed)")
b_v2nf = ax2.bar(xc + w2, np.nan_to_num(v2_nofilt_p, nan=0.0), width=w2, color="#ff7f0e", edgecolor="black",
        label="v2 senza filtro (mediana 8 seed)")

for bar, val in zip(b_v1, v1_p):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.015, f"{val:.3f}", ha="center", va="bottom", fontsize=8)
for bar, val in zip(b_v2f, v2_filt_p):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.015, f"{val:.4f}" if val > 0.99 else f"{val:.3f}", ha="center", va="bottom", fontsize=8)
for bar, val in zip(b_v2nf, v2_nofilt_p):
    if not np.isnan(val):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 0.015, f"{val:.4f}" if val > 0.99 else f"{val:.3f}", ha="center", va="bottom", fontsize=8)

ax2.axhline(0.99, color="crimson", linestyle="--", linewidth=1.0, label="Soglia $P_{\\mathrm{target}} = 0.99$")
ax2.set_xticks(xc)
ax2.set_xticklabels(comp_labels)
ax2.set_ylim(0, 1.12)
ax2.set_ylabel("Probabilità target $P_{\\mathrm{target}}$")
ax2.set_title("Confronto diretto di $P_{\\mathrm{target}}$ tra le run v1 (post-PCHIP) e la campagna v2")
ax2.grid(axis="y", linestyle=":", alpha=0.6)
ax2.legend(loc="lower left", fontsize=8.5)

fig.tight_layout()
fig.savefig(OUT / "fig3_confronto_v1_v2.pdf")
fig.savefig(OUT / "fig3_confronto_v1_v2.png")
plt.close(fig)

# ---------------------------------------------------------
# FIGURA 4: Dinamica temporale Fock |6> a T=10 tau_s (main_006): 1q vs 2q_norm_ind vs 2q_ind
# ---------------------------------------------------------
run_m006 = CAMP / "runs/main_006_20261007T160413_143151Z"
selected_m006 = [
    ("1q", 3, "1Q ($g=0.3$, seed 3) — $P(T)=0.777$ (non valid.)"),
    ("2q_normalized_independent", 0, "2Q norm. ind. ($g=0.3/\\sqrt{2}$, seed 0) — $P(T)=0.838$ (non valid.)"),
    ("2q_common", 7, "2Q common ($g=0.3$, seed 7) — $P(T)=0.99998$ (validato)"),
    ("2q_independent", 2, "2Q indep. ($g=0.3$, seed 2) — $P(T)=0.99999$ (validato)"),
]

fig, axes = plt.subplots(2, 1, figsize=(10.0, 6.2), sharex=True)
tau_s = np.pi / (2 * 0.3)

for case_key, seed_id, lbl in selected_m006:
    npz_path = run_m006 / case_key / f"seed_{seed_id}" / "arrays.npz"
    with np.load(npz_path, allow_pickle=False) as data:
        t = data["times"] / tau_s
        n_mean = data["mean_photons"]
        p_traj = data["target_probability_trajectory"]
        axes[0].plot(t, p_traj, lw=1.8, color=COLORS[case_key], label=lbl)
        axes[1].plot(t, n_mean, lw=1.8, color=COLORS[case_key], label=lbl)

axes[0].axvline(10.0, color="black", linestyle="--", lw=1.0, label="Fine impulso $t = T = 10\\,\\tau_s$ (inizio hold)")
axes[1].axvline(10.0, color="black", linestyle="--", lw=1.0)
axes[0].axhline(0.99, color="crimson", linestyle=":", lw=1.0)
axes[1].axhline(6.0, color="gray", linestyle=":", lw=1.0, label="Target $\\langle n \\rangle = 6$")

axes[0].set_ylabel("Probabilità target $P_{|n=6\\rangle}(t)$")
axes[0].set_title("Dinamica temporale su Fock $|n=6\\rangle$ a durata dimezzata $T = 10\\,\\tau_s$ (main_006, con hold di $2\\,\\tau_s$)")
axes[0].grid(True, linestyle=":", alpha=0.6)
axes[0].legend(loc="upper left", fontsize=8.5)

axes[1].set_ylabel("Numero medio di fotoni $\\langle n \\rangle(t)$")
axes[1].set_xlabel("Tempo normalizzato $t / \\tau_s$")
axes[1].grid(True, linestyle=":", alpha=0.6)
axes[1].legend(loc="upper left", fontsize=8.5)

fig.tight_layout()
fig.savefig(OUT / "fig4_dinamica_fock6_t10.pdf")
fig.savefig(OUT / "fig4_dinamica_fock6_t10.png")
plt.close(fig)

# ---------------------------------------------------------
# Copia dei grafici originali delle run v1 (prima della v2)
# ---------------------------------------------------------
v1_f6_t20 = ROOT / "results_2q_fock_n6_dim40_T20taus/run_2026-09-30_14-42-12"
v1_f10_t20 = ROOT / "results_2q_fock_n10_dim40_T20taus/run_2026-10-02_12-17-00"
v1_f10_t10 = ROOT / "results_both_fock_n10_dim40_T10taus/run_2026-10-02_16-53-17"
v1_cat_t15 = ROOT / "results_both_cat_2.00_dim40_T15taus/run_2026-10-03_15-06-31"

# Fock 6 e 10 a T=20 tau_s (2Q)
shutil.copy2(v1_f6_t20 / "nmean.pdf", OUT / "v1_fock6_t20_2q_nmean.pdf")
shutil.copy2(v1_f6_t20 / "wigner.png", OUT / "v1_fock6_t20_2q_wigner.png")
shutil.copy2(v1_f6_t20 / "drives_comparison.pdf", OUT / "v1_fock6_t20_2q_drives.pdf")
shutil.copy2(v1_f10_t20 / "nmean.pdf", OUT / "v1_fock10_t20_2q_nmean.pdf")
shutil.copy2(v1_f10_t20 / "wigner.png", OUT / "v1_fock10_t20_2q_wigner.png")

# Fock 10 a T=10 tau_s (1Q vs 2Q)
shutil.copy2(v1_f10_t10 / "comparison_nmean.pdf", OUT / "v1_fock10_t10_comparison_nmean.pdf")
shutil.copy2(v1_f10_t10 / "comparison_drives.pdf", OUT / "v1_fock10_t10_comparison_drives.pdf")
shutil.copy2(v1_f10_t10 / "1q/wigner.png", OUT / "v1_fock10_t10_1q_wigner.png")
shutil.copy2(v1_f10_t10 / "2q/wigner.png", OUT / "v1_fock10_t10_2q_wigner.png")

# Cat alpha=2.0 a T=15 tau_s (1Q vs 2Q)
shutil.copy2(v1_cat_t15 / "comparison_nmean.pdf", OUT / "v1_cat2_t15_comparison_nmean.pdf")
shutil.copy2(v1_cat_t15 / "comparison_drives.pdf", OUT / "v1_cat2_t15_comparison_drives.pdf")
shutil.copy2(v1_cat_t15 / "1q/wigner.png", OUT / "v1_cat2_t15_1q_wigner.png")
shutil.copy2(v1_cat_t15 / "2q/wigner.png", OUT / "v1_cat2_t15_2q_wigner.png")

# Copia figure native v2 (Wigner di main_009 e main_006)
run_m009 = CAMP / "runs/main_009_20261010T163427_063639Z"
shutil.copy2(run_m009 / "1q/seed_3/wigner.png", OUT / "main009_1q_seed3_wigner.png")
shutil.copy2(run_m009 / "2q_independent/seed_4/wigner.png", OUT / "main009_2q_ind_seed4_wigner.png")
shutil.copy2(run_m006 / "2q_independent/seed_2/wigner.png", OUT / "main006_2q_ind_seed2_wigner.png")
shutil.copy2(run_m006 / "1q/seed_3/wigner.png", OUT / "main006_1q_seed3_wigner.png")

# ---------------------------------------------------------
# FIGURA 5: Scaling del costo energetico C_2 / omega_c^2 (Eq. 4 paper):
#           Totale vs Singolo Canale a T = 20 tau_s (main_005, main_007, main_009)
# ---------------------------------------------------------
import json

runs_t20 = [
    ("main_005_20261006T123440_491824Z", "Fock $|2\\rangle$"),
    ("main_007_20261008T053403_792418Z", "Fock $|6\\rangle$"),
    ("main_009_20261010T163427_063639Z", "Fock $|10\\rangle$"),
]

fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.7), sharey=True)
x = np.arange(len(runs_t20))
width = 0.15

for panel_idx, (ax, metric_key, panel_title, y_lbl) in enumerate([
    (axes[0], "modulation_fluence_total",
     "(a) Costo totale del sistema: $C_{2,\\mathrm{tot}} / \\omega_c^2 = \\frac{1}{2}\\sum_j \\int_0^T \\Omega_{D,j}(t)^2 dt$",
     "Costo energetico $C_2 / \\omega_c^2$ (Eq. 4 paper)"),
    (axes[1], "modulation_fluence_max_channel",
     "(b) Costo massimo per singolo canale: $C_{2,\\mathrm{max\\,ch}} / \\omega_c^2 = \\frac{1}{2}\\max_j \\int_0^T \\Omega_{D,j}(t)^2 dt$",
     ""),
]):
    for idx, (case_key, case_label) in enumerate(CASES):
        meds, q25_err, q75_err = [], [], []
        for rname, _ in runs_t20:
            s = json.loads((CAMP / "runs" / rname / "summary.json").read_text())
            c_obj = next(c for c in s["cases"] if c["name"] == case_key)
            vals = np.array([0.5 * item["actuator"][metric_key] for item in c_obj["seeds"]])
            med = float(np.median(vals))
            q25 = float(np.quantile(vals, 0.25))
            q75 = float(np.quantile(vals, 0.75))
            meds.append(med)
            q25_err.append(med - q25)
            q75_err.append(q75 - med)

        pos = x + (idx - 2) * width
        bars = ax.bar(
            pos,
            meds,
            width=width * 0.92,
            color=COLORS[case_key],
            alpha=0.88,
            label=case_label.replace("\n", " "),
            edgecolor="black",
            linewidth=0.5,
        )
        ax.errorbar(
            pos,
            meds,
            yerr=[q25_err, q75_err],
            fmt="none",
            ecolor="black",
            elinewidth=1.0,
            capsize=2.5,
        )
        for b, med, up in zip(bars, meds, q75_err):
            ax.text(
                b.get_x() + b.get_width() / 2,
                med + up + 1.0,
                f"{med:.1f}",
                ha="center",
                va="bottom",
                fontsize=7.2,
                rotation=90 if med > 35 else 0,
            )

    ax.set_xticks(x)
    ax.set_xticklabels([r[1] for r in runs_t20])
    ax.set_title(panel_title, fontsize=10.0)
    ax.set_ylim(0, 72)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    if y_lbl:
        ax.set_ylabel(y_lbl)

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 0.99), frameon=False)
fig.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig(OUT / "fig5_scaling_costo_C2.pdf")
fig.savefig(OUT / "fig5_scaling_costo_C2.png")
plt.close(fig)

# ---------------------------------------------------------
# FIGURA 6: Anatomia del meccanismo a 2 qubit (scala di Dicke, singoletto dark e purezza)
#           su Fock |10>, T = 10 tau_s senza filtro (main_010)
# ---------------------------------------------------------
run_m010 = CAMP / "runs/main_010_20261013T052230_477141Z"
cfg_m010 = json.loads((run_m010 / "config.json").read_text())
idx_T_010 = cfg_m010["validation"]["trajectory_points"] - 1

d_1q = np.load(run_m010 / "1q/seed_0/arrays.npz", allow_pickle=False)
d_2qc = np.load(run_m010 / "2q_common/seed_7/arrays.npz", allow_pickle=False)
d_2qi = np.load(run_m010 / "2q_independent/seed_5/arrays.npz", allow_pickle=False)

t_tau = d_2qi["times"][:idx_T_010 + 1] / tau_s

fig, axes = plt.subplots(3, 1, figsize=(10.0, 7.4), sharex=True)

# Pannello 1: Singoletto dark vs Tripletto bright in 2q_independent vs 2q_common
qpop_2qc = d_2qc["qubit_basis_populations"][:idx_T_010 + 1]
qpop_2qi = d_2qi["qubit_basis_populations"][:idx_T_010 + 1]
sing_2qc = d_2qc["singlet_population"][:idx_T_010 + 1]
sing_2qi = d_2qi["singlet_population"][:idx_T_010 + 1]
bright_2qi = (qpop_2qi[:, 1] + qpop_2qi[:, 2]) - sing_2qi

axes[0].plot(t_tau, bright_2qi, color="#1f77b4", lw=1.7, label="2Q indep. (seed 5): tripletto simmetrico $P_{|B\\rangle}(t)$")
axes[0].plot(t_tau, sing_2qi, color="#2ca02c", lw=1.9, label="2Q indep. (seed 5): singoletto dark $P_{|D\\rangle}(t)$ (max $= 0.423$, finale $= 8\\times 10^{-6}$)")
axes[0].plot(t_tau, sing_2qc, color="#ff7f0e", lw=1.5, ls="--", label="2Q common (seed 7): singoletto dark $P_{|D\\rangle}(t) \\equiv 0$ (simmetria conservata)")
axes[0].set_ylabel("Popolazione 1-eccit.")
axes[0].set_title("Meccanismo interno 1Q vs 2Q su Fock $|n=10\\rangle$ a $T = 10\\,\\tau_s$ (main_010)")
axes[0].legend(loc="upper right", fontsize=8.3)
axes[0].grid(True, linestyle=":", alpha=0.6)
axes[0].set_ylim(-0.03, 0.72)

# Pannello 2: Popolazione doppiamente eccitata |e,e> (scala di Dicke)
axes[1].plot(t_tau, qpop_2qc[:, 3], color="#ff7f0e", lw=1.6, label="2Q common (seed 7): doppia eccitazione $P_{|e,e\\rangle}(t)$ (max $= 0.767$)")
axes[1].plot(t_tau, qpop_2qi[:, 3], color="#2ca02c", lw=1.8, label="2Q indep. (seed 5): doppia eccitazione $P_{|e,e\\rangle}(t)$ (max $= 0.566$)")
axes[1].plot(t_tau, d_1q["qubit_basis_populations"][:idx_T_010 + 1, 1], color="#7f7f7f", lw=1.3, ls=":", label="1Q (seed 0): singola eccitazione $P_{|e\\rangle}(t)$ (satura a 1 qubit)")
axes[1].set_ylabel("Popolazione $|e,e\\rangle$ / $|e\\rangle$")
axes[1].legend(loc="upper right", fontsize=8.3)
axes[1].grid(True, linestyle=":", alpha=0.6)
axes[1].set_ylim(-0.03, 0.90)

# Pannello 3: Purezza della cavità Tr(rho_cav^2) e soglia di Schmidt 1/2 vs 1/4
axes[2].plot(t_tau, d_1q["purity"][:idx_T_010 + 1], color="#1f77b4", lw=1.6, label="1Q (seed 0): $\\mathrm{Tr}[\\rho_{\\mathrm{cav}}^2] \\geq 0.50$ (rango Schmidt $\\leq 2$, finale $0.897$)")
axes[2].plot(t_tau, d_2qc["purity"][:idx_T_010 + 1], color="#ff7f0e", lw=1.6, label="2Q common (seed 7): $\\mathrm{Tr}[\\rho_{\\mathrm{cav}}^2] \\geq 0.339$ (rango $\\leq 3$, finale $0.9999$)")
axes[2].plot(t_tau, d_2qi["purity"][:idx_T_010 + 1], color="#2ca02c", lw=1.8, label="2Q indep. (seed 5): $\\mathrm{Tr}[\\rho_{\\mathrm{cav}}^2]$ scende a $0.277$ (rango $4$, finale $0.99995$)")
axes[2].axhline(0.50, color="#1f77b4", ls="--", lw=0.9, alpha=0.7, label="Limite inferiore purezza 1Q ($1/2 = 0.50$) e 2Q common ($1/3 \\approx 0.333$)")
axes[2].axhline(1.0 / 3.0, color="#ff7f0e", ls=":", lw=0.9, alpha=0.8)
axes[2].set_ylabel("Purezza cavità $\\mathrm{Tr}[\\rho_c^2]$")
axes[2].set_xlabel("Tempo normalizzato $t / \\tau_s$")
axes[2].legend(loc="lower left", fontsize=8.0)
axes[2].grid(True, linestyle=":", alpha=0.6)
axes[2].set_ylim(0.20, 1.05)

fig.tight_layout()
fig.savefig(OUT / "fig6_meccanismo_dicke_singoletto.pdf")
fig.savefig(OUT / "fig6_meccanismo_dicke_singoletto.png")
plt.close(fig)

# ---------------------------------------------------------
# FIGURA 7: Effetto del filtro causale (omega_cut = 3.0) su Fock |10>:
#           forma d'onda applicata e spettro di potenza cumulativo (CDF)
# ---------------------------------------------------------
from pathlib import Path as _P
import sys as _sys
if str(ROOT / "v2") not in _sys.path:
    _sys.path.insert(0, str(ROOT / "v2"))
from qoc.controls import Signal

run_m008 = CAMP / "runs/main_008_20261009T115245_877405Z"
run_m011 = CAMP / "runs/main_011_20261014T120443_697233Z"

d_m009 = np.load(run_m009 / "2q_independent/seed_4/arrays.npz", allow_pickle=False)
d_m011 = np.load(run_m011 / "2q_independent/seed_1/arrays.npz", allow_pickle=False)
d_m008 = np.load(run_m008 / "2q_independent/seed_6/arrays.npz", allow_pickle=False)
d_m010 = np.load(run_m010 / "2q_independent/seed_5/arrays.npz", allow_pickle=False)

T_20 = float(d_m009["command_times"][-1])
M_20 = len(d_m009["command_times"])
dense_t20 = np.linspace(0, T_20, 4001)

T_10 = float(d_m008["command_times"][-1])
M_10 = len(d_m008["command_times"])
dense_t10 = np.linspace(0, T_10, 4001)

deliv_009 = Signal(T_20, M_20, 3.0).values(d_m009["physical_command_modulation"], dense_t20)[0]
deliv_011 = Signal(T_20, M_20, None).values(d_m011["physical_command_modulation"], dense_t20)[0]
deliv_008 = Signal(T_10, M_10, 3.0).values(d_m008["physical_command_modulation"], dense_t10)[0]
deliv_010 = Signal(T_10, M_10, None).values(d_m010["physical_command_modulation"], dense_t10)[0]

fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.4))

# Pannello (a): Zoom forma d'onda su [0, 5 tau_s] a T=10 tau_s (main_008 vs main_010)
mask_t10 = (dense_t10 / tau_s) <= 5.0
axes[0].plot(dense_t10[mask_t10] / tau_s, deliv_010[mask_t10], color="#ff7f0e", lw=1.35, alpha=0.88,
             label="Senza filtro ($10\\tau_s$, main_010): $\\mathrm{SR}_{\\max}=4.77$, $P=0.99997$")
axes[0].plot(dense_t10[mask_t10] / tau_s, deliv_008[mask_t10], color="#1f77b4", lw=1.9,
             label="Con filtro $3\\omega_c$ ($10\\tau_s$, main_008): $\\mathrm{SR}_{\\max}=3.78$, $P=0.9618$")
axes[0].set_xlabel("Tempo normalizzato $t / \\tau_s$ (zoom su $[0, 5\\,\\tau_s]$)")
axes[0].set_ylabel("Modulazione applicata $\\Omega_{D,1}(t) / \\omega_c$")
axes[0].set_title("(a) Profilo temporale applicato su Q1 (Fock $|10\\rangle$, $T=10\\,\\tau_s$)")
axes[0].legend(loc="lower left", fontsize=8.1)
axes[0].grid(True, linestyle=":", alpha=0.6)
axes[0].set_ylim(-1.65, 1.25)

# Pannello (b): Frazione cumulativa della potenza AC (spiega direttamente omega_99%)
for delta, t_arr, col, ls_style, lbl in [
    (deliv_009, dense_t20, "#2ca02c", "-", "$20\\tau_s$ con filtro $3\\omega_c$ (main_009): $\\omega_{99\\%}=4.44\\,\\omega_c$ ($P=0.999995$)"),
    (deliv_011, dense_t20, "#2ca02c", "--", "$20\\tau_s$ senza filtro (main_011): $\\omega_{99\\%}=8.10\\,\\omega_c$ ($P=0.999974$)"),
    (deliv_008, dense_t10, "#1f77b4", "-", "$10\\tau_s$ con filtro $3\\omega_c$ (main_008): $\\omega_{99\\%}=5.52\\,\\omega_c$ ($P=0.9618$)"),
    (deliv_010, dense_t10, "#ff7f0e", "--", "$10\\tau_s$ senza filtro (main_010): $\\omega_{99\\%}=8.04\\,\\omega_c$ ($P=0.999970$)"),
]:
    ac = delta[:-1] - np.mean(delta[:-1])
    omega = 2 * np.pi * np.fft.rfftfreq(len(ac), t_arr[1] - t_arr[0])
    power = np.abs(np.fft.rfft(ac)) ** 2
    if len(power) > 2:
        power[1:-1] *= 2
    cdf = np.cumsum(power) / power.sum()
    axes[1].plot(omega, cdf, color=col, ls=ls_style, lw=1.8, label=lbl)

axes[1].axhline(0.99, color="crimson", ls=":", lw=1.1, label="Soglia banda $\\omega_{99\\%}$ ($99\\%$ potenza AC)")
axes[1].axvline(2.0, color="gray", ls="--", lw=1.0, label="Risonanza DCE $2\\omega_c$ e polo $\\omega_{\\mathrm{cut}}=3\\omega_c$")
axes[1].axvline(3.0, color="black", ls=":", lw=1.1)
axes[1].set_xlim(0, 9.5)
axes[1].set_ylim(0.0, 1.04)
axes[1].set_xlabel("Frequenza angolare $\\omega / \\omega_c$")
axes[1].set_ylabel("Frazione cumulativa di potenza AC $\\int_0^\\omega S(\\omega')d\\omega' / P_{\\mathrm{AC}}$")
axes[1].set_title("(b) Distribuzione spettrale cumulativa e banda $\\omega_{99\\%}$ (2Q indep.)")
axes[1].legend(loc="lower right", fontsize=7.6)
axes[1].grid(True, linestyle=":", alpha=0.6)

fig.tight_layout()
fig.savefig(OUT / "fig7_spettro_filtro_main009_vs_011.pdf")
fig.savefig(OUT / "fig7_spettro_filtro_main009_vs_011.png")
plt.close(fig)

print("Tutte le figure (v1 e v2) sono state generate/copiate con successo in:", OUT)
