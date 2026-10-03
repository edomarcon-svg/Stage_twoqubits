# Simulazioni cavità + uno o due qubit — v2

Progetto autonomo per confrontare la preparazione di stati di Fock, squeezed e cat a quattro componenti. Nessun modulo importa file dalla cartella superiore. I file della versione precedente non sono necessari e non sono stati modificati.

La v2 ottimizza il **segnale applicato dopo il filtro dell'attuatore**, con gli stessi vincoli in CRAB e GRAPE. Ogni impulso finale viene verificato con un'integrazione continua indipendente e con una dimensione di cavità maggiore. Il completamento del programma non significa né alta fedeltà né validazione superata: sono esiti separati.

## Avvio

Su questa macchina è già stato creato un ambiente locale in `.venv`. Dalla cartella `v2`:

```bash
.venv/bin/python run_simulation.py --config configs/smoke.json
```

Su un'altra macchina copia la cartella, **escludendo `.venv`, `test_outputs` e `__pycache__`**, e ricrea l'ambiente con Python >= 3.10:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python run_simulation.py --config configs/smoke.json
```

Su Windows usa `.venv\Scripts\python.exe`. `requirements-tested.txt` registra le versioni dell'ambiente verificato; le versioni effettive e la versione Python sono anche salvate in ogni run. La disponibilità delle ruote binarie dipende dalla piattaforma/versione Python.

`smoke.json` è un collaudo veloce con budget bassi, **non un benchmark di alta fedeltà**. Le configurazioni scientifiche possono richiedere molte ore. Non vengono lanciate automaticamente.

## Configurazioni

| File | Scopo |
|---|---|
| `configs/smoke.json` | Collaudo completo: 1Q, 2Q comune, 2Q indipendente, due seed |
| `configs/fock10_comparison.json` | Fock n=10, cinque confronti A–E, T=52.35987756 |
| `configs/cat2_comparison.json` | Cat alpha=2, cinque confronti, T=78.53981634 |
| `configs/squeezed3dB_comparison.json` | Squeezed 3 dB, theta=pi/4; conversione esplicita |
| `configs/fock10_slew_limited.json` | Fock n=10 con limite sulla derivata del comando e penalità |

I cinque casi sono: 1Q con g=0.3; 2Q con g1=g2=0.3 e comando comune/indipendente; 2Q con g1=g2=0.3/sqrt(2) e comando comune/indipendente. La normalizzazione non rende equivalenti i due modelli USC: è un controllo aggiuntivo sulle risorse. Il confronto comune/indipendente a Hamiltoniana fissata identifica meglio il valore del secondo comando.

Tutte le frequenze sono **angolari**, espresse nella stessa unità di riferimento. Con `omega_c=1`, i tempi sono in 1/omega_c. `duration` è un tempo esplicito e non viene ricalcolato cambiando g. `filter_cutoff` e `frequency_range` sono valori nelle stesse unità di frequenza, non fattori moltiplicati implicitamente per omega_c. Il modello non converte questi numeri in GHz, volt o watt.

```bash
.venv/bin/python run_simulation.py --config configs/fock10_comparison.json --validate-config
.venv/bin/python run_simulation.py --config configs/fock10_comparison.json --case 1q --case 2q_independent
.venv/bin/python run_simulation.py --config configs/fock10_comparison.json --workers 2 --output results
```

Parametri principali nel JSON:

- `dimension`: numero di livelli della cavità. La validazione aggiunge `dimension_increment` livelli.
- `intervals`: N intervalli esatti, passo T/N e N+1 estremi. Serve a integrare, non a imporre una banda hardware.
- `control.nodes`: campioni del **comando di modulazione** lineare a tratti, inclusi due estremi fissati a zero.
- `control.total_frequency_bounds`: limiti sulla frequenza totale del qubit; entrambi gli ottimizzatori li rispettano.
- `control.filter_cutoff`: frequenza del filtro causale del primo ordine; `null` significa nessun filtro. Un filtro del primo ordine attenua, non elimina esattamente tutte le frequenze oltre il taglio.
- `control.max_slew`: opzionale, limite su |d(delta)/dt| del comando. Per questo filtro passivo inizialmente all'equilibrio limita anche la derivata della risposta. Attiva SLSQP anziché L-BFGS-B.
- `control.fluence_weight`, `slew_weight`: penalità sul segnale **applicato**, sommate sui canali fisici e mediate nel tempo. Il costo è `1 - P_target + lambda_E * mean(sum(delta_applied**2)) + lambda_S * mean(sum(rate_applied**2))`.
- `optimization.seeds`: partenze CRAB indipendenti; per default vengono raffinate tutte.
- `optimization.refine_top`: `null` = tutti i seed; un intero raffina solo i migliori e il report segnala il bias di selezione.
- `crab_max_evaluations`, `grape_max_evaluations`, `grape_max_iterations`: budget espliciti. A parità di budget, diverse dimensionalità possono avere diversa difficoltà: confrontare anche curve di convergenza e tempi.
- `workers` e `blas_threads`: processi e thread BLAS per processo; il default evita moltiplicazioni incontrollate dei thread.
- `initial_state`: `bare` = |0,g,...,g>; `ground` = fondamentale dell'Hamiltoniana interagente con modulazione nulla.
- `parity_reduction`: riduzione al settore di parità iniziale per la dinamica unitaria.
- `target.reset_qubits`: se vero il target comprende anche il ritorno di tutti i qubit a |g>. I target incompatibili con la parità iniziale generano un errore.
- `target_probability_goal`: soglia su **P**, non sulla sua radice. Default 0.99.
- `validation.hold_time`: ulteriore osservazione dopo T, con comando nullo, filtro ancora in rilassamento e accoppiamento acceso.

Non modificare una configurazione per riprendere una run già avviata: usa un nuovo esperimento. I valori predefiniti non sono una certificazione automatica della convergenza.

## Fisica e controllo

Con la convenzione QuTiP |g>=|0>, sigma_z|g>=|g>, l'Hamiltoniana è

`H(t) = omega_c n - (1/2) sum_j [omega_qj + delta_j(t)] sigma_zj + (a+a†) sum_j g_j sigma_xj`.

Il termine di punto zero, proporzionale all'identità, è omesso. `direct_exchange` aggiunge opzionalmente `J (sigma_x1 sigma_x2 + sigma_y1 sigma_y2)`; il default è zero. La modulazione non è un drive trasverso. Un valore base della frequenza del qubit pari a 2 non è una frequenza di modulazione pari a 2.

Per il comando comune i due qubit ricevono la stessa **modulazione**, eventualmente attorno a frequenze di base diverse. In questo caso si usa l'intersezione dei limiti ammessi dai canali. La simmetria di scambio richiede anche accoppiamenti e frequenze uguali.

La parità totale `(-1)^(n + numero_qubit_eccitati)` è conservata. Un Fock dispari della sola cavità è ammesso se resta un numero dispari di qubit eccitati. Imporre invece qubit tutti a terra può renderlo inaccessibile. Il target di cavità è rappresentato da `|target><target| ⊗ I`, **senza normalizzare l'identità**.

Il cat è `C_alpha+ - C_ialpha+`, per alpha>0. È costruito direttamente dai coefficienti di Fock n=2 mod 4, evitando cancellazioni numeriche per alpha piccolo. Lo squeezed usa `r = dB * ln(10)/20` se `squeezing_unit` è `dB`. La costruzione dei target viene confrontata anche a dimensione maggiore.

CRAB cerca coefficienti Fourier casuali; i valori del comando sui nodi sono resi ammissibili per ampiezza e slew. Il segnale fisico è sempre quello ricostruito dai nodi e passato nel filtro: la massima frequenza estratta nella base CRAB **non è una banda rigida del segnale finale**.

GRAPE ottimizza gli stessi nodi con la derivata esatta degli esponenziali di ciascun intervallo, applicando la regola della catena attraverso interpolazione e filtro. L'esponenziale è esatto per il valore al punto medio dell'intervallo; l'approssimazione della curva continua resta soggetta a un controllo di convergenza. Non è più presente un lisciamento PCHIP successivo che cambia il problema dopo l'ottimizzazione.

## Lettura dei risultati

Ogni nuova run ha un identificativo UTC univoco. La struttura è:

```text
results/<nome>_<timestamp>/
  config.json                  configurazione completa risolta
  provenance.json              versioni, hash dei sorgenti e riferimento Git
  source_snapshot/              codice effettivamente eseguito + resolved_config.json
  status.json                  running / interrupted / failed / complete
  summary.json, summary.csv     risultati e statistiche dei seed
  report.md, report.html        report rigenerabili
  <caso>/baseline.json, .npz    evoluzione con modulazione nulla
  <caso>/seed_<n>/
    crab.json, crab.npz         frequenze, coefficienti, controlli e storia CRAB
    result.json                 esiti GRAPE, metriche e controlli numerici
    arrays.npz                  stati, controlli, target, distribuzioni e Wigner
    dynamics.*, wigner.*, optimization.*, actuator.*
```

`states_reduced` è un array di ket nel settore di parità, non una matrice ridotta della cavità; `parity_indices` permette la ricostruzione nello spazio completo. `rho_cavity_final` è invece la matrice densità ridotta. Per l'ordinamento dei sottosistemi si usa cavità, qubit 1, qubit 2. Gli NPZ si aprono con `allow_pickle=False`.

Il costo e le metriche distinguono:

- `target_probability = <target|rho_c|target>` oppure probabilità congiunta quando si richiede il reset;
- `fidelity_root = sqrt(target_probability)`, convenzione di `qutip.fidelity` per target puro;
- `cavity_target_probability` e `cavity_fidelity_root`, sempre riferite alla sola cavità;
- `modulation_fluence`, che esclude il valore di base, e `total_frequency_fluence`, che lo include;
- `normalized_hilbert_schmidt_control_cost = modulation_fluence_total/4`: norma Hilbert–Schmidt normalizzata per la dimensione dello spazio totale;
- costo totale, costo del canale più esigente, slew, banda AC al 99% e residuo del filtro a T;
- purezza, entropia della cavità, distribuzione fotonica, quadratura minima, Wigner e popolazioni dei qubit;
- nel caso 2Q, concorrenza e popolazione del singoletto. L'entropia della cavità misura l'entanglement cavità–qubit soltanto per stato globale puro.

Le fluenze non sono direttamente energia dissipata nell'elettronica. La negatività Wigner non è un criterio universale: uno squeezed può essere nonclassico con Wigner positiva. Il volume negativo Wigner è una stima sulla griglia salvata, accompagnata dall'errore dell'integrale; per una misura quantitativa controllare anche la convergenza della griglia di fase.

La validazione verifica: accordo con `sesolve` continuo; raddoppio degli intervalli; tolleranze ODE più strette; dimensione maggiore (sia fedeltà sia distanza di traccia della cavità); convergenza del target e della preparazione iniziale; occupazione degli ultimi livelli; norma e parità; vincoli sul comando. Se un controllo fallisce, la run resta salvata ma non viene dichiarata validata. Per i risultati finali si preferiscono seed validati, ordinati per costo continuo. La diagnostica dopo T non certifica un protocollo di estrazione del campo dalla cavità.

## Ripresa e report

```bash
.venv/bin/python run_simulation.py --resume results/NOME_RUN
.venv/bin/python run_simulation.py --report-only results/NOME_RUN
```

La ripresa controlla hash del codice, configurazione, versioni delle dipendenze e integrità dei checkpoint; non ricalcola seed già completati. Una run con codice o configurazione diversi richiede una nuova directory. Non sono previsti dati simulati fittizi quando un file manca.

## Campagne e robustezza

```bash
.venv/bin/python run_sweep.py --config configs/fock10_comparison.json --durations 40 50 60 --cutoffs 2 3 4
.venv/bin/python analyze_run.py results/NOME_RUN --case 2q_independent --cutoffs 1 2 3 5
.venv/bin/python analyze_run.py results/NOME_RUN --case 2q_independent --noise-samples 100 --noise-seed 1234 --gain-std 0.01 --detuning-std 0.01 --coupling-relative-std 0.01
```

`run_sweep.py` **riottimizza** a ogni durata/taglio e mantiene i passi temporali dei controlli e della propagazione non più grandi di quelli della configurazione base. Le partenze sono indipendenti, senza warm-start tra durate. `analyze_run.py` ripropaga **lo stesso comando** per studiarne la sensibilità. Non confondere le due domande. Le perturbazioni non vengono automaticamente validate a dimensione maggiore: il JSON lo dichiara.

Il rumore disponibile è quasi-statico gaussiano, indipendente sui canali fisici: errore relativo di guadagno, offset assoluto di frequenza e errore relativo di g. Lo stato iniziale nominale resta fissato. Non è rumore bianco né uno spettro 1/f. Eventuali violazioni dei limiti sotto rumore sono riportate senza clipping artificiale.

Il modulo opzionale dissipativo usa Bloch–Redfield nell'autobase dell'Hamiltoniana dipendente dal tempo, con operatori di bagno `a+a†`, sigma_x e sigma_z, spettro Ohmico termico e cutoff secolare:

```bash
.venv/bin/python analyze_run.py results/NOME_RUN --case 1q --bath --cavity-strength 0.0001 --qubit-strength 0.0001 --bath-cutoff 10 --temperature 0
```

L'analisi usa lo spazio completo perché le perdite possono cambiare parità. Le forze del bagno sono coefficienti dello spettro definito nel codice, non tassi T1/T2 già calibrati. La temperatura è in unità di frequenza (hbar=kB=1). Il caso sigma_z Ohmico a T=0 non introduce un tasso arbitrario di dephasing a frequenza zero.

Questa è una **approssimazione fisica esplicita**: richiede accoppiamento debole al bagno, memoria breve e giustificazione dell'approssimazione secolare e della base istantanea sotto drive rapido. Non sostituisce la modellazione della piattaforma sperimentale, non ottimizza direttamente la dinamica dissipativa e non certifica automaticamente convergenza dimensionale o positività per qualsiasi regime. Si salvano controlli di traccia e autovalore minimo. Può essere molto più costosa della simulazione unitaria.

Riferimenti: [documentazione QuTiP Bloch–Redfield](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-bloch-redfield.html), [Beaudoin, Gambetta e Blais, 2011](https://arxiv.org/abs/1107.3990), [derivata di Fréchet dell'esponenziale in SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.expm_frechet.html).

## Struttura del software

`qoc/config.py` valida gli input; `models.py` costruisce modelli e target; `controls.py` descrive il segnale; `propagation.py` implementa propagazione e gradienti; `optimizers.py` contiene CRAB e GRAPE; `validation.py` verifica i risultati; `metrics.py` calcola le osservabili; `storage.py` e `pipeline.py` gestiscono riproducibilità e checkpoint; `reporting.py` legge i dati; `robustness.py` e `dissipation.py` sono analisi successive.

I notebook duplicati della prima versione non sono stati ricreati: per esplorazioni interattive si importano queste stesse funzioni. Per una campagna scientifica partire dai casi piccoli, controllare i fallimenti numerici, aumentare risoluzione e budget, poi confrontare distribuzioni su più seed. Il minimo tempo trovato per una soglia è un risultato dell'ottimizzazione con quei vincoli, non una dimostrazione di quantum speed limit.
