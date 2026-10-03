# Verifica della v2

Verifica eseguita il 3 ottobre 2026. Questo documento distingue il collaudo software dai risultati scientifici ancora da ottenere.

## Risultati del collaudo

- Ambiente virtuale nuovo e indipendente creato in `v2/.venv`; dipendenze installate da `requirements.txt`.
- `pip check`: nessuna dipendenza incompatibile. Versioni esatte in `requirements-tested.txt` e nei metadati delle run.
- **46 test automatici superati**, senza fallimenti; log in [test_outputs/unittest.log](test_outputs/unittest.log).
- Modelli e configurazioni Fock, cat, squeezed e slew-limited caricati e validati.
- Copia dei sorgenti in una directory temporanea esterna: pipeline CLI completata senza file del progetto originale.
- Ripresa completa e parziale testata; checkpoint corrotti o configurazioni/codice incompatibili vengono rifiutati.
- Analisi di un riepilogo incompleto gestita con messaggio esplicito; i seed già completi restano analizzabili con `--seed`.
- Suite numerica: gradienti esatti vs differenze finite, autovalori degeneri, conservazione di norma/parità, confronto con `scipy.linalg.expm`, integrazione continua, filtro vs ODE indipendente, riduzione di parità vs spazio completo.
- Suite fisica: limite g=0, equivalenza 1Q/2Q con seconda ancilla disaccoppiata, comando comune vs comandi identici, accesso al singoletto tramite controllo differenziale, Fock dispari/reset, cat e conversione dB.
- Analisi dissipativa: detailed balance, assenza di riscaldamento artificiale del fondamentale dressed a temperatura zero, coincidenza con la dinamica unitaria a bagno nullo. Un controllo CLI con bagno non nullo è stato eseguito su un caso piccolo.
- Campagna CLI su due durate e due tagli: quattro run completate e tabella CSV generata in `test_outputs/sweep/`.
- Analisi filtro (tre cutoff) e rumore quasi-statico (quattro realizzazioni) eseguita sul controllo 2Q indipendente del collaudo finale. Quattro campioni servono solo a verificare il funzionamento, non a stimare robustezza statistica.
- Figure di dinamica, Wigner e attuatore ispezionate visivamente; collegamenti locali del report verificati.

## Collaudo completo con più processi

[Report finale](test_outputs/final_verified/smoke_20261003T153732_090050Z/report.html) · [Configurazione effettiva](test_outputs/final_verified/smoke_20261003T153732_090050Z/config.json)

Configurazione `smoke.json`: cavità con 14 livelli, T=3, 80 intervalli, 9 nodi di comando, filtro a 3, due seed per ciascuno dei tre casi, due processi. CRAB: 40 valutazioni per seed. GRAPE: massimo 8 iterazioni/20 valutazioni. Validazione anche con 20 livelli e osservazione aggiuntiva per 0.5 unità di tempo.

**6/6 risultati finali hanno superato tutti i controlli numerici.** Le probabilità target sono basse perché durata e budget sono intenzionalmente piccoli; nessun risultato di questo collaudo raggiunge la soglia P=0.99. Non è una dimostrazione di vantaggio fisico.

| Caso | P minimo sui seed | P massimo sui seed | Validati |
|---|---:|---:|---:|
| 1q | 0.03155041 | 0.03524783 | 2/2 |
| 2q_common | 0.11358209 | 0.11359177 | 2/2 |
| 2q_independent | 0.11284065 | 0.11354613 | 2/2 |

Massimi errori/indicatori sui sei risultati:

| Indicatore | Massimo |
|---|---:|
| `midpoint_fidelity_error` | 2.51659e-05 |
| `double_intervals_fidelity_error` | 6.28579e-06 |
| `tighter_ode_fidelity_error` | 1.4643e-09 |
| `dimension_fidelity_error` | 1.24866e-09 |
| `dimension_cavity_trace_distance` | 7.3456e-06 |
| `max_norm_error` | 1.73271e-08 |
| `max_edge_population` | 4.8885e-09 |

Un primo collaudo con 8 livelli è stato correttamente rifiutato per alcuni casi 2Q a causa di troncamento e occupazione del bordo. Si è aumentata la dimensione a 14 mantenendo le stesse tolleranze; non si sono nascoste le insufficienze numeriche.

## Integrità del progetto precedente

Sono stati confrontati gli hash SHA-256 di **95 file originali** (sorgenti, notebook, appunti e risultati): **nessun file modificato o rimosso**. Sono esclusi dal confronto directory Git, ambienti virtuali, cache Python e la nuova cartella `v2`. Nessuna dipendenza è stata installata nell’ambiente virtuale della prima versione.

## Limiti della verifica

Le configurazioni scientifiche complete Fock n=10, cat alpha=2 e squeezed 3 dB sono state controllate strutturalmente ma **non ottimizzate fino ad alta fedeltà**: richiedono una nuova campagna con budget adeguati. La convergenza sui casi piccoli non certifica automaticamente risoluzione e budget per quelli grandi.

Il bagno Bloch–Redfield è un modulo esplorativo con ipotesi dichiarate nel README: la sua calibrazione sperimentale, la validità sotto drive rapido e la convergenza dimensionale non sono state certificate. Non viene simulato il leakage in livelli superiori di un transmon. I controlli di robustezza non ripetono automaticamente tutti i test di convergenza a ogni perturbazione.
