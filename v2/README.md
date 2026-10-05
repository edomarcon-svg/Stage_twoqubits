# Cavità con uno o due qubit — manuale di simulazione v2

Questa cartella è un progetto autonomo per ottimizzare la preparazione di stati non classici di una cavità accoppiata a uno o due qubit. Contiene modello fisico, generazione dei controlli, ottimizzazione CRAB/GRAPE, verifica numerica, report e analisi successive degli impulsi. Può essere copiata senza i file della cartella superiore.

Il manuale è diviso in due parti: **come usare e gestire le simulazioni** e **come funziona il codice**. Le istruzioni descrivono il comportamento implementato, comprese le verifiche che restano a carico di chi conduce lo studio. Una run completata non implica né precisione numerica sufficiente né raggiungimento del target.

## Nuova campagna multi-target

La configurazione [configurazione_campagna.jsonc](configurazione_campagna.jsonc) esegue un collaudo di 16 tentativi e, se efficace, le 320 pipeline Fock proposte. Usare `run_campaign.py`, con supporto per `--validate-config`, `--pilot-only` e `--resume`. Costi, inizializzazione, diagnostiche, target opzionali e ripartenze da impulsi salvati sono descritti in [CAMPAGNA.md](CAMPAGNA.md).

## Archivio esterno e email

`auto_v2.sh` usa ora un archivio S3 privato verificato tramite lettura remota e SHA-256, inviando soltanto un riepilogo e il link via email. Creazione del bucket, configurazione `archive.env`, recupero delle vecchie run e cancellazione opzionale del server sono descritti in [ARCHIVIAZIONE.md](ARCHIVIAZIONE.md). Il nuovo default conserva il server; la cancellazione richiede `DELETE_SERVER_AFTER_DELIVERY=true` e una consegna verificata.

## Indice

**Parte I — Guida operativa**

- [1. Installazione e primo avvio](#1-installazione-e-primo-avvio)
- [2. Organizzare un esperimento](#2-organizzare-un-esperimento)
- [3. Configurazione completa](#3-configurazione-completa)
- [4. Esecuzione, risorse e ripresa](#4-esecuzione-risorse-e-ripresa)
- [5. Risultati e criteri di accettazione](#5-risultati-e-criteri-di-accettazione)
- [6. Scansioni e confronto tra sistemi](#6-scansioni-e-confronto-tra-sistemi)
- [7. Robustezza e dissipazione](#7-robustezza-e-dissipazione)
- [8. Problemi frequenti e percorso di lavoro](#8-problemi-frequenti-e-percorso-di-lavoro)

**Parte II — Spiegazione del codice**

- [9. Architettura e flusso dei dati](#9-architettura-e-flusso-dei-dati)
- [10. Configurazione e modello fisico](#10-configurazione-e-modello-fisico)
- [11. Comandi e attuatore](#11-comandi-e-attuatore)
- [12. Propagazione, costo e gradiente](#12-propagazione-costo-e-gradiente)
- [13. Ottimizzatori](#13-ottimizzatori)
- [14. Validazione e osservabili](#14-validazione-e-osservabili)
- [15. Pipeline, salvataggi e report](#15-pipeline-salvataggi-e-report)
- [16. Analisi di robustezza e bagno](#16-analisi-di-robustezza-e-bagno)
- [17. Dizionario degli array e lettura da Python](#17-dizionario-degli-array-e-lettura-da-python)
- [18. Test ed estensioni](#18-test-ed-estensioni)

Per le differenze rispetto alla versione precedente vedere [CAMBIAMENTI.md](CAMBIAMENTI.md); per i controlli eseguiti durante la realizzazione vedere [VERIFICA.md](VERIFICA.md).

# Parte I — Guida operativa

## 1. Installazione e primo avvio

### Ambiente Python

Aprire un terminale nella cartella `v2`. Nel progetto attuale:

```bash
cd /home/edo_laptop/Desktop/Stage_twoqubits/v2
```

Tutti i comandi successivi assumono questa directory di lavoro. Dopo aver copiato `v2` altrove, usare il nuovo percorso. È richiesto Python 3.10 o successivo, con versioni delle librerie compatibili con il proprio interprete.

Se l'ambiente `.venv` è già presente e funzionante, si può usarlo direttamente. Per un'installazione nuova:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

`requirements.txt` specifica gli intervalli di versioni supportati; `requirements-tested.txt` registra le versioni dell'ambiente verificato. Per riprodurre quell'ambiente, su un interprete compatibile, installare invece il secondo file. Non è necessario installare il pacchetto con `pip install -e .` per eseguire gli script da questa cartella. Usare esplicitamente `.venv/bin/python` evita di avviare per errore un altro Python; in alternativa attivare l'ambiente con `source .venv/bin/activate`.

### Controllare l'installazione e fare una prova breve

```bash
.venv/bin/python run_simulation.py --config configs/smoke.json --validate-config
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -u run_simulation.py --config configs/smoke.json
```

Il primo comando risolve i valori predefiniti e costruisce i modelli, senza ottimizzare. Il secondo esegue i test automatici. Il terzo esegue un esperimento piccolo: tre casi, due seed per caso, budget ridotti. Serve a verificare il percorso completo dei dati; una probabilità target bassa è compatibile con lo scopo di questa prova.

Il terminale stampa `Run: ...`: conservare quel percorso. Alla fine aprire il `report.html` contenuto nella run, oppure leggere `report.md` e `summary.csv`. Per evitare inizialmente il costo delle figure aggiungere `--no-plots`; i dati vengono comunque salvati.

## 2. Organizzare un esperimento

### Che cosa si sta confrontando

Un **caso** è una configurazione fisica: numero di qubit, accoppiamenti, frequenze e controlli comuni o indipendenti. Un **seed** determina una diversa inizializzazione casuale di CRAB. Una **run** esegue tutti i casi e i seed definiti in una configurazione. Una **scansione** crea più run variando durata e, facoltativamente, filtro.

La sequenza per ogni caso è:

1. Evoluzione senza modulazione, usata come baseline.
2. CRAB per tutti i seed richiesti.
3. Selezione di tutti i seed o dei migliori `refine_top` secondo il costo CRAB.
4. GRAPE, seguito dalla validazione indipendente, per ogni seed selezionato.
5. Confronto dei risultati, scelta di un seed e generazione dei report.

Per ottenere statistiche sui tentativi di ottimizzazione, lasciare `refine_top: null`. Se si raffinano soltanto i migliori CRAB, le statistiche finali descrivono quel sottoinsieme selezionato.

### Modello e unità da fissare prima di iniziare

Si usa ℏ = 1. Frequenze della cavità, dei qubit, accoppiamenti, frequenze CRAB e polo del filtro sono frequenze angolari espresse nella stessa unità; il tempo usa l'unità inversa. Con `omega_c = 1`, la durata è in unità di `1/omega_c`. Per passare a secondi occorre conoscere la frequenza angolare fisica della cavità: `t_fisico = t_simulato / omega_c_fisica`. Se si parte da Hz, prima convertire con `omega = 2*pi*f`.

La forma controllata è la frequenza totale del qubit:

```text
omega_q,j(t) = omega_q,j,bare + delta_j(t)
```

L'ottimizzatore produce un comando per la **modulazione**. Il filtro determina la modulazione effettivamente applicata. I limiti in configurazione sono invece limiti sulla **frequenza totale**. La documentazione del codice nella Parte II esplicita segni, operatori e convenzioni.

### Scegliere un punto di partenza

| File in `configs/` | Scopo e impostazioni caratteristiche |
| --- | --- |
| `smoke.json` | Prova funzionale: Fock 2, dimensione 14, durata 3, 80 intervalli, 9 nodi, 2 seed e budget piccoli. |
| `fock10_comparison.json` | Fock 10: dimensione 40, durata circa 52.36, 1200 intervalli, 121 nodi, 8 seed; cinque casi per separare numero di qubit, controllabilità e accoppiamento collettivo. |
| `cat2_comparison.json` | Cat con alpha = 2: durata circa 78.54, 1800 intervalli e 181 nodi. |
| `squeezed3dB_comparison.json` | Vuoto squeezed con 3 dB e angolo pi/4; durata e griglie del preset cat. |
| `fock10_slew_limited.json` | Confronto Fock 10 con slew massimo 1 e pesi di fluence e slew pari a 0.001. |

Questi file sono impostazioni iniziali di esperimenti, non promesse di convergenza o alta fedeltà. Per lavorare su una propria configurazione senza perdere il riferimento:

```bash
cp configs/smoke.json configs/mio_esperimento.json
```

Modificare la copia, darle un `name` descrittivo e controllarla con `--validate-config`. Conviene eseguire prima un solo caso e pochi seed, poi aumentare il campione. Per gli studi definitivi fissare in anticipo target, vincoli, soglia di successo e criteri del confronto.

## 3. Configurazione completa

### Un unico file da modificare

Aprire [configurazione.jsonc](configurazione.jsonc): contiene **tutti i campi configurabili dell'esperimento**, con spiegazione, unità, opzioni ammesse e vincoli accanto ai valori. Modificare direttamente questo file per scegliere modello, casi 1Q/2Q, target, controlli, filtro, penalità, budget, seed e validazione. La durata iniziale è `20*tau_s`, come nella versione precedente; gli altri valori sono quelli del collaudo smoke e vanno adeguati alla durata per una ricerca accurata. Per il collaudo breve usare `configs/smoke.json`.

```bash
.venv/bin/python run_simulation.py --config configurazione.jsonc --validate-config
.venv/bin/python -u run_simulation.py --config configurazione.jsonc
```

Il primo comando controlla i parametri senza ottimizzare; il secondo avvia tutti i casi elencati in `cases`. Per eseguirne uno solo, eliminare dal file gli altri oggetti sistemando le virgole. Per conservarne diverse versioni, copiare il file con un altro nome mantenendo l'estensione `.jsonc` e passarlo a `--config`. Lo stesso formato funziona con `run_sweep.py --config`: durate e cutoff della campagna restano selezionabili dalle opzioni dello sweep. Le analisi successive di rumore e bagno usano invece le opzioni di `analyze_run.py` descritte nella sezione 7: non sono parametri dell'ottimizzazione unitaria.

I commenti `// ...` e `/* ... */` sono ammessi nei file `.jsonc`; i `.json` restano JSON standard senza commenti. Entrambi usano `null` per assenza di un limite/opzione e `true`/`false` per i booleani. Non sono ammesse virgole finali o espressioni Python. Le run salvano sempre un `config.json` standard con i valori risolti, senza commenti; il resume rilegge questo snapshot, non le modifiche successive al file di lavoro. Senza `--config`, lo script continua a usare il preset smoke.

I nomi sconosciuti vengono rifiutati, evitando che un refuso ignori silenziosamente un parametro. I campi omessi assumono i valori delle dataclass: **i default nelle tabelle non sono necessariamente i valori dei preset**.

### Durata come multiplo intero di tau_s

Nel file `configurazione.jsonc` modifica `factor_taus`, ad esempio 10, 15 o 20. Il codice calcola automaticamente:

```text
tau_s = pi / (2 * tau_s_coupling)
T = factor_taus * tau_s
```

Con `tau_s_coupling = 0.3`, 10 corrisponde a T ≈ 52.36 e 20 a T ≈ 104.72. Il riferimento è esplicito e comune a tutti i casi: nella v1 era g del sistema 1Q o g1 del sistema 2Q. Per legarlo a un accoppiamento modificato, aggiornare anche `tau_s_coupling`. Non viene ricalcolato dalla lista dei casi, quindi selezionare un altro caso o confrontare accoppiamenti normalizzati non cambia la durata fisica.

Nel file `configurazione.jsonc` il campo `duration` è assente: per scegliere la durata si modifica soltanto `factor_taus`. Il codice calcola T e le run salvano sia il fattore e l'accoppiamento di riferimento sia `duration` effettivo; i report mostrano la conversione. I vecchi JSON che specificano soltanto `duration` continuano a usare quel valore. Per una configurazione alternativa a tempo esplicito è possibile aggiungere `duration` e impostare `factor_taus: null`. Hold e array temporali restano nelle unità di tempo del modello, non in multipli di tau_s.

Cambiare T non adatta automaticamente `intervals` o `control.nodes` in una singola run: verificare la risoluzione temporale, soprattutto passando dal collaudo breve a 20 tau_s. Gli sweep adattano invece queste griglie secondo la politica descritta nella sezione 6.

### Parametri generali

| Campo | Default | Significato e uso |
| --- | --- | --- |
| `name` | `"fock6"` | Nome dell'esperimento; identifica la directory dei risultati. |
| `dimension` | `40` | Numero di livelli Fock della cavità, da 0 a `dimension-1`. Aumentarlo estende lo spazio fisico simulato e costa memoria/tempo. |
| `omega_c` | `1.0` | Frequenza angolare della cavità, positiva. |
| `duration` | `104.71975511965978` | Tempo fisico T; usato direttamente solo con `factor_taus: null`, altrimenti derivato. |
| `factor_taus` | `null` | Intero positivo: T = fattore × tau_s. Nel file commentato è impostato a 20. |
| `tau_s_coupling` | `0.3` | Accoppiamento di riferimento positivo: tau_s = pi/(2*g_ref), comune a tutti i casi. |
| `intervals` | `800` | Numero N di intervalli del propagatore usato nell'ottimizzazione. Il passo è T/N. |
| `initial_state` | `"bare"` | `bare`: vuoto della cavità e qubit in g; `ground`: stato fondamentale del sistema interagente. |
| `parity_reduction` | `true` | Usa il settore di parità iniziale per ridurre le matrici. Disattivabile per controlli incrociati. |
| `target_probability_goal` | `0.99` | Soglia sul quadrato della fedeltà, cioè sulla probabilità target P. |
| `cases` | Un caso 1Q | Lista dei casi fisici, descritti sotto. |

Il modello contiene i termini contro-rotanti: lo stato `bare` non è in generale stazionario. Il ground state interagente può contenere popolazione fotonica e correlazioni già all'inizio. Confrontare preparazioni diverse significa anche confrontare risorse iniziali diverse.

### Casi: `cases`

Ogni elemento della lista contiene:

| Campo | Default | Significato |
| --- | --- | --- |
| `name` | `"1q"` | Nome unico; usare lettere, numeri, `_` o `-`. |
| `couplings` | `[0.3]` | Un accoppiamento per qubit; la lunghezza determina se il sistema è 1Q o 2Q. |
| `qubit_frequencies` | `[2.0]` | Frequenze bare, nello stesso ordine degli accoppiamenti. Devono essere strettamente interne ai limiti di frequenza totale. |
| `control` | `"independent"` | `independent`: un comando per qubit; `common`: un solo comando di modulazione condiviso. |
| `direct_exchange` | `0.0` | Coefficiente J di `J*(sigma_x1*sigma_x2 + sigma_y1*sigma_y2)`; non nullo soltanto per 2Q. |

Per esempio, un caso 2Q indipendente si inserisce nell'array `cases` come oggetto con `couplings: [0.3, 0.3]`, `qubit_frequencies: [2.0, 2.0]` e `control: "independent"`. Le due liste devono avere la stessa lunghezza. Con controllo comune e frequenze bare diverse, i due qubit ricevono la stessa **modulazione**, ma conservano frequenze totali diverse.

### Target: `target`

| Campo | Default | Significato |
| --- | --- | --- |
| `kind` | `"fock"` | `fock`, `squeezed` oppure `cat`. |
| `value` | `6` | Numero intero di fotoni per Fock; intensità dello squeezing per squeezed; alpha reale positivo per cat. |
| `theta` | `0.0` | Fase del parametro di squeezing, in radianti; non ruota il target cat implementato. |
| `squeezing_unit` | `"r"` | `r` oppure `dB`; `dB` è ammesso soltanto per squeezed. |
| `reset_qubits` | `false` | Se falso il target riguarda solo la cavità; se vero richiede contemporaneamente tutti i qubit in g. |

Per Fock occorre `0 <= value < dimension`. Per squeezed si usa `z = r*exp(i*theta)`; per un valore in dB, `r = value*ln(10)/20`. Il cat implementato è una particolare sovrapposizione a quattro componenti con supporto sui livelli `n = 2 mod 4`: non è il semplice cat pari a due componenti. Vedere la costruzione in Parte II.

`reset_qubits` cambia l'obiettivo fisico. Senza reset, un'ottima cavità può essere associata a qubit eccitati. Con reset, la stessa cavità deve essere ottenuta con ancille in g. La parità può rendere alcuni obiettivi impossibili: partendo dalla preparazione bare di parità positiva, un Fock dispari con tutte le ancille in g viene rifiutato.

### Controlli: `control`

| Campo | Default | Significato e conseguenze |
| --- | --- | --- |
| `nodes` | `81` | Numero M di nodi del comando lineare a tratti, inclusi i due estremi fissati a zero. Tra 3 e N+1. |
| `total_frequency_bounds` | `[0.5, 3.0]` | Limiti inferiore e superiore della frequenza totale di ciascun qubit. |
| `filter_cutoff` | `3.0` | Polo angolare del filtro causale del primo ordine; `null` elimina il filtro. |
| `max_slew` | `null` | Limite rigido sul modulo della derivata del comando; unità frequenza/tempo. Attiva SLSQP nel raffinamento. |
| `fluence_weight` | `0.0` | Peso della media temporale della somma delle modulazioni fisiche al quadrato. |
| `slew_weight` | `0.0` | Peso della media temporale della somma delle derivate delle modulazioni applicate al quadrato. |

Il comando inizia e termina a zero, ma il segnale filtrato può essere ancora diverso da zero al tempo T: il filtro ha memoria. Durante l'eventuale hold il comando è spento e questa coda decade esponenzialmente.

Aumentare `nodes` rende il controllo più flessibile e aumenta le variabili GRAPE. Aumentare `intervals` migliora la discretizzazione della propagazione. Aumentare `trajectory_points` rende più fitto il campionamento dei risultati e dei controlli sulla traiettoria. **Non sono tre modi equivalenti di migliorare la simulazione.**

I pesi del costo non sono vincoli rigidi: con pesi positivi l'ottimizzatore può accettare una probabilità leggermente inferiore per un impulso meno intenso o più lento. Le penalità sommano sui canali fisici, quindi un segnale comune a due qubit conta due contributi.

### Ottimizzazione: `optimization`

| Campo | Default | Uso |
| --- | --- | --- |
| `seeds` | `[0,1,2,3,4,5,6,7]` | Interi non negativi distinti. Definiscono inizializzazioni CRAB riproducibili. |
| `frequencies` | `20` | Numero di frequenze casuali per canale CRAB; ognuna ha coefficiente seno e coseno. |
| `frequency_range` | `[0.05, 3.0]` | Intervallo di estrazione delle frequenze angolari CRAB, con minimo non negativo. |
| `crab_max_evaluations` | `1600` | Budget di valutazioni della ricerca Nelder–Mead. |
| `grape_max_iterations` | `200` | Massimo numero di iterazioni del raffinamento. |
| `grape_max_evaluations` | `1600` | Limite esplicito delle valutazioni del costo/gradiente GRAPE. |
| `refine_top` | `null` | Raffina tutti; un intero seleziona i migliori k CRAB, con k non superiore al numero di seed. |
| `workers` | `1` | Processi massimi per seed dello stesso caso. |
| `blas_threads` | `1` | Thread numerici per processo. |
| `ftol` | `1e-12` | Tolleranza sul costo nei criteri di arresto, secondo l'ottimizzatore. |
| `gtol` | `1e-7` | Tolleranza del gradiente per L-BFGS-B; non viene usata da SLSQP. |

Più seed esplorano più inizializzazioni; più budget permette di approfondire ogni tentativo. Aumentare soltanto `frequencies` senza aumentare il budget può rendere CRAB più difficile. CRAB e GRAPE non garantiscono l'ottimo globale.

### Validazione: `validation`

| Campo | Default | Uso |
| --- | --- | --- |
| `dimension_increment` | `20` | Livelli aggiunti per ripetere la stessa evoluzione in una cavità più grande. |
| `trajectory_points` | `601` | Campioni salvati su [0,T]; non fissa i passi interni del solutore ODE. |
| `atol`, `rtol` | `1e-10`, `1e-10` | Tolleranze assoluta e relativa dell'evoluzione continua. |
| `fidelity_tolerance` | `1e-3` | Soglia sulle differenze di fedeltà radice nei confronti temporali. |
| `truncation_tolerance` | `1e-5` | Soglia per convergenza in dimensione, costruzione del target e dello stato iniziale. |
| `edge_tolerance` | `1e-5` | Soglia sulla massima popolazione campionata degli ultimi livelli. |
| `edge_levels` | `5` | Numero di livelli superiori sommati per il controllo di bordo. |
| `hold_time` | `0.0` | Evoluzione aggiuntiva a comando spento, dopo T; aggiunge 100 campioni. |
| `phase_grid_points` | `121` | Punti per asse della griglia di Wigner. |

I limiti minimi implementati sono: `dimension >= 3`, `intervals >= 2`, `dimension_increment >= 2`, `trajectory_points >= 3`, `phase_grid_points >= 21` e `1 <= edge_levels < dimension`. Durata, frequenza della cavità, tolleranze e budget devono essere positivi; hold e pesi delle penalità non negativi.

Il risultato principale si riferisce sempre a T, anche se si salva un hold. `hold_metrics` descrive la fine dell'hold. Le verifiche indipendenti di dimensione e tolleranze riguardano la preparazione fino a T; per uno studio quantitativo della conservazione dello stato occorre verificare separatamente anche l'intero intervallo di hold.

## 4. Esecuzione, risorse e ripresa

### Avviare una run

```bash
.venv/bin/python -u run_simulation.py --config configs/mio_esperimento.json
```

Per un pilot con un solo caso:

```bash
.venv/bin/python -u run_simulation.py --config configs/fock10_comparison.json --case 1q --workers 1 --no-plots
```

`--case` è ripetibile e deve corrispondere esattamente a un nome nel JSON. La selezione mantiene l'ordine dei casi nel file. Queste opzioni sono disponibili:

| Opzione | Effetto |
| --- | --- |
| `--config FILE` | Configurazione; senza opzione né resume usa `configs/smoke.json`. |
| `--output DIRECTORY` | Directory base per nuove run; viene creata una sottocartella unica. |
| `--case NOME` | Seleziona un caso; ripetere per più casi. |
| `--duration T` | Imposta T esplicito e disattiva `factor_taus`; non adatta intervalli o nodi. |
| `--factor-taus K` | Imposta T = K*tau_s con K intero positivo; alternativo a `--duration`. |
| `--tau-s-coupling G` | Cambia g di riferimento per tau_s; non cambia gli accoppiamenti fisici. |
| `--intervals N` | Sostituisce il numero di intervalli. |
| `--workers W` | Sostituisce il numero di processi. |
| `--validate-config` | Verifica configurazione e costruzione dei modelli, stampa il JSON risolto ed esce. |
| `--no-plots` | Produce dati e tabelle senza generare nuove figure. |
| `--resume DIRECTORY_RUN` | Riprende la run compatibile indicata. |
| `--report-only DIRECTORY_RUN` | Rigenera report e figure dai risultati salvati, senza ottimizzazione. |

Le opzioni della versione precedente non sono automaticamente compatibili. Per dimensione, target, filtro, pesi e budget modificare il JSON, non inventare nuovi flag. Usare `--help` per vedere le opzioni effettive di ciascuno script.

### Risorse e avanzamento

I casi vengono eseguiti in sequenza; i seed di una stessa fase possono lavorare in parallelo. `workers = 2` e `blas_threads = 1` è un punto di partenza prudente per un portatile, da adattare alla memoria disponibile. Ogni processo conserva matrici e traiettorie proprie. La memoria del gradiente cresce soprattutto come `N*D^2`, dove D è la dimensione Hilbert effettivamente usata; aumentare dimensione, intervalli e worker contemporaneamente può essere molto costoso.

Il terminale stampa una riga al completamento di un CRAB o di un raffinamento con validazione. Un lungo silenzio non dimostra un blocco: non c'è una barra di avanzamento per ogni iterazione. La validazione ripete più evoluzioni, inclusa una a dimensione aumentata, e può richiedere una parte rilevante del tempo totale.

Per conservare un log restando in primo piano:

```bash
mkdir -p logs
.venv/bin/python -u run_simulation.py --config configs/mio_esperimento.json > logs/mio_esperimento.log 2>&1
```

Leggerlo da un secondo terminale con `tail -f logs/mio_esperimento.log`. Scegliere un nome diverso per un nuovo log da conservare: `>` sostituisce un file già presente. Se serve lasciare il terminale, su Linux è possibile usare `nohup` prima del comando e `&` alla fine; il PID si legge con `echo $!`. Le run non si riprendono automaticamente dopo arresto del computer.

### Interrompere e riprendere

Per un'esecuzione in primo piano usare Ctrl+C. I checkpoint completi restano disponibili. La ripresa avviene tra fasi complete, non dall'ultima iterazione interna dell'ottimizzatore: se CRAB è salvato e il raffinamento è stato interrotto, riparte il raffinamento da quel CRAB; se CRAB era ancora in corso, quel CRAB viene rifatto.

Nei comandi seguenti sostituire `results/NOME_RUN` con il percorso stampato all'avvio:

```bash
RUN="results/NOME_RUN"
.venv/bin/python -u run_simulation.py --resume "$RUN"
```

Non occorre ripassare il JSON: viene letto quello risolto dentro la run. La ripresa verifica identità della configurazione, hash del codice e versioni delle dipendenze. Anche cambiare seed, budget o worker cambia la configurazione e impedisce il resume. Per un esperimento diverso creare una nuova run. Una modifica al solo README non cambia gli hash del codice scientifico.

L'aggiunta del supporto JSONC modifica il codice del lettore di configurazione: le run create prima di questo aggiornamento richiedono il loro codice originale per il resume. I loro dati e report restano leggibili; non modificare gli hash salvati per aggirare il controllo.

Non avviare due processi di ripresa sulla stessa directory: non è implementato un lock per scritture concorrenti alla medesima run. Un arresto forzato può lasciare `status.json` su `running`; il resume si basa sui checkpoint verificati, non soltanto su questa etichetta. Un checkpoint con hash errato viene rifiutato, senza essere sostituito silenziosamente.

### Rigenerare i report

```bash
.venv/bin/python run_simulation.py --report-only "$RUN"
```

Funziona quando esiste `summary.json`. Durante una run questo riepilogo viene salvato alla fine di ciascun caso, quindi può non esserci ancora o essere parziale. Il comando rigenera le presentazioni dei risultati presenti nel riepilogo, non completa calcoli mancanti.

## 5. Risultati e criteri di accettazione

### Dove sono i dati

```text
results/nome_TIMESTAMP/
  config.json                 configurazione risolta realmente usata
  provenance.json             ambiente, versioni e hash
  source_snapshot/            copia del codice e dei requisiti
  status.json                 stato di esecuzione
  summary.json                riepilogo strutturato dei casi completati
  summary.csv                 una riga per seed raffinato
  report.md / report.html     lettura dei risultati
  NOME_CASO/
    baseline.json / baseline.npz
    seed_0/
      crab.json / crab.npz     checkpoint della prima fase
      result.json             metriche, diagnostica, metadati
      arrays.npz              comandi, stati, osservabili
      ... png / pdf           figure, se richieste
  analyses/TIMESTAMP/          analisi aggiuntive richieste in seguito
```

La directory `source_snapshot` contiene anche la configurazione risolta. Gli NPZ sono archivi NumPy compressi; caricarli con `allow_pickle=False`. Per condividere il report HTML, mantenere le sottocartelle delle figure: le immagini sono riferimenti relativi, non incorporate nell'HTML.

### Tre domande separate

1. **Il calcolo è terminato?** Guardare `status.json` e `summary.json`.
2. **Il risultato è numericamente affidabile ai criteri scelti?** Guardare `result.json -> validation -> passed`, quindi i singoli `checks`.
3. **L'obiettivo fisico è stato raggiunto?** Guardare `metrics -> target_probability` e `goal_reached`.

Lo stato `success` di SciPy riguarda il criterio di arresto dell'ottimizzatore. Un budget esaurito può lasciare un buon impulso, e una convergenza dichiarata può lasciare una probabilità bassa. Anche un codice di uscita zero dello script non significa che i punti 2 e 3 siano soddisfatti.

### Probabilità, fedeltà e purezza

Si distingue sempre `P = target_probability` da `F_root = sqrt(P)`. La soglia `target_probability_goal` si applica a P: `P = 0.99` corrisponde a `F_root` circa 0.99499. Le differenze di fedeltà usate nella validazione sono differenze di `F_root`.

Senza reset, P è la probabilità di trovare la cavità nel target, dopo aver ignorato i qubit. Con reset, P richiede anche le ancille in g. `cavity_target_probability` resta il solo overlap della cavità: è utile per capire se una mancata riuscita dipende dalla cavità o dal reset. La curva salvata `cavity_fidelity_root` riguarda sempre la cavità, anche con reset attivo.

La purezza della cavità è `Tr(rho_c^2)`. In un'evoluzione globale pura, una purezza inferiore a uno segnala correlazioni entangled con le ancille. La negatività della Wigner, lo squeezing e la distribuzione fotonica sono diagnostiche diverse: non basta guardare un'unica figura per caratterizzare tutti i tipi di non classicità.

### Verifiche automatiche e come intervenire

| Check in `validation.checks` | Confronto effettivo | Se fallisce |
| --- | --- | --- |
| `time_grid` | Propagazione midpoint con N e 2N intervalli contro l'evoluzione continua; entrambi gli errori in F devono essere entro `fidelity_tolerance`. | Aumentare N; controllare durata e rapidità degli impulsi. |
| `ode_tolerance` | Evoluzione continua nominale contro tolleranze 10 volte più strette e passo massimo dimezzato; soglia `fidelity_tolerance/10`. | Stringere `atol` e `rtol`, investigare il segnale e la scala temporale. |
| `dimension` | Errore in F e distanza di traccia dell'intera densità della cavità aumentando i livelli; entrambi entro `truncation_tolerance`. | Aumentare `dimension` e verificare di nuovo la convergenza. |
| `target_construction` | Overlap tra target nelle due dimensioni, dopo immersione nello spazio più grande. | Aumentare dimensione, soprattutto per target con code fotoniche. |
| `initial_construction` | Analogo confronto dello stato iniziale, con stessa parità. | Verificare convergenza del ground state e dimensione. |
| `edge_population` | Massimo campionato della popolazione negli ultimi `edge_levels`, incluso l'hold. | Aumentare dimensione; infittire i campioni se sospettati picchi brevi. |
| `norm` | Massimo errore della norma sulla traiettoria, entro `max(1e-7,100*atol)`. | Controllare precisione ODE e modello. |
| `parity` | Errore di parità al tempo T, stessa soglia della norma. | Controllare operatori e propagazione. |
| `command_bounds` | Nodi entro i limiti logici, con tolleranza numerica `1e-9`. | Verificare vincoli e ogni eventuale modifica al codice dei controlli. |
| `command_slew` | Derivata del comando entro il limite, con margine `1e-8`. | Verificare vincoli e compatibilità della soluzione. |
| `command_endpoints` | Modulazione dei nodi iniziali/finali inferiore a `1e-12` in modulo. | Controllare la costruzione dei nodi. |

`passed` è la congiunzione di tutti questi check. Il controllo del bordo è campionato, non un massimo analitico su tutti gli istanti. La convergenza della griglia Wigner non rientra in `passed`: per quantificare la negatività controllare anche normalizzazione e stabilità al variare della griglia.

Non allargare le tolleranze soltanto per far comparire `true`. Decidere quale accuratezza serve alla domanda scientifica e risolvere la sorgente dell'errore. Prima si può verificare lo stesso impulso con maggiore precisione, senza riottimizzarlo; se la discrepanza compromette l'obiettivo, riottimizzare con una discretizzazione adeguata. Un esempio di verifica a impulso fissato è nella sezione 17.

### Quale seed viene selezionato

La pipeline sceglie il costo continuo minimo tra i seed numericamente validi. Se nessuno è valido, sceglie comunque il minimo tra quelli disponibili: **`selected_seed` non è un certificato di validità**. Con pesi di penalità non nulli, il seed scelto può non essere quello con P massimo.

La media, la mediana e la deviazione standard della probabilità sono calcolate sui seed raffinati. La deviazione standard è quella della popolazione campionata (`ddof=0`), non l'incertezza sulla media. Leggere anche `numerically_valid_count`, `validated_goal_count` e `selection_bias_top_only`. Per sostenere un vantaggio 2Q, mostrare distribuzione dei tentativi e successi validati, oltre al miglior caso.

### Figure

- **Dinamica:** frequenze totali applicate, numero medio di fotoni, fedeltà della cavità e purezza. La linea a T separa preparazione e hold.
- **Wigner:** target e stato finale sulla stessa scala di colore, utile per confrontare forma e interferenze.
- **Ottimizzazione:** costo per valutazione, non per iterazione; la storia può non essere monotona perché contiene tentativi poi scartati. Include il confronto delle popolazioni fotoniche.
- **Attuatore:** comando e segnale applicato, più spettro AC. Ogni spettro è normalizzato al proprio massimo: da quel grafico non si ricava un confronto assoluto dell'energia tra canali.

## 6. Scansioni e confronto tra sistemi

### Durata e filtro

Per scegliere le durate con multipli interi, usare per esempio:

```bash
.venv/bin/python -u run_sweep.py --config configurazione.jsonc --factors-taus 10 15 20 --no-plots
```

`--factors-taus` e `--durations` sono alternativi. Il primo usa il `tau_s_coupling` della configurazione; il secondo impone tempi espliciti e disattiva il fattore in ogni sottorun, anche se attivo nel file di partenza.


```bash
.venv/bin/python -u run_sweep.py --config configs/fock10_comparison.json --durations 40 52.3598775598 65 --cutoffs 1.5 3 6 --output results --no-plots
```

Questo esempio avvia nove run e può essere costoso. Per collaudare la procedura usare prima `configs/smoke.json` con due durate brevi. Le durate e i cutoff forniti devono essere positivi. Omettendo `--cutoffs` si mantiene quello della configurazione, anche se `null`.

Lo sweep mantiene approssimativamente la risoluzione temporale del preset: ricalcola N da `ceil(T_nuovo/dt_originale)` e i nodi da `ceil(T_nuovo/h_originale)+1`, rispettando i limiti minimi. È diverso da `run_simulation.py --duration`, che cambia soltanto T. Ogni punto riparte con nuove ottimizzazioni; non usa l'impulso del punto precedente come inizializzazione.

La directory di campagna contiene `campaign.json`, le sottorun e `sweep.csv`, aggiornato dopo ogni punto. Lo script non implementa il resume dell'intera campagna. Una sottorun interrotta può essere ripresa con `run_simulation.py --resume`, ma ciò non ricostruisce automaticamente il CSV della campagna.

### Confronto scientifico 1Q/2Q

I cinque casi dei preset di confronto includono 1Q, 2Q comune, 2Q indipendente e due casi 2Q con accoppiamenti ridotti. Con due accoppiamenti uguali a g, la scala collettiva `sqrt(g1^2+g2^2)` vale `sqrt(2)*g`. Usare `g/sqrt(2)` per ciascuno dei due qubit mantiene questa particolare scala uguale a quella del caso 1Q: serve a separare un aumento della risorsa di accoppiamento da altri possibili vantaggi. Non rende automaticamente equivalenti tutte le risorse dei sistemi.

Mantenere uguali target, preparazione, durata fisica, limiti di frequenza, modello di filtro, criterio di costo, soglia target e accuratezza numerica. Confrontare controlli comuni e indipendenti separatamente: due controlli aggiungono libertà ma anche risorse. Usare gli stessi seed e budget rende il protocollo trasparente, ma non garantisce uguale difficoltà o uguale tempo di calcolo nei diversi spazi di ricerca.

Possibili risultati da cercare sono: minore durata per raggiungere la stessa P validata, maggiore probabilità di successo tra i seed, minore fluence a pari qualità, minore sensibilità a errori, oppure migliore separazione finale dalle ancille. Sono ipotesi da misurare. Nel modello simmetrico il settore singoletto può restare inaccessibile con preparazione e controlli simmetrici; la sola presenza del secondo qubit non garantisce un nuovo canale utile. Controlli indipendenti possono rompere questa simmetria, pur conservando la parità.

Per stimare una durata minima operativa, iniziare con una griglia grossolana di T, poi infittire intorno alla transizione osservata. Un fallimento dell'ottimizzatore a T breve non dimostra un limite quantistico fondamentale: può dipendere da budget o parametrizzazione.

## 7. Robustezza e dissipazione

Queste analisi usano un impulso salvato **senza riottimizzarlo**. Richiedono un `result.json` completo per il seed. Senza `--seed` usano quello selezionato nel riepilogo; durante una run parziale può essere necessario specificare un seed già completato.

### Sensibilità al filtro

```bash
.venv/bin/python analyze_run.py "$RUN" --case 1q --cutoffs 1.5 3 6
```

Cambia il filtro applicato allo stesso comando. Risponde a «quanto è sensibile questo impulso a un diverso attuatore?». Uno sweep con riottimizzazione risponde invece a «quale prestazione riesco a ottenere progettando l'impulso per quell'attuatore?». Da CLI i cutoff sono positivi; la funzione Python accetta anche `None` per assenza di filtro.

### Errori statici

```bash
.venv/bin/python analyze_run.py "$RUN" --case 1q --noise-samples 100 --noise-seed 1234 --gain-std 0.01 --detuning-std 0.01 --coupling-relative-std 0.01
```

Per ogni realizzazione si estraggono errori gaussiani indipendenti per qubit, costanti durante l'evoluzione:

- `gain-std`: deviazione standard relativa del guadagno della modulazione; 0.01 significa 1%.
- `detuning-std`: deviazione standard **assoluta** dello spostamento della frequenza bare, nelle unità del modello.
- `coupling-relative-std`: deviazione standard relativa degli accoppiamenti.

La preparazione iniziale nominale resta fissa: non si ricalibra il ground state per ogni errore. Anche un comando nominalmente comune può avere guadagni fisici diversi sui due qubit. Si registrano gli eventuali superamenti dei limiti, senza tagliare i segnali perturbati. Questo modello non è rumore variabile nel tempo e non include automaticamente correlazioni tra gli errori.

I risultati riportano campioni, media, deviazione standard, quantili 5/50/95% e frazione che supera la soglia target. I quantili descrivono la distribuzione campionata, non un intervallo di confidenza sulla media. Aumentare i campioni e confrontare più seed del rumore per stabilizzare le stime.

### Bagno dissipativo

```bash
.venv/bin/python analyze_run.py "$RUN" --case 1q --bath --cavity-strength 0.001 --qubit-strength 0.001 --dephasing-strength 0.0001 --bath-cutoff 10 --temperature 0
```

I numeri sono un esempio di uso, non una calibrazione sperimentale. Si applica un modello Bloch–Redfield con operatori di accoppiamento al bagno e spettro ohmico, sullo spazio Hilbert completo. Questo calcolo può essere molto più costoso dell'evoluzione unitaria ridotta per parità.

`--bath` da solo lascia tutte le intensità a zero: non introduce dissipazione. `temperature` usa unità energetiche coerenti con ℏ = kB = 1; `bath-cutoff` è il cutoff del bagno, distinto dal filtro dei controlli. Le intensità non vanno identificate direttamente con T1/T2 senza derivare la relazione per il sistema e le convenzioni adottate.

L'analisi salva errori di traccia e autovalore minimo della densità per controlli di base. Non certifica automaticamente convergenza in dimensione, accuratezza dell'approssimazione debole/Markov/secolare o validità del bagno per il dispositivo. Per uno studio dissipativo occorre motivare questi aspetti e verificare anche la discretizzazione e le scale del drive.

### Output delle analisi

Ogni invocazione crea `analyses/TIMESTAMP/analysis.json`; il bagno aggiunge `bath.npz`. Si possono combinare filtro, rumore e bagno nello stesso comando. Sono registrati provenienza dell'analisi, hash dell'impulso e validità nominale. `perturbations_numerically_revalidated` resta falso: le singole perturbazioni non ripetono l'intera suite di convergenza della run nominale. Non vengono generate automaticamente nuove figure di analisi.

## 8. Problemi frequenti e percorso di lavoro

| Situazione | Azione utile |
| --- | --- |
| `ModuleNotFoundError` | Verificare di usare `.venv/bin/python` e installare i requisiti nello stesso ambiente. |
| Configurazione rifiutata | Leggere il campo indicato; controllare nomi, interi, liste per qubit, limiti, nodi e target. |
| Target senza supporto nel settore iniziale | Controllare parità e reset. Disattivare la riduzione non elimina una conservazione fisica. |
| P bassa con validazione superata | Provare più seed/budget; esaminare vincoli, durata, numero di nodi e stato iniziale. |
| P alta soltanto nel propagatore di ottimizzazione | Controllare `time_grid`; aumentare N e valutare nuovamente l'impulso continuo. |
| Popolazione sul bordo o dipendenza dalla dimensione | Aumentare i livelli, anche se il numero di fotoni del target è molto più basso del cutoff. |
| GRAPE fermo per budget | Leggere P e validazione del miglior punto conservato; aumentare il budget in una nuova run se necessario. |
| Calcolo lento o memoria insufficiente | Ridurre worker; fare prima un pilot; misurare il costo di dimensione e intervalli senza ridurli sotto l'accuratezza necessaria. |
| Resume rifiutato | Verificare configurazione, sorgenti e dipendenze; non aggirare gli hash modificando i metadati. |
| Report mancante durante il primo caso | Attendere il primo riepilogo; i checkpoint dei seed possono già essere presenti. |
| Perdita di fedeltà durante hold | Esaminare coda del filtro ed evoluzione sotto l'Hamiltoniana ancora interagente; il codice non spegne g dopo T. |

Un percorso pratico per lo stage è: collaudo smoke; convergenza numerica di un pilot; confronto multi-seed 1Q/2Q a T fissato; scansione della durata; confronto a risorse di accoppiamento e controllo dichiarate; analisi di robustezza degli impulsi promettenti; eventuale studio dissipativo motivato fisicamente. Conservare l'intera directory della run insieme alle conclusioni, così da poter risalire a configurazione, codice e dati.

# Parte II — Spiegazione del codice

## 9. Architettura e flusso dei dati

Il pacchetto `qoc` contiene il calcolo scientifico; i tre script nella radice sono interfacce da terminale. Non ci sono import dal progetto precedente. La separazione permette di usare le stesse funzioni in uno script Python di analisi senza passare dall'ottimizzazione completa.

```text
run_simulation.py
  -> config.load_config / Experiment.validate
  -> pipeline.run_experiment
       -> storage.prepare_run
       -> models.build_model + controls.Signal
       -> baseline continua
       -> optimizers.crab(Objective)
       -> optimizers.grape(Objective)
       -> validation.validate_waveform
            -> propagazione continua, griglie raffinate, dimensione maggiore
            -> metrics.state_metrics / actuator_metrics / phase_space
       -> checkpoint, summary, reporting.write_reports

run_sweep.py -> modifica copie della configurazione -> run_experiment per punto
analyze_run.py -> carica comando salvato -> robustness / dissipation
```

### Dimensioni e convenzioni degli array

Useremo `d` per il numero di livelli della cavità, `Q` per il numero di qubit, `C` per il numero di controlli logici, `L = d*2^Q` per la dimensione completa, `D` per quella effettivamente propagata, `M` per i nodi del comando e `N` per gli intervalli midpoint.

Con riduzione a una parità definita, `D = L/2`; senza riduzione `D = L`. Per 2Q comune `C = 1`, per 2Q indipendente `C = 2`. Gli array di controllo hanno il canale come primo indice e il tempo come secondo. Le traiettorie degli stati hanno invece il tempo come primo indice.

Gli stati sono vettori complessi e le Hamiltoniane matrici dense nel nucleo di ottimizzazione. La riduzione di parità dimezza il vettore e i lati delle matrici; non elimina la crescita del costo delle diagonalizzazioni. L'evoluzione unitaria conserva uno stato puro globale, mentre lo stato ridotto della cavità può essere misto.

## 10. Configurazione e modello fisico

### `qoc/config.py`

Le dataclass `Case`, `Target`, `Control`, `Optimization`, `Validation` ed `Experiment` raccolgono rispettivamente sistema fisico, target, attuatore, ricerca, verifiche ed esperimento completo. Separare questi gruppi rende esplicito quale parte del problema viene modificata.

- `load_config(path)` legge JSON o JSONC e chiama `from_dict`. Per `.jsonc`, `_without_json_comments` elimina i commenti preservando stringhe, numeri di riga e colonne degli errori; il file non viene eseguito come codice.
- `_strict(cls, data)` rifiuta le chiavi non appartenenti alla dataclass richiesta.
- `from_dict(data)` costruisce anche gli oggetti annidati e applica i default ai campi assenti.
- `Experiment.to_dict()` produce un dizionario serializzabile, includendo i valori risolti.
- `Experiment.validate()` risolve prima T dal fattore intero e dall’accoppiamento di riferimento, quando richiesto, poi controlla tipi, intervalli, relazioni tra dimensioni e parametri, univocità dei seed e dei casi, vincoli sul target e assenza di NaN/infinito.

La validazione sintattica non basta a garantire un obiettivo fisico possibile: `build_model` controlla anche il supporto del target nel settore di parità iniziale. Questo avviene prima dell'ottimizzazione.

### `qoc/models.py`: Hamiltoniana

Il modello di drift è

```text
H0 = omega_c * a†a
     - (1/2) * sum_j omega_q,j * sigma_z,j
     + (a + a†) * sum_j g_j * sigma_x,j
     + J * (sigma_x,1*sigma_x,2 + sigma_y,1*sigma_y,2).
```

L'ultimo termine compare soltanto in 2Q. L'identità di energia di punto zero della cavità è omessa perché produce soltanto una fase globale. Si usa `|g> = |0>` di QuTiP e `sigma_z|0> = +|0>`: il segno meno davanti al termine dei qubit rende g lo stato di energia inferiore a frequenza positiva.

L'interazione contiene sia termini rotanti sia contro-rotanti: non è il modello Jaynes–Cummings ottenuto con rotating-wave approximation. Il coefficiente `direct_exchange` moltiplica precisamente la somma XX+YY; in termini di operatori di salita/discesa tale somma introduce il relativo fattore 2. Tenerne conto quando si confrontano altre convenzioni per J.

La mappa fisica `A = physical_map`, di forma `(Q,C)`, converte le modulazioni logiche u in modulazioni dei singoli qubit: `delta = A*u`. È l'identità per controlli indipendenti e una colonna di uno per controllo comune. Gli operatori di controllo sono

```text
Hc,k = -(1/2) * sum_j A[j,k] * sigma_z,j
H(t) = H0 + sum_k u_k(t) * Hc,k.
```

### Target e obiettivo

`cavity_target(dimension, target)` costruisce un ket normalizzato nello spazio della cavità:

- Fock: il vettore di base `|n>`.
- Squeezed: `S(z)|0>`, con l'operatore di squeezing QuTiP e il parametro z definito nella configurazione.
- Cat: coefficienti non nulli soltanto per `n = 2 mod 4`, proporzionali ad `alpha^n/sqrt(n!)`. Vengono calcolati in forma logaritmica tramite `gammaln`, traslati prima dell'esponenziale e normalizzati. Questa forma evita sottrazioni quasi cancellanti per alpha piccolo. È equivalente, a meno della normalizzazione e del troncamento, alla combinazione `|alpha> + |-alpha> - |i alpha> - |-i alpha>`.

Il proiettore-obiettivo completo è `O = |target><target| tensor I_qubit` senza reset, oppure `|target><target| tensor |gg...><gg...|` con reset. L'identità delle ancille **non viene divisa per la sua traccia**: P deve essere una probabilità di successo, non una media sulle dimensioni delle ancille.

### Preparazione, parità e oggetto modello

`build_model(cfg, case, dimension=None)` costruisce operatori, stato iniziale, target e mappe. L'argomento opzionale `dimension` serve alla validazione del troncamento senza mutare la configurazione originale.

La base completa è ordinata come cavità, qubit 1, qubit 2. L'indice piatto è `n*2^Q + indice_qubit`; per due qubit l'ordine è gg, ge, eg, ee. La parità di un vettore di base è `(-1)^(n + numero_qubit_eccitati)`. Drift e controlli implementati conservano questa parità.

Per `bare` lo stato iniziale è `|0,g,...,g>`. Per `ground`, il codice diagonalizza separatamente i due blocchi di parità del drift e prende il fondamentale globale; così evita una combinazione numerica di settori in caso di degenerazioni. Il settore iniziale definisce `indices`, l'elenco delle componenti conservate nella rappresentazione ridotta. Anche senza riduzione, un target completamente fuori dal settore accessibile viene rifiutato; avere supporto non è comunque una prova di completa raggiungibilità.

L'oggetto modello conserva `drift`, `controls`, `initial`, `target_operator`, `target_cavity`, `indices`, `initial_parity`, `physical_map`, `bare_frequencies` e gli operatori completi QuTiP. La proprietà `ncontrols` restituisce C. I metodi:

- `expand(state)` reinserisce gli zeri delle componenti escluse e restituisce un vettore di lunghezza L.
- `full_ket(state)` restituisce quel vettore come `Qobj` con dimensioni tensoriali corrette.
- `cavity_density(state)` riorganizza il ket in una matrice `Psi` di forma `(d,2^Q)` e calcola `rho_c = Psi*Psi†`, cioè la traccia parziale sulle ancille.

## 11. Comandi e attuatore

### `qoc/controls.py`: `Signal`

`Signal(duration, nodes, cutoff)` definisce M tempi uniformi, con distanza `h = T/(M-1)`. Tra due nodi il comando x(t) è lineare. Prima dell'inizio e dopo T è zero; i nodi estremi ottimizzati sono fissati a zero. Senza filtro, il segnale applicato coincide con il comando.

Con cutoff `wc`, il segnale applicato y soddisfa

```text
y'(t) = wc * (x(t) - y(t)),     y(0) = 0.
```

Se `s = t - t_i` appartiene a un intervallo, la soluzione analitica è

```text
y(t) = exp(-wc*s)*y_i
       + (1-exp(-wc*s))*x_i
       + [s - (1-exp(-wc*s))/wc] * (x_(i+1)-x_i)/h.
```

`_factors` valuta questi coefficienti con `expm1` e sviluppi per argomento piccolo, riducendo la cancellazione numerica. Non si integra numericamente un filtro diverso durante la validazione: la stessa risposta analitica descrive sia il costo sia il callback continuo.

- `matrix(times, derivative=False)` restituisce B, di forma `(numero_tempi,M)`, tale che `y = nodes @ B.T`. Con `derivative=True` costruisce la mappa della derivata.
- `values(nodes, times)` applica questa matrice a tutti i canali.
- `callback(nodes)` precalcola la risposta ai nodi e restituisce una funzione efficiente dell'istante t, adatta al solutore ODE.

Dopo T, con filtro, `y(t) = y(T)*exp[-wc*(t-T)]`. Senza filtro il comando è zero fuori dall'intervallo. Il parametro del filtro è un polo: attenua progressivamente le frequenze elevate, non impone una banda rigorosamente nulla sopra wc.

### Limiti e slew

`logical_bounds(model, control)` sottrae le frequenze bare dai limiti totali e, per un canale comune, interseca gli intervalli ammessi da tutti i qubit che quel canale pilota.

`feasible_nodes` rende ammissibile il comando CRAB: fissa gli estremi e restringe uniformemente l'ampiezza di ciascun canale verso zero finché rispetta limiti e slew. Non esegue clipping punto per punto e non è una proiezione euclidea sul poliedro dei vincoli.

`slew_constraint` costruisce una `LinearConstraint` sulle differenze tra nodi adiacenti, divise per h, includendo gli estremi nulli. Serve a SLSQP. Il filtro passivo del primo ordine, inizializzato in equilibrio, preserva i limiti convessi del comando e non aumenta il limite di slew di un comando continuo con derivata limitata.

## 12. Propagazione, costo e gradiente

### `qoc/propagation.py`: propagatore midpoint

`propagate_midpoint(model, amplitudes, duration, gradient=False, intervals=None)` usa il numero di colonne di `amplitudes` per determinare N; il parametro opzionale `intervals` non determina la griglia nell'implementazione attuale. Le ampiezze sono campionate a `t_k = (k+1/2)*T/N`.

Per ogni intervallo forma `H_k = H0 + sum_j amplitudes[j,k]*Hc,j`, diagonalizza `H_k = V diag(e) V†` e applica

```text
psi_(k+1) = V * diag(exp(-i*dt*e)) * V† * psi_k,   dt = T/N.
```

Il prodotto copre esattamente T con N intervalli. Restituisce P e lo stato finale; se richiesto, anche il gradiente `(C,N)` rispetto alle ampiezze midpoint. L'esponenziale è esatto per ogni Hamiltoniana costante dell'intervallo, mentre sostituire il segnale continuo con valori midpoint resta un'approssimazione temporale.

### Derivata esatta dell'esponenziale

Durante la propagazione in avanti vengono conservati stati, autovettori, autovalori e fasi. All'indietro si parte da `lambda_N = O*psi_N` e si applicano gli aggiunti dei propagatori. Il contributo al gradiente è

```text
dP/du_j,k = 2 Re[ lambda_(k+1)† * (dU_k/du_j,k) * psi_k ].
```

Nella base degli autovettori, la derivata di U è il prodotto elemento per elemento tra `V† Hc,j V` e la matrice

```text
G_ab = -i*dt * exp[-i*dt*(e_a+e_b)/2]
       * sinc[dt*(e_a-e_b)/(2*pi)],
```

con `sinc(x) = sin(pi*x)/(pi*x)`, la convenzione NumPy. La formula resta finita per autovalori uguali. È una forma della derivata di Fréchet dell'esponenziale e include la non commutatività tra drift e controlli: non sostituisce la derivata con una semplice approssimazione al primo ordine nel passo.

Il termine «GRAPE esatto» si riferisce a questa derivata del propagatore discretizzato, non all'assenza di errori di discretizzazione rispetto all'evoluzione continua.

### Evoluzione continua indipendente

`continuous_evolution(model, signal, nodes, times, atol, rtol, max_step=None)` costruisce una Hamiltoniana QuTiP dipendente dal tempo tramite il callback di `Signal` e usa `sesolve`. Il passo massimo predefinito è `h/8`; `times` fissa i tempi di output, mentre il solutore gestisce passi interni adattivi. La normalizzazione automatica dell'output è disabilitata, così gli errori di norma restano osservabili. Restituisce un array `(numero_tempi,D)`.

Questa evoluzione è indipendente dalla suddivisione midpoint dell'ottimizzazione e permette di rilevare un impulso che sfrutta una griglia troppo grossolana.

### `Objective`: dalle variabili al costo

`Objective(model, signal, cfg)` precalcola le matrici del segnale B e della sua derivata ai midpoint. Le variabili GRAPE sono i soli nodi interni, appiattiti: `nfree = C*(M-2)`. `unpack(flat)` ripristina la matrice dei nodi con estremi nulli.

Il costo discretizzato è

```text
J = 1 - P
    + fluence_weight * mean_t[sum_j delta_j(t)^2]
    + slew_weight    * mean_t[sum_j delta'_j(t)^2].
```

`delta` è il segnale applicato ai qubit, dopo filtro e mappa A, non il comando grezzo. `evaluate_nodes(nodes, gradient=False)` restituisce costo, P e stato finale. Con gradiente restituisce costo e gradiente dei nodi interni. `__call__(flat)` espone la coppia costo/gradiente a SciPy.

La regola della catena riporta il gradiente delle ampiezze ai nodi tramite B. Le penalità aggiungono, prima di eliminare gli estremi:

```text
-dP/du @ B
+ (2*fluence_weight/N) * (A.T @ delta) @ B
+ (2*slew_weight/N)    * (A.T @ delta_rate) @ B_derivative.
```

La normalizzazione per N approssima una media temporale, equivalente all'integrale diviso T. Il costo continuo usato per selezionare i seed impiega invece l'overlap da ODE e quadrature dense del segnale, mantenendo la stessa normalizzazione fisica.

## 13. Ottimizzatori

### `qoc/optimizers.py`: contenitore dei risultati

`OptimizationResult` raccoglie nodi, costo, probabilità, stato finale, metadati e storia delle valutazioni. Per CRAB aggiunge coefficienti e frequenze casuali, così il punto iniziale della ricerca e il risultato sono ispezionabili.

### `crab(objective, seed)`

Per ciascun canale estrae `frequencies` frequenze uniformemente nell'intervallo configurato. Costruisce una base seno/coseno ai nodi e la moltiplica per l'inviluppo `sin^2(pi*t/T)`. I coefficienti iniziali sono gaussiani con scala `0.15/sqrt(numero_frequenze)`. Il seed controlla entrambe le estrazioni tramite `default_rng`.

Il numero di parametri è `2*C*numero_frequenze`. Ogni proposta viene convertita in nodi e resa ammissibile da `feasible_nodes`; il costo viene valutato con la stessa `Objective` usata da GRAPE. SciPy minimizza con Nelder–Mead adattivo, senza gradiente. Il codice conserva il miglior punto valutato, non si affida soltanto all'ultimo punto restituito.

CRAB è qui una ricerca locale senza derivate in una base casuale, ripetuta per più seed; non è un algoritmo con garanzia di ottimo globale. Il limite di valutazioni riguarda la ricerca; la rivalutazione finale del punto scelto introduce ulteriore lavoro fuori dal contatore riportato.

### `grape(objective, initial_nodes)`

Parte dai nodi CRAB e libera tutti quelli interni. Può quindi esplorare forme non contenute nella base Fourier CRAB, restando nella parametrizzazione del comando lineare filtrato.

Usa L-BFGS-B con limiti sui nodi se `max_slew` è assente; usa SLSQP con limiti e vincoli lineari sulle differenze se è presente. Valuta costo e gradiente analitico insieme. Un piccolo cache evita di ricalcolare la stessa coppia quando SciPy richiede due volte lo stesso punto.

Il codice conta esplicitamente le valutazioni e solleva internamente `BudgetExceeded` al superamento del budget; la gestione restituisce il miglior punto ammissibile già visitato con `success = false` e messaggio esplicito. Anche in una terminazione ordinaria viene conservato il migliore ammissibile, includendo quello iniziale. Pertanto il costo discretizzato restituito non peggiora rispetto al CRAB ammissibile di partenza; ciò non garantisce un aumento di P quando ci sono penalità, né un miglioramento identico nella propagazione continua.

Le storie contengono valutazioni, incluse proposte non accettate. Le rivalutazioni finali per produrre stato e metriche non coincidono necessariamente con il contatore delle valutazioni dell'ottimizzatore. `iterations`, `evaluations`, `message` ed `elapsed_seconds` nei metadati servono a distinguere comportamento della ricerca e costo computazionale.

## 14. Validazione e osservabili

### `qoc/validation.py`: `validate_waveform`

Questa funzione riceve un impulso già ottimizzato e non cambia i suoi nodi. Esegue l'evoluzione continua nominale, l'eventuale hold e le osservabili lungo la traiettoria. Identifica il finale della preparazione con l'indice `trajectory_points-1`, così l'hold non sostituisce accidentalmente il risultato al tempo T.

Poi confronta l'evoluzione nominale con midpoint a N e 2N, ODE più accurata e modello a `dimension + dimension_increment`. Per la dimensione confronta sia la fedeltà sia l'intera densità della cavità. La densità piccola viene immersa con zeri nello spazio grande e si calcola

```text
D_trace(rho_small, rho_large) = (1/2) * sum(abs(eigenvalues(rho_small-rho_large))).
```

Controlla separatamente che anche target e stato iniziale convergano aumentando i livelli: una buona dinamica in una base insufficiente non corregge un target o un ground state mal rappresentato. Gli errori di costruzione sono `1 - |overlap|^2` tra i ket immersi e quelli ricostruiti.

Restituisce due oggetti: un dizionario con `metrics`, `actuator`, `validation` e `hold_metrics`, e un dizionario di array. I criteri booleani sono elencati in sezione 5; `passed` è il loro AND. La funzione calcola inoltre il costo continuo per il confronto dei seed e le metriche di Wigner, che sono salvate ma non tutte incluse nei criteri di accettazione.

### `qoc/metrics.py`: `state_metrics`

Dallo stato completo ricostruisce le densità ridotte della cavità e delle ancille. Calcola:

- Norma, P dell'obiettivo completo, probabilità del solo target della cavità e rispettive fedeltà radice. La radice usa clipping in [0,1]; la probabilità grezza resta disponibile per diagnosticare errori numerici.
- Numero medio di fotoni e varianza da `rho_c`, purezza ed entropia `-sum(lambda*ln(lambda))`, espressa in nats.
- Parità attesa e scostamento dal valore iniziale; popolazioni eccitate dei singoli qubit e probabilità di tutte le ancille in g.
- Varianza minima delle quadrature dalla matrice di covarianza di `x=(a+a†)/sqrt(2)` e `p=(a-a†)/(i*sqrt(2))`. Il vuoto ha varianza 1/2. Lo squeezing è `-10*log10(2*varianza_minima)` dB; un valore negativo non indica squeezing sotto il vuoto.
- Per 2Q, concurrence della densità delle ancille e popolazione del singoletto `(ge-eg)/sqrt(2)`.

L'entropia della cavità misura l'entanglement con le ancille soltanto quando il sistema globale è puro. Non trasferire automaticamente questa interpretazione al caso dissipativo.

### `actuator_metrics`

Campiona il segnale applicato su 4001 punti in [0,T]. Integra la modulazione al quadrato per ogni canale e la frequenza totale al quadrato come quantità distinta. Riporta derivata massima campionata, slew RMS, estremi della frequenza totale e modulazione residua a T. Lo slew del comando si calcola esattamente dalle differenze dei nodi.

`omega_99_ac` stima la frequenza angolare sotto cui cade il 99% della potenza AC: toglie la media, esclude l'ultimo campione per la FFT, usa lo spettro reale con pesi corretti per le frequenze interne e conserva il contributo di Nyquist. È una diagnostica su una finestra temporale finita, sensibile alla finestra; non è un vincolo rigido di banda. Le quantità aggregate sommano le fluence dei qubit e usano il peggiore canale per banda/slew. Il costo Hilbert–Schmidt normalizzato riportato per la modulazione è `fluence_total/4`.

### `phase_space`

Sceglie una griglia quadrata con semilato `max(6, sqrt(2*mean_photons+1)+4)`, calcola la Wigner tramite QuTiP e integra con la regola trapezoidale. Salva integrale, errore di normalizzazione e volume negativo `(integral(abs(W))-integral(W))/2`. Una griglia finita può perdere code o strutture fini: ripetere con più punti quando questa quantità sostiene una conclusione quantitativa.

## 15. Pipeline, salvataggi e report

### `qoc/storage.py`

`save_json` scrive prima un file temporaneo e poi lo sostituisce con `os.replace`, evitando che un JSON parziale appaia come risultato completo. Usa JSON rigoroso, rifiutando NaN e infinito.

`config_digest` calcola SHA-256 della configurazione risolta con ordinamento canonico. `source_hashes` registra moduli `qoc`, script Python nella radice, requisiti e `pyproject.toml`. README, test e preset non rientrano in questi hash; il contenuto effettivo della configurazione è comunque protetto dal proprio digest.

`provenance` registra schema, versione del pacchetto, data UTC, interprete, piattaforma, versioni di NumPy/SciPy/QuTiP/Matplotlib/threadpoolctl, hash e commit Git quando disponibile. Il commit può appartenere alla repository superiore; gli hash dei file descrivono il codice effettivo anche quando ci sono modifiche non committate.

`prepare_run` crea una directory con timestamp univoco oppure verifica una richiesta di resume. Per nuove run salva configurazione, provenienza e snapshot dei sorgenti. Lo snapshot include `resolved_config.json`: per rieseguirlo come cartella autonoma fornire esplicitamente `--config resolved_config.json`, perché non contiene la raccolta dei preset predefiniti. Il resume usa il codice attualmente avviato e ne confronta gli hash: non ripristina automaticamente lo snapshot.

### `qoc/pipeline.py`

`save_arrays` scrive un NPZ compresso tramite file temporaneo, esegue la sostituzione atomica e restituisce l'hash. `load_checkpoint(folder, name)` legge il JSON e verifica esistenza e hash dell'NPZ associato. JSON assente significa fase non completata; NPZ non coerente significa checkpoint corrotto e genera un errore.

`_crab_worker` ricostruisce configurazione, modello e segnale in un processo, applica il limite ai thread BLAS, esegue CRAB e salva `crab.npz` prima di `crab.json`.

`_refine_worker` carica il CRAB verificato, esegue GRAPE e validazione, unisce gli array scientifici con quelli CRAB prefissati da `crab_`, salva `arrays.npz` e infine `result.json`. Quest'ultimo marca quindi il completamento dell'intera fase di raffinamento e verifica, non soltanto dell'ottimizzatore.

`_dispatch` esegue serialmente con un worker oppure usa `ProcessPoolExecutor` con avvio `spawn`. I processi figli ricostruiscono gli oggetti, evitando di ereditare pool BLAS già attivi. Ogni worker scrive soltanto nella propria cartella seed.

`run_experiment` coordina il flusso:

1. Valida configurazione e modelli prima di iniziare il lavoro costoso.
2. Prepara directory e stato `running`.
3. Per ciascun caso carica o calcola la baseline a modulazione nulla. Questa baseline ha metriche ma non una propria suite completa di convergenza.
4. Riutilizza i checkpoint CRAB validi ed esegue quelli mancanti.
5. Ordina per costo CRAB, con seed come spareggio, e seleziona il sottoinsieme da raffinare.
6. Riutilizza i risultati completi o esegue raffinamento e validazione mancanti.
7. Sceglie il seed secondo validità e costo continuo, calcola statistiche e salva il riepilogo dopo il caso.
8. Marca il riepilogo completo, genera i report e aggiorna lo stato finale.

Le eccezioni intercettate producono `failed`; un `KeyboardInterrupt` produce `interrupted`. Non vengono aumentati automaticamente dimensione, budget o intervalli dopo un fallimento: tali modifiche definiscono un nuovo esperimento da documentare.

### `qoc/reporting.py`

Usa Matplotlib con backend `Agg`, quindi può generare figure senza un desktop grafico. `_save` salva PNG e PDF e chiude la figura, limitando la memoria accumulata. `seed_figures` legge gli array e crea grafici di dinamica, Wigner, ottimizzazione e attuatore; per il filtro ricostruisce `Signal` dalla configurazione e dai nodi salvati.

`write_reports(root, make_figures=True)` legge `summary.json`, genera le eventuali figure e produce CSV, Markdown e HTML. Mostra separatamente validazione, soglia fisica, stato degli ottimizzatori, baseline e statistiche. Con `make_figures=False` può comunque collegare immagini già presenti. Rigenerare un report non esegue nuovamente la validazione scientifica.

### I tre script CLI

`run_simulation.py` usa `argparse`, sceglie il JSON, applica selezione dei casi e override, poi chiama la pipeline. La modalità report-only esce prima dell'avvio scientifico. La modalità validate-config stampa la configurazione risolta dopo aver costruito i modelli.

`run_sweep.py` genera il prodotto cartesiano delle durate e dei cutoff, copia la configurazione a ogni punto, adatta griglie, esegue la pipeline e aggiorna il CSV della campagna. I risultati per caso fanno riferimento al seed selezionato dalla relativa run.

`analyze_run.py` verifica il checkpoint finale, carica `command_modulation`, seleziona il caso e crea una directory di analisi nuova. Registra la provenienza del codice usato per l'analisi; diversamente dal resume, non richiede che coincida con quella dell'ottimizzazione. Per confronti riproducibili controllare quindi entrambe le provenienze.

## 16. Analisi di robustezza e bagno

### `qoc/robustness.py`

`filter_scan(cfg, case, nodes, cutoffs)` costruisce il modello nominale una volta e applica nuovi `Signal` allo stesso comando per ogni cutoff. Evolve fino a T e calcola le metriche finali. Non riottimizza e non estende l'analisi all'hold.

`static_noise_ensemble` genera un insieme di perturbazioni con seed proprio. Converte prima il comando logico in comandi fisici. Ogni realizzazione modifica frequenze bare e accoppiamenti, moltiplica la sola modulazione per il guadagno e usa controlli indipendenti per rappresentare errori diversi sui qubit. Lo stato iniziale resta quello nominale; se la costruzione perturbata del ground state selezionasse un altro settore, il codice può usare lo spazio completo per rappresentare correttamente la preparazione fissata.

Per ogni campione salva parametri estratti, metriche e segnalazione di frequenze fuori limite. La distribuzione gaussiana non è troncata: deviazioni molto grandi possono produrre parametri lontani dal regime che si intende studiare. Scegliere il modello degli errori in base alla calibrazione che si vuole rappresentare. La funzione aggrega probabilità, quantili e successi, senza attribuire automaticamente validità numerica completa alle perturbazioni.

### `qoc/dissipation.py`: spettro

`ohmic_spectrum(strength, cutoff, temperature)` costruisce una funzione S(w). Indicando l'intensità con eta, il cutoff del bagno con OmegaB e la temperatura con Theta:

```text
scale(w) = eta * |w| * exp(-|w|/OmegaB)
nB(w) = 1 / (exp(|w|/Theta)-1)
S(w>0) = scale(w) * (nB(w)+1)
S(w<0) = scale(w) * nB(w).
```

A temperatura zero restano i contributi a frequenza positiva; vicino a zero si usa il limite `eta*Theta`. Per grandi argomenti si evita overflow nell'esponenziale. Lo spettro soddisfa il bilancio dettagliato `S(-w) = exp(-w/Theta)*S(w)` a temperatura positiva.

### `dressed_bath_evolution`

Ricostruisce il modello completo senza riduzione di parità, usa l'Hamiltoniana dipendente dal tempo e chiama `qutip.brmesolve`. Gli operatori di accoppiamento al bagno sono `a+a†` per la cavità, `sigma_x` per i qubit e `sigma_z` per il contributo dephasing. Gli operatori con intensità nulla vengono omessi; i bagni dei qubit hanno la stessa intensità configurata ma contributi separati.

Lo stato iniziale è la densità pura della preparazione nominale. La funzione evolve su [0,T], restituisce metriche e salva tempi, densità finali completa/ridotta e numero medio di fotoni. Calcola massimo errore di traccia e minimo autovalore lungo la traiettoria. Il controllo di base richiede errori di traccia inferiori a `1e-7` e autovalori maggiori di `-1e-7`; il flag `dimension_and_bath_approximation_validated` resta falso.

Il parametro Python `secular_cutoff` ha default `1e-8` e non è esposto dalla CLI. Questo modulo non fornisce gradienti dissipativi, quindi non ottimizza impulsi tenendo già conto del bagno. Per il contesto dell'approccio consultare la [documentazione QuTiP su Bloch–Redfield](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-bloch-redfield.html) e il [riferimento sul trattamento dissipativo in ultrastrong coupling](https://arxiv.org/abs/1107.3990).

## 17. Dizionario degli array e lettura da Python

### Contenuto di `arrays.npz`

Nella tabella `Nt` comprende i campioni dell'hold, se presente; `K = phase_grid_points`.

| Chiave | Forma | Significato |
| --- | --- | --- |
| `command_times` | `(M,)` | Tempi dei nodi su [0,T]. |
| `command_modulation` | `(C,M)` | Nodi logici ottimizzati, prima del filtro. |
| `physical_command_modulation` | `(Q,M)` | Gli stessi comandi sui qubit, dopo A. |
| `times` | `(Nt,)` | Tempi delle traiettorie continue salvate. |
| `delivered_modulation` | `(C,Nt)` | Segnale logico dopo filtro. |
| `physical_delivered_modulation` | `(Q,Nt)` | Modulazione realmente applicata ai qubit. |
| `physical_total_frequency` | `(Q,Nt)` | Frequenze bare più modulazione applicata. |
| `states_reduced` | `(Nt,D)` | Ket continui; D può essere L se la riduzione è disattivata. |
| `parity_indices` | `(D,)` | Posizioni dei coefficienti nel vettore completo. |
| `state_final_full` | `(L,)` | Ket completo al tempo T. |
| `rho_cavity_final` | `(d,d)` | Densità della cavità al tempo T. |
| `target_cavity` | `(d,)` | Ket target normalizzato usato nella run. |
| `mean_photons`, `purity`, `edge_population` | `(Nt,)` | Osservabili della traiettoria. |
| `cavity_fidelity_root` | `(Nt,)` | Radice della probabilità del solo target della cavità. |
| `qubit_basis_populations` | `(Nt,2^Q)` | Popolazioni nella base g/e delle ancille. |
| `singlet_population` | `(Nt,)` per 2Q | Popolazione singoletto; array vuoto per 1Q. |
| `wigner_grid` | `(K,)` | Coordinate comuni dei due assi di fase. |
| `wigner_final` | `(K,K)` | Wigner della cavità a T. |
| `photon_distribution` | `(d,)` | Diagonale della densità finale della cavità. |
| `crab_nodes`, `crab_parameters`, `crab_frequencies` | Dipende da C, M e base | Comando e parametrizzazione della prima fase. |
| `crab_history`, `grape_history` | Una voce per valutazione | Storie del costo. |
| `crab_state`, `grape_midpoint_state` | `(D,)` | Stati finali del propagatore discretizzato, distinti dal risultato ODE. |

Non assumere che l'ultimo campione di una traiettoria sia il finale dell'ottimizzazione: con hold attivo è successivo a T. Usare gli array `*_final` oppure l'indice `validation.trajectory_points-1`.

### Leggere un seed selezionato

Il seguente codice Python si esegue dalla cartella `v2`, dopo aver sostituito il percorso e, se necessario, il nome del caso. Usa lo stesso controllo di integrità della pipeline:

```python
from pathlib import Path
import json
import numpy as np
from qoc.pipeline import load_checkpoint

run = Path("results/NOME_RUN")
case_name = "1q"
summary = json.loads((run / "summary.json").read_text())
case_summary = next(c for c in summary["cases"] if c["name"] == case_name)
seed = case_summary["selected_seed"]
folder = run / case_name / f"seed_{seed}"
result = load_checkpoint(folder, "result")
if result is None:
    raise RuntimeError("Il seed non ha un risultato completo")
print("P:", result["metrics"]["target_probability"])
print("Validazione:", result["validation"]["checks"])
with np.load(folder / "arrays.npz", allow_pickle=False) as data:
    rho = data["rho_cavity_final"].copy()
    nodes = data["command_modulation"].copy()
    print("Traccia cavità:", np.trace(rho))
    print("Forma del comando:", nodes.shape)
```

### Ricontrollare lo stesso impulso con una griglia più fine

Questo frammento continua il precedente. Non sovrascrive i risultati della run e non riottimizza. Ripete una validazione completa, che può essere costosa:

```python
from qoc.config import load_config
from qoc.models import build_model
from qoc.controls import Signal
from qoc.validation import validate_waveform

cfg = load_config(run / "config.json")
cfg.intervals *= 2
cfg.validation.atol /= 10
cfg.validation.rtol /= 10
cfg.validate()
case = next(c for c in cfg.cases if c.name == case_name)
model = build_model(cfg, case)
signal = Signal(cfg.duration, cfg.control.nodes, cfg.control.filter_cutoff)
checked, checked_arrays = validate_waveform(cfg, case, model, signal, nodes)
print(checked["validation"])
```

I nodi, la durata e il filtro sono mantenuti: si sta verificando il medesimo impulso. Per studiare il troncamento si può aumentare anche `cfg.dimension` prima di costruire il modello, sapendo che vengono ricostruiti target e preparazione secondo la configurazione. Il frammento tiene i risultati soltanto in memoria; se si salvano analisi proprie, usare una directory nuova e registrare configurazione, provenienza e hash dell'impulso, come fa `analyze_run.py`.

## 18. Test ed estensioni

### File di supporto

`qoc/__init__.py` definisce la versione del pacchetto. `pyproject.toml` contiene metadati, versione minima di Python, dipendenze e configurazione del packaging. I due file dei requisiti distinguono intervalli supportati e ambiente verificato. `.gitignore` esclude artefatti locali come ambiente e risultati secondo le regole del progetto. I documenti `CAMBIAMENTI.md` e `VERIFICA.md` mantengono rispettivamente motivazioni delle modifiche e resoconto delle verifiche pregresse.

### Cosa verificano i test

`tests/test_time_config.py` verifica conversione fattore–tempo, riferimento comune tra casi, valori non ammessi, roundtrip e override da CLI e sweep. Il test di run/ripresa del file commentato usa anche il tempo derivato da tau_s.

`tests/test_commented_config.py` verifica che il file modificabile esponga tutti i campi delle dataclass, che i commenti non alterino stringhe o posizioni degli errori, che i JSON standard restino rigorosi e che una run da JSONC possa essere salvata e ripresa. Il controllo di completezza segnala anche futuri parametri aggiunti al codice ma dimenticati nel file commentato.

`tests/test_numerics.py` copre configurazione, costruzione dei modelli, parità, riduzione dello spazio, target, filtro analitico, derivate del segnale, vincoli, gradiente contro differenze finite e confronti con esponenziali di matrice. Comprende casi 1Q/2Q, controlli comuni, penalità e degenerazioni, oltre a test di ottimizzazione, validazione, rumore nullo e bagno.

`tests/test_pipeline.py` esercita run piccole complete, report, resume completo e parziale, riuso dei checkpoint, rifiuto di corruzione e incompatibilità, analisi di risultati parziali con seed esplicito e avvio della cartella copiata autonomamente. Usa esperimenti piccoli per testare il comportamento software; non dimostra la convergenza di ogni configurazione scientifica.

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m unittest discover -s tests -p test_numerics.py -v
.venv/bin/python -m unittest discover -s tests -p test_pipeline.py -v
```

Il primo esegue tutto; gli altri due selezionano una delle due parti. Dopo modifiche alla fisica o alla numerica eseguire i test pertinenti e verificare nuovi impulsi rappresentativi; i risultati delle run precedenti conservano la provenienza del vecchio codice e non diventano automaticamente risultati della nuova versione.

### Dove intervenire per estendere il progetto

| Estensione | Componenti coinvolti e verifica necessaria |
| --- | --- |
| Nuovo target | `Target`/validazione in `config.py`, `cavity_target` in `models.py`, test di normalizzazione e convergenza in dimensione. |
| Nuovo termine Hamiltoniano | `models.py`; verificare Hermiticità, unità e conservazione della parità. Un termine che rompe parità richiede di ripensare anche la selezione del settore. |
| Nuovo attuatore | `Signal`, mappa del gradiente in `Objective`, callback continuo, vincoli e metriche. La stessa risposta deve essere usata nell'ottimizzazione e nella verifica. |
| Nuovo costo | Valore e gradiente in `Objective`, costo continuo in `validation.py`, report e test a differenze finite. |
| Nuova osservabile | `metrics.py`, eventuali traiettorie in `validation.py`, array salvati e report. Distinguere sempre finale T e hold. |
| Rumore temporale/correlato | `robustness.py`, modello casuale esplicito, seed/provenienza e verifiche di convergenza temporale. |
| Ottimizzazione dissipativa | Propagazione e gradienti per densità, costo, validazione e risorse computazionali; il solo modulo bagno attuale non la implementa. |

Quando cambia il significato di un dato salvato, aggiornare anche documentazione e schema anziché riutilizzare una chiave con semantica diversa. L'obiettivo della struttura è poter collegare ogni conclusione fisica all'impulso realmente applicato, alla precisione verificata e al codice che ha prodotto i dati.
