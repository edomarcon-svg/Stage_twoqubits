# Spiegazione Dettagliata del Codice — Sistema Cavità + 2 Qubit

## Indice

1. [Il Modello Fisico](#1-il-modello-fisico)
2. [Estensione a Due Qubit](#2-estensione-a-due-qubit)
3. [Il Kernel: `two_qubit_system.py`](#3-il-kernel-two_qubit_systempy)
4. [L'Ottimizzatore CRAB: `crab_optimizer.py`](#4-lottimizzatore-crab-crab_optimizerpy)
5. [L'Ottimizzatore GRAPE: `grape_optimizer.py`](#5-lottimizzatore-grape-grape_optimizerpy)
6. [Lo Script CRAB: `run_crab_2q.py`](#6-lo-script-crab-run_crab_2qpy)
7. [Lo Script GRAPE: `run_grape_2q.py`](#7-lo-script-grape-run_grape_2qpy)
8. [La Pipeline Completa: `run_full_pipeline_2q.py`](#8-la-pipeline-completa-run_full_pipeline_2qpy)
9. [Gli Stati Target](#9-gli-stati-target)
10. [Le Metriche](#10-le-metriche)
11. [Interpretazione dei Grafici](#11-interpretazione-dei-grafici)

---

## 1. Il Modello Fisico

### 1.1 Hamiltoniana di Rabi

Il sistema di partenza è una **cavità elettromagnetica a singolo modo** accoppiata ad un **qubit** (sistema a due livelli). L'interazione è descritta dall'Hamiltoniana di Rabi:

```
H_R = (ω_q / 2) σ_z  +  ω_c a†a  +  g (a† + a)(σ₊ + σ₋)
```

dove:
- `ω_c` = frequenza della cavità
- `ω_q` = frequenza del qubit
- `a, a†` = operatori di distruzione e creazione della cavità
- `σ_z, σ₊, σ₋` = operatori di Pauli del qubit
- `g` = costante di accoppiamento luce-materia

### 1.2 Regime di Accoppiamento Ultrastro (USC)

Nel regime USC si ha `g/ω_c ≳ 0.1`. In questo regime, i **termini contro-rotanti** `aσ₋ + a†σ₊` non sono più trascurabili (a differenza del modello di Jaynes-Cummings). Questi termini **rompono la conservazione del numero di eccitazioni** `n_ex = a†a + σ₊σ₋`, permettendo la **creazione di fotoni dal vuoto** (Effetto Casimir Dinamico, DCE).

### 1.3 Hamiltoniana di Controllo

Un campo classico esterno modula la frequenza del qubit nel tempo:

```
H_D(t) = Ω_D(t) / 2 · σ_z
```

L'Hamiltoniana totale del sistema diventa:

```
H_S(t) = H_R + H_D(t)
```

### 1.4 Effetto Casimir Dinamico (DCE)

Modulando non-adiabaticamente la frequenza del qubit tramite `Ω_D(t)`, si generano **coppie di eccitazioni dal vuoto**. Il punto chiave del paper è che, **ottimizzando la forma di `Ω_D(t)`**, si può sfruttare il DCE per **generare deterministicamente stati non-classici** della cavità.

### 1.5 Simmetrie: Conservazione della Parità

Sia l'Hamiltoniana di Rabi sia quella di controllo conservano la **parità**:
```
Π = exp(iπ n_ex)
```
Questo implica che le eccitazioni vengono create/annichilate **a coppie**. Lo stato iniziale `|0,g⟩` ha parità +1, quindi gli stati raggiungibili hanno parità pari.

---

## 2. Estensione a Due Qubit

### 2.1 Spazio di Hilbert

| Sistema | Dimensione | Spazio |
|---------|-----------|--------|
| 1 qubit | `dim × 2` = 60 | `H_cav ⊗ H_q` |
| 2 qubit | `dim × 2 × 2` = 120 | `H_cav ⊗ H_q1 ⊗ H_q2` |

Con `dim = 30` (troncamento dello spazio di Fock della cavità), lo spazio di Hilbert raddoppia passando a 120 dimensioni.

### 2.2 Hamiltoniana per Due Qubit

L'Hamiltoniana di drift (senza controllo) per il sistema cavità + 2 qubit diventa:

```
H₀ = ω_c (a†a + 1/2)  +  g₁ (a + a†) σ_x1  +  g₂ (a + a†) σ_x2
```

dove:
- `g₁` = accoppiamento cavità-qubit 1
- `g₂` = accoppiamento cavità-qubit 2
- `σ_x1 = I_cav ⊗ σ_x ⊗ I_2` = sigma-x del qubit 1 nello spazio completo
- `σ_x2 = I_cav ⊗ I_2 ⊗ σ_x` = sigma-x del qubit 2 nello spazio completo

**Nota**: Le energie proprie dei qubit `(ω_q/2)σ_z` non compaiono in `H₀` perché sono **assorbite nelle Hamiltoniane di controllo** (come nel codice originale a un qubit).

### 2.3 Hamiltoniane di Controllo

Ora ci sono **due controlli indipendenti**, uno per ogni qubit:

```
H₁ = -1/2 · σ_z1    (drive sul qubit 1)
H₂ = -1/2 · σ_z2    (drive sul qubit 2)
```

Ciascun controllo `Ω_D1(t)` e `Ω_D2(t)` modula la frequenza del rispettivo qubit:

```
H_S(t) = H₀  +  Ω_D1(t) · H₁  +  Ω_D2(t) · H₂
```

### 2.4 Stato Iniziale

```
|ψ₀⟩ = |0⟩ |g⟩ |g⟩
```

Cavità nel vuoto, entrambi i qubit nello stato fondamentale.

### 2.5 Interazione Qubit-Qubit

Nel nostro modello, i due qubit **non interagiscono direttamente** tra loro. L'interazione avviene **indirettamente tramite la cavità**: entrambi i qubit sono accoppiati alla stessa cavità, quindi la dinamica di un qubit influenza l'altro attraverso lo scambio di fotoni virtuali.

---

## 3. Il Kernel: `two_qubit_system.py`

Questo modulo è il **cuore del sistema a due qubit**. Costruisce tutti gli operatori necessari nello spazio di Hilbert completo.

### 3.1 Prodotti Tensoriali in QuTiP

In QuTiP, gli operatori nello spazio prodotto tensoriale si costruiscono con `tensor()`. L'ordine è: **cavità ⊗ qubit1 ⊗ qubit2**.

```python
# Operatore di distruzione della cavità nello spazio completo
a_tot = tensor(a, I_q, I_q)      # a ⊗ I₂ ⊗ I₂

# Sigma-z del qubit 1
sz1 = tensor(I_c, sigmaz(), I_q)  # I_dim ⊗ σ_z ⊗ I₂

# Sigma-z del qubit 2
sz2 = tensor(I_c, I_q, sigmaz())  # I_dim ⊗ I₂ ⊗ σ_z

# Accoppiamento cavità-qubit 1
x_couple1 = tensor(x_op, sigmax(), I_q)  # (a+a†) ⊗ σ_x ⊗ I₂
```

**Regola**: per costruire un operatore che agisce sul sottosistema `k`, si mette l'operatore nella posizione `k` del `tensor()` e l'identità nelle altre posizioni.

### 3.2 La Classe `TwoQubitSystem`

È un `dataclass` che contiene tutti gli operatori e le Hamiltoniane pre-calcolati:

```python
sys2q = build_two_qubit_system(dim=30, omega_c=1.0, g1=0.3, g2=0.3)
# Ora si può usare:
# sys2q.H0          → Hamiltoniana di drift
# sys2q.H_controls  → [H1_ctrl, H2_ctrl]
# sys2q.n_tot       → operatore numero di fotoni
# sys2q.psi0_ket    → stato iniziale |0,g,g⟩
```

### 3.3 Funzioni per gli Stati Target

Il modulo fornisce costruttori per diversi stati target:

| Funzione | Stato Target | Uso |
|----------|-------------|-----|
| `target_fock_2q(dim, n)` | `\|n⟩` della cavità | CRAB (ket cavità) |
| `target_squeezed_2q(dim, r, θ)` | Vuoto squeezed | CRAB |
| `target_cat_2q(dim, α)` | Cat state `C⁺_α - C⁺_{iα}` | CRAB |
| `target_bell_2q(dim, n, type)` | Stato di Bell dei qubit | CRAB/GRAPE |
| `grape_target_fock_2q(dim, n)` | `\|n⟩⟨n\| ⊗ I₂ ⊗ I₂` | GRAPE (DM completa) |

### 3.4 Funzioni di Costo

Le funzioni di costo sono **factory functions** che restituiscono una funzione compatibile con l'interfaccia dell'ottimizzatore:

```python
# Per CRAB: la cost function riceve (final_state, pulses)
cost_fn = make_crab_cost_cavity(target_ket)
# Internamente fa:
#   1. ptrace(final_state, 0) → matrice densità ridotta della cavità
#   2. 1 - fidelity(target, rho_cav) → infedeltà
```

### 3.5 Tracce Parziali

Operazione fondamentale per estrarre lo stato di un sottosistema:

```python
# ptrace(stato_completo, [indici_da_tenere])
rho_cav = ptrace(psi_full, 0)       # traccia su qubit1,2 → solo cavità
rho_qubits = ptrace(psi_full, [1,2]) # traccia su cavità → solo qubit
```

---

## 4. L'Ottimizzatore CRAB: `crab_optimizer.py`

### 4.1 Idea di Base

CRAB (Chopped Random Basis) è un metodo di controllo ottimo **gradient-free**. L'idea è parametrizzare il polso di controllo come una **serie di Fourier troncata** con frequenze casuali:

```
Ω_D(t) = ω_base + s(t) · Σ_k [A_k sin(ω_k t) + B_k cos(ω_k t)]
```

dove:
- `{A_k, B_k}` sono i parametri da ottimizzare
- `{ω_k}` sono frequenze estratte casualmente
- `s(t)` è una funzione di confine (boundary function)
- `ω_base` è l'ampiezza base del controllo

### 4.2 Parametri di Ottimizzazione

Il numero totale di parametri per N controlli è:
```
N_params = 2 × N_freqs × N_controls
```

Per il caso a 2 qubit con `num_freqs = 20`:
```
N_params = 2 × 20 × 2 = 80 parametri
```

### 4.3 Boundary Function (Funzione di Confine)

Garantisce che il polso si accenda e si spenga gradualmente:

```python
def _boundary_function(self, t):
    sigma = self.boundary_sigma  # larghezza (default 0.7)
    return (1 - exp(-(t/σ)²)) * (1 - exp(-((t-T)/σ)²))
```

- A `t = 0`: la funzione vale ~0 → il polso è spento
- A `t = T`: la funzione vale ~0 → il polso è spento
- Nel mezzo: vale ~1 → il polso è attivo

### 4.4 Costruzione del Polso

Per ogni controllo `k`:

1. Si estraggono le frequenze casuali `ω_k`
2. Si estraggono i coefficienti `{A_k, B_k}` dal vettore di parametri
3. Si calcola la serie di Fourier per ogni punto temporale
4. Si moltiplica per la boundary function
5. Si aggiunge l'offset `ω_base`

```python
pulse[t] = omega_base + boundary(t) × Σ [A sin(ω t) + B cos(ω t)]
```

### 4.5 Costruzione dell'Hamiltoniana Dipendente dal Tempo

QuTiP richiede le Hamiltoniane dipendenti dal tempo nel formato:

```python
H = [H_drift, [H_control_1, pulse_array_1], [H_control_2, pulse_array_2], ...]
```

### 4.6 Ottimizzazione

CRAB usa `scipy.optimize.minimize` con il metodo **Nelder-Mead** (simplex):
- Non richiede gradienti
- Robusto per landscape complessi
- Può essere lento per molti parametri

L'obiettivo è minimizzare la **funzione costo** (infedeltà):
```
C = 1 - F(ρ_final, ρ_target)
```

### 4.7 Perché CRAB Funziona Senza Modifiche per 2 Qubit

L'ottimizzatore CRAB è **già generico**: accetta una lista arbitraria di Hamiltoniane di controllo `H_controls`. Per passare da 1 a 2 qubit basta:
- Passare `H_controls = [H1, H2]` (lista di 2 elementi)
- Passare `omega_bases = [2.0, 2.0]` (uno per controllo)

Il CRAB genera automaticamente 2 set di parametri e 2 polsi indipendenti.

---

## 5. L'Ottimizzatore GRAPE: `grape_optimizer.py`

### 5.1 Idea di Base

GRAPE (Gradient Ascent Pulse Engineering) è un metodo **gradient-based** dove il polso è **costante a tratti** (piecewise constant). Si calcola il gradiente della fedeltà rispetto ad ogni valore del polso in ogni intervallo temporale.

### 5.2 Propagazione Forward

Si propaga la **matrice densità** ρ dal tempo iniziale al tempo finale:

```python
def forward_propagation(self, controls, psi0):
    rho_list = [psi0]
    for t in range(num_tslots):
        # Hamiltoniana totale al tempo t
        H_total = H_drift + Σ_k controls[k][t] * H_controls[k]
        # Operatore unitario per questo step
        U = exp(-i H_total dt)
        # Evoluzione della matrice densità
        rho_list.append(U · rho · U†)
    return rho_list
```

**Nota**: GRAPE lavora con **matrici densità** (non ket), perché il target può essere uno stato misto (es. `|n⟩⟨n| ⊗ I/4` dove si traccia sui qubit).

### 5.3 Propagazione Backward

Si propaga lo stato target **all'indietro nel tempo**:

```python
def backward_propagation(self, controls, target_state):
    lambda_list[-1] = target_state
    for t in reversed(range(num_tslots)):
        U = exp(-i H_total dt)
        lambda_list[t] = U† · lambda_list[t+1] · U
    return lambda_list
```

### 5.4 Calcolo dei Gradienti

Il gradiente della fedeltà rispetto al controllo `k` al tempo `t` è:

```
∂F/∂u_k(t) = -Re{ Tr[ λ(t)† · (i dt [H_k, ρ(t)]) ] }
```

dove `[H_k, ρ]` è il **commutatore** tra l'Hamiltoniana di controllo `k` e la matrice densità.

```python
def compute_gradients(self, rho_list, lambda_list):
    for k, Hc in enumerate(H_controls):
        for t in range(num_tslots):
            comm = commutator(Hc, rho_list[t])
            grad = -Re{ Tr[λ†(t) · (i dt · comm)] }
            gradients[k][t] = grad
```

### 5.5 Metodo Gradient Ascent

Aggiornamento iterativo semplice:
```
u_k(t) ← u_k(t) + ε · ∂F/∂u_k(t)
```

### 5.6 Metodo L-BFGS-B

Ottimizzazione più sofisticata che:
- Usa approssimazioni del Hessiano (L-BFGS)
- Supporta **vincoli di ampiezza** (Bounded → `-B`)
- I punti estremi del polso sono fissati a `ω_base`

```python
result = minimize(
    objective,         # 1 - F e il gradiente
    initial_guess,     # polsi iniziali (senza i bordi)
    method="L-BFGS-B",
    jac=True,          # il gradiente è fornito da objective
    bounds=bounds,     # vincoli [amp_min, amp_max]
)
```

### 5.7 Come GRAPE Gestisce 2 Controlli

Come CRAB, anche GRAPE gestisce automaticamente N controlli. I gradienti vengono calcolati **indipendentemente** per ogni Hamiltoniana di controllo `H_k`, e i polsi vengono aggiornati separatamente. Per L-BFGS-B, tutti i polsi vengono **appiattiti** in un unico vettore per l'ottimizzatore SciPy.

---

## 6. Lo Script CRAB: `run_crab_2q.py`

### Flusso di Esecuzione

```
1. Parametri fisici
       ↓
2. build_two_qubit_system() → TwoQubitSystem
       ↓
3. Definisci target: target_fock_2q(dim, n=6)
       ↓
4. Crea cost function: make_crab_cost_cavity(target)
       ↓
5. Crea CRABOptimizer con H_controls=[H1, H2]
       ↓
6. optimizer.optimize(psi0, cost_fn, ...)
       ↓
7. Post-processing:
   - Re-evolve con sesolve
   - Calcola fedeltà, ⟨n⟩, costo
       ↓
8. Grafici: ⟨n⟩(t), drives, Wigner, FFT
```

### Configurazione Chiave

```python
optimizer = CRABOptimizer(
    H_drift=sys2q.H0,             # Hamiltoniana di drift (120×120)
    H_controls=sys2q.H_controls,  # [H1_ctrl, H2_ctrl]
    T=T,                          # tempo totale
    num_tslots=400,               # griglia temporale
    num_freqs=20,                 # armoniche di Fourier per controllo
    omega_bases=[2.0, 2.0],       # ampiezza base per ogni qubit
)
```

---

## 7. Lo Script GRAPE: `run_grape_2q.py`

### Differenze Rispetto a CRAB

| Aspetto | CRAB | GRAPE |
|---------|------|-------|
| Stato iniziale | ket `\|ψ₀⟩` | density matrix `ρ₀` |
| Target | ket cavità | DM completa `ρ_target` |
| Metodo | Nelder-Mead (gradient-free) | L-BFGS-B (gradient-based) |
| Polso | Fourier continuo | Costante a tratti |
| Vincoli ampiezza | No (ma clipping opzionale) | Sì (amp_bound) |

### Il Target GRAPE per 2 Qubit

Per GRAPE, il target deve essere una **matrice densità nello spazio completo**. Se ci interessa solo la cavità:

```python
target_dm = |n⟩⟨n| ⊗ I₂ ⊗ I₂  (normalizzata)
```

Questo significa: "voglio che la cavità sia in `|n⟩`, non mi importa dello stato dei qubit".

### Interpolazione (Smoothing)

Dopo GRAPE, il polso è costante a tratti (gradini). Per renderlo sperimentalmente realizzabile, si applica un'**interpolazione PCHIP** (Piecewise Cubic Hermite Interpolating Polynomial):

```python
cs = PchipInterpolator(tlist_coarse, pulse_coarse)
pulse_smooth = cs(tlist_fine)  # polso liscio su griglia più fine
```

---

## 8. La Pipeline Completa: `run_full_pipeline_2q.py`

### Le 3 Fasi

```
╔══════════════════════════════════════════════════════════╗
║  FASE 1: CRAB (multi-seed)                              ║
║  - 10 ottimizzazioni indipendenti con semi diversi       ║
║  - Seleziona la migliore (fedeltà massima)               ║
╠══════════════════════════════════════════════════════════╣
║  FASE 2: GRAPE (refinement)                              ║
║  - Usa il miglior polso CRAB come initial guess          ║
║  - L-BFGS-B con vincoli di ampiezza                     ║
║  - Migliora la fedeltà e riduce il costo di controllo    ║
╠══════════════════════════════════════════════════════════╣
║  FASE 3: Interpolazione                                  ║
║  - Smoothing PCHIP su griglia temporale più fine         ║
║  - Polso continuo e sperimentalmente realizzabile        ║
║  - Verifica che la fedeltà non degradi                   ║
╚══════════════════════════════════════════════════════════╝
```

### Perché Questa Strategia?

1. **CRAB** esplora il landscape in modo globale (gradient-free) → trova una buona regione
2. **GRAPE** raffina localmente (gradient-based) → alta fedeltà + vincoli
3. **Interpolazione** rende il polso fisicamente realizzabile → smooth

### Output

- File `results.npz` con tutti i polsi e le metriche
- Grafici PDF: `⟨n⟩(t)`, drives, Wigner, FFT

---

## 9. Gli Stati Target

### 9.1 Stato di Fock `|n⟩`

Autostato del numero di fotoni. Stato non-classico con esattamente `n` fotoni nella cavità.

```python
target = basis(dim, n)  # |n⟩ ∈ H_cav
```

Funzione di Wigner: anelli concentrici alternati positivi/negativi.

### 9.2 Stato Squeezed

Stato con incertezza ridotta in una quadratura (a spese dell'altra):

```python
target = squeeze(dim, r * exp(iθ)) * basis(dim, 0)
```

- `r` = parametro di squeezing (in unità lineari)
- `θ` = angolo di squeezing (ruota la direzione di compressione)
- Conversione da dB: `r = r_dB / (20 log₁₀(e)) ≈ r_dB / 8.686`

### 9.3 Stato Cat (Schrödinger)

Sovrapposizione macroscopica di stati coerenti:

```python
|C⁺_α⟩ ∝ |α⟩ + |-α⟩        # even cat state
|ψ_target⟩ ∝ |C⁺_α⟩ - |C⁺_{iα}⟩  # cat-state superposition (Eq. B4)
```

Funzione di Wigner: pattern a scacchiera con frange di interferenza.

### 9.4 Stato di Bell (Solo 2 Qubit)

Stati massimamente entangled dei due qubit:

```python
|Φ⁺⟩ = (|gg⟩ + |ee⟩) / √2
|Φ⁻⟩ = (|gg⟩ - |ee⟩) / √2
|Ψ⁺⟩ = (|ge⟩ + |eg⟩) / √2
|Ψ⁻⟩ = (|ge⟩ - |eg⟩) / √2
```

Questi stati sono una novità del caso a 2 qubit e non hanno analogo nel caso a 1 qubit.

---

## 10. Le Metriche

### 10.1 Fedeltà (Fidelity)

Misura la "vicinanza" tra lo stato preparato e il target:

```
F(ρ, σ) = [Tr(√(√ρ · σ · √ρ))]²
```

- `F = 1`: stati identici
- `F = 0`: stati ortogonali
- Per stati puri: `F = |⟨ψ|φ⟩|²`

**Nell'ottimizzazione** si minimizza l'**infedeltà** `C = 1 - F`.

### 10.2 Costo di Controllo C²

Quantifica l'energia del campo di controllo:

```
C²(T) = ∫₀ᵀ ||H_D(s)||² ds ≈ Σ_k Σ_t [Ω_Dk(t)]² · dt
```

Un costo minore indica un protocollo più efficiente dal punto di vista energetico.

### 10.3 Numero Medio di Fotoni ⟨n⟩(t)

```
⟨n⟩(t) = Tr[ρ(t) · (a†a ⊗ I ⊗ I)]
```

Mostra come la popolazione della cavità evolve nel tempo sotto il controllo ottimo.

---

## 11. Interpretazione dei Grafici

### 11.1 Polsi di Controllo `Ω_D(t)`

- **Forma**: il polso parte e finisce a ~`ω_base` (per CRAB, con la boundary function)
- **Oscillazioni**: modulazioni rapide che sfruttano il DCE per creare eccitazioni
- **Confronto Q1 vs Q2**: con qubit identici, i polsi possono essere molto diversi (la simmetria può rompersi spontaneamente durante l'ottimizzazione)

### 11.2 ⟨n⟩(t) — Media Fotonica

- **Crescita**: il DCE trasferisce energia dal vuoto alla cavità
- **Plateau finale**: indica il raggiungimento dello stato target
- **Oscillazioni**: scambio di eccitazioni tra cavità e qubit

### 11.3 Funzione di Wigner

Rappresentazione quasiprobabilistica nello spazio delle fasi (x, p):
- **Regioni positive**: comportamento "classico"
- **Regioni negative**: indica non-classicità (firma quantistica)
- **Confronto target vs ottimizzato**: l'accordo visivo conferma la fedeltà numerica

### 11.4 Spettro FFT dei Polsi

- **Picco a `2ω_c`**: frequenza caratteristica del DCE parametrico (frequenza di risonanza per la creazione di coppie di fotoni)
- **Contenuto spettrale**: polsi con più armoniche sono generalmente più efficaci ma più difficili da realizzare sperimentalmente

---

## Appendice: Struttura dei File

```
Stage_twoqubits/
├── two_qubit_system.py      ← KERNEL: operatori, Hamiltoniane, target, costi
├── crab_optimizer.py        ← Ottimizzatore CRAB (invariato dal caso 1-qubit)
├── grape_optimizer.py       ← Ottimizzatore GRAPE (invariato dal caso 1-qubit)
├── run_crab_2q.py           ← Script: simulazione CRAB per 2 qubit
├── run_grape_2q.py          ← Script: simulazione GRAPE per 2 qubit
├── run_full_pipeline_2q.py  ← Script: pipeline completa CRAB→GRAPE→Interp.
├── twoqubits.ipynb          ← Notebook originale (1 qubit)
├── main.pdf                 ← Paper di riferimento
└── spiegazione_codice.md    ← Questo file
```
