# Campagna Fock multi-target

La configurazione `configurazione_campagna.jsonc` prepara **320 pipeline principali**, precedute da **16 pipeline di collaudo**. Non esegue automaticamente calcoli quando viene aperta o validata. Ogni target ha un impulso autonomo; non si chiede a un unico stato finale di coincidere con target diversi.

## Avvio

Dalla radice del repository, con l'ambiente locale già disponibile:

```bash
.venv/bin/python v2/run_campaign.py --config v2/configurazione_campagna.jsonc --validate-config
.venv/bin/python -u v2/run_campaign.py --config v2/configurazione_campagna.jsonc
```

Su un server dove l'ambiente è già attivato, dalla cartella `v2`:

```bash
python -u run_campaign.py --config configurazione_campagna.jsonc
```

Per eseguire soltanto il collaudo aggiungere `--pilot-only`. Per ridurre il costo delle figure aggiungere `--no-plots`: CSV, JSON e array vengono comunque salvati. `run_simulation.py` resta l'ingresso per un singolo esperimento; `run_sweep.py` conserva gli sweep esistenti. Il nuovo formato va passato a **run_campaign.py**, non agli altri runner. Lo script `auto_v2.sh` ora avvia la campagna e archivia i risultati su storage S3 esterno prima dell’email; richiede la configurazione descritta in [ARCHIVIAZIONE.md](ARCHIVIAZIONE.md). Non è stato avviato durante l’implementazione.

Il programma stampa `Campaign: <cartella>`. Per continuare, anche dopo un'interruzione:

```bash
python -u run_campaign.py --resume results/campagna_fock_completa_TIMESTAMP
```

Non modificare codice, dipendenze o configurazione di una campagna in corso: la ripresa ne verifica la compatibilità. Una configurazione diversa richiede una nuova campagna. I figli già completati vengono verificati e i checkpoint CRAB riutilizzati. La ripresa opera fra fasi: un CRAB/GRAPE interrotto durante l'ottimizzazione riparte dal checkpoint precedente, non dallo stato interno di SciPy.

Per un collaudo rapido dell'infrastruttura usare `configs/campaign_smoke.json`: è un caso artificiale a g=0, con budget minimi e due processi, che verifica orchestrazione e salvataggi; non testa la raggiungibilità fisica di Fock 10.

## Disegno dell'esperimento

| Blocco | Target | Durate | Sistemi | Seed | Pipeline |
| --- | --- | --- | --- | --- | --- |
| Collaudo | Fock 10 | 20 tau_s | 1q e 2q normalized independent | 100, 101 per profilo | 16 |
| Principale filtrato | Fock 2, 6, 10 | 10 e 20 tau_s | Tutti i cinque | 0–7 | 240 |
| Diagnostica senza filtro | Fock 10 | 10 e 20 tau_s | Tutti i cinque | 0–7 | 80 |
| Opzionale, disattivato | Cat alpha=2 e squeezed 3 dB | 10 e 20 tau_s | Tutti i cinque | 0–7 | 160 aggiuntive |

I cinque sistemi sono 1q, 2q common, 2q independent, 2q normalized common e 2q normalized independent. I normalized hanno g1=g2=0.3/sqrt(2); gli altri hanno g=0.3 per ogni qubit. Il riferimento temporale rimane g_ref=0.3 in tutti i casi. Il cat implementato è a quattro componenti, con supporto n=2 mod 4.

Il confronto principale mantiene frequenze totali in [0.5,3], frequenze bare 2, stato iniziale bare, nessun reset, nessuna penalità di fluenza o slew e nessun limite slew. Il filtro con polo 3 **non è un taglio spettrale rigido**. `null` nei cutoff significa assenza del filtro.

Dimensione 60 con confronto a 80; 1000/2000 intervalli e 101/201 nodi alle durate 10/20 tau_s. I passi di propagazione e comando non crescono all'aumentare della durata. Le griglie sono calcolate rispetto a quelle dell'esperimento base. Le tolleranze ODE sono 1e-12, la tolleranza sulla fedeltà radice 1e-4, quelle di troncamento e bordo 1e-5. Il successo richiede P>=0.99 **e** validazione numerica. Il mantenimento viene osservato per altre 2 tau_s (10.4719755 unità), con 401 campioni; non viene ottimizzato.

## Collaudo e scelta del costo

Il collaudo confronta quattro profili: `probability`/`root`, ciascuno con deviazione standard iniziale dei coefficienti CRAB 0.10/0.30. La forma finale è sempre ricondotta ai limiti fisici; questi valori non sono l'ampiezza del segnale effettivamente applicato. Le tolleranze dei profili sono gtol=1e-10 e ftol=1e-14. Budget del collaudo: 1200 valutazioni CRAB, 80 iterazioni e 800 valutazioni GRAPE.

Per ogni profilo si calcola la mediana di P su ciascun caso, contando come zero i tentativi non validati, poi la media delle mediane fra i due casi. È ammissibile soltanto un profilo che in **entrambi** i casi abbia almeno un tentativo validato con un passo GRAPE accettato e un guadagno continuo rispetto all'inizializzazione CRAB di almeno 1e-6, oppure un tentativo che raggiunga già la soglia target.

Il profilo migliore ammissibile viene applicato a **tutti** i casi e target principali, lasciando invariati i budget principali (6000 valutazioni CRAB, 600 iterazioni e 6000 valutazioni GRAPE). In caso di pareggio prevale l'ordine dei profili nel file. La decisione e tutti i punteggi sono salvati in `pilot_selection.json`. I seed principali sono disgiunti da quelli del collaudo: non si seleziona il metodo usando i risultati che saranno poi confrontati. È una selezione empirica con pochi tentativi, non una dimostrazione di ottimalità o trasferibilità a ogni target.

Se nessun profilo è ammissibile, lo stato diventa `pilot_failed` e il processo termina con codice 2 **prima** delle 320 pipeline. Non significa impossibilità fisica: indica che il collaudo non giustifica ancora il costo della campagna. Per cambiare profili/budget avviare una nuova campagna. La configurazione consente `pilot.enabled=false`, ma in quel caso usa direttamente il profilo base senza collaudo.

## Costi e gradienti

In `optimization`:

- `objective`: `probability` (predefinito storico) oppure `root`.
- `objective_scale`: fattore positivo che moltiplica l'intero costo, incluse le penalità.
- `root_epsilon`: regolarizzazione positiva, predefinita 1e-12.
- `crab_initial_std`: deviazione standard dei coefficienti gaussiani; `null` conserva 0.15/sqrt(frequencies).

Con root si usa `scale * (sqrt(1+epsilon) - sqrt(P+epsilon) + penalty)`. Il gradiente include esattamente il fattore `-scale/(2*sqrt(P+epsilon))`. La regolarizzazione evita una singolarità a P=0; non crea un gradiente non nullo quando il gradiente fisico di P è esattamente zero. La probabilità e la fedeltà riportate rimangono P e sqrt(P), senza regolarizzazione o riscalamento.

`continuous_objective` conserva la vecchia diagnostica 1-P+penalty; `continuous_optimization_objective` corrisponde al costo configurato ed è usato nella selezione del miglior seed validato. Nel caso senza penalità i due ordinamenti coincidono.

Ogni valutazione GRAPE salva costo, probabilità, norma infinita del gradiente e gradiente proiettato sui limiti di ampiezza. Ogni iterazione accettata salva anche la variazione massima dei comandi. Con SLSQP la diagnostica proiettata riguarda soltanto i limiti di ampiezza, non è una misura completa delle condizioni KKT con vincoli slew. Il gradiente finale del miglior impulso richiede una valutazione diagnostica extra, esplicitamente indicata nei metadati e distinta dal budget di ricerca.

## Ripartenze da impulsi salvati

`optimization.warm_starts` è una lista opzionale. Ogni elemento produce una prova **aggiuntiva**, separata dai seed casuali e dalla selezione/statistica principale. Il comando importato viene raffinato con GRAPE senza ripetere CRAB. Esempio in un esperimento singolo:

```json
"warm_starts": [
  {
    "name": "vecchio_1q",
    "case": "1q",
    "path": "../results_both_fock_n10_dim40_T10taus/run_2026-10-02_16-53-17/1q/results.npz",
    "format": "legacy_smooth",
    "rescale_time": false
  }
]
```

I percorsi sono relativi al file di configurazione. Per il comando v2 usare `format: "v2"` e `arrays.npz`; per i vecchi array sono ammessi `legacy_crab`, `legacy_grape` e `legacy_smooth`. Le frequenze totali legacy vengono convertite in modulazione attorno alle frequenze bare del caso di destinazione. Si importano i **comandi**, quindi si applica il filtro del nuovo esperimento: non è una riproduzione identica dell'interpolazione precedente.

L'importazione controlla la durata e i canali. Per durate differenti occorre `rescale_time: true`: questo dilata il comando e cambia l'esperimento. Un controllo comune può inizializzare due canali indipendenti; due controlli diversi non vengono mediati automaticamente per creare un controllo comune. L'impulso viene reso ammissibile (estremi, ampiezza e slew); l'entità della modifica è registrata. La sorgente viene copiata nella run con checksum, così la ripresa non dipende dal file originale.

Nella campagna si può usare `optimization.warm_starts` **in uno specifico blocco**, per esempio un blocco solo Fock 10/T10/1q, evitando che venga applicato a tutte le durate. La configurazione proposta mantiene la lista vuota, così i 320 tentativi restano partenze casuali confrontabili e non richiedono file esterni. L'uso come inizializzazione non garantisce la stessa prestazione dell'impulso sorgente.

## Risultati

La cartella principale contiene:

- `campaign.json`, `plan.json`, `provenance.json`, `source_snapshot/`: configurazione, piano e codice riproducibile.
- `state.json`: avanzamento, cartelle figlie, eventuale eccezione.
- `pilot_selection.json`: punteggi e scelta del collaudo.
- `summary.csv`: mediana, quartili, dispersione, successi validati e frazione di successo per esperimento/caso.
- `seeds.csv`: risultati e diagnostiche per singolo tentativo, con fase pilot/main e cohort random/warm_start.
- `report.html`: tabella comparativa con collegamenti ai report delle run figlie.

Gli array dei tentativi includono `photon_populations[tempo,n]`, `target_probability_trajectory` (include l'eventuale reset), `grape_diagnostics` e `grape_diagnostic_columns`. Le iterazioni accettate sono nei metadati GRAPE; gli array delle valutazioni comprendono anche i tentativi della ricerca lungo la direzione.

I report includono popolazioni fotoniche, massimo numero medio di fotoni, minimo e media della probabilità nel hold, primo campione sotto soglia, fluenza, slew, banda 99% e frazione di potenza AC sopra `validation.spectral_threshold` (3). Il primo campione sotto soglia è una diagnostica alla risoluzione del campionamento, non un tempo di attraversamento esatto. Le quantità spettrali usano il segnale finito campionato, senza includere la componente media; non sono un vincolo aggiuntivo né una prova di banda rigorosa.

Le tolleranze scelte non garantiscono la validazione di ogni nuovo impulso. Un risultato che fallisce dimensione/precisione deve essere ricontrollato a risoluzione maggiore prima di trarne conclusioni fisiche. Il limite di tempo computazionale resta distinto dal limite fisico di preparazione.
