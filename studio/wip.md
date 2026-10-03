# Work in Progress (WIP): Studio di Fattibilità Fisica ed Efficienza Quantistica (2 Qubit vs 1 Qubit)

## 1. Obiettivo della Ricerca

Verificare se e in che misura l'introduzione di **due qubit di controllo indipendenti** accoppiati a una singola cavità in regime di accoppiamento ultrastro (**USC**, $g/\omega_c \gtrsim 0.1$):
1. **Renda i campi di controllo fisicamente realizzabili** da generatori di forme d'onda reali (**AWG** - Arbitrary Waveform Generator) e linee di polarizzazione a microonde in *circuit-QED*, eliminando le oscillazioni ad altissima frequenza e i gradienti temporali repentini (elevato *slew rate*) richiesti nel caso a singolo qubit.
2. **Aumenti l'efficacia e l'efficienza quantistica** nella generazione deterministica di stati non-classici della cavità (stati di Fock $|n\rangle$, stati squeezed e gatti di Schrödinger) tramite Effetto Casimir Dinamico parametrico (**DCE**).

---

## 2. Il Problema Aperto: I Limiti dell'Attuazione con 1 Qubit

Nel modello standard con 1 solo qubit (come studiato nel paper di riferimento):
- **Unico canale di controllo**: Tutto il carico energetico e spettrale necessario a estrarre quanti dal vuoto quantistico è convogliato su un solo grado di libertà, $\Omega_D(t)$.
- **Richieste irrealistiche sull'attuatore**:
  - **Alte frequenze**: L'algoritmo di controllo ottimo sintetizza componenti spettrali rapide (fino a $4\omega_c - 6\omega_c$) per guidare la dinamica non-lineare nel tempo $T$.
  - **Slew Rate estremo**: La derivata temporale $|d\Omega_D(t)/dt|$ presenta picchi bruschi, che richiederebbero tempi di salita (*rise time*) prossimi allo zero.
  - **Banda passante limitata in laboratorio**: I cavi coassiali criogenici, gli attenuatori termici e i convertitori digitale-analogico (DAC) dei criostati a diluizione fungono da **filtro passa-basso naturale**. Se il segnale teorico supera la banda passante dell'hardware, il filtro ne taglia le componenti rapide, provocando un **crollo drastico della fedeltà effettiva $F$**.
  - **Riscaldamento ed eccitazioni parassite**: Spingere un singolo qubit a frequenze e ampiezze estreme introduce calore nel criostato ($15\text{ mK}$) e rischia di far uscire il transmon dal sottospazio a due livelli $\{|g\rangle, |e\rangle\}$, eccitando i livelli non-computazionali ($|f\rangle, |h\rangle$).

---

## 3. Ipotesi Fondamentale dei 2 Qubit

La presenza di due qubit controllabili introduce due vantaggi fisici e strutturali:

1. **Attuazione Distribuita e Cooperativa**:
   L'Hamiltoniana di interazione cavità-qubit nello spazio congiunto è:
   $$H_I = (a + a^\dagger)\left(g_1 \sigma_{x1} + g_2 \sigma_{x2}\right)$$
   I due campi di controllo $\Omega_{D1}(t)$ e $\Omega_{D2}(t)$ modulano i due qubit in modo indipendente. L'eccitazione del campo di cavità avviene per **interferenza quantistica costruttiva**: i due attuatori si dividono lo sforzo, consentendo forme d'onda più morbide, frequenze più basse e minori derivate temporali.

2. **Cooperatività Quantistica ($g_{\text{eff}} \sim \sqrt{2}g$)**:
   Con due qubit identici ($g_1 = g_2 = g$), l'accoppiamento collettivo scala come $g_{\text{eff}} = \sqrt{g_1^2 + g_2^2} \approx 1.414 g$.
   Poiché la probabilità di emissione parametrica di coppie di fotoni DCE scala quadraticamente con l'accoppiamento ($\propto g^2$), la sorgente di fotoni è intrinsecamente più reattiva: a parità di spinta dei drive, si possono generare più fotoni o completare la sintesi in un tempo $T$ sensibilmente inferiore.

---

## 4. Metodologia di Verifica Sperimentale-Numerica (I 4 Test Chiave)

Per trasformare questa ipotesi in un risultato scientifico solido e quantitativo, si definiscono quattro verifiche comparative sistematiche tra il sistema a 1 qubit e il sistema a 2 qubit.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   ROADMAP DI VERIFICA SPERIMENTALE                     │
├─────────────────────┬───────────────────────┬──────────────────────────┤
│       Test 1        │        Test 2         │          Test 3          │
│  Benchmark Diretto  │  Metriche Fisiche     │  Filtro Passa-Basso      │
│  (1Q vs 2Q)         │  di Realizzabilità    │  Hardware                │
│                     │                       │                          │
│  • Stessi parametri │  • Slew Rate (dΩ/dt)  │  • Taglio alle alte freq │
│  • Stesso tempo T   │  • Banda spettrale    │  • Simulazione AWG reale │
│  • Stesso stato |n⟩ │    al 99% (FFT)       │  • Curva F vs ω_cut      │
│  • GRAPE + PCHIP    │  • Costo C² per linea │  • Tenuta della fedeltà  │
└─────────────────────┴───────────────────────┴──────────────────────────┘
```

---

### Test 1: Benchmark Diretto Bilanciato (1 Qubit vs 2 Qubit)

Simulazione della pipeline completa (CRAB $\to$ GRAPE $\to$ PCHIP) per entrambi i sistemi impostando condizioni identiche:
- Frequenza cavità: $\omega_c = 1.0$
- Troncamento spazio di Fock: $\text{dim} = 30$
- Durata del protocollo: $T = 30/\omega_c$
- Stato target: Fock $|n=6\rangle$ (e poi $|n=2, 4, 8\rangle$)
- Vincoli di ampiezza in GRAPE: $\Omega_D(t)/\omega_c \in [0.5, 3.0]$

#### Due modalità di confronto sull'accoppiamento:
1. **Confronto a parità di $g$ locale ($g_1 = g_2 = g_{\text{1Q}} = 0.3$)**:
   Mostra il beneficio complessivo derivante dalla cooperatività collettiva unita alla presenza di due canali indipendenti.
2. **Confronto a parità di accoppiamento globale ($g_1 = g_2 = 0.3/\sqrt{2} \approx 0.212$ vs $g_{\text{1Q}} = 0.3$)**:
   Isola in modo rigoroso il ruolo puramente geometrico e dinamico dei **due canali di controllo indipendenti**, azzerando il vantaggio puramente energetico della cooperatività di accoppiamento.

---

### Test 2: Metriche Quantitative di Morbidezza e Fattibilità dell'Attuatore

Per ciascun polso lisciato finale $\Omega_D(t)$ (campionato a $N = 4000$ punti temporali con passo $\Delta t = T/N$), calcolare le seguenti grandezze:

1. **Slew Rate Massimo ($\text{SR}_{\max}$)**:
   $$\text{SR}_{\max} = \max_{t} \left| \frac{d\Omega_D(t)}{dt} \right|$$
   *Obiettivo*: verificare che $\text{SR}_{\max}^{(2Q)} < \text{SR}_{\max}^{(1Q)}$. Se verificato, l'attuatore reale può avere un rise-time più lento.

2. **Slew Rate Quadratico Medio ($\text{SR}_{\text{rms}}$)**:
   $$\text{SR}_{\text{rms}} = \sqrt{\frac{1}{T} \int_0^T \left(\frac{d\Omega_D(t)}{dt}\right)^2 dt}$$
   Misura la "nervosità" globale dell'intero profilo temporale.

3. **Banda Passante Efficace al 99% della Potenza ($\omega_{99\%}$)**:
   Dallo spettro di potenza $S(\omega) = |\tilde{\Omega}_D(\omega)|^2$ calcolato tramite FFT, trovare la frequenza $\omega_{99\%}$ tale che:
   $$\int_0^{\omega_{99\%}} S(\omega) d\omega = 0.99 \int_0^{\infty} S(\omega) d\omega$$
   *Obiettivo*: verificare che $\omega_{99\%}^{(2Q)} < \omega_{99\%}^{(1Q)}$, provando che 2 qubit richiedono convertitori DAC a banda più stretta.

4. **Costo Energetico Integrato ($C^2$)**:
   - Per 1 qubit: $C^2 = \int_0^T \Omega_D(t)^2 dt$
   - Per 2 qubit: $C^2_{\text{tot}} = \int_0^T [\Omega_{D1}(t)^2 + \Omega_{D2}(t)^2] dt$
   - Costo massimo per singolo canale: $C^2_{\text{channel}} = \max\left( \int_0^T \Omega_{D1}^2 dt, \int_0^T \Omega_{D2}^2 dt \right)$
   *Obiettivo*: verificare che ciascuna singola linea criogenica sia sollecitata a livelli di potenza inferiori rispetto alla singola linea del caso a 1 qubit.

---

### Test 3: La "Prova del Nove" — Simulazione di Robustezza al Filtro Passa-Basso Hardware

Questa è la dimostrazione sperimentale numerica definitiva:

1. Si prendono i polsi ottimali lisciati $\Omega_D(t)$ ottenuti per 1 qubit e per 2 qubit.
2. Si applica un **filtro passa-basso digitale** (ad esempio un filtro IIR Butterworth del 4° ordine o filtro causale ad eliminazione delle armoniche elevate) con frequenza di taglio variabile:
   $$\omega_{\text{cut}} \in [8.0, 6.0, 5.0, 4.0, 3.5, 3.0, 2.5, 2.0]\, \omega_c$$
3. Si propaga l'equazione di Schrödinger esatta (`sesolve`) utilizzando il polso **filtrato** $\Omega_{D, \text{filtered}}(t)$.
4. Si traccia la curva di **degradazione della fedeltà**:
   $$\mathcal{F} \quad \text{vs} \quad \omega_{\text{cut}}$$
5. **Criterio di Successo**:
   - Se il sistema a 1 qubit vede la fedeltà crollare al di sotto di $0.90$ già a $\omega_{\text{cut}} = 4\omega_c$,
   - mentre il sistema a 2 qubit mantiene una fedeltà elevata ($F \ge 0.98$) anche a frequenze di taglio più aggressive ($\omega_{\text{cut}} \approx 2.5\omega_c - 3\omega_c$),
   - **si ottiene la prova inconfutabile che i 2 qubit rendono l'attuatore realizzabile con l'elettronica da laboratorio disponibile oggi**.

---

### Test 4: Quantum Speed Limit (Tempo Minimo $T$)

Studio dell'efficacia temporale del protocollo:
- Riduzione progressiva del tempo totale di pilotaggio:
  $$T = 30/\omega_c \longrightarrow 25/\omega_c \longrightarrow 20/\omega_c \longrightarrow 15/\omega_c \longrightarrow 10/\omega_c$$
- Ottimizzazione di 1Q e 2Q con gli stessi vincoli di ampiezza.
- **Obiettivo**: Determinare il tempo minimo $T_{\min}$ per cui è ancora possibile raggiungere la soglia di fedeltà $F \ge 0.99$.
- *Vantaggio atteso*: Un tempo $T$ più breve riduce l'esposizione del sistema ai canali di decoerenza e perdita di fotoni della cavità reale (tempo di vita $\tau_{\text{cav}} = 1/\kappa$).

---

## 5. Implementazione Effettiva: Il Runner Unificato `run_simulation.py`

Il benchmark comparativo e le metriche di fattibilità fisica sono stati interamente unificati nello script **`run_simulation.py`**. Questo strumento automatizza l'intera pipeline di controllo quantistico per il sistema a **1 qubit**, **2 qubit** o in modalità comparativa simultanea **`both`**:

```
┌────────────────────────────────────────────────────────────────────────┐
│             PIPELINE AUTOMATICA UNIFICATA (run_simulation.py)          │
├─────────────────────┬───────────────────────┬──────────────────────────┤
│   Fase 1: CRAB      │     Fase 2: GRAPE     │  Fase 3: Interpolazione  │
│  (Esplorazione      │    (Raffinamento      │    (Fattibilità          │
│   Globale)          │     Locale)           │     Sperimentale)        │
│                     │                       │                          │
│  • Gradient-free    │  • Gradient-based     │  • Spline cubica PCHIP   │
│  • Nelder-Mead      │  • L-BFGS-B           │  • Da gradini a liscio   │
│  • Fourier troncat. │  • Vincoli ampiezza   │  • Senza perdita         │
│  • Multi-seed       │  • Trova il minimo    │    di fedeltà            │
│    (parallelo CPU)  │    locale perfetto    │  • Calcolo metriche AWG  │
└─────────────────────┴───────────────────────┴──────────────────────────┘
```

### Funzionalità Implementate nel Runner:
1. **Multiprocessing Cross-Platform**: esegue i semi casuali di CRAB in parallelo (`ProcessPoolExecutor`) rilevando automaticamente i core logici disponibili.
2. **Supporto Multi-Target**: Fock $|n\rangle$ (anche a elevata eccitazione), stati squeezed $S(r, \theta)|0\rangle$ (in unità lineari o dB) e Schrödinger cat superpositions a 4 componenti $C^+_\alpha - C^+_{i\alpha}$.
3. **Calcolo Automatico delle Metriche Fisiche dell'Attuatore**:
   - Slew Rate Massimo: $\text{SR}_{\max} = \max_t |d\Omega/dt|$
   - Slew Rate Quadratico Medio: $\text{SR}_{\text{rms}} = \sqrt{\frac{1}{T}\int_0^T (d\Omega/dt)^2 dt}$
   - Costo Energetico per Singolo Canale: $C_k^2 = \int_0^T \Omega_{Dk}(t)^2 dt$
   - Banda Passante Efficace al 99% della Potenza: $\omega_{99\%}$ via FFT
4. **Reportistica Interattiva Automatica**:
   - In modalità `both`, crea una cartella gerarchica contenente i sottoprogetti `1q/` e `2q/` e un report di confronto side-by-side **`comparison_report.html`** con schede colorate, grafici vettoriali PDF/PNG e tabelle analitiche delle differenze percentuali.

---

## 6. Risultati Preliminari Ottenuti: Prove Empiriche del Vantaggio 2Q

### 6.1 Benchmark Fock $|n=10\rangle$ a Tempo Ridotto ($T = 10\,\tau_s$) — Prova del Quantum Speed Limit
La prima conferma sperimentale-numerica del vantaggio dei 2 qubit è emersa dal test su stato di Fock altamente eccitato **$|n=10\rangle$** con tempo di pilotaggio ridotto **$T = 10\,\tau_s$** (cartella `results_both_fock_n10_dim40_T10taus`):

| Metrica Chiave | 1 Qubit (1Q) | 2 Qubit (2Q) | Differenza / Vantaggio 2Q |
| :--- | :---: | :---: | :---: |
| **Fedeltà CRAB (Best Seed)** | `0.9698` | `0.9578` | Esplorazione globale analoga |
| **CRAB Mean ± Std (Landscape)** | `0.9097 ± 0.0579` | `0.9433 ± 0.0201` | **Dispersione quasi 3x inferiore**: landscape 2Q molto più denso di ottimi |
| **Fedeltà GRAPE (L-BFGS-B)** | `0.8720` | `0.9988` | **+12.68%**: 1Q intrappolato, 2Q converge a quasi 1 |
| **Fedeltà Finale PCHIP Smoothed** | **`0.8397`** (Crollo) | **`0.9622`** (Eccellente) | **+12.25%**: 1Q fallisce all'atto pratico, 2Q realizzabile |
| **Costo Canale Max ($C^2_{\text{ch}}$)** | `220.20` | `217.17` | Costo per singola linea inferiore |

> [!IMPORTANT]
> **Interpretazione Fisica (Fock |n=10⟩ a T=10τs):**  
> A $T = 10\,\tau_s$, un singolo qubit non ha sufficiente reattività parametrica per estrarre 10 fotoni dal vuoto entro i vincoli di ampiezza imposti. Per compensare, GRAPE genera discontinuità ad alta frequenza che vengono distrutte dallo smoothing PCHIP ($\mathcal{F} \approx 0.84$). Al contrario, i **due qubit cooperano costruttivamente**: GRAPE raggiunge $\mathcal{F} = 0.9988$ e il polso lisciato mantiene una fedeltà del $96.2\%$, provando l'estensione del **Quantum Speed Limit**.

---

### 6.2 Benchmark Cat State a 4 Componenti ($\alpha = 2.0$, $T = 15\,\tau_s$) — Prova della Morbidezza dell'Attuatore
Il test sullo stato gatto ortogonale a 4 componenti (cartella `results_both_cat_2.00_dim40_T15taus`) ha evidenziato in modo netto i **vantaggi fisici sull'elettronica di controllo**:

| Metrica Attuatore | 1 Qubit (1Q) | 2 Qubit (2Q - Qubit 1) | Vantaggio 2Q |
| :--- | :---: | :---: | :---: |
| **Slew Rate Massimo ($\max|d\Omega/dt|$)** | `6.333` | **`5.116`** | **-19.2%** (polsi notevolmente più dolci) |
| **Slew Rate RMS** | `1.738` | **`1.523`** | **-12.4%** (minore nervosità globale) |
| **Banda Passante al 99% ($\omega_{99\%}$)** | `6.47` $\omega_c$ | **`5.43` $\omega_c$** | **-16.1%** (meno armoniche ad alta freq.) |
| **Costo Energetico Singolo Canale ($C_k^2$)** | `340.35` | **`328.65`** | **-3.4%** (minor riscaldamento per linea) |
| **Fedeltà GRAPE pre-smoothing** | `0.99935` | **`0.99956`** | Convergenza quasi unitaria in entrambi |

> [!TIP]
> **Nota Tecnica sulla Discretizzazione Temporale ($N_t$):**  
> Per durate temporali ampie ($T = 15\,\tau_s \approx 78.5/\omega_c$), 150 slot GRAPE corrispondono a un passo $\Delta t \approx 0.53/\omega_c$. Poiché lo stato cat ha una struttura d'interferenza a scacchiera fine nello spazio delle fasi, lo smoothing PCHIP da soli 150 punti perde fedeltà (scendendo a $\approx 0.898$). Per durate $T \ge 15\,\tau_s$, impostare `--grape-nt 250` o `300` per mantenere $\mathcal{F}_{\text{smooth}} > 0.98$ preservando la risoluzione fine.

---

## 7. Le 5 Configurazioni Strategiche di Simulazione per `run_simulation.py`

Per strutturare i capitoli numerici della tesi e dimostrare in modo inoppugnabile i singoli aspetti del vantaggio dei 2 qubit, sono state individuate **5 configurazioni mirate**:

```
┌────────────────────────────────────────────────────────────────────────┐
│              LE 5 CONFIGURAZIONI STRATEGICHE DI SIMULAZIONE            │
├─────────────────────┬───────────────────────┬──────────────────────────┤
│ Configurazione 1    │ Configurazione 2      │ Configurazione 3         │
│  Quantum Speed      │  Vincoli Stretti      │  Isolamento del          │
│  Limit (QSL)        │  di Ampiezza Drive    │  Controllo (g_eff)       │
│                     │                       │                          │
│ • T = 10 -> 8 taus  │ • amp_bound (1.2, 2.8)│ • g1 = g2 = 0.212        │
│ • Fock |n=10>       │ • Fock |n=8>          │ • Pareggio g_1Q = 0.3    │
│ • Corsa contro κ    │ • No leakage transmon │ • Vantaggio geometrico   │
├─────────────────────┼───────────────────────┴──────────────────────────┤
│ Configurazione 4    │ Configurazione 5                                 │
│  Stati Cat a        │  Banda Stretta dell'AWG                          │
│  4 Componenti       │  (Filtro Anti-Armoniche)                         │
│                     │                                                  │
│ • Cat α = 2.0       │ • crab_freq_max = 2.3 ω_c                        │
│ • Simmetria di fase │ • grape_nt = 100 slots                           │
│ • Pattern scacchiera│ • Dimostra fattibilità con DAC standard          │
└─────────────────────┴──────────────────────────────────────────────────┘
```

---

### Configurazione 1: Regime di Quantum Speed Limit ($T \le 10\,\tau_s \to 8\,\tau_s$)
* **Obiettivo:** Misurare il tempo minimo $T_{\min}$ sotto il quale la fedeltà del sistema a 1 qubit collassa, mentre 2 qubit continuano a generare stati ad alta fedeltà ($\mathcal{F} \ge 0.95$).
* **Importanza per la tesi:** Dimostra che 2Q permette di completare la generazione prima che la decoerenza e la fuga di fotoni dalla cavità (tempo di vita $\tau_{\text{cav}} = 1/\kappa$) degradino lo stato.
* **Parametri:**
  - `--system both --target fock --param 10 --dim 40`
  - Scansione temporale: `--factor-taus 10.0` $\to$ `--factor-taus 8.0` $\to$ `--factor-taus 7.0`
* **Comando:**
  ```bash
  python run_simulation.py --system both --target fock --param 10 --dim 40 --factor-taus 8.0
  ```

---

### Configurazione 2: Vincoli Stringenti sull'Ampiezza del Drive (Fattibilità Transmon)
* **Obiettivo:** Evitare l'uscita dal modello a due livelli (leakage verso il secondo stato eccitato $|f\rangle$ o ionizzazione del transmon) e minimizzare il carico termico sul criostato a diluizione (15 mK).
* **Meccanismo fisico:** Con vincoli di ampiezza stretti attorno al valore base $\omega_{\text{base}} = 2.0$ (ad es. $\Omega_D(t)/\omega_c \in [1.2, 2.8]$ invece del permissivo $[0.5, 3.0]$), il singolo qubit non ha sufficiente escursione dinamica per pompare molti fotoni; due qubit sommano le rispettive oscillazioni per interferenza quantistica costruttiva.
* **Parametri:**
  - In `run_simulation.py`: impostare `GRAPE_AMP_BOUND = (1.2, 2.8)`
  - Target: Fock $|n=8\rangle$ o $|n=10\rangle$, durata $T = 15\,\tau_s$, $\text{dim} = 35$
* **Comando:**
  ```bash
  python run_simulation.py --system both --target fock --param 8 --dim 35 --factor-taus 15.0
  ```

---

### Configurazione 3: Isolamento del Canale di Controllo (Parità di $g$ Collettivo)
* **Obiettivo:** Separare in modo matematicamente rigoroso il vantaggio dovuto al raddoppio dell'accoppiamento collettivo ($g_{\text{eff}} = \sqrt{g_1^2+g_2^2} = \sqrt{2}g$) dal **vantaggio puramente geometrico e dinamico di avere due canali di controllo indipendenti**.
* **Impostazione:**
  - Sistema 1Q: $g = 0.3$
  - Sistema 2Q: $g_1 = g_2 = \frac{0.3}{\sqrt{2}} \approx 0.21213 \implies g_{\text{collettivo}} = \sqrt{g_1^2+g_2^2} = 0.3$
* **Cosa verificare:** A parità di accoppiamento globale, il sistema a 2Q mostra comunque un **Slew Rate massimo inferiore** e una **Banda al 99% più concentrata**, provando che due modulatori indipendenti "lisciano" naturalmente le traiettorie nello spazio degli stati.
* **Parametri:** Modificare temporaneamente $G_1 = G_2 = 0.21213$ in `run_simulation.py` ed eseguire su Fock $|n=6\rangle$ con $T = 20\,\tau_s$.

---

### Configurazione 4: Target ad Alta Non-Gaussianità — Stati Cat a 4 Componenti ($\alpha \ge 2.0$)
* **Obiettivo:** Verificare la sintesi deterministica di stati con interferenza complessa nello spazio delle fasi (la superposizione su assi ortogonali $C^+_\alpha - C^+_{i\alpha}$, Eq. B4 del paper di riferimento).
* **Meccanismo fisico:** Con $\alpha = 2.0$, il numero medio di fotoni è $\langle n \rangle \approx 4$, ma lo stato presenta un reticolo di Wigner a scacchiera con forti negatività sia lungo l'asse $x$ sia lungo $p$. Con un solo qubit la simmetria quadripolare deve essere forzata sequenzialmente nel tempo; con due qubit la rottura di simmetria di fase tra i due drive sintetizza naturalmente i quattro lobi coerenti.
* **Parametri:**
  - `--system both --target cat --param 2.0 --dim 40 --factor-taus 15.0 --crab-seeds 8`
* **Comando:**
  ```bash
  python run_simulation.py --system both --target cat --param 2.0 --dim 40 --factor-taus 15.0
  ```

---

### Configurazione 5: Banda Spettrale Stretta dell'AWG (Filtro Anti-Armoniche Rapide)
* **Obiettivo:** Dimostrare che il sistema a 2 qubit opera efficacemente anche se l'elettronica di controllo ha una banda passante limitata e taglia le frequenze elevate.
* **Meccanismo fisico:** Un generatore di forme d'onda commerciale e le linee coassiali criogeniche filtrano le armoniche oltre $3\omega_c - 4\omega_c$. Limitando la ricerca CRAB a $\omega \le 2.3\,\omega_c$ (subito sopra la risonanza DCE $2\omega_c$) e riducendo gli slot temporali GRAPE a $N_t = 100$ (fissando la frequenza di Nyquist a $\omega_{\text{Nyq}} \approx 5\omega_c$), si verifica se 2Q riesce a raggiungere il target usando solo la frequenza di risonanza fondamentale.
* **Parametri:**
  - `--system both --target fock --param 6 --dim 30 --factor-taus 15.0 --crab-freq-max 2.3 --grape-nt 100`
* **Comando:**
  ```bash
  python run_simulation.py --system both --target fock --param 6 --dim 30 --factor-taus 15.0 --crab-freq-max 2.3 --grape-nt 100
  ```

---

## 8. Cheat-Sheet dei Comandi CLI per `run_simulation.py`

| Test / Obiettivo | Comando da Eseguire | Note / Risultato Atteso |
| :--- | :--- | :--- |
| **QSL Fock \|n=10⟩ (T=10 taus)** | `python run_simulation.py --system both --target fock --param 10 --dim 40 --factor-taus 10.0` | 2Q raggiunge $\mathcal{F} > 0.96$, 1Q crolla a $\sim 0.84$ |
| **QSL Fock \|n=10⟩ Estremo (T=8 taus)** | `python run_simulation.py --system both --target fock --param 10 --dim 40 --factor-taus 8.0` | Test limite del Quantum Speed Limit collettivo |
| **Cat Superposition (α=2.0, T=15 taus)** | `python run_simulation.py --system both --target cat --param 2.0 --dim 40 --factor-taus 15.0` | Confronto fedeltà Wigner a scacchiera su 4 lobi |
| **Banda Stretta / Low Slew Rate** | `python run_simulation.py --system both --target fock --param 6 --dim 30 --factor-taus 15.0 --crab-freq-max 2.3 --grape-nt 100` | Slew rate 2Q ridotto e banda 99% concentrata a $2\omega_c$ |
| **Test Squeezing Spinto (r=1.2 ~ 10 dB)** | `python run_simulation.py --system both --target squeezed --param 1.2 --dim 35 --factor-taus 15.0` | Generazione rapida di stati compressi non-classici |

---

## 9. Criteri di Valutazione per la Tesi nei Report Comparativi

All'interno di ogni esecuzione in modalità `both`, consultare il file `comparison_report.html`:

1. **Card Fedeltà Finale Smoothed ($\mathcal{F}_{\text{smooth}}$)**:
   - Se 2Q supera 1Q di oltre il $5\%-15\%$, si ha la dimostrazione quantitativa del vantaggio di cooperatività.
2. **Tabella "Metriche Fisiche dell'Attuatore"**:
   - **Slew Rate Massimo ($\max |d\Omega/dt|$)**: un valore inferiore per 2Q prova che l'AWG non deve compiere variazioni di tensione repentine.
   - **Banda al 99% ($\omega_{99\%}$)**: un valore più basso per 2Q certifica che lo spettro RF del segnale è compatibile con i filtri passa-basso criogenici commerciali.
   - **Costo Energetico Massimo per Canale ($\max(C_1^2, C_2^2)$)**: un valore sensibilmente inferiore rispetto al costo dell'unico canale di 1Q prova che ciascuna linea criogenica disperde meno calore nel criostato a diluizione.
3. **Dispersione dei Seed CRAB (Media $\pm$ Deviazione Standard)**:
   - Una deviazione standard molto più piccola per 2Q prova che il *control landscape* a due qubit è privo di falsi minimi locali e converge in modo robusto e deterministico.

---

## 10. Questioni Aperte da Approfondire (Note per il Relatore)

1. **Interazione Diretta Qubit-Qubit ($H_{qq}$)**:
   - Nel modello attuale, i due qubit non interagiscono direttamente tra loro ($J = 0$), ma solo per mediazione della cavità.
   - *Domanda da porre*: ha senso fisico/sperimentale aggiungere un accoppiamento diretto (es. dipolare $XX+YY$ o capacitivo/induttivo $J (\sigma_{x1}\sigma_{x2} + \sigma_{y1}\sigma_{y2})$), oppure è preferibile tenerli spazialmente distanziati per massimizzare l'indipendenza dei drive?
2. **Asimmetria Sperimentale**:
   - Cosa succede se i due qubit non sono perfettamente identici ($g_1 \neq g_2$ o $\omega_{q1} \neq \omega_{q2}$)?
   - Il controllo ottimo si adatta naturalmente a compensare le asimmetrie costruttive?
3. **Dissipazione Aperta (Equazione Master di Lindblad)**:
   - Valutare la robustezza in presenza di perdita di fotoni di cavità $\kappa$ e dephasing dei qubit $\gamma_\phi$. Se il tempo $T$ necessario con 2 qubit è minore, le perdite totali integrate saranno inferiori.

