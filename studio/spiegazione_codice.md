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
12. [Guida Pratica all'Esecuzione, Gestione e Analisi della Simulazione](#12-guida-pratica-allesecuzione-gestione-e-analisi-della-simulazione)

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

Il modulo fornisce costruttori per diversi stati target sia per CRAB (ket del sottosistema cavità o stato congiunto di Bell) sia per GRAPE (operatori nello spazio congiunto a 120 dimensioni):

| Funzione | Stato Target | Spazio | Uso |
|----------|-------------|--------|-----|
| `target_fock_2q(dim, n)` | $\|n\rangle$ della cavità | $\mathcal{H}_{\text{cav}}$ (dim 30) | CRAB (ket cavità) |
| `target_squeezed_2q(dim, r, θ)` | Vuoto squeezed $S(r e^{i\theta})\|0\rangle$ | $\mathcal{H}_{\text{cav}}$ (dim 30) | CRAB (ket cavità) |
| `target_cat_2q(dim, α)` | Cat state $\|C^+_\alpha\rangle - \|C^+_{i\alpha}\rangle$ | $\mathcal{H}_{\text{cav}}$ (dim 30) | CRAB (ket cavità) |
| `target_bell_2q(dim, n, type)` | Stato di Bell dei qubit con cavità in $\|n\rangle$ | $\mathcal{H}_{\text{tot}}$ (dim 120) | CRAB / GRAPE |
| `grape_target_fock_2q(dim, n, ground_qubits=False)` | $\|n\rangle\langle n\| \otimes \mathbb{I}_2 \otimes \mathbb{I}_2$ oppure $\|n, g, g\rangle\langle n, g, g\|$ | $\mathcal{H}_{\text{tot}}$ (dim 120) | GRAPE (operatore target) |
| `grape_target_squeezed_2q(dim, r, θ, ground_qubits=False)` | $\rho_{\text{sq}} \otimes \mathbb{I}_2 \otimes \mathbb{I}_2$ oppure $\|\psi_{\text{sq}}, g, g\rangle\langle \psi_{\text{sq}}, g, g\|$ | $\mathcal{H}_{\text{tot}}$ (dim 120) | GRAPE (operatore target) |
| `grape_target_cat_2q(dim, α, ground_qubits=False)` | $\rho_{\text{cat}} \otimes \mathbb{I}_2 \otimes \mathbb{I}_2$ oppure $\|\psi_{\text{cat}}, g, g\rangle\langle \psi_{\text{cat}}, g, g\|$ | $\mathcal{H}_{\text{tot}}$ (dim 120) | GRAPE (operatore target) |

#### Regola Fondamentale di Normalizzazione in GRAPE
In GRAPE la fedeltà viene valutata tramite l'overlap della traccia:
$$\mathcal{F} = \operatorname{Tr}[O_{\text{target}} \rho(T)]$$
Quando vogliamo generare uno stato nella sola cavità lasciando i qubit liberi (`ground_qubits=False`), l'operatore target è un **proiettore di sottospazio**:
$$O_{\text{target}} = \rho_{\text{cav}} \otimes \mathbb{I}_2 \otimes \mathbb{I}_2$$
dove $\mathbb{I}_4 = \mathbb{I}_2 \otimes \mathbb{I}_2$ ha traccia 4.

> [!IMPORTANT]
> **Non dividere $O_{\text{target}}$ per la sua traccia!**  
> Se si dividesse $O_{\text{target}}$ per $\operatorname{Tr}[O_{\text{target}}] = 4$, l'autovalore massimo dell'operatore scenderebbe a $0.25$, bloccando artificialmente la fedeltà a un quarto del valore reale. Con la corretta definizione del proiettore non normalizzato in traccia:
> $$\operatorname{Tr}[(\rho_{\text{cav}} \otimes \mathbb{I}_4)\rho(T)] = \operatorname{Tr}_{\text{cav}}\Big[\rho_{\text{cav}} \operatorname{Tr}_{\text{qubits}}\big(\rho(T)\big)\Big] = \operatorname{Tr}_{\text{cav}}[\rho_{\text{cav}} \rho_{\text{cav}}(T)] = \mathcal{F}_{\text{cavity}} \in [0, 1]$$
> Se invece si desidera vincolare sia la cavità sia entrambi i qubit nel ground state $|gg\rangle$, basta impostare `ground_qubits=True`: in questo caso l'operatore target diventa la matrice densità pura $|n, g, g\rangle\langle n, g, g|$, che ha traccia 1 per costruzione.

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

**Nota**: GRAPE lavora con **matrici densità** (e operatori Hermitiani nello spazio congiunto $120 \times 120$). Quando il target riguarda solo la cavità, si utilizza il proiettore di sottosistema $O_{\text{target}} = \rho_{\text{cav}} \otimes \mathbb{I}_2 \otimes \mathbb{I}_2$ (non diviso per la traccia di $\mathbb{I}_4$), cosicché l'overlap $\operatorname{Tr}[O_{\text{target}} \rho(T)] = \operatorname{Tr}_{\text{cav}}[\rho_{\text{cav}} \rho_{\text{cav}}(T)] \in [0, 1]$ corrisponde esattamente alla fedeltà sul solo modo della cavità senza vincolare lo stato finale dei qubit. Se invece si impone `ground_qubits=True`, $O_{\text{target}}$ diventa la matrice densità pura congiunta $|n, g, g\rangle\langle n, g, g|$.

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
    fun=self._objective_and_gradient,  # restituisce (1 - F, gradiente analitico)
    x0=x0,                             # parametri interni (senza i bordi)
    args=(psi0, target_state, dt),
    method="L-BFGS-B",
    jac=True,                          # il gradiente è fornito direttamente da fun
    bounds=bounds,                     # vincoli di ampiezza [amp_min, amp_max]
    options={"maxiter": max_iter},
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

Per GRAPE, il target deve essere un operatore nello spazio di Hilbert completo ($120 \times 120$).

Se ci interessa solo lo stato della cavità senza vincolare lo stato finale dei qubit:
```python
# ground_qubits=False (default): proiettore di sottospazio
target_op = grape_target_fock_2q(dim, n=6, ground_qubits=False)
# Matematicamente: O_target = |n⟩⟨n| ⊗ I₂ ⊗ I₂
```
La misura di fedeltà $\operatorname{Tr}[O_{\text{target}} \rho(T)]$ valuta la probabilità che la cavità si trovi in $|n\rangle$, indipendentemente dallo stato dei due qubit. L'operatore non è diviso per la traccia di $\mathbb{I}_4$, evitando la limitazione artificiale a $0.25$.

Se invece si richiede che entrambi i qubit tornino nel loro stato fondamentale $|g, g\rangle$:
```python
# ground_qubits=True: stato puro congiunto
target_dm = grape_target_fock_2q(dim, n=6, ground_qubits=True)
# Matematicamente: ρ_target = |n, g, g⟩⟨n, g, g|
```

### Interpolazione (Smoothing)

Dopo GRAPE, il polso risultante è costante a tratti (gradini discreti). Per renderlo fisicamente realizzabile in laboratorio da un generatore di forme d'onda (AWG), si applica un'**interpolazione PCHIP** (Piecewise Cubic Hermite Interpolating Polynomial):

```python
cs = PchipInterpolator(tlist_coarse, pulse_coarse)
pulse_smooth = cs(tlist_fine)  # polso continuo liscio su griglia fine (es. 4000 punti)
```

**Perché PCHIP e non una spline cubica standard?**  
A differenza delle normali spline cubiche, PCHIP **preserva la monotonicità locale**: non produce sovra-oscillazioni parassite (overshooting) in prossimità dei bordi o delle brusche variazioni di pendenza. Ciò garantisce che il polso lisciato rispetti rigorosamente i limiti fisici di ampiezza `[amp_min, amp_max]` imposti durante l'ottimizzazione GRAPE.

---

## 8. La Pipeline Completa: `run_full_pipeline_2q.py`

### 8.1 Le 3 Fasi di Ottimizzazione

```
╔════════════════════════════════════════════════════════════════════════╗
║  FASE 1: CRAB Parallelo Multi-Seed (Esplorazione Globale)              ║
║  - N semi indipendenti (default 10) eseguiti in parallelo su più core ║
║  - Esplorazione globale dello spazio dei parametri (Nelder-Mead)       ║
║  - Selezione del miglior polso (massima fedeltà raggiunta)             ║
╠════════════════════════════════════════════════════════════════════════╣
║  FASE 2: GRAPE con Vincoli (Raffinamento Locale)                       ║
║  - Utilizza il miglior polso CRAB come punto di partenza (guess)       ║
║  - Discretizzazione su 400 slot e ottimizzazione quasi-Newton L-BFGS-B ║
║  - Vincoli rigidi sull'ampiezza: amp_bound = (0.5, 3.0)                ║
║  - Porta la fedeltà oltre 0.998 e riduce drasticamente il costo C²     ║
╠════════════════════════════════════════════════════════════════════════╣
║  FASE 3: Interpolazione PCHIP e Validazione                            ║
║  - Smoothing con spline cubica Hermite (PCHIP) su griglia fine (4000)  ║
║  - Eliminazione dei gradini discreti senza overshooting                ║
║  - Risimulazione esatta Schrödinger (sesolve) per verifica fedeltà    ║
╚════════════════════════════════════════════════════════════════════════╝
```

### 8.2 Architettura Multiprocessing Cross-Platform

Nello script `run_full_pipeline_2q.py`, la Fase 1 sfrutta appieno l'hardware a disposizione tramite un'architettura robusta e portabile:

1. **Allocazione Dinamica delle Risorse**:
   ```python
   cpu_count = os.cpu_count() or 1
   N_WORKERS = min(CRAB_NUM_SEEDS, max(1, cpu_count - 1))
   ```
   Rileva automaticamente i core logici disponibili nel sistema, lasciando un core libero per mantenere il sistema operativo reattivo.
2. **Compatibilità Cross-Platform (Linux e Windows)**:
   - Su Linux il default storicamente è `fork`, mentre su Windows e macOS viene utilizzato obbligatoriamente `spawn`.
   - Per garantire la massima stabilità su tutti i sistemi operativi, il worker è una funzione a livello modulo (`_crab_worker`) che accetta solo argomenti primitivi serializzabili (niente lambda o lock di QuTiP non-picklable).
   - L'avvio dell'intero script è incapsulato all'interno del blocco `if __name__ == '__main__':`.
3. **Convergenza Naturale (Senza Troncamento Forzato)**:
   - Il parametro `CRAB_MAX_ITER = None` permette a Nelder-Mead di proseguire fino a convergenza numerica delle tolleranze (tolleranze `xatol` e `fatol` a `1e-4`), evitando troncamenti prematuri che degraderebbero la fedeltà.
4. **Streaming Asincrono dei Risultati**:
   - Con `concurrent.futures.as_completed(futures)`, i risultati dei semi vengono stampati a video in ordine di completamento temporale, permettendo di verificare in tempo reale i progressi della simulazione.

### 8.3 Perché Questa Strategia Ibrida Funziona Meglio?

1. **CRAB** evita le trappole dei minimi locali non-fisici grazie alla randomizzazione multi-frequenza globale.
2. **GRAPE** perfeziona la soluzione muovendosi lungo la direzione di massima pendenza calcolata analiticamente con i commutatori quantistici, e rispetta rigorosamente i limiti di sicurezza dell'hardware (`amp_bound`).
3. **Interpolazione PCHIP** trasforma il controllo ideale a gradini in una forma d'onda analogica continua e realizzabile con un AWG da laboratorio.

### 8.4 Output Generati

Tutti gli output vengono salvati nella cartella dedicata `results_2q_pipeline_n<N>/`:
- `results.npz`: dizionario di array NumPy contenente tutti i parametri, i polsi grezzi e lisciati, e le traiettorie di stato.
- `nmean.pdf`: evoluzione temporale della popolazione media di fotoni $\langle n \rangle(t)$.
- `drives_comparison.pdf`: confronto side-by-side tra il polso CRAB di partenza e il polso finale GRAPE/PCHIP per entrambi i qubit.
- `wigner.pdf`: funzione di Wigner bidimensionale calcolata sullo stato finale ridotto della cavità.
- `fft.pdf`: densità spettrale di potenza dei drive per evidenziare la risonanza a $2\omega_c$.

---

## 9. Gli Stati Target

### 9.1 Stato di Fock `|n⟩`

Autostato del numero di fotoni. Stato non-classico con esattamente `n` fotoni nella cavità.

```python
target = basis(dim, n)  # |n⟩ ∈ H_cav
```

> [!NOTE]
> **Vincolo di Parità per gli Stati di Fock**:  
> Poiché lo stato iniziale è $|0, g, g\rangle$ (parità pari $\Pi = +1$) e l'Hamiltoniana preserva la parità, **è possibile generare deterministicamente solo stati di Fock con $n$ pari** ($n = 2, 4, 6, 8, \dots$). La generazione di un fotone singolo $n=1$ o di stati dispari è rigorosamente vietata dalle regole di selezione a meno di non rompere la simmetria di parità.

Funzione di Wigner: anelli concentrici alternati positivi/negativi, con valore al centro $W(0,0) = \frac{2}{\pi}(-1)^n$. Per $n=6$, il centro è un pozzo negativo profondo $\approx -0.135$.

### 9.2 Stato Squeezed

Stato con incertezza ridotta in una quadratura (a spese dell'altra):

```python
target = squeeze(dim, r * exp(iθ)) * basis(dim, 0)
```

- `r` = parametro di squeezing (in unità lineari)
- `θ` = angolo di squeezing (ruota la direzione di compressione)
- Conversione da dB: `r = r_dB / (20 log₁₀(e)) ≈ r_dB / 8.686`

Contiene solo componenti a numero pari di fotoni, quindi è perfettamente compatibile con la conservazione della parità dal vuoto.

### 9.3 Stato Cat (Schrödinger)

Sovrapposizione macroscopica di stati coerenti:

```python
|C⁺_α⟩ ∝ |α⟩ + |-α⟩        # even cat state (parità pari)
|ψ_target⟩ ∝ |C⁺_α⟩ - |C⁺_{iα}⟩  # cat-state superposition a 4 componenti (Eq. B4 del paper)
```

Anche questa combinazione ha parità pari e viene sintetizzata tramite la creazione coordinata di fotoni dal vuoto.

Funzione di Wigner: pattern a scacchiera con frange di interferenza quantistica e ampie regioni a valori negativi.

### 9.4 Stato di Bell (Solo 2 Qubit)

Stati massimamente entangled dei due qubit:

```python
|Φ⁺⟩ = (|gg⟩ + |ee⟩) / √2   # parità di qubit pari (Π_q = +1)
|Φ⁻⟩ = (|gg⟩ - |ee⟩) / √2   # parità di qubit pari (Π_q = +1)
|Ψ⁺⟩ = (|ge⟩ + |eg⟩) / √2   # parità di qubit dispari (Π_q = -1)
|Ψ⁻⟩ = (|ge⟩ - |eg⟩) / √2   # parità di qubit dispari (Π_q = -1)
```

- Se la cavità termina nel vuoto ($|0\rangle$), la conservazione della parità totale permette la transizione verso gli stati $|\Phi^\pm\rangle$.
- Gli stati $|\Psi^\pm\rangle$ hanno parità di qubit dispari, quindi per conservare la parità totale possono essere raggiunti solo se la cavità contiene un numero dispari di fotoni (es. $|1\rangle \otimes |\Psi^\pm\rangle$).
Questi stati di entanglement puro tra i due qubit sono una caratteristica esclusiva del sistema a due qubit.

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

## 12. Guida Pratica all'Esecuzione, Gestione e Analisi della Simulazione

Questa sezione riassume operativamente la logica fisica del codice, i comandi per avviare le simulazioni, come gestire i parametri e come interpretare i dati e i grafici prodotti.

---

### 12.1 Il Procedimento Fisico della Simulazione

L'obiettivo è generare deterministicamente uno stato quantistico non-classico della cavità (come lo stato di Fock $|n=6\rangle$, stati squeezed o cat states) partendo dal **vuoto quantistico congiunto** $|0, g, g\rangle$.

Nel regime di **accoppiamento ultrastro (USC)** ($g/\omega_c = 0.3$), i termini contro-rotanti $(a^\dagger \sigma_+ + a \sigma_-)$ dell'Hamiltoniana di Rabi rompono la conservazione del numero di eccitazioni, permettendo di convertire le fluttuazioni del vuoto in coppie di fotoni reali modulando la frequenza dei qubit nel tempo tramite i campi di controllo $\Omega_{D1}(t)$ e $\Omega_{D2}(t)$ (**Effetto Casimir Dinamico parametrico, DCE**).

Per trovare le forme ottimali di $\Omega_{D1}(t)$ e $\Omega_{D2}(t)$, si segue una **pipeline ibrida a tre fasi**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PIPELINE IBRIDA DI CONTROLLO OTTIMO                  │
├─────────────────────┬───────────────────────┬──────────────────────────┤
│   Fase 1: CRAB      │     Fase 2: GRAPE     │  Fase 3: Interpolazione  │
│  (Esplorazione      │    (Raffinamento      │    (Fattibilità          │
│   Globale)          │     Locale)           │     Sperimentale)        │
│                     │                       │                          │
│  • Gradient-free    │  • Gradient-based     │  • Spline cubica PCHIP   │
│  • Nelder-Mead      │  • L-BFGS-B           │  • Da gradini a liscio   │
│  • Fourier troncat. │  • Vincoli ampiezza   │  • Senza perdita         │
│  • Multi-seed       │  • Trova il minimo    │    di fedeltà            │
│    (parallelo)      │    locale perfetto    │                          │
└─────────────────────┴───────────────────────┴──────────────────────────┘
```

---

### 12.2 Mappa dei File: Cosa Fanno e Come si Collegano

#### Moduli Motore (la logica di calcolo)
1. **`two_qubit_system.py`**:
   - Costruisce lo spazio di Hilbert a **120 dimensioni** ($dim=30 \times 2 \times 2$).
   - Definisce l'Hamiltoniana di drift $H_0$ (cavità + accoppiamenti $g_1, g_2$) e le Hamiltoniane di controllo $H_1 = -\frac{1}{2}\sigma_{z1}$, $H_2 = -\frac{1}{2}\sigma_{z2}$.
   - Costruisce gli stati target e le funzioni di costo (infedeltà della cavità).
2. **`crab_optimizer.py`**:
   - Parametrizza ciascun drive come somma di $N_f$ sinusoidi a frequenze casuali moltiplicate per una funzione di confine $s(t)$ che forza l'accensione e lo spegnimento a zero:
     $$\Omega_{D}(t) = \omega_{\text{base}} + s(t) \sum_{k=1}^{N_f} [A_k \sin(\omega_k t) + B_k \cos(\omega_k t)]$$
   - Ottimizza i coefficienti con il metodo Nelder-Mead (simplesso). Supporta liste arbitrarie di controlli ($N_{\text{controls}} = 2$).
3. **`grape_optimizer.py`**:
   - Discretizza il tempo a tratti ($N_t$ intervalli).
   - Calcola analiticamente i gradienti tramite i commutatori: $\frac{\partial F}{\partial u_j} = -\text{Re}\{\operatorname{Tr}[\lambda_j^\dagger (i \delta t [H_k, \rho_j])] \}$.
   - Usa l'algoritmo quasi-Newton **L-BFGS-B** imponendo vincoli rigidi sulle ampiezze (es. $0.5 \le \Omega_D(t) \le 3.0$).

#### Script di Esecuzione e Notebook
- **`twoqubits.ipynb`**: **Il banco di prova interattivo**. Esegue la pipeline cella per cella e mostra subito i grafici a schermo (Wigner, drive, popolazioni ed FFT).
- **`run_crab_2q.py`**: Script standalone per testare solo la fase CRAB da terminale.
- **`run_grape_2q.py`**: Script standalone per testare solo la fase GRAPE da terminale.
- **`run_full_pipeline_2q.py`**: **Lo script di produzione**. Lancia i seed indipendenti di CRAB in parallelo con multiprocessing cross-platform, sceglie il migliore, lo rifinisce con GRAPE, applica PCHIP e salva tutti i dati e le figure in `results_2q_pipeline_n6/`.

---

### 12.3 I Comandi da Eseguire

Tutti i comandi vanno eseguiti dalla cartella del progetto:

#### A. Attivare l'ambiente virtuale
```bash
source .venv/bin/activate
```
*(In alternativa puoi invocare direttamente l'interprete `.venv/bin/python`)*

#### B. Modalità 1: Lavoro Interattivo (Jupyter Notebook)
Avvia Jupyter:
```bash
jupyter lab
# oppure: jupyter notebook
```
Apri il file `twoqubits.ipynb`:
- **Vantaggio**: Esegui una cella alla volta, vedi i grafici inline e puoi modificare parametri o intervalli di plot senza ricalcolare tutto.

#### C. Modalità 2: Test Rapido da Terminale (solo CRAB)
```bash
python run_crab_2q.py
```
- Esegue un run singolo di CRAB su $|n=6\rangle$, calcola la fedeltà e genera le figure PDF (`crab_2q_nmean.pdf`, `crab_2q_drives.pdf`, `crab_2q_wigner.pdf`, `crab_2q_fft.pdf`).

#### D. Modalità 3: Simulazione Completa di Produzione (in Background con Multiprocessing)
```bash
nohup python run_full_pipeline_2q.py > pipeline.log 2>&1 &
```
Per monitorare lo stato di avanzamento in tempo reale:
```bash
tail -f pipeline.log
```
Al termine troverai tutti i dati salvati nella cartella `results_2q_pipeline_n6/`:
- `results.npz`: array NumPy con tutti i polsi, griglie temporali e fedeltà.
- `nmean.pdf`: andamento della popolazione fotonica.
- `drives_comparison.pdf`: confronto tra i drive CRAB e i drive lisciati.
- `wigner.pdf`: funzione di Wigner finale ad alta risoluzione.
- `fft.pdf`: spettro in frequenza.

---

### 12.4 Come Gestire i Parametri Fisici e Numerici

| Parametro | Posizione | Significato e Suggerimenti |
| :--- | :--- | :--- |
| `n_target` | cella 3 notebook o riga 71 `run_full_pipeline_2q.py` | Numero di fotoni dello stato di Fock. **Attenzione**: deve essere **pari** ($n=2, 4, 6, 8$) per la conservazione della parità partendo da $|0, g, g\rangle$. |
| `dim = 30` | setup iniziale | Troncamento dello spazio di Fock. 30 va benissimo fino a $n=8$. Se provi $n=10$, alza a `dim = 35` o `40`. |
| `CRAB_NUM_SEEDS = 10` | `run_full_pipeline_2q.py` | Numero di tentativi casuali con CRAB. Più seed provi, più è probabile trovare il minimo globale assoluto con $F > 0.98$. |
| `amp_bound = (0.5, 3.0)` | GRAPE | Limiti fisici di ampiezza del drive $\Omega_D(t)/\omega_c$. Impediscono di generare campi irrealistici che riscalderebbero il criostato. |
| `ground_qubits = False` | `grape_target_*` | Se `False` (default), ottimizza la cavità a prescindere dai qubit. Se `True`, impone che a $t=T$ entrambi i qubit tornino in $|g, g\rangle$. |

---

### 12.5 Come Analizzare i Risultati (Interpretazione dei Grafici)

1. **Popolazione Media $\langle n \rangle(t)$**:
   - Parte da $0$ a $t=0$ e oscilla salendo gradualmente nel tempo.
   - All'istante finale $t=T$, la curva deve attestarsi esattamente sul valore desiderato (es. $\langle n \rangle(T) \approx 6.0$).
2. **Forme d'Onda dei Due Drive $\Omega_{D1}(t)$ e $\Omega_{D2}(t)$**:
   - Devono partire da $\Omega_{\text{base}} = 2.0$ a $t=0$, variare in modo continuo e tornare a $2.0$ a $t=T$ (spegnimento morbido senza shock).
   - I due drive sono diversi tra loro: l'ottimizzatore sfrutta una strategia cooperativa asimmetrica per interferire costruttivamente nella cavità.
3. **Spettro in Frequenza (FFT)**:
   - Presenta un picco netto e prominente centrato su **$\omega \approx 2\omega_c$**. Questa è la firma fisica fondamentale del DCE parametrico: modulare il qubit al doppio della frequenza di risonanza estrae coppie di fotoni dal vuoto.
4. **Funzione di Wigner $W(x, p)$**:
   - Per lo stato di Fock $|n=6\rangle$, presenta **$n=6$ anelli concentrici** alternati di valore positivo (rosso) e negativo (blu).
   - La presenza di valori fortemente negativi al centro ($\approx -0.135$) è la prova inconfutabile della non-classicalità dello stato preparato.
5. **Tabella delle Metriche**:
   - **Fedeltà $F$**: $F \ge 0.95$ per CRAB; dopo GRAPE e PCHIP si raggiungono valori d'eccellenza $F \ge 0.998$.
   - **Costo energetico $C^2$**: GRAPE e PCHIP abbattono notevolmente il costo energetico rispetto al polso CRAB grezzo, grazie ai vincoli di ampiezza.

---

### 12.6 Il Multiprocessing Cross-Platform

Nello script `run_full_pipeline_2q.py`, i 10 seed di CRAB vengono eseguiti in parallelo sfruttando `concurrent.futures.ProcessPoolExecutor`:
- Rileva automaticamente i core disponibili (`os.cpu_count()`) e alloca fino a `N_WORKERS = min(CRAB_NUM_SEEDS, max(1, cpu_count - 1))`.
- È protetto da `if __name__ == '__main__':` e utilizza solo tipi serializzabili, garantendo la compatibilità sia con il meccanismo `spawn` di **Windows** e macOS sia con il sistema di **Linux**.
- Grazie a `as_completed`, stampa a video il progresso in tempo reale non appena ciascun seed completa il calcolo.

---

## Appendice: Struttura dei File

```
Stage_twoqubits/
├── two_qubit_system.py      ← KERNEL: operatori, Hamiltoniane, target, costi
├── crab_optimizer.py        ← Ottimizzatore CRAB multi-controllo
├── grape_optimizer.py       ← Ottimizzatore GRAPE multi-controllo (L-BFGS-B e gradiente)
├── run_crab_2q.py           ← Script standalone: simulazione CRAB per 2 qubit
├── run_grape_2q.py          ← Script standalone: simulazione GRAPE per 2 qubit
├── run_full_pipeline_2q.py  ← Script: pipeline completa parallela (CRAB→GRAPE→PCHIP)
├── twoqubits.ipynb          ← Notebook interattivo per la simulazione a 2 qubit
├── main.pdf                 ← Paper scientifico di riferimento
├── results_2q_pipeline_n6/  ← Cartella con risultati .npz e grafici PDF salvati
└── spiegazione_codice.md    ← Questo documento
```

