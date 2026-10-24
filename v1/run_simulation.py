"""
run_simulation.py
=================
File di configurazione ed esecuzione unificato per la full pipeline di controllo
quantistico ottimo (CRAB multi-seed -> GRAPE refinement -> PCHIP smoothing).

Permette di eseguire simulazioni per il sistema a 1 QUBIT, 2 QUBIT o ENTRAMBI (both),
senza dover modificare gli script originali.

ORGANIZZAZIONE CARTELLE E REPORT:
---------------------------------
I risultati vengono organizzati gerarchicamente:
    results_{sistema}_{target}_{param}_dim{dim}_{durataT}/
        run_YYYY-MM-DD_HH-MM-SS/
            ├── report.html            (Report completo interattivo con tutti i grafici e tabelle)
            ├── report.md              (Report Markdown analitico)
            ├── results.npz            (Dati grezzi NumPy per analisi numeriche)
            ├── nmean.png / .pdf       (Evoluzione numero medio di fotoni)
            ├── drives_comparison.png  (Forme d'onda dei controlli CRAB vs Lisciati)
            ├── wigner.png / .pdf      (Funzioni di Wigner target e finale)
            └── fft.png / .pdf         (Spettro di Fourier con frequenze di taglio)

In modalità "both", viene generata anche una cartella di run contenente i sottoprogetti 1q/ e 2q/
insieme a un report comparativo side-by-side (`comparison_report.html`).

ISTRUZIONI D'USO:
-----------------
1. Modifica i parametri nella sezione "CONFIGURAZIONE PARAMETRI" qui sotto.
2. Esegui dal terminale:
       python run_simulation.py
   (oppure con l'interprete dell'ambiente virtuale: .venv/bin/python run_simulation.py)

In alternativa, puoi sovrascrivere i parametri da riga di comando:
       python run_simulation.py --system 2q --target fock --param 6 --dim 30
       python run_simulation.py --help
"""

import sys
import os
import time
import argparse
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from qutip import (
    destroy, basis, expect, ptrace, fidelity, wigner, ket2dm, Qobj
)

# ── Assicura che la directory del progetto sia nel path di sistema ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from one_qubit_system import (
    build_one_qubit_system,
    target_fock_1q,
    target_squeezed_1q,
    target_cat_1q,
    grape_target_fock_1q,
    grape_target_squeezed_1q,
    grape_target_cat_1q,
    make_crab_cost_cavity as make_crab_cost_1q,
    compute_control_cost as compute_control_cost_1q,
    db_to_r,
)

from two_qubit_system import (
    build_two_qubit_system,
    target_fock_2q,
    target_squeezed_2q,
    target_cat_2q,
    grape_target_fock_2q,
    grape_target_squeezed_2q,
    grape_target_cat_2q,
    make_crab_cost_cavity as make_crab_cost_2q,
    compute_control_cost as compute_control_cost_2q,
)

from crab_optimizer import CRABOptimizer
from grape_optimizer import GRAPEOptimizer


# ==============================================================================
# CONFIGURAZIONE PARAMETRI (MODIFICA QUI I TUOI VALORI)
# ==============================================================================

# 1. SELEZIONE DEL SISTEMA FISICO
# ------------------------------------------------------------------------------
# "2q"   : cavità + 2 qubit di controllo indipendenti
# "1q"   : cavità + 1 singolo qubit di controllo
# "both" : esegue 1Q e poi 2Q con gli stessi parametri e mostra un confronto diretto
SYSTEM_TYPE = "both"

# 2. STATO TARGET (TIPO ED ENERGIA)
# ------------------------------------------------------------------------------
# Tipo di stato quantistico target per la cavità:
#   "fock"     -> Stato di Fock |n⟩ (numero fotoni definito)
#   "squeezed" -> Stato di vuoto compresso / squeezed S(r, θ)|0⟩
#   "cat"      -> Stato gatto di Schrödinger (superposizione C+_α - C+_iα)
TARGET_TYPE = "cat"

# Parametro caratteristico (associato all'energia media dei fotoni nella cavità):
#   - Se TARGET_TYPE = "fock"     : n (numero intero di fotoni, es. 6 o 10; E = n * ħω_c)
#   - Se TARGET_TYPE = "squeezed" : r (parametro di squeezing, es. 0.8; <n>=sinh²(r))
#   - Se TARGET_TYPE = "cat"      : alpha (ampiezza coerente α, es. 2.0; <n>≈|α|²)
TARGET_PARAM = 2.0

# Parametri opzionali dello stato target:
TARGET_THETA = 0.0          # Angolo di fase dello squeezing (usato solo se squeezed)
TARGET_R_IN_DB = False      # Se True e squeezed, interpreta TARGET_PARAM come dB invece di r lineare

# 3. DIMENSIONE DELLO SPAZIO DI HILBERT
# ------------------------------------------------------------------------------
# Troncamento dello spazio di Fock della cavità (numero di livelli fotonici).
# Regola empirica: dim >= <n> + 15  (es. dim=30 per n=6; dim=40 per n=10 o α=2.0).
DIM = 40

# 4. DURATA TOTALE DELL'EVOLUZIONE (T)
# ------------------------------------------------------------------------------
# Può essere espressa come multiplo del tempo tipico di Rabi τ_s = π / (2*g):
T_FACTOR_TAUS = 15.0        # T = 20 * τ_s (benchmark tipico del paper)
# Oppure, se vuoi fissare direttamente il valore numerico di T in unità 1/ω_c:
T_FIXED = None              # Es: 104.72 oppure None per usare (T_FACTOR_TAUS * τ_s)

# 5. ITERAZIONI DI CRAB E GRAPE
# ------------------------------------------------------------------------------
# CRAB (ricerca globale con Nelder-Mead):
CRAB_NUM_SEEDS = 8         # Numero di seed indipendenti eseguiti in parallelo
CRAB_MAX_ITER = None        # Massimo numero di iterazioni Nelder-Mead (None = default auto)
CRAB_METHOD = "Nelder-Mead"

# GRAPE (raffinamento locale con L-BFGS-B con vincoli di ampiezza):
GRAPE_MAX_ITER = 150        # Massimo numero di iterazioni L-BFGS-B

# 6. FREQUENZE E TRONCAMENTI DI CRAB E GRAPE
# ------------------------------------------------------------------------------
# --- CRAB: Troncamento spettrale su base di Fourier randomizzata ---
CRAB_NUM_FREQS = 20         # Numero di frequenze/armoniche nella base troncata (N_f)
CRAB_FREQ_MIN = 0.0         # Frequenza minima di campionamento (unità ω_c)
CRAB_FREQ_MAX = 3.0         # Frequenza di taglio superiore per CRAB (es. 3.0 * ω_c)
CRAB_NT = 400               # Numero di punti temporali della griglia di CRAB

# --- GRAPE: Discretizzazione temporale e banda di Nyquist ---
GRAPE_NT = 150              # Numero di time slots di GRAPE.
                            # Determina il campionamento dt = T/(Nt-1) e la frequenza
                            # di taglio di Nyquist: ω_Nyq = π/dt = π*(Nt-1)/T
GRAPE_AMP_BOUND = (0.5, 3.0)# Limiti fisici inferiore e superiore per il drive |Ω_D(t)/ω_c|

# --- FASE 3: Interpolazione e smoothing finale ---
INTERP_NT = 600             # Numero di punti temporali per l'interpolazione lisciata PCHIP

# 7. PARAMETRI FISICI DEL SISTEMA
# ------------------------------------------------------------------------------
OMEGA_C = 1.0               # Frequenza naturale della cavità (unità di energia)
G1 = 0.3                    # Accoppiamento qubit 1 (regime USC: g/ω_c = 0.3)
G2 = 0.3                    # Accoppiamento qubit 2 (solo per sistema a 2 qubit)
OMEGA_BASE_1 = 2.0          # Ampiezza costante di base per il drive 1
OMEGA_BASE_2 = 2.0          # Ampiezza costante di base per il drive 2

# 8. CARTELLA BASE DI SALVATAGGIO DEI RISULTATI
# ------------------------------------------------------------------------------
# Se None, viene generata automaticamente con la struttura:
#   results_{system}_{target}_{param}_dim{dim}_{durataT}/run_YYYY-MM-DD_HH-MM-SS/
BASE_OUTPUT_DIR = None

# ==============================================================================
# FINE SEZIONE CONFIGURAZIONE — I dettagli implementativi seguono sotto
# ==============================================================================


# ── Stile grafici Matplotlib ──
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 13,
})


def _build_target_states(system_type: str, dim: int, target_type: str, target_param: float, theta: float = 0.0):
    """
    Costruisce lo stato target della cavità (ket ridotto) e l'operatore target per GRAPE (spazio intero).
    Ritorna: (target_cav_ket, target_dm, target_label, expected_n)
    """
    target_type = target_type.lower()
    a_op = destroy(dim)
    n_op = a_op.dag() * a_op

    if target_type == "fock":
        n = int(target_param)
        if system_type == "1q":
            target_cav = target_fock_1q(dim, n, trace_over_qubit=True)
            target_dm = grape_target_fock_1q(dim, n, ground_qubit=False)
        else:
            target_cav = target_fock_2q(dim, n, trace_over_qubits=True)
            target_dm = grape_target_fock_2q(dim, n, ground_qubits=False)
        label = f"Fock |n={n}⟩"
        expected_n = float(n)

    elif target_type == "squeezed":
        r = float(target_param)
        if system_type == "1q":
            target_cav = target_squeezed_1q(dim, r, theta=theta, trace_over_qubit=True)
            target_dm = grape_target_squeezed_1q(dim, r, theta=theta, ground_qubit=False)
        else:
            target_cav = target_squeezed_2q(dim, r, theta=theta, trace_over_qubits=True)
            target_dm = grape_target_squeezed_2q(dim, r, theta=theta, ground_qubits=False)
        label = f"Squeezed(r={r:.2f}, θ={theta:.2f})"
        expected_n = float(expect(n_op, target_cav))

    elif target_type == "cat":
        alpha = float(target_param)
        if system_type == "1q":
            target_cav = target_cat_1q(dim, alpha, trace_over_qubit=True)
            target_dm = grape_target_cat_1q(dim, alpha, ground_qubit=False)
        else:
            target_cav = target_cat_2q(dim, alpha, trace_over_qubits=True)
            target_dm = grape_target_cat_2q(dim, alpha, ground_qubits=False)
        label = f"Cat(α={alpha:.2f})"
        expected_n = float(expect(n_op, target_cav))

    else:
        raise ValueError(f"Tipo di stato target sconosciuto: {target_type}. Scegli tra 'fock', 'squeezed', 'cat'.")

    return target_cav, target_dm, label, expected_n


def _compute_actuator_metrics(pulses: list, dt: float) -> list:
    """
    Calcola le metriche quantitative di fattibilità fisica dell'attuatore (dal WIP):
      - Slew Rate Massimo: max |dΩ/dt|
      - Slew Rate RMS: sqrt(mean((dΩ/dt)^2))
      - Costo energetico canale: integral(Ω^2 dt)
      - Banda passante al 99% della potenza spettrale (omega_99%)
    """
    metrics = []
    for p in pulses:
        deriv = np.diff(p) / dt
        sr_max = float(np.max(np.abs(deriv)))
        sr_rms = float(np.sqrt(np.mean(deriv ** 2)))
        c2_ch = float(np.sum(p ** 2) * dt)

        # Spettro FFT e potenza
        p_centered = p - np.mean(p)
        fft_v = np.fft.fft(p_centered)
        freqs = np.fft.fftfreq(len(p_centered), d=dt)
        mask = freqs >= 0
        freqs_pos = freqs[mask] * (2.0 * np.pi)
        power = np.abs(fft_v[mask]) ** 2
        total_p = np.sum(power)
        if total_p > 1e-12:
            cum_p = np.cumsum(power) / total_p
            idx_99 = np.searchsorted(cum_p, 0.99)
            omega_99 = float(freqs_pos[min(idx_99, len(freqs_pos) - 1)])
        else:
            omega_99 = 0.0

        metrics.append({
            "sr_max": sr_max,
            "sr_rms": sr_rms,
            "cost_channel": c2_ch,
            "omega_99": omega_99,
        })
    return metrics


# ==============================================================================
# Worker Multiprocessing per CRAB (Top-level per compatibilità Windows/macOS/Linux)
# ==============================================================================
def _crab_worker_task(args):
    """
    Funzione worker eseguita nei processi paralleli per il campionamento multi-seed di CRAB.
    """
    (seed, system_type, dim, omega_c, g1, g2, target_type, target_param, theta,
     T, Nt, num_freqs, freq_range, omega_bases, max_iter, method) = args

    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)

    t0 = time.time()

    if system_type == "1q":
        sys_obj = build_one_qubit_system(dim=dim, omega_c=omega_c, g=g1)
        cost_maker = make_crab_cost_1q
        cost_calc = compute_control_cost_1q
    else:
        sys_obj = build_two_qubit_system(dim=dim, omega_c=omega_c, g1=g1, g2=g2)
        cost_maker = make_crab_cost_2q
        cost_calc = compute_control_cost_2q

    target_cav, _, _, _ = _build_target_states(system_type, dim, target_type, target_param, theta)
    cost_fn = cost_maker(target_cav)

    opt = CRABOptimizer(
        H_drift=sys_obj.H0,
        H_controls=sys_obj.H_controls,
        T=T,
        num_tslots=Nt,
        num_freqs=num_freqs,
        omega_bases=omega_bases,
        freq_range=freq_range,
        basis_type="uniform",
        seed=seed,
    )

    res = opt.optimize(
        psi0=sys_obj.psi0_ket,
        cost_function=cost_fn,
        max_iter=max_iter,
        method=method,
    )

    rho_cav = ptrace(res.final_state, 0)
    F = float(fidelity(target_cav, rho_cav))
    dt_crab = T / (Nt - 1)
    C2 = float(cost_calc(res.control_pulses, dt_crab))
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


# ==============================================================================
# Generazione Report HTML e Markdown
# ==============================================================================
def _write_single_system_reports(out_dir: str, data: dict):
    """
    Scrive sia il report HTML (con immagini integrate e styling moderno)
    sia il report Markdown riassuntivo per facilitare l'analisi immediata.
    """
    sys_type = data["system_type"].upper()
    target_lbl = data["target_label"]
    f_smooth = data["fidelity_smooth"]
    f_grape = data["fidelity_grape"]
    f_crab = data["fidelity_crab"]
    c2 = data["cost_smooth"]
    t_tot = data["elapsed_total"]
    act_metrics = data["actuator_metrics"]

    # 1. Report Markdown (report.md)
    md_content = f"""# Report Simulazione Quantum Optimal Control — {sys_type}

**Data e Ora Esecuzione:** {data['run_datetime']}  
**Cartella:** `{os.path.basename(out_dir)}`  

## 1. Risultati Chiave
| Fase | Fedeltà ($\\mathcal{{F}}$) | Costo Energetico ($C^2$) | Tempo Esecuzione | Iterazioni / Note |
| :--- | :---: | :---: | :---: | :--- |
| **CRAB (Miglior Seed #{data['best_crab_seed']})** | `{f_crab:.6f}` | `{data['cost_crab']:.2f}` | `{data['elapsed_crab']:.1f}s` | Media {data['crab_mean_f']:.4f} ± {data['crab_std_f']:.4f} |
| **GRAPE (L-BFGS-B)** | `{f_grape:.6f}` | `{data['cost_grape']:.2f}` | `{data['elapsed_grape']:.1f}s` | {data['grape_iterations']} iterazioni |
| **PCHIP Smoothed (Finale)** | **`{f_smooth:.6f}`** | **`{c2:.2f}`** | `{data['elapsed_smooth']:.1f}s` | Interpolazione fine ({data['interp_nt']} pts) |

## 2. Metriche Fisiche dell'Attuatore
| Canale | Slew Rate Max $\\max|d\\Omega/dt|$ | Slew Rate RMS | Costo Canale $C_k^2$ | Banda 99% $\\omega_{{99\\%}}$ |
| :--- | :---: | :---: | :---: | :---: |
"""
    for i, m in enumerate(act_metrics):
        md_content += f"| Qubit {i+1} | `{m['sr_max']:.3f}` | `{m['sr_rms']:.3f}` | `{m['cost_channel']:.2f}` | `{m['omega_99']:.2f}` $\\omega_c$ |\n"

    md_content += f"""
## 3. Parametri di Configurazione
- **Stato Target:** {target_lbl} (Fotoni attesi $\\langle n \\rangle = {data['expected_n']:.2f}$)
- **Dimensione Spazio Fock:** {data['dim']} (Dimensione totale: {data['total_hilbert_dim']})
- **Durata Evoluzione $T$:** {data['T']:.3f} ($T/\\tau_s = {data['T_factor_taus']:.2f}$, $\\tau_s = {data['tau_s']:.3f}$)
- **CRAB:** {data['crab_seeds']} seeds paralleli, {data['crab_freqs']} armoniche, taglio $\\omega \\in [0, {data['crab_freq_max']:.1f}\\omega_c]$, $N_t = {data['crab_nt']}$
- **GRAPE:** $N_t = {data['grape_nt']}$ time slots (taglio Nyquist $\\omega_{{\\text{{Nyq}}}} = {data['omega_nyquist']:.2f}\\omega_c$), bound ampiezza {data['grape_amp_bound']}
- **Tempo totale simulazione:** {t_tot:.1f}s ({t_tot / 60.0:.2f} min)

## 4. Grafici Analitici Generati
1. **Numero medio di fotoni:** [nmean.pdf](nmean.pdf)  
   ![Numero medio fotoni](nmean.png)

2. **Confronto Forme d'Onda di Controllo:** [drives_comparison.pdf](drives_comparison.pdf)  
   ![Controlli](drives_comparison.png)

3. **Funzioni di Wigner (Target vs Finale):** [wigner.pdf](wigner.pdf)  
   ![Wigner](wigner.png)

4. **Spettro di Fourier (FFT):** [fft.pdf](fft.pdf)  
   ![FFT](fft.png)
"""
    with open(os.path.join(out_dir, "report.md"), "w", encoding="utf-8") as f:
        f.write(md_content)

    # 2. Report HTML Interattivo e Autocontenuto (report.html)
    badge_color = "#10b981" if f_smooth >= 0.95 else ("#f59e0b" if f_smooth >= 0.85 else "#ef4444")
    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Report Simulazione {sys_type} — {target_lbl}</title>
<style>
  :root {{
    --bg: #0f172a;
    --card-bg: #1e293b;
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --border: #334155;
    --success: #10b981;
    --warning: #f59e0b;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 30px 20px;
    line-height: 1.6;
  }}
  .container {{
    max-width: 1200px;
    margin: 0 auto;
  }}
  header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 20px;
    margin-bottom: 30px;
  }}
  h1 {{ margin: 0; font-size: 1.8rem; color: #fff; }}
  .tag {{
    display: inline-block;
    padding: 6px 14px;
    border-radius: 9999px;
    font-weight: 600;
    font-size: 0.9rem;
    background-color: {badge_color}22;
    color: {badge_color};
    border: 1px solid {badge_color}44;
  }}
  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
  }}
  .card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
  }}
  .card-label {{ font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }}
  .card-val {{ font-size: 1.8rem; font-weight: 700; margin-top: 6px; color: #fff; }}
  .card-sub {{ font-size: 0.85rem; color: var(--accent); margin-top: 4px; }}
  
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
  }}
  th, td {{
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid var(--border);
  }}
  th {{
    background-color: rgba(255, 255, 255, 0.03);
    color: var(--text-muted);
    font-size: 0.85rem;
    text-transform: uppercase;
  }}
  tr:hover {{ background-color: rgba(255, 255, 255, 0.02); }}
  
  .section-title {{
    font-size: 1.3rem;
    font-weight: 600;
    margin-top: 40px;
    margin-bottom: 15px;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .plots-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(540px, 1fr));
    gap: 25px;
    margin-top: 20px;
  }}
  .plot-card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
  }}
  .plot-header {{
    padding: 14px 18px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .plot-title {{ font-weight: 600; font-size: 1rem; color: #fff; }}
  .plot-link {{
    font-size: 0.8rem;
    color: var(--accent);
    text-decoration: none;
    border: 1px solid var(--accent);
    padding: 3px 8px;
    border-radius: 6px;
  }}
  .plot-link:hover {{ background-color: var(--accent); color: var(--bg); }}
  .plot-card img {{
    width: 100%;
    display: block;
    background-color: #fff;
  }}
  footer {{
    margin-top: 50px;
    border-top: 1px solid var(--border);
    padding-top: 20px;
    text-align: center;
    color: var(--text-muted);
    font-size: 0.85rem;
  }}
</style>
</head>
<body>
<div class="container">

  <header>
    <div>
      <h1>Quantum Optimal Control — Sistema {sys_type}</h1>
      <div style="color: var(--text-muted); font-size: 0.9rem; margin-top: 4px;">
        Target: <strong style="color: #fff;">{target_lbl}</strong> | Eseguito il: {data['run_datetime']}
      </div>
    </div>
    <div>
      <span class="tag">Fedeltà Finale: {f_smooth:.4f}</span>
    </div>
  </header>

  <div class="cards-grid">
    <div class="card">
      <div class="card-label">Fedeltà Finale (Smooth)</div>
      <div class="card-val" style="color: {badge_color};">{f_smooth:.6f}</div>
      <div class="card-sub">CRAB: {f_crab:.4f} &rarr; GRAPE: {f_grape:.4f}</div>
    </div>
    <div class="card">
      <div class="card-label">Costo Energetico Integrato (C²)</div>
      <div class="card-val">{c2:.2f}</div>
      <div class="card-sub">&int; ||&Omega;<sub>D</sub>(t)||² dt</div>
    </div>
    <div class="card">
      <div class="card-label">Durata Evoluzione (T)</div>
      <div class="card-val">{data['T']:.2f} <span style="font-size: 1rem; color: var(--text-muted);">1/&omega;<sub>c</sub></span></div>
      <div class="card-sub">{data['T_factor_taus']:.1f} &times; &tau;<sub>s</sub> (&tau;<sub>s</sub>={data['tau_s']:.2f})</div>
    </div>
    <div class="card">
      <div class="card-label">Tempo di Calcolo</div>
      <div class="card-val">{t_tot:.1f}s</div>
      <div class="card-sub">{t_tot / 60.0:.2f} minuti totali</div>
    </div>
  </div>

  <div class="section-title">📊 Risultati e Fasi di Ottimizzazione</div>
  <div class="card" style="padding: 0; overflow-x: auto;">
    <table>
      <thead>
        <tr>
          <th>Fase</th>
          <th>Fedeltà (&Fscr;)</th>
          <th>Costo C²</th>
          <th>Tempo (s)</th>
          <th>Dettagli / Convergenza</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>CRAB (Miglior Seed #{data['best_crab_seed']})</strong></td>
          <td><code>{f_crab:.6f}</code></td>
          <td><code>{data['cost_crab']:.2f}</code></td>
          <td>{data['elapsed_crab']:.1f}s</td>
          <td>Media {data['crab_mean_f']:.4f} &plusmn; {data['crab_std_f']:.4f} su {data['crab_seeds']} seeds</td>
        </tr>
        <tr>
          <td><strong>GRAPE (L-BFGS-B)</strong></td>
          <td><code>{f_grape:.6f}</code></td>
          <td><code>{data['cost_grape']:.2f}</code></td>
          <td>{data['elapsed_grape']:.1f}s</td>
          <td>{data['grape_iterations']} iterazioni (bound {data['grape_amp_bound']})</td>
        </tr>
        <tr>
          <td><strong>PCHIP Smoothed (Finale)</strong></td>
          <td><strong style="color: {badge_color}; font-size: 1.05rem;">{f_smooth:.6f}</strong></td>
          <td><strong>{c2:.2f}</strong></td>
          <td>{data['elapsed_smooth']:.1f}s</td>
          <td>Interpolazione cubica lisciata ({data['interp_nt']} time slots)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section-title">⚡ Metriche Fisiche dell'Attuatore (AWG / Elettronica di Controllo)</div>
  <div class="card" style="padding: 0; overflow-x: auto;">
    <table>
      <thead>
        <tr>
          <th>Canale</th>
          <th>Slew Rate Max (max |d&Omega;/dt|)</th>
          <th>Slew Rate RMS</th>
          <th>Costo Canale C<sub>k</sub>²</th>
          <th>Banda Passante al 99% (&omega;<sub>99%</sub>)</th>
        </tr>
      </thead>
      <tbody>
"""
    for i, m in enumerate(act_metrics):
        html_content += f"""        <tr>
          <td><strong>Qubit {i+1}</strong></td>
          <td><code>{m['sr_max']:.3f}</code></td>
          <td><code>{m['sr_rms']:.3f}</code></td>
          <td><code>{m['cost_channel']:.2f}</code></td>
          <td><code>{m['omega_99']:.2f} &omega;<sub>c</sub></code></td>
        </tr>
"""
    html_content += f"""      </tbody>
    </table>
  </div>

  <div class="section-title">⚙️ Parametri Completi della Simulazione</div>
  <div class="card">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; font-size: 0.95rem;">
      <div>&bull; <strong>Stato Target:</strong> {target_lbl}</div>
      <div>&bull; <strong>Dimensione Fock Cavità:</strong> {data['dim']}</div>
      <div>&bull; <strong>Dimensione Spazio Totale:</strong> {data['total_hilbert_dim']}</div>
      <div>&bull; <strong>Accoppiamento g<sub>1</sub>:</strong> {data['g1']} &omega;<sub>c</sub></div>
      <div>&bull; <strong>Accoppiamento g<sub>2</sub>:</strong> {data['g2']} &omega;<sub>c</sub></div>
      <div>&bull; <strong>Armoniche CRAB (N<sub>f</sub>):</strong> {data['crab_freqs']}</div>
      <div>&bull; <strong>Banda CRAB:</strong> [0, {data['crab_freq_max']:.1f}] &omega;<sub>c</sub></div>
      <div>&bull; <strong>Time Slots GRAPE:</strong> {data['grape_nt']} (&omega;<sub>Nyq</sub> = {data['omega_nyquist']:.2f} &omega;<sub>c</sub>)</div>
      <div>&bull; <strong>Vincoli Ampiezza GRAPE:</strong> {data['grape_amp_bound']}</div>
      <div>&bull; <strong>Punti Interpolazione Fine:</strong> {data['interp_nt']}</div>
    </div>
  </div>

  <div class="section-title">📈 Grafici di Analisi</div>
  <div class="plots-grid">
    <div class="plot-card">
      <div class="plot-header">
        <span class="plot-title">Numero Medio di Fotoni &lang;n&rang;(t)</span>
        <a class="plot-link" href="nmean.pdf" target="_blank">PDF Vettoriale</a>
      </div>
      <img src="nmean.png" alt="Numero medio fotoni">
    </div>

    <div class="plot-card">
      <div class="plot-header">
        <span class="plot-title">Forme d'Onda di Controllo &Omega;<sub>D</sub>(t)</span>
        <a class="plot-link" href="drives_comparison.pdf" target="_blank">PDF Vettoriale</a>
      </div>
      <img src="drives_comparison.png" alt="Forme d'onda controlli">
    </div>

    <div class="plot-card">
      <div class="plot-header">
        <span class="plot-title">Funzioni di Wigner (Target vs Ottimizzato)</span>
        <a class="plot-link" href="wigner.pdf" target="_blank">PDF Vettoriale</a>
      </div>
      <img src="wigner.png" alt="Funzioni di Wigner">
    </div>

    <div class="plot-card">
      <div class="plot-header">
        <span class="plot-title">Spettro di Fourier (FFT)</span>
        <a class="plot-link" href="fft.pdf" target="_blank">PDF Vettoriale</a>
      </div>
      <img src="fft.png" alt="Spettro FFT">
    </div>
  </div>

  <footer>
    Report generato automaticamente da <code>run_simulation.py</code> | Stage Quantum Optimal Control
  </footer>

</div>
</body>
</html>
"""
    with open(os.path.join(out_dir, "report.html"), "w", encoding="utf-8") as f:
        f.write(html_content)


def _write_comparison_reports(comp_dir: str, res_1q: dict, res_2q: dict, cfg: dict):
    """
    Genera un report HTML e Markdown di confronto diretto (1Q vs 2Q)
    salvato nella cartella principale della run in modalità 'both'.
    """
    f1 = res_1q["fidelity_smooth"]
    f2 = res_2q["fidelity_smooth"]
    c1 = res_1q["cost_smooth"]
    c2 = res_2q["cost_smooth"]

    sr_max_1 = res_1q["actuator_metrics"][0]["sr_max"]
    sr_max_2_1 = res_2q["actuator_metrics"][0]["sr_max"]
    sr_max_2_2 = res_2q["actuator_metrics"][1]["sr_max"]
    sr_max_2 = max(sr_max_2_1, sr_max_2_2)

    w99_1 = res_1q["actuator_metrics"][0]["omega_99"]
    w99_2_1 = res_2q["actuator_metrics"][0]["omega_99"]
    w99_2_2 = res_2q["actuator_metrics"][1]["omega_99"]
    w99_2 = max(w99_2_1, w99_2_2)

    sr_gain = ((sr_max_2 - sr_max_1) / sr_max_1) * 100.0
    w_gain = ((w99_2 - w99_1) / w99_1) * 100.0

    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Confronto Diretto: 1 Qubit vs 2 Qubit</title>
<style>
  :root {{
    --bg: #0f172a;
    --card-bg: #1e293b;
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --border: #334155;
    --success: #10b981;
    --warning: #f59e0b;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 30px 20px;
    line-height: 1.6;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; }}
  header {{
    border-bottom: 1px solid var(--border);
    padding-bottom: 20px;
    margin-bottom: 30px;
  }}
  h1 {{ margin: 0; font-size: 1.9rem; color: #fff; }}
  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
  }}
  .card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
  }}
  .card-label {{ font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; }}
  .card-val {{ font-size: 1.8rem; font-weight: 700; margin-top: 6px; color: #fff; }}
  .card-sub {{ font-size: 0.85rem; color: var(--accent); margin-top: 4px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
  th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); }}
  th {{ background-color: rgba(255, 255, 255, 0.03); color: var(--text-muted); font-size: 0.85rem; }}
  tr:hover {{ background-color: rgba(255, 255, 255, 0.02); }}
  .section-title {{ font-size: 1.3rem; font-weight: 600; margin-top: 40px; margin-bottom: 15px; color: var(--accent); }}
  .plots-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(540px, 1fr)); gap: 25px; }}
  .plot-card {{ background-color: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
  .plot-header {{ padding: 14px 18px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; }}
  .plot-link {{ color: var(--accent); text-decoration: none; border: 1px solid var(--accent); padding: 3px 8px; border-radius: 6px; font-size: 0.8rem; }}
  .plot-card img {{ width: 100%; display: block; background: #fff; }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>Confronto Diretto: 1 Qubit vs 2 Qubit</h1>
    <div style="color: var(--text-muted); font-size: 0.95rem; margin-top: 6px;">
      Stato Target: <strong style="color: #fff;">{res_1q['target_label']}</strong> | Durata T = {res_1q['T']:.2f} ({res_1q['T_factor_taus']:.1f} &tau;<sub>s</sub>) | Eseguito il: {res_1q['run_datetime']}
    </div>
  </header>

  <div class="cards-grid">
    <div class="card">
      <div class="card-label">Fedeltà Finale 1Q vs 2Q</div>
      <div class="card-val">{f1:.4f} <span style="font-size: 1.2rem; color: var(--text-muted);">&rarr;</span> <span style="color: var(--success);">{f2:.4f}</span></div>
      <div class="card-sub">{'+' if f2 >= f1 else ''}{((f2 - f1)/f1)*100.0:.2f}% variazione</div>
    </div>
    <div class="card">
      <div class="card-label">Costo Energetico Totale (C²)</div>
      <div class="card-val">{c1:.1f} <span style="font-size: 1.2rem; color: var(--text-muted);">&rarr;</span> {c2:.1f}</div>
      <div class="card-sub">Distribuito su {2 if res_2q['actuator_metrics'] else 1} canali</div>
    </div>
    <div class="card">
      <div class="card-label">Slew Rate Massimo (d&Omega;/dt)</div>
      <div class="card-val">{sr_max_1:.2f} <span style="font-size: 1.2rem; color: var(--text-muted);">&rarr;</span> {sr_max_2:.2f}</div>
      <div class="card-sub" style="color: {'var(--success)' if sr_gain < 0 else 'var(--warning)'};">{sr_gain:+.1f}% variazione attuatore</div>
    </div>
    <div class="card">
      <div class="card-label">Banda Spettrale 99% (&omega;<sub>99%</sub>)</div>
      <div class="card-val">{w99_1:.2f} <span style="font-size: 1.2rem; color: var(--text-muted);">&rarr;</span> {w99_2:.2f} <span style="font-size: 0.9rem;">&omega;<sub>c</sub></span></div>
      <div class="card-sub" style="color: {'var(--success)' if w_gain < 0 else 'var(--warning)'};">{w_gain:+.1f}% larghezza di banda</div>
    </div>
  </div>

  <div class="section-title">📊 Tabella di Confronto Benchmark</div>
  <div class="card" style="padding: 0; overflow-x: auto;">
    <table>
      <thead>
        <tr>
          <th>Metrica</th>
          <th>1 Qubit</th>
          <th>2 Qubit</th>
          <th>Variazione / Rapporto</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Fedeltà CRAB (Best Seed)</strong></td>
          <td><code>{res_1q['fidelity_crab']:.6f}</code></td>
          <td><code>{res_2q['fidelity_crab']:.6f}</code></td>
          <td><code>{res_2q['fidelity_crab'] - res_1q['fidelity_crab']:+.6f}</code></td>
        </tr>
        <tr>
          <td><strong>Fedeltà GRAPE</strong></td>
          <td><code>{res_1q['fidelity_grape']:.6f}</code></td>
          <td><code>{res_2q['fidelity_grape']:.6f}</code></td>
          <td><code>{res_2q['fidelity_grape'] - res_1q['fidelity_grape']:+.6f}</code></td>
        </tr>
        <tr>
          <td><strong>Fedeltà Finale (PCHIP Smoothed)</strong></td>
          <td><strong style="color: var(--accent);">{f1:.6f}</strong></td>
          <td><strong style="color: var(--success);">{f2:.6f}</strong></td>
          <td><strong>{f2 - f1:+.6f}</strong></td>
        </tr>
        <tr>
          <td><strong>Costo Energetico Totale (C²)</strong></td>
          <td><code>{c1:.2f}</code></td>
          <td><code>{c2:.2f}</code></td>
          <td><code>{((c2 - c1)/c1)*100.0:+.1f}%</code></td>
        </tr>
        <tr>
          <td><strong>Costo Massimo per Singolo Canale</strong></td>
          <td><code>{res_1q['actuator_metrics'][0]['cost_channel']:.2f}</code></td>
          <td><code>{max(res_2q['actuator_metrics'][0]['cost_channel'], res_2q['actuator_metrics'][1]['cost_channel']):.2f}</code></td>
          <td><code>{((max(res_2q['actuator_metrics'][0]['cost_channel'], res_2q['actuator_metrics'][1]['cost_channel']) - res_1q['actuator_metrics'][0]['cost_channel']) / res_1q['actuator_metrics'][0]['cost_channel']) * 100.0:+.1f}%</code></td>
        </tr>
        <tr>
          <td><strong>Slew Rate Massimo (max |d&Omega;/dt|)</strong></td>
          <td><code>{sr_max_1:.3f}</code></td>
          <td><code>{sr_max_2:.3f}</code></td>
          <td><code>{sr_gain:+.1f}%</code></td>
        </tr>
        <tr>
          <td><strong>Banda Passante 99% (&omega;<sub>99%</sub>)</strong></td>
          <td><code>{w99_1:.2f} &omega;<sub>c</sub></code></td>
          <td><code>{w99_2:.2f} &omega;<sub>c</sub></code></td>
          <td><code>{w_gain:+.1f}%</code></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section-title">📈 Grafici Comparativi Diretti</div>
  <div class="plots-grid">
    <div class="plot-card">
      <div class="plot-header">
        <span class="plot-title">Numero Medio Fotoni &lang;n&rang;(t) — 1Q vs 2Q</span>
        <a class="plot-link" href="comparison_nmean.pdf" target="_blank">PDF Vettoriale</a>
      </div>
      <img src="comparison_nmean.png" alt="Confronto nmean">
    </div>
    <div class="plot-card">
      <div class="plot-header">
        <span class="plot-title">Forme d'Onda di Controllo &Omega;<sub>D</sub>(t) — 1Q vs 2Q</span>
        <a class="plot-link" href="comparison_drives.pdf" target="_blank">PDF Vettoriale</a>
      </div>
      <img src="comparison_drives.png" alt="Confronto drive">
    </div>
  </div>

  <div style="margin-top: 30px; text-align: center;">
    <a href="1q/report.html" style="color: var(--accent); margin-right: 25px; text-decoration: none;">&rarr; Apri Report Dettagliato 1 Qubit</a>
    <a href="2q/report.html" style="color: var(--accent); text-decoration: none;">&rarr; Apri Report Dettagliato 2 Qubit</a>
  </div>
</div>
</body>
</html>
"""
    with open(os.path.join(comp_dir, "comparison_report.html"), "w", encoding="utf-8") as f:
        f.write(html_content)


# ==============================================================================
# Pipeline di Simulazione per Singolo Sistema
# ==============================================================================
def run_single_system_pipeline(cfg: dict, run_dir: str) -> dict:
    """
    Esegue la full pipeline (CRAB -> GRAPE -> PCHIP) salvando tutti i risultati
    e i report all'interno della cartella specifica di run `run_dir`.
    """
    t_start_sys = time.time()
    system_type = cfg["system_type"]
    dim = cfg["dim"]
    omega_c = cfg["omega_c"]
    g1 = cfg["g1"]
    g2 = cfg["g2"]
    target_type = cfg["target_type"]
    target_param = cfg["target_param"]
    theta = cfg["target_theta"]

    # Calcolo tempo T
    tau_s = np.pi / (2.0 * g1)
    T = cfg["t_fixed"] if cfg["t_fixed"] is not None else cfg["t_factor_taus"] * tau_s
    t_factor_taus = T / tau_s

    # Control bases
    omega_bases = [cfg["omega_base_1"]] if system_type == "1q" else [cfg["omega_base_1"], cfg["omega_base_2"]]

    # Troncamenti e frequenze
    crab_freq_range = (cfg["crab_freq_min"], cfg["crab_freq_max"] * omega_c)
    crab_num_freqs = cfg["crab_num_freqs"]
    crab_nt = cfg["crab_nt"]
    crab_num_seeds = cfg["crab_num_seeds"]
    crab_max_iter = cfg["crab_max_iter"]
    crab_method = cfg["crab_method"]

    grape_nt = cfg["grape_nt"]
    grape_max_iter = cfg["grape_max_iter"]
    grape_amp_bound = cfg["grape_amp_bound"]
    interp_nt = cfg["interp_nt"]

    os.makedirs(run_dir, exist_ok=True)

    # Costruzione sistema
    if system_type == "1q":
        sys_obj = build_one_qubit_system(dim=dim, omega_c=omega_c, g=g1)
        compute_cost_fn = compute_control_cost_1q
    else:
        sys_obj = build_two_qubit_system(dim=dim, omega_c=omega_c, g1=g1, g2=g2)
        compute_cost_fn = compute_control_cost_2q

    target_cav_ket, target_dm, target_label, expected_n = _build_target_states(
        system_type, dim, target_type, target_param, theta
    )

    dt_grape = T / (grape_nt - 1)
    omega_nyquist_grape = np.pi / dt_grape

    print("\n" + "=" * 70)
    print(f"  AVVIO FULL PIPELINE — SISTEMA: {system_type.upper()}")
    print(f"  Target: {target_label} | Dimensione Fock cavità: {dim}")
    print(f"  Spazio di Hilbert totale: {sys_obj.H0.shape[0]} dimensioni")
    print(f"  Durata T: {T:.3f} ({t_factor_taus:.2f} τ_s) | Passo dt GRAPE: {dt_grape:.4f}")
    print(f"  CRAB: {crab_num_freqs} armoniche, freq max = {crab_freq_range[1]:.2f} ω_c")
    print(f"  GRAPE: {grape_nt} time slots, Nyquist cutoff = {omega_nyquist_grape:.2f} rad/s")
    print(f"  Cartella Specifica Run: {run_dir}")
    print("=" * 70)

    # --------------------------------------------------------------------------
    # FASE 1: CRAB Multi-Seed Parallelo
    # --------------------------------------------------------------------------
    cpu_count = os.cpu_count() or 1
    n_workers = min(crab_num_seeds, max(1, cpu_count - 1))

    print(f"\n--- FASE 1: Ottimizzazione CRAB ({crab_num_seeds} seeds, {n_workers} CPU worker) ---")
    t_crab_start = time.time()

    worker_args = [
        (seed, system_type, dim, omega_c, g1, g2, target_type, target_param, theta,
         T, crab_nt, crab_num_freqs, crab_freq_range, omega_bases, crab_max_iter, crab_method)
        for seed in range(crab_num_seeds)
    ]

    crab_results = []
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        future_to_seed = {executor.submit(_crab_worker_task, arg): arg[0] for arg in worker_args}
        completed = 0
        for future in as_completed(future_to_seed):
            completed += 1
            res = future.result()
            crab_results.append(res)
            print(f"  [{completed:>2d}/{crab_num_seeds}] Seed {res['seed'] + 1:>2d} completato | "
                  f"Fedeltà: {res['fidelity']:.6f} | Costo C²: {res['cost']:7.2f} | Tempo: {res['elapsed']:.1f}s")

    elapsed_crab = time.time() - t_crab_start
    crab_results.sort(key=lambda r: r["seed"])

    fidelities = [r["fidelity"] for r in crab_results]
    costs = [r["cost"] for r in crab_results]
    best_idx = int(np.argmax(fidelities))
    best_crab = crab_results[best_idx]

    print(f"\nRiepilogo CRAB: Fedeltà media = {np.mean(fidelities):.6f} ± {np.std(fidelities):.6f} "
          f"(Tempo totale: {elapsed_crab:.1f}s)")
    print(f"  >>> MIGLIOR SEED CRAB: Seed {best_crab['seed'] + 1} | "
          f"Fedeltà = {best_crab['fidelity']:.6f} | Costo C² = {best_crab['cost']:.2f} <<<")

    best_pulses_crab = best_crab["control_pulses"]
    tlist_crab = np.linspace(0, T, crab_nt)

    # --------------------------------------------------------------------------
    # FASE 2: Raffinamento GRAPE (L-BFGS-B)
    # --------------------------------------------------------------------------
    print(f"\n--- FASE 2: Raffinamento GRAPE (L-BFGS-B con vincoli {grape_amp_bound}) ---")
    tlist_grape = np.linspace(0, T, grape_nt)

    opt_grape = GRAPEOptimizer(
        H_drift=sys_obj.H0,
        H_controls=sys_obj.H_controls,
        T=T,
        num_tslots=grape_nt,
        omega_bases=omega_bases,
        seed=None,
    )

    t0_grape = time.time()
    res_grape = opt_grape.optimize_minimize(
        psi0=sys_obj.psi0_dm,
        target_state=target_dm,
        max_iter=grape_max_iter,
        amp_bound=grape_amp_bound,
        initial_guess=best_pulses_crab,
    )
    elapsed_grape = time.time() - t0_grape

    states_grape = opt_grape.forward_propagation(res_grape.control_pulses, sys_obj.psi0_dm)
    rho_cav_grape = ptrace(states_grape[-1], 0)
    F_grape = float(fidelity(target_cav_ket, rho_cav_grape))
    C2_grape = float(compute_cost_fn(res_grape.control_pulses, dt_grape))

    print(f"  GRAPE terminato in {elapsed_grape:.1f}s ({res_grape.iterations} iterazioni):")
    print(f"  Fedeltà cavità GRAPE: {F_grape:.6f} | Costo C²: {C2_grape:.2f}")

    # --------------------------------------------------------------------------
    # FASE 3: Interpolazione Lisciata PCHIP
    # --------------------------------------------------------------------------
    print(f"\n--- FASE 3: Smoothing tramite interpolazione PCHIP ({interp_nt} punti) ---")
    t0_smooth = time.time()
    tlist_fine = np.linspace(0, T, interp_nt)
    dt_fine = tlist_fine[1] - tlist_fine[0]

    ctrl_smooth = []
    for k in range(len(sys_obj.H_controls)):
        cs = PchipInterpolator(tlist_grape, res_grape.control_pulses[k])
        ctrl_smooth.append(cs(tlist_fine))

    opt_fine = GRAPEOptimizer(
        H_drift=sys_obj.H0,
        H_controls=sys_obj.H_controls,
        T=T,
        num_tslots=interp_nt,
        omega_bases=omega_bases,
    )

    states_smooth = opt_fine.forward_propagation(ctrl_smooth, sys_obj.psi0_dm)
    rho_cav_smooth = ptrace(states_smooth[-1], 0)
    F_smooth = float(fidelity(target_cav_ket, rho_cav_smooth))
    C2_smooth = float(compute_cost_fn(ctrl_smooth, dt_fine))
    elapsed_smooth = time.time() - t0_smooth

    print(f"  Fedeltà finale lisciata: {F_smooth:.6f} | Costo C²: {C2_smooth:.2f}")

    # Calcolo metriche dell'attuatore
    act_metrics = _compute_actuator_metrics(ctrl_smooth, dt_fine)

    # --------------------------------------------------------------------------
    # Salvataggio Dati (.npz)
    # --------------------------------------------------------------------------
    results_path = os.path.join(run_dir, "results.npz")
    save_data = {
        "system_type": system_type,
        "dim": dim,
        "target_type": target_type,
        "target_param": target_param,
        "target_label": target_label,
        "T": T,
        "tau_s": tau_s,
        "tlist_crab": tlist_crab,
        "tlist_grape": tlist_grape,
        "tlist_fine": tlist_fine,
        "ctrl_crab": np.array(best_pulses_crab),
        "ctrl_grape": np.array(res_grape.control_pulses),
        "ctrl_smooth": np.array(ctrl_smooth),
        "fidelity_crab": best_crab["fidelity"],
        "fidelity_grape": F_grape,
        "fidelity_smooth": F_smooth,
        "cost_crab": best_crab["cost"],
        "cost_grape": C2_grape,
        "cost_smooth": C2_smooth,
        "all_crab_fidelities": fidelities,
        "all_crab_costs": costs,
    }
    np.savez(results_path, **save_data)
    print(f"\nDati completi salvati in: {results_path}")

    # --------------------------------------------------------------------------
    # Generazione Grafici (Sia PNG per Report sia PDF Vettoriali)
    # --------------------------------------------------------------------------
    n_expect = [expect(sys_obj.n_tot, rho) for rho in states_smooth]

    # 1. Numero medio di fotoni <n>(t)
    fig_n = plt.figure(figsize=(7.5, 4.2))
    plt.plot(tlist_fine / tau_s, n_expect[1:], "crimson", lw=2, label=r"$\langle n(t) \rangle$")
    plt.axhline(expected_n, color="black", ls="--", lw=1.5, label=f"Target ({target_label})")
    plt.xlabel(r"$t / \tau_s$")
    plt.ylabel(r"$\langle n \rangle$")
    plt.title(f"Sistema {system_type.upper()} — Numero medio fotoni (F = {F_smooth:.4f})")
    plt.legend(frameon=True)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(run_dir, "nmean.png"), dpi=300)
    plt.savefig(os.path.join(run_dir, "nmean.pdf"), dpi=300)
    plt.close(fig_n)

    # 2. Forme d'onda di Controllo
    n_ctrl = len(sys_obj.H_controls)
    fig_d, axes_d = plt.subplots(n_ctrl, 2, figsize=(14, 4.2 * n_ctrl), squeeze=False)
    for k in range(n_ctrl):
        # CRAB
        axes_d[k, 0].plot(tlist_crab / tau_s, best_pulses_crab[k], color="darkgreen" if k == 0 else "navy", lw=1.5)
        axes_d[k, 0].set_title(f"CRAB — Qubit {k+1} (F={best_crab['fidelity']:.4f})")
        axes_d[k, 0].set_ylabel(rf"$\Omega_{{D{k+1}}}(t) / \omega_c$")
        axes_d[k, 0].set_xlabel(r"$t / \tau_s$")
        axes_d[k, 0].grid(True, alpha=0.3)

        # Smoothed
        axes_d[k, 1].plot(tlist_fine / tau_s, ctrl_smooth[k], color="darkgreen" if k == 0 else "navy", lw=1.8)
        axes_d[k, 1].set_title(f"Smoothed PCHIP — Qubit {k+1} (F={F_smooth:.4f})")
        axes_d[k, 1].set_ylabel(rf"$\Omega_{{D{k+1}}}(t) / \omega_c$")
        axes_d[k, 1].set_xlabel(r"$t / \tau_s$")
        axes_d[k, 1].grid(True, alpha=0.3)

    fig_d.tight_layout()
    plt.savefig(os.path.join(run_dir, "drives_comparison.png"), dpi=300)
    plt.savefig(os.path.join(run_dir, "drives_comparison.pdf"), dpi=300)
    plt.close(fig_d)

    # 3. Funzioni di Wigner
    xvec = np.linspace(-5, 5, 200)
    w_target = wigner(target_cav_ket, xvec, xvec)
    w_final = wigner(rho_cav_smooth, xvec, xvec)

    fig_w, axes_w = plt.subplots(1, 2, figsize=(12, 5))
    axes_w[0].contourf(xvec, xvec, w_target, 100, cmap="RdBu_r")
    axes_w[0].set_title(f"Target: {target_label}")
    axes_w[0].set_xlabel("x")
    axes_w[0].set_ylabel("p")

    im = axes_w[1].contourf(xvec, xvec, w_final, 100, cmap="RdBu_r")
    axes_w[1].set_title(f"Stato Finale Cavità (F={F_smooth:.4f})")
    axes_w[1].set_xlabel("x")
    axes_w[1].set_ylabel("p")
    fig_w.colorbar(im, ax=axes_w[1])
    fig_w.tight_layout()
    plt.savefig(os.path.join(run_dir, "wigner.png"), dpi=300)
    plt.savefig(os.path.join(run_dir, "wigner.pdf"), dpi=300)
    plt.close(fig_w)

    # 4. Spettro FFT
    fig_f, axes_f = plt.subplots(1, n_ctrl, figsize=(6.5 * n_ctrl, 4.2), squeeze=False)
    for k in range(n_ctrl):
        pulse_c = ctrl_smooth[k] - np.mean(ctrl_smooth[k])
        fft_v = np.fft.fft(pulse_c)
        freqs = np.fft.fftfreq(len(pulse_c), d=dt_fine)
        mask = freqs >= 0
        freqs_rad = freqs[mask] * (2.0 * np.pi)

        ax = axes_f[0, k]
        ax.plot(freqs_rad, np.abs(fft_v[mask]), lw=1.8, label=f"FFT Qubit {k+1}")
        ax.axvline(2.0 * omega_c, color="red", ls="--", label=r"DCE Risonanza $2\omega_c$")
        ax.axvline(crab_freq_range[1], color="darkorange", ls=":", label=rf"CRAB cut (${crab_freq_range[1]:.1f}\omega_c$)")
        ax.set_xlim(0, max(6.0 * omega_c, crab_freq_range[1] * 1.5))
        ax.set_xlabel(r"Frequenza $\omega / \omega_c$")
        ax.set_ylabel("Ampiezza")
        ax.set_title(f"FFT Spettro — Qubit {k+1}")
        ax.legend(loc="upper right", fontsize=10)
        ax.grid(True, alpha=0.3)

    fig_f.tight_layout()
    plt.savefig(os.path.join(run_dir, "fft.png"), dpi=300)
    plt.savefig(os.path.join(run_dir, "fft.pdf"), dpi=300)
    plt.close(fig_f)

    # --------------------------------------------------------------------------
    # Scrittura Report Completo (report.html & report.md)
    # --------------------------------------------------------------------------
    report_data = {
        "system_type": system_type,
        "run_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_label": target_label,
        "expected_n": expected_n,
        "dim": dim,
        "total_hilbert_dim": sys_obj.H0.shape[0],
        "g1": g1,
        "g2": g2,
        "T": T,
        "tau_s": tau_s,
        "T_factor_taus": t_factor_taus,
        "crab_seeds": crab_num_seeds,
        "best_crab_seed": best_crab["seed"] + 1,
        "crab_freqs": crab_num_freqs,
        "crab_freq_max": crab_freq_range[1],
        "crab_nt": crab_nt,
        "crab_mean_f": float(np.mean(fidelities)),
        "crab_std_f": float(np.std(fidelities)),
        "grape_nt": grape_nt,
        "omega_nyquist": omega_nyquist_grape,
        "grape_amp_bound": str(grape_amp_bound),
        "grape_iterations": res_grape.iterations,
        "interp_nt": interp_nt,
        "fidelity_crab": best_crab["fidelity"],
        "fidelity_grape": F_grape,
        "fidelity_smooth": F_smooth,
        "cost_crab": best_crab["cost"],
        "cost_grape": C2_grape,
        "cost_smooth": C2_smooth,
        "elapsed_crab": elapsed_crab,
        "elapsed_grape": elapsed_grape,
        "elapsed_smooth": elapsed_smooth,
        "elapsed_total": time.time() - t_start_sys,
        "actuator_metrics": act_metrics,
        "tlist_fine": tlist_fine,
        "ctrl_smooth": ctrl_smooth,
        "n_expect": n_expect,
    }

    _write_single_system_reports(run_dir, report_data)
    print(f"\nReport interattivo HTML e Markdown salvati in:\n  -> {os.path.join(run_dir, 'report.html')}\n  -> {os.path.join(run_dir, 'report.md')}")

    return report_data


# ==============================================================================
# Funzione Principale (Main)
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Full pipeline runner per controllo quantistico 1Q e 2Q con parametri personalizzabili."
    )
    parser.add_argument("--system", choices=["1q", "2q", "both"], default=SYSTEM_TYPE,
                        help="Sistema fisico da simulare ('1q', '2q', o 'both')")
    parser.add_argument("--target", choices=["fock", "squeezed", "cat"], default=TARGET_TYPE,
                        help="Tipo di stato target ('fock', 'squeezed', 'cat')")
    parser.add_argument("--param", type=float, default=TARGET_PARAM,
                        help="Parametro dello stato (n fotoni per Fock, r per squeezed, alpha per cat)")
    parser.add_argument("--dim", type=int, default=DIM,
                        help="Dimensione troncamento Fock cavità")
    parser.add_argument("--factor-taus", type=float, default=T_FACTOR_TAUS,
                        help="Fattore moltiplicativo di tau_s per T (T = factor * tau_s)")
    parser.add_argument("--t-fixed", type=float, default=T_FIXED,
                        help="Durata T fissata esplicitamente (sovrascrive factor-taus)")
    parser.add_argument("--crab-seeds", type=int, default=CRAB_NUM_SEEDS,
                        help="Numero di seed paralleli per CRAB")
    parser.add_argument("--crab-max-iter", type=int, default=CRAB_MAX_ITER,
                        help="Massimo numero di iterazioni per CRAB")
    parser.add_argument("--grape-max-iter", type=int, default=GRAPE_MAX_ITER,
                        help="Massimo numero di iterazioni per GRAPE")
    parser.add_argument("--crab-freqs", type=int, default=CRAB_NUM_FREQS,
                        help="Numero di frequenze nella base di Fourier di CRAB")
    parser.add_argument("--crab-freq-max", type=float, default=CRAB_FREQ_MAX,
                        help="Frequenza di taglio superiore di CRAB (in unità omega_c)")
    parser.add_argument("--grape-nt", type=int, default=GRAPE_NT,
                        help="Numero di time-slots per GRAPE (fissa il campionamento e la banda di Nyquist)")
    parser.add_argument("--out-dir", type=str, default=BASE_OUTPUT_DIR,
                        help="Cartella base di output (se None, creata automaticamente con parametri e data)")

    args = parser.parse_args()

    # Prepara dizionario di configurazione base
    target_param_val = TARGET_PARAM
    if TARGET_TYPE == "squeezed" and TARGET_R_IN_DB:
        target_param_val = db_to_r(TARGET_PARAM)

    base_config = {
        "system_type": args.system,
        "target_type": args.target,
        "target_param": args.param if args.param is not None else target_param_val,
        "target_theta": TARGET_THETA,
        "dim": args.dim,
        "omega_c": OMEGA_C,
        "g1": G1,
        "g2": G2,
        "omega_base_1": OMEGA_BASE_1,
        "omega_base_2": OMEGA_BASE_2,
        "t_factor_taus": args.factor_taus,
        "t_fixed": args.t_fixed,
        "crab_num_seeds": args.crab_seeds,
        "crab_max_iter": args.crab_max_iter,
        "crab_method": CRAB_METHOD,
        "crab_num_freqs": args.crab_freqs,
        "crab_freq_min": CRAB_FREQ_MIN,
        "crab_freq_max": args.crab_freq_max,
        "crab_nt": CRAB_NT,
        "grape_nt": args.grape_nt,
        "grape_max_iter": args.grape_max_iter,
        "grape_amp_bound": GRAPE_AMP_BOUND,
        "interp_nt": INTERP_NT,
    }

    # Calcolo identificatore durata T per il nome della cartella
    tau_s = np.pi / (2.0 * G1)
    if args.t_fixed is not None:
        t_tag = f"T{args.t_fixed:.1f}"
    else:
        t_tag = f"T{args.factor_taus:.0f}taus"

    param_tag = f"n{base_config['target_param']}" if base_config["target_type"] == "fock" else f"{base_config['target_param']:.2f}"

    # Timestamp per la specifica run
    run_timestamp = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")

    t_total_start = time.time()
    results_summary = []

    if args.system in ["1q", "2q"]:
        # Cartella base di parametri + sottocartella timestamp della run
        if args.out_dir is None:
            param_dir = f"results_{args.system}_{base_config['target_type']}_{param_tag}_dim{args.dim}_{t_tag}"
        else:
            param_dir = args.out_dir

        run_dir = os.path.join(param_dir, run_timestamp)
        cfg = dict(base_config)
        res = run_single_system_pipeline(cfg, run_dir)
        results_summary.append(res)

    elif args.system == "both":
        print("\n" + "#" * 70)
        print("  MODALITÀ CONFRONTO 'BOTH': ESECUZIONE 1Q E 2Q CON GLI STESSI PARAMETRI")
        print("#" * 70)

        if args.out_dir is None:
            param_dir = f"results_both_{base_config['target_type']}_{param_tag}_dim{args.dim}_{t_tag}"
        else:
            param_dir = args.out_dir

        main_run_dir = os.path.join(param_dir, run_timestamp)
        dir_1q = os.path.join(main_run_dir, "1q")
        dir_2q = os.path.join(main_run_dir, "2q")

        # Esegui 1Q
        cfg_1q = dict(base_config)
        cfg_1q["system_type"] = "1q"
        res_1q = run_single_system_pipeline(cfg_1q, dir_1q)
        results_summary.append(res_1q)

        # Esegui 2Q
        cfg_2q = dict(base_config)
        cfg_2q["system_type"] = "2q"
        res_2q = run_single_system_pipeline(cfg_2q, dir_2q)
        results_summary.append(res_2q)

        # ----------------------------------------------------------------------
        # Generazione Grafici Comparativi 1Q vs 2Q
        # ----------------------------------------------------------------------
        tlist_fine = res_1q["tlist_fine"]
        tau_s_val = res_1q["tau_s"]

        # 1. Comparazione numero medio fotoni
        fig_cmp_n = plt.figure(figsize=(8, 4.5))
        plt.plot(tlist_fine / tau_s_val, res_1q["n_expect"][1:], "crimson", lw=2, label=f"1 Qubit (F={res_1q['fidelity_smooth']:.4f})")
        plt.plot(tlist_fine / tau_s_val, res_2q["n_expect"][1:], "dodgerblue", lw=2, label=f"2 Qubit (F={res_2q['fidelity_smooth']:.4f})")
        plt.axhline(res_1q["expected_n"], color="black", ls="--", lw=1.5, label=f"Target ({res_1q['target_label']})")
        plt.xlabel(r"$t / \tau_s$")
        plt.ylabel(r"$\langle n \rangle$")
        plt.title(f"Confronto Dinamica Cavità — 1Q vs 2Q")
        plt.legend(frameon=True)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(main_run_dir, "comparison_nmean.png"), dpi=300)
        plt.savefig(os.path.join(main_run_dir, "comparison_nmean.pdf"), dpi=300)
        plt.close(fig_cmp_n)

        # 2. Comparazione Controlli
        fig_cmp_d, ax_d = plt.subplots(figsize=(10, 4.5))
        ax_d.plot(tlist_fine / tau_s_val, res_1q["ctrl_smooth"][0], "crimson", lw=1.8, label=r"1 Qubit: $\Omega_D(t)$")
        ax_d.plot(tlist_fine / tau_s_val, res_2q["ctrl_smooth"][0], "darkgreen", lw=1.8, label=r"2 Qubit: $\Omega_{D1}(t)$")
        ax_d.plot(tlist_fine / tau_s_val, res_2q["ctrl_smooth"][1], "navy", lw=1.8, label=r"2 Qubit: $\Omega_{D2}(t)$")
        ax_d.set_xlabel(r"$t / \tau_s$")
        ax_d.set_ylabel(r"$\Omega_D(t) / \omega_c$")
        ax_d.set_title("Confronto Forme d'Onda di Controllo Lisciate — 1Q vs 2Q")
        ax_d.legend(frameon=True)
        ax_d.grid(True, alpha=0.3)
        fig_cmp_d.tight_layout()
        plt.savefig(os.path.join(main_run_dir, "comparison_drives.png"), dpi=300)
        plt.savefig(os.path.join(main_run_dir, "comparison_drives.pdf"), dpi=300)
        plt.close(fig_cmp_d)

        # Scrivi report comparativo
        _write_comparison_reports(main_run_dir, res_1q, res_2q, base_config)
        print(f"\n>>> REPORT COMPARATIVO COMPLETO GENERATO:")
        print(f"  -> {os.path.join(main_run_dir, 'comparison_report.html')}")

    # --------------------------------------------------------------------------
    # Tabella Riassuntiva Finale a Terminale
    # --------------------------------------------------------------------------
    total_time = time.time() - t_total_start
    print("\n" + "=" * 75)
    print("  RIASSUNTO FINALE DELLE SIMULAZIONI")
    print("=" * 75)
    print(f"  {'Sistema':<10s}  {'Fedeltà CRAB':>14s}  {'Fedeltà GRAPE':>14s}  {'Fedeltà Smooth':>14s}  {'Costo C²':>10s}")
    print(f"  {'-'*10}  {'-'*14}  {'-'*14}  {'-'*14}  {'-'*10}")
    for r in results_summary:
        print(f"  {r['system_type'].upper():<10s}  {r['fidelity_crab']:14.6f}  {r['fidelity_grape']:14.6f}  "
              f"{r['fidelity_smooth']:14.6f}  {r['cost_smooth']:10.2f}")
    print("=" * 75)
    print(f"Tempo totale di esecuzione: {total_time:.1f}s ({total_time / 60:.1f} min)")


if __name__ == "__main__":
    main()
