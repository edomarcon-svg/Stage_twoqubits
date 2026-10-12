# Cosa è cambiato e perché

La cartella `v2` è una nuova implementazione autonoma. Non sono stati modificati né importati i moduli originali, i notebook, gli appunti o i dati della prima versione. La nuova pipeline non tenta di riprodurre numericamente gli stessi ottimi: usa un insieme di controlli fisici e una propagazione diversi e meglio definiti.

## Correzioni che incidono sui risultati

| Problema individuato | Intervento in v2 | Motivazione |
|---|---|---|
| N propagatori con passo T/(N-1) | N intervalli con passo T/N; campionamento al punto medio | L'evoluzione termina esattamente a T |
| Curva PCHIP verificata come gradini, con un intervallo in più | Verifica indipendente con `sesolve` della funzione continua effettiva | Non attribuire alla curva continua la fedeltà di un altro segnale |
| Gradiente al primo ordine usato con passi non piccoli | Derivata esatta degli esponenziali, tramite autovalori e differenze divise stabili anche alle degenerazioni | L'ottimizzatore riceve il gradiente del funzionale discretizzato effettivamente valutato |
| Vincoli CRAB e GRAPE diversi | Stessi nodi, stessi limiti, stesso filtro e medesimo obiettivo | Il raffinamento non cambia arbitrariamente il problema fisico |
| Lisciamento applicato dopo la ricerca | Filtro causale incluso nel problema e nella derivata; nessun PCHIP finale | Ottimizzare direttamente il segnale applicato |
| Numero slot interpretato come limite di banda | Separazione tra nodi del comando, intervalli dell'integratore e cutoff fisico | Convergenza numerica e fattibilità dell'attuatore sono proprietà diverse |
| “Fedeltà” usata sia per P sia per sqrt(P) | Salvataggio esplicito di entrambe le convenzioni | Soglie e statistiche non ambigue |
| Frequenza totale e modulazione confuse | Frequenza di base nel drift; controllo delta a estremi nulli | Costo, limiti e significato fisico restano coerenti |
| Costo con norma dipendente dalla dimensione non dichiarata | Fluenze totale/per canale e costo Hilbert–Schmidt normalizzato | Confrontare 1Q e 2Q senza fattori di dimensione impliciti |
| Fock dispari dichiarati sempre proibiti | Controllo della parità del target con o senza reset delle ancille | La cavità da sola può avere parità dispari |
| Conversione dB aggirata nel runner | `squeezing_unit` esplicito nel target condiviso | La conversione viene realmente applicata |

La ricostruzione del controllo usa un comando lineare a tratti. Se è attivo il filtro del primo ordine, la risposta e la mappa dai nodi ai valori applicati sono calcolate analiticamente. Il filtro parte all'equilibrio con modulazione nulla. Il residuo a T non viene cancellato artificialmente; può essere osservato durante `hold_time`.

L'esattezza del gradiente non elimina l'errore di discretizzazione della curva nel tempo. Per questo la fedeltà pubblicata deriva dalla propagazione continua e viene confrontata con N e 2N intervalli.

## Confronti scientifici

Le configurazioni separano accoppiamento 1Q, accoppiamenti 2Q, frequenze di base e durata assoluta. Sono inclusi casi a comando comune, indipendente e con g1=g2=0.3/sqrt(2). Il confronto a pari somma dei quadrati degli accoppiamenti è un controllo sulle risorse; non viene presentato come perfetta equivalenza tra modelli USC.

Si raffinano tutti i seed per default. Se si sceglie `refine_top`, il report dichiara che la distribuzione è selezionata. Si registrano budget, numero di valutazioni, messaggi di uscita e tempi. Non si deduce l'assenza di minimi locali da una dispersione piccola. Le campagne temporali mantengono controllata la risoluzione, ma non certificano limiti di velocità fondamentali.

Ogni caso comprende anche una propagazione senza modulazione: il vuoto bare non è il fondamentale interagente e può evolvere anche senza controllo. `initial_state=ground` permette un confronto con il fondamentale dressed. Per target di cavità non è imposto implicitamente il reset dei qubit; il reset è un'opzione esplicita.

Le metriche dell'attuatore considerano tutti i canali, il peggiore e il costo totale. Una riduzione su un solo canale non viene dichiarata vantaggio dell'intero apparato. Una fluence di frequenza non viene convertita in calore senza calibrazione hardware.

## Diagnostica, efficienza e riproducibilità

- Propagazione unitaria con ket e, quando richiesto, riduzione al settore di parità. La matrice densità della cavità è ricostruita per le osservabili.
- Validazione a dimensione maggiore, con confronto della fedeltà, della matrice ridotta, del target e dello stato iniziale. Controllo degli ultimi livelli occupati lungo la traiettoria.
- Purezza, distribuzione fotonica, entropia, quadratura minima, Wigner con stessa scala cromatica per target e finale, popolazioni delle ancille e correlazioni 2Q.
- Separazione tra successo numerico dell'ottimizzatore, validazione del risultato e raggiungimento della soglia fisica.
- Configurazioni JSON rigorose; parametri sconosciuti o incompatibili vengono rifiutati. Nessuna conversione silenziosa di un Fock non intero.
- Budget espliciti e limitazione dei thread BLAS nei processi dei seed.
- Dati NPZ senza pickle; JSON con schema, hash, versioni e copia del codice effettivo. Frequenze e coefficienti casuali CRAB sono conservati.
- Checkpoint atomici e ripresa controllata. La mancanza di dati non produce risultati artificiali.
- Report rigenerabili senza ripetere l'ottimizzazione. Nessuna duplicazione di logica tra notebook e script dedicati 1Q/2Q.

## Robustezza e dissipazione

`analyze_run.py` permette di variare il filtro mantenendo lo stesso comando e di campionare errori quasi-statici su guadagni, frequenze e accoppiamenti. `run_sweep.py` risolve invece nuovi problemi di ottimizzazione a ciascun punto: le due analisi restano distinte.

È disponibile una prima analisi dissipativa Bloch–Redfield nella base dressed istantanea, con bagno Ohmico termico, anziché inserire automaticamente dissipatori locali bare nel regime USC. Sono dichiarate le approssimazioni e salvati controlli di traccia/positività. La dissipazione non è inclusa nel gradiente dell'ottimizzatore e non è stata calibrata su una piattaforma sperimentale: per una conclusione fisica occorre validare il modello di bagno, l'approssimazione sotto drive rapido e la convergenza della simulazione dissipativa.

Non vengono simulati livelli non computazionali di un transmon, risposta misurata delle linee, conversione flusso-frequenza o estrazione dei fotoni. Questi richiedono parametri e un modello specifici dell'esperimento; i limiti di ampiezza da soli non certificano assenza di leakage.

## Come usare la nuova versione

Leggere `README.md`, lanciare `configs/smoke.json` e controllare `report.html`. Passare poi ai benchmark Fock/cat/squeezed aumentando budget e risoluzione quando la validazione lo richiede. Le configurazioni complete sono punti di partenza riproducibili, non risultati di vantaggio 2Q già ottenuti.

Le verifiche realmente eseguite su questa implementazione e i loro esiti sono riportati in `VERIFICA.md`.
