# Risultati v2

Durata fisica T = 52.35987756. T = 10 × tau_s; tau_s = pi/(2*g_ref) = 5.235987756, g_ref = 0.3.

Ogni riga usa la propagazione continua del controllo con il filtro configurato.
P_target è la probabilità target; F_root = sqrt(P_target). Il reset dei qubit, se richiesto, entra in P_target.
Una soluzione non validata non è evidenza di vantaggio fisico. La convergenza dell'ottimizzatore è distinta dalla validazione numerica.
Le statistiche e il seed selezionato riguardano solo partenze casuali; i warm start sono separati.
La banda 99% è una diagnostica del segnale finito, non un limite spettrale imposto. Le fluenze non sono calore dissipato.

| Caso | Seed | P target | F radice | Purezza | Validato | Soglia raggiunta |
|---|---:|---:|---:|---:|---|---|
| 1q | 0 | 0.77330605 | 0.87937822 | 0.916090 | False | False |
| 1q | 1 | 0.75849067 | 0.87091370 | 0.794882 | False | False |
| 1q | 2 | 0.60191822 | 0.77583389 | 0.854166 | False | False |
| 1q | 3 | 0.77681600 | 0.88137166 | 0.929489 | False | False |
| 1q | 4 | 0.67758553 | 0.82315584 | 0.808639 | False | False |
| 1q | 5 | 0.59685669 | 0.77256501 | 0.936153 | False | False |
| 1q | 6 | 0.64841719 | 0.80524356 | 0.907957 | False | False |
| 1q | 7 | 0.72027280 | 0.84868887 | 0.893922 | False | False |
| 2q_common | 0 | 0.99983841 | 0.99991920 | 0.999779 | True | True |
| 2q_common | 1 | 0.99701661 | 0.99850719 | 0.996452 | True | True |
| 2q_common | 2 | 0.99483378 | 0.99741354 | 0.994638 | True | True |
| 2q_common | 3 | 0.99975759 | 0.99987879 | 0.999665 | True | True |
| 2q_common | 4 | 0.99818517 | 0.99909217 | 0.997544 | True | True |
| 2q_common | 5 | 0.99835168 | 0.99917550 | 0.997814 | True | True |
| 2q_common | 6 | 0.98673039 | 0.99334304 | 0.986046 | True | False |
| 2q_common | 7 | 0.99998221 | 0.99999111 | 0.999984 | True | True |
| 2q_independent | 0 | 0.99998625 | 0.99999313 | 0.999979 | True | True |
| 2q_independent | 1 | 0.99998511 | 0.99999256 | 0.999978 | True | True |
| 2q_independent | 2 | 0.99999395 | 0.99999697 | 0.999994 | True | True |
| 2q_independent | 3 | 0.99999374 | 0.99999687 | 0.999992 | True | True |
| 2q_independent | 4 | 0.99999180 | 0.99999590 | 0.999988 | True | True |
| 2q_independent | 5 | 0.99997690 | 0.99998845 | 0.999968 | True | True |
| 2q_independent | 6 | 0.99996296 | 0.99998148 | 0.999948 | True | True |
| 2q_independent | 7 | 0.99998815 | 0.99999407 | 0.999989 | True | True |
| 2q_normalized_common | 0 | 0.63805615 | 0.79878417 | 0.857907 | False | False |
| 2q_normalized_common | 1 | 0.58041693 | 0.76185099 | 0.787745 | False | False |
| 2q_normalized_common | 2 | 0.75065012 | 0.86640067 | 0.821296 | False | False |
| 2q_normalized_common | 3 | 0.64537755 | 0.80335394 | 0.872599 | False | False |
| 2q_normalized_common | 4 | 0.50721563 | 0.71219072 | 0.691910 | False | False |
| 2q_normalized_common | 5 | 0.39326233 | 0.62710631 | 0.877339 | False | False |
| 2q_normalized_common | 6 | 0.57073416 | 0.75546949 | 0.794674 | False | False |
| 2q_normalized_common | 7 | 0.71815648 | 0.84744114 | 0.841905 | False | False |
| 2q_normalized_independent | 0 | 0.83784653 | 0.91533957 | 0.817651 | False | False |
| 2q_normalized_independent | 1 | 0.71243651 | 0.84405954 | 0.760327 | False | False |
| 2q_normalized_independent | 2 | 0.79331208 | 0.89068068 | 0.814136 | False | False |
| 2q_normalized_independent | 3 | 0.80877983 | 0.89932187 | 0.891494 | False | False |
| 2q_normalized_independent | 4 | 0.63716448 | 0.79822583 | 0.593357 | False | False |
| 2q_normalized_independent | 5 | 0.65032505 | 0.80642734 | 0.654333 | False | False |
| 2q_normalized_independent | 6 | 0.57731356 | 0.75981153 | 0.832099 | False | False |
| 2q_normalized_independent | 7 | 0.78630934 | 0.88674085 | 0.865113 | False | False |

## 1q
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.6942078940971927, "probability_std_population": 0.06915562427893476, "probability_median": 0.6989291665790465, "probability_min": 0.5968566923462955, "probability_max": 0.7768160023041271, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.6367924465620336, "probability_q75": 0.7621945117072427, "selection_bias_top_only": false}.
Seed selezionato: 3. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000027.

### random — 0
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_0/result.json)
![dynamics](1q/seed_0/dynamics.png)
![wigner](1q/seed_0/wigner.png)
![actuator](1q/seed_0/actuator.png)
![populations](1q/seed_0/populations.png)

### random — 1
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_1/result.json)
![dynamics](1q/seed_1/dynamics.png)
![wigner](1q/seed_1/wigner.png)
![actuator](1q/seed_1/actuator.png)
![populations](1q/seed_1/populations.png)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_2/result.json)
![dynamics](1q/seed_2/dynamics.png)
![wigner](1q/seed_2/wigner.png)
![actuator](1q/seed_2/actuator.png)
![populations](1q/seed_2/populations.png)

### random — 3
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_3/result.json)
![dynamics](1q/seed_3/dynamics.png)
![wigner](1q/seed_3/wigner.png)
![actuator](1q/seed_3/actuator.png)
![populations](1q/seed_3/populations.png)

### random — 4
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_4/result.json)
![dynamics](1q/seed_4/dynamics.png)
![wigner](1q/seed_4/wigner.png)
![actuator](1q/seed_4/actuator.png)
![populations](1q/seed_4/populations.png)

### random — 5
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_5/result.json)
![dynamics](1q/seed_5/dynamics.png)
![wigner](1q/seed_5/wigner.png)
![actuator](1q/seed_5/actuator.png)
![populations](1q/seed_5/populations.png)

### random — 6
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_6/result.json)
![dynamics](1q/seed_6/dynamics.png)
![wigner](1q/seed_6/wigner.png)
![actuator](1q/seed_6/actuator.png)
![populations](1q/seed_6/populations.png)

### random — 7
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_7/result.json)
![dynamics](1q/seed_7/dynamics.png)
![wigner](1q/seed_7/wigner.png)
![actuator](1q/seed_7/actuator.png)
![populations](1q/seed_7/populations.png)

## 2q_common
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9968369811607432, "probability_std_population": 0.004149267056382401, "probability_median": 0.9982684277923702, "probability_min": 0.9867303860139869, "probability_max": 0.999982212883646, "numerically_valid_count": 8, "validated_goal_count": 7, "validated_goal_fraction": 0.875, "probability_q25": 0.9964709040242288, "probability_q75": 0.9997777960482855, "selection_bias_top_only": false}.
Seed selezionato: 7. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00003451.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_0/result.json)
![dynamics](2q_common/seed_0/dynamics.png)
![wigner](2q_common/seed_0/wigner.png)
![actuator](2q_common/seed_0/actuator.png)
![populations](2q_common/seed_0/populations.png)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_1/result.json)
![dynamics](2q_common/seed_1/dynamics.png)
![wigner](2q_common/seed_1/wigner.png)
![actuator](2q_common/seed_1/actuator.png)
![populations](2q_common/seed_1/populations.png)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_2/result.json)
![dynamics](2q_common/seed_2/dynamics.png)
![wigner](2q_common/seed_2/wigner.png)
![actuator](2q_common/seed_2/actuator.png)
![populations](2q_common/seed_2/populations.png)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_3/result.json)
![dynamics](2q_common/seed_3/dynamics.png)
![wigner](2q_common/seed_3/wigner.png)
![actuator](2q_common/seed_3/actuator.png)
![populations](2q_common/seed_3/populations.png)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_4/result.json)
![dynamics](2q_common/seed_4/dynamics.png)
![wigner](2q_common/seed_4/wigner.png)
![actuator](2q_common/seed_4/actuator.png)
![populations](2q_common/seed_4/populations.png)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_5/result.json)
![dynamics](2q_common/seed_5/dynamics.png)
![wigner](2q_common/seed_5/wigner.png)
![actuator](2q_common/seed_5/actuator.png)
![populations](2q_common/seed_5/populations.png)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_6/result.json)
![dynamics](2q_common/seed_6/dynamics.png)
![wigner](2q_common/seed_6/wigner.png)
![actuator](2q_common/seed_6/actuator.png)
![populations](2q_common/seed_6/populations.png)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_7/result.json)
![dynamics](2q_common/seed_7/dynamics.png)
![wigner](2q_common/seed_7/wigner.png)
![actuator](2q_common/seed_7/actuator.png)
![populations](2q_common/seed_7/populations.png)

## 2q_independent
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999848575070918, "probability_std_population": 9.780171883139636e-06, "probability_median": 0.9999872010187258, "probability_min": 0.99996296477675, "probability_max": 0.9999939466072792, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999830574695046, "probability_q75": 0.999992285139383, "selection_bias_top_only": false}.
Seed selezionato: 2. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00003451.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_0/result.json)
![dynamics](2q_independent/seed_0/dynamics.png)
![wigner](2q_independent/seed_0/wigner.png)
![actuator](2q_independent/seed_0/actuator.png)
![populations](2q_independent/seed_0/populations.png)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_1/result.json)
![dynamics](2q_independent/seed_1/dynamics.png)
![wigner](2q_independent/seed_1/wigner.png)
![actuator](2q_independent/seed_1/actuator.png)
![populations](2q_independent/seed_1/populations.png)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_2/result.json)
![dynamics](2q_independent/seed_2/dynamics.png)
![wigner](2q_independent/seed_2/wigner.png)
![actuator](2q_independent/seed_2/actuator.png)
![populations](2q_independent/seed_2/populations.png)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_3/result.json)
![dynamics](2q_independent/seed_3/dynamics.png)
![wigner](2q_independent/seed_3/wigner.png)
![actuator](2q_independent/seed_3/actuator.png)
![populations](2q_independent/seed_3/populations.png)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_4/result.json)
![dynamics](2q_independent/seed_4/dynamics.png)
![wigner](2q_independent/seed_4/wigner.png)
![actuator](2q_independent/seed_4/actuator.png)
![populations](2q_independent/seed_4/populations.png)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_5/result.json)
![dynamics](2q_independent/seed_5/dynamics.png)
![wigner](2q_independent/seed_5/wigner.png)
![actuator](2q_independent/seed_5/actuator.png)
![populations](2q_independent/seed_5/populations.png)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_6/result.json)
![dynamics](2q_independent/seed_6/dynamics.png)
![wigner](2q_independent/seed_6/wigner.png)
![actuator](2q_independent/seed_6/actuator.png)
![populations](2q_independent/seed_6/populations.png)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_7/result.json)
![dynamics](2q_independent/seed_7/dynamics.png)
![wigner](2q_independent/seed_7/wigner.png)
![actuator](2q_independent/seed_7/actuator.png)
![populations](2q_independent/seed_7/populations.png)

## 2q_normalized_common
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.6004836680187027, "probability_std_population": 0.10767504784691635, "probability_median": 0.6092365392972547, "probability_min": 0.3932623263643489, "probability_max": 0.7506501247146721, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.5548545236815551, "probability_q75": 0.6635722808957976, "selection_bias_top_only": false}.
Seed selezionato: 2. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000198.

### random — 0
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_0/result.json)
![dynamics](2q_normalized_common/seed_0/dynamics.png)
![wigner](2q_normalized_common/seed_0/wigner.png)
![actuator](2q_normalized_common/seed_0/actuator.png)
![populations](2q_normalized_common/seed_0/populations.png)

### random — 1
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_1/result.json)
![dynamics](2q_normalized_common/seed_1/dynamics.png)
![wigner](2q_normalized_common/seed_1/wigner.png)
![actuator](2q_normalized_common/seed_1/actuator.png)
![populations](2q_normalized_common/seed_1/populations.png)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_2/result.json)
![dynamics](2q_normalized_common/seed_2/dynamics.png)
![wigner](2q_normalized_common/seed_2/wigner.png)
![actuator](2q_normalized_common/seed_2/actuator.png)
![populations](2q_normalized_common/seed_2/populations.png)

### random — 3
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_3/result.json)
![dynamics](2q_normalized_common/seed_3/dynamics.png)
![wigner](2q_normalized_common/seed_3/wigner.png)
![actuator](2q_normalized_common/seed_3/actuator.png)
![populations](2q_normalized_common/seed_3/populations.png)

### random — 4
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_4/result.json)
![dynamics](2q_normalized_common/seed_4/dynamics.png)
![wigner](2q_normalized_common/seed_4/wigner.png)
![actuator](2q_normalized_common/seed_4/actuator.png)
![populations](2q_normalized_common/seed_4/populations.png)

### random — 5
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_5/result.json)
![dynamics](2q_normalized_common/seed_5/dynamics.png)
![wigner](2q_normalized_common/seed_5/wigner.png)
![actuator](2q_normalized_common/seed_5/actuator.png)
![populations](2q_normalized_common/seed_5/populations.png)

### random — 6
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_6/result.json)
![dynamics](2q_normalized_common/seed_6/dynamics.png)
![wigner](2q_normalized_common/seed_6/wigner.png)
![actuator](2q_normalized_common/seed_6/actuator.png)
![populations](2q_normalized_common/seed_6/populations.png)

### random — 7
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_7/result.json)
![dynamics](2q_normalized_common/seed_7/dynamics.png)
![wigner](2q_normalized_common/seed_7/wigner.png)
![actuator](2q_normalized_common/seed_7/actuator.png)
![populations](2q_normalized_common/seed_7/populations.png)

## 2q_normalized_independent
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.7254359226324942, "probability_std_population": 0.08904900912833469, "probability_median": 0.7493729218419151, "probability_min": 0.5773135581835351, "probability_max": 0.8378465334419856, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.6470349090995156, "probability_q75": 0.7971790172439478, "selection_bias_top_only": false}.
Seed selezionato: 0. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000198.

### random — 0
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_0/result.json)
![dynamics](2q_normalized_independent/seed_0/dynamics.png)
![wigner](2q_normalized_independent/seed_0/wigner.png)
![actuator](2q_normalized_independent/seed_0/actuator.png)
![populations](2q_normalized_independent/seed_0/populations.png)

### random — 1
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_1/result.json)
![dynamics](2q_normalized_independent/seed_1/dynamics.png)
![wigner](2q_normalized_independent/seed_1/wigner.png)
![actuator](2q_normalized_independent/seed_1/actuator.png)
![populations](2q_normalized_independent/seed_1/populations.png)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_2/result.json)
![dynamics](2q_normalized_independent/seed_2/dynamics.png)
![wigner](2q_normalized_independent/seed_2/wigner.png)
![actuator](2q_normalized_independent/seed_2/actuator.png)
![populations](2q_normalized_independent/seed_2/populations.png)

### random — 3
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_3/result.json)
![dynamics](2q_normalized_independent/seed_3/dynamics.png)
![wigner](2q_normalized_independent/seed_3/wigner.png)
![actuator](2q_normalized_independent/seed_3/actuator.png)
![populations](2q_normalized_independent/seed_3/populations.png)

### random — 4
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_4/result.json)
![dynamics](2q_normalized_independent/seed_4/dynamics.png)
![wigner](2q_normalized_independent/seed_4/wigner.png)
![actuator](2q_normalized_independent/seed_4/actuator.png)
![populations](2q_normalized_independent/seed_4/populations.png)

### random — 5
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_5/result.json)
![dynamics](2q_normalized_independent/seed_5/dynamics.png)
![wigner](2q_normalized_independent/seed_5/wigner.png)
![actuator](2q_normalized_independent/seed_5/actuator.png)
![populations](2q_normalized_independent/seed_5/populations.png)

### random — 6
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_6/result.json)
![dynamics](2q_normalized_independent/seed_6/dynamics.png)
![wigner](2q_normalized_independent/seed_6/wigner.png)
![actuator](2q_normalized_independent/seed_6/actuator.png)
![populations](2q_normalized_independent/seed_6/populations.png)

### random — 7
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_7/result.json)
![dynamics](2q_normalized_independent/seed_7/dynamics.png)
![wigner](2q_normalized_independent/seed_7/wigner.png)
![actuator](2q_normalized_independent/seed_7/actuator.png)
![populations](2q_normalized_independent/seed_7/populations.png)
