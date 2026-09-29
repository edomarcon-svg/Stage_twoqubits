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

## 5. Struttura del Codice per le Verifiche

Per implementare questi test in modo pulito e modulare, si prevede la creazione dei seguenti strumenti:

1. **`benchmark_1q_vs_2q.py`**:
   - Esegue la pipeline sia sul sistema a 1 qubit sia sul sistema a 2 qubit.
   - Calcola la tabella comparativa riassuntiva:
     | Metrica | 1 Qubit | 2 Qubit (Q1 / Q2) | Guadagno / Rapporto |
     | :--- | :--- | :--- | :--- |
     | Fedeltà finale $F$ | ... | ... | ... |
     | Slew Rate max ($\text{SR}_{\max}$) | ... | ... | -X% |
     | Banda 99% ($\omega_{99\%}$) | ... | ... | -Y% |
     | Costo max per canale $C^2$ | ... | ... | -Z% |
2. **`filter_robustness_test.py`**:
   - Carica i risultati salvati.
   - Applica il filtro passa-basso a diverse frequenze di taglio.
   - Calcola le fedeltà risultanti e salva il grafico comparativo `fidelity_vs_bandwidth.pdf`.
3. **Integrazione nel Notebook `twoqubits.ipynb`**:
   - Aggiunta di una sezione visuale di confronto diretto per la tesi / presentazione.

---

## 6. Questioni Aperte da Approfondire (Note per il Relatore)

1. **Interazione Diretta Qubit-Qubit ($H_{qq}$)**:
   - Nel modello attuale, i due qubit non interagiscono direttamente tra loro ($J = 0$), ma solo per mediazione della cavità.
   - *Domanda da porre*: ha senso fisico/sperimentale aggiungere un accoppiamento diretto (es. dipolare $XX+YY$ o capacitivo/induttivo $J (\sigma_{x1}\sigma_{x2} + \sigma_{y1}\sigma_{y2})$), oppure è preferibile tenerli spazialmente distanziati per massimizzare l'indipendenza dei drive?
2. **Asimmetria Sperimentale**:
   - Cosa succede se i due qubit non sono perfettamente identici ($g_1 \neq g_2$ o $\omega_{q1} \neq \omega_{q2}$)?
   - Il controllo ottimo si adatta naturalmente a compensare le asimmetrie costruttive?
3. **Dissipazione Aperta (Equazione Master di Lindblad)**:
   - Valutare la robustezza in presenza di perdita di fotoni di cavità $\kappa$ e dephasing dei qubit $\gamma_\phi$. Se il tempo $T$ necessario con 2 qubit è minore, le perdite totali integrate saranno inferiori.
