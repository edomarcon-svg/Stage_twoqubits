# Risultati v2

Durata fisica T = 52.35987756. T = 10 × tau_s; tau_s = pi/(2*g_ref) = 5.235987756, g_ref = 0.3.

Ogni riga usa la propagazione continua del controllo con il filtro configurato.
P_target è la probabilità target; F_root = sqrt(P_target). Il reset dei qubit, se richiesto, entra in P_target.
Una soluzione non validata non è evidenza di vantaggio fisico. La convergenza dell'ottimizzatore è distinta dalla validazione numerica.
Le statistiche e il seed selezionato riguardano solo partenze casuali; i warm start sono separati.
La banda 99% è una diagnostica del segnale finito, non un limite spettrale imposto. Le fluenze non sono calore dissipato.

| Caso | Seed | P target | F radice | Purezza | Validato | Soglia raggiunta |
|---|---:|---:|---:|---:|---|---|
| 1q | 0 | 0.70315751 | 0.83854488 | 0.897471 | False | False |
| 1q | 1 | 0.67983422 | 0.82452060 | 0.762101 | False | False |
| 1q | 2 | 0.64276724 | 0.80172766 | 0.797645 | False | False |
| 1q | 3 | 0.62829418 | 0.79265010 | 0.620789 | False | False |
| 1q | 4 | 0.65752314 | 0.81087800 | 0.754206 | False | False |
| 1q | 5 | 0.57346632 | 0.75727559 | 0.676321 | False | False |
| 1q | 6 | 0.62261421 | 0.78905906 | 0.638272 | False | False |
| 1q | 7 | 0.62147977 | 0.78833988 | 0.634794 | False | False |
| 2q_common | 0 | 0.96712965 | 0.98342750 | 0.959082 | False | False |
| 2q_common | 1 | 0.96783660 | 0.98378687 | 0.956482 | False | False |
| 2q_common | 2 | 0.97598805 | 0.98792108 | 0.974848 | False | False |
| 2q_common | 3 | 0.98780415 | 0.99388337 | 0.981326 | False | False |
| 2q_common | 4 | 0.97515645 | 0.98750010 | 0.976534 | False | False |
| 2q_common | 5 | 0.99750293 | 0.99875068 | 0.997250 | True | True |
| 2q_common | 6 | 0.99204137 | 0.99601274 | 0.992592 | False | True |
| 2q_common | 7 | 0.99987902 | 0.99993951 | 0.999863 | True | True |
| 2q_independent | 0 | 0.99996564 | 0.99998282 | 0.999958 | True | True |
| 2q_independent | 1 | 0.99941382 | 0.99970687 | 0.999022 | True | True |
| 2q_independent | 2 | 0.99988248 | 0.99994124 | 0.999823 | True | True |
| 2q_independent | 3 | 0.99992600 | 0.99996300 | 0.999889 | True | True |
| 2q_independent | 4 | 0.99994772 | 0.99997386 | 0.999928 | True | True |
| 2q_independent | 5 | 0.99996980 | 0.99998490 | 0.999949 | True | True |
| 2q_independent | 6 | 0.99983191 | 0.99991595 | 0.999719 | True | True |
| 2q_independent | 7 | 0.99996087 | 0.99998044 | 0.999946 | True | True |
| 2q_normalized_common | 0 | 0.50685706 | 0.71193894 | 0.784685 | False | False |
| 2q_normalized_common | 1 | 0.61388968 | 0.78351112 | 0.765995 | False | False |
| 2q_normalized_common | 2 | 0.67618429 | 0.82230425 | 0.797155 | False | False |
| 2q_normalized_common | 3 | 0.55645903 | 0.74596182 | 0.751655 | False | False |
| 2q_normalized_common | 4 | 0.56613482 | 0.75241931 | 0.758035 | False | False |
| 2q_normalized_common | 5 | 0.51929617 | 0.72062207 | 0.823447 | False | False |
| 2q_normalized_common | 6 | 0.55576783 | 0.74549837 | 0.794268 | False | False |
| 2q_normalized_common | 7 | 0.65134098 | 0.80705699 | 0.859083 | False | False |
| 2q_normalized_independent | 0 | 0.73157092 | 0.85531919 | 0.855938 | False | False |
| 2q_normalized_independent | 1 | 0.61877629 | 0.78662334 | 0.864781 | False | False |
| 2q_normalized_independent | 2 | 0.77789417 | 0.88198309 | 0.691289 | False | False |
| 2q_normalized_independent | 3 | 0.73035821 | 0.85460997 | 0.849429 | False | False |
| 2q_normalized_independent | 4 | 0.59852689 | 0.77364520 | 0.815590 | False | False |
| 2q_normalized_independent | 5 | 0.82919913 | 0.91060372 | 0.763801 | False | False |
| 2q_normalized_independent | 6 | 0.71949935 | 0.84823307 | 0.780289 | False | False |
| 2q_normalized_independent | 7 | 0.76207983 | 0.87297184 | 0.690334 | False | False |

## 1q
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.6411420718432799, "probability_std_population": 0.03723060055199197, "probability_median": 0.6355307060139784, "probability_min": 0.5734663172574099, "probability_max": 0.7031575100326513, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.6223305992359518, "probability_q75": 0.6631009076178068, "selection_bias_top_only": false}.
Seed selezionato: 0. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

### random — 0
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_0/result.json)

### random — 1
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_1/result.json)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_2/result.json)

### random — 3
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_3/result.json)

### random — 4
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_4/result.json)

### random — 5
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_5/result.json)

### random — 6
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_6/result.json)

### random — 7
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_7/result.json)

## 2q_common
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9829172770639871, "probability_std_population": 0.012209079651414831, "probability_median": 0.9818961003302551, "probability_min": 0.9671296502795421, "probability_max": 0.9998790167770881, "numerically_valid_count": 2, "validated_goal_count": 2, "validated_goal_fraction": 0.25, "probability_q25": 0.9733264874859945, "probability_q75": 0.9934067609868863, "selection_bias_top_only": false}.
Seed selezionato: 7. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000037.

### random — 0
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_0/result.json)

### random — 1
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_1/result.json)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_2/result.json)

### random — 3
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_3/result.json)

### random — 4
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_4/result.json)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_5/result.json)

### random — 6
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_6/result.json)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_7/result.json)

## 2q_independent
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9998622796092929, "probability_std_population": 0.00017527497576806344, "probability_median": 0.9999368591054245, "probability_min": 0.9994138204125055, "probability_max": 0.999969795738848, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9998698372137627, "probability_q75": 0.9999620654431369, "selection_bias_top_only": false}.
Seed selezionato: 5. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000037.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_0/result.json)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_1/result.json)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_2/result.json)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_3/result.json)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_independent/seed_4/result.json)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_5/result.json)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_6/result.json)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_7/result.json)

## 2q_normalized_common
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.5807412324370529, "probability_std_population": 0.05684796805037519, "probability_median": 0.5612969284178091, "probability_min": 0.5068570587956254, "probability_max": 0.6761842868197824, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.546649911832235, "probability_q75": 0.6232525054155175, "selection_bias_top_only": false}.
Seed selezionato: 2. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

### random — 0
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_0/result.json)

### random — 1
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: ABNORMAL: .
[Metadati completi](2q_normalized_common/seed_1/result.json)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_2/result.json)

### random — 3
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_3/result.json)

### random — 4
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_4/result.json)

### random — 5
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_5/result.json)

### random — 6
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_6/result.json)

### random — 7
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_7/result.json)

## 2q_normalized_independent
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.7209880972081281, "probability_std_population": 0.0727001301201666, "probability_median": 0.7309645630191728, "probability_min": 0.5985268934725919, "probability_max": 0.8291991320195748, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.6943185814072174, "probability_q75": 0.7660334110652919, "selection_bias_top_only": false}.
Seed selezionato: 5. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

### random — 0
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_0/result.json)

### random — 1
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_1/result.json)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_2/result.json)

### random — 3
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_3/result.json)

### random — 4
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_4/result.json)

### random — 5
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_5/result.json)

### random — 6
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_6/result.json)

### random — 7
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_7/result.json)
