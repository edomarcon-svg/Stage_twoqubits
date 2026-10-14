# Risultati v2

Durata fisica T = 52.35987756. T = 10 × tau_s; tau_s = pi/(2*g_ref) = 5.235987756, g_ref = 0.3.

Ogni riga usa la propagazione continua del controllo con il filtro configurato.
P_target è la probabilità target; F_root = sqrt(P_target). Il reset dei qubit, se richiesto, entra in P_target.
Una soluzione non validata non è evidenza di vantaggio fisico. La convergenza dell'ottimizzatore è distinta dalla validazione numerica.
Le statistiche e il seed selezionato riguardano solo partenze casuali; i warm start sono separati.
La banda 99% è una diagnostica del segnale finito, non un limite spettrale imposto. Le fluenze non sono calore dissipato.

| Caso | Seed | P target | F radice | Purezza | Validato | Soglia raggiunta |
|---|---:|---:|---:|---:|---|---|
| 1q | 0 | 0.35280622 | 0.59397493 | 0.673335 | False | False |
| 1q | 1 | 0.32195818 | 0.56741359 | 0.614410 | False | False |
| 1q | 2 | 0.31589024 | 0.56204113 | 0.778418 | False | False |
| 1q | 3 | 0.30448214 | 0.55179900 | 0.627194 | False | False |
| 1q | 4 | 0.34274140 | 0.58544120 | 0.575405 | False | False |
| 1q | 5 | 0.27140611 | 0.52096651 | 0.867215 | False | False |
| 1q | 6 | 0.27205261 | 0.52158663 | 0.721083 | False | False |
| 1q | 7 | 0.28331994 | 0.53227806 | 0.738726 | False | False |
| 2q_common | 0 | 0.91833035 | 0.95829554 | 0.875288 | False | False |
| 2q_common | 1 | 0.85298045 | 0.92356941 | 0.913928 | False | False |
| 2q_common | 2 | 0.87335748 | 0.93453597 | 0.899902 | False | False |
| 2q_common | 3 | 0.90032525 | 0.94885470 | 0.929648 | False | False |
| 2q_common | 4 | 0.86553227 | 0.93033987 | 0.929378 | False | False |
| 2q_common | 5 | 0.82067787 | 0.90591273 | 0.850532 | False | False |
| 2q_common | 6 | 0.80277661 | 0.89597802 | 0.840967 | False | False |
| 2q_common | 7 | 0.93630835 | 0.96763027 | 0.953840 | False | False |
| 2q_independent | 0 | 0.94575920 | 0.97250152 | 0.943953 | False | False |
| 2q_independent | 1 | 0.87552428 | 0.93569454 | 0.882679 | False | False |
| 2q_independent | 2 | 0.94450695 | 0.97185747 | 0.947974 | False | False |
| 2q_independent | 3 | 0.93742222 | 0.96820567 | 0.913620 | False | False |
| 2q_independent | 4 | 0.95089942 | 0.97514072 | 0.932884 | False | False |
| 2q_independent | 5 | 0.92232215 | 0.96037604 | 0.910850 | False | False |
| 2q_independent | 6 | 0.96178111 | 0.98070440 | 0.956661 | False | False |
| 2q_independent | 7 | 0.92905431 | 0.96387463 | 0.927306 | False | False |
| 2q_normalized_common | 0 | 0.44217504 | 0.66496244 | 0.826413 | False | False |
| 2q_normalized_common | 1 | 0.26137760 | 0.51125102 | 0.727794 | False | False |
| 2q_normalized_common | 2 | 0.32695730 | 0.57180180 | 0.591499 | False | False |
| 2q_normalized_common | 3 | 0.37443021 | 0.61190703 | 0.751510 | False | False |
| 2q_normalized_common | 4 | 0.36991690 | 0.60820794 | 0.787004 | False | False |
| 2q_normalized_common | 5 | 0.20867434 | 0.45680886 | 0.749313 | False | False |
| 2q_normalized_common | 6 | 0.17907951 | 0.42317787 | 0.650051 | False | False |
| 2q_normalized_common | 7 | 0.32938560 | 0.57392125 | 0.738625 | False | False |
| 2q_normalized_independent | 0 | 0.45845700 | 0.67709453 | 0.469081 | False | False |
| 2q_normalized_independent | 1 | 0.30323437 | 0.55066720 | 0.739394 | False | False |
| 2q_normalized_independent | 2 | 0.33885999 | 0.58211682 | 0.423513 | False | False |
| 2q_normalized_independent | 3 | 0.37318312 | 0.61088716 | 0.497728 | False | False |
| 2q_normalized_independent | 4 | 0.37136777 | 0.60939951 | 0.560208 | False | False |
| 2q_normalized_independent | 5 | 0.46793539 | 0.68405803 | 0.475282 | False | False |
| 2q_normalized_independent | 6 | 0.29426801 | 0.54246476 | 0.364572 | False | False |
| 2q_normalized_independent | 7 | 0.30121101 | 0.54882694 | 0.481687 | False | False |

## 1q
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.3080821047688358, "probability_std_population": 0.028992247961071284, "probability_median": 0.31018618785822705, "probability_min": 0.2714061094171599, "probability_max": 0.352806222255004, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.2805031053731576, "probability_q75": 0.32715398557201913, "selection_bias_top_only": false}.
Seed selezionato: 0. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.871286078702518, "probability_std_population": 0.043173433756312996, "probability_median": 0.8694448776212249, "probability_min": 0.802776611638942, "probability_max": 0.9363083458667326, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.8449048061836344, "probability_q75": 0.9048265249940548, "selection_bias_top_only": false}.
Seed selezionato: 7. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000037.

### random — 0
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_0/result.json)
![dynamics](2q_common/seed_0/dynamics.png)
![wigner](2q_common/seed_0/wigner.png)
![actuator](2q_common/seed_0/actuator.png)
![populations](2q_common/seed_0/populations.png)

### random — 1
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_1/result.json)
![dynamics](2q_common/seed_1/dynamics.png)
![wigner](2q_common/seed_1/wigner.png)
![actuator](2q_common/seed_1/actuator.png)
![populations](2q_common/seed_1/populations.png)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_2/result.json)
![dynamics](2q_common/seed_2/dynamics.png)
![wigner](2q_common/seed_2/wigner.png)
![actuator](2q_common/seed_2/actuator.png)
![populations](2q_common/seed_2/populations.png)

### random — 3
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_3/result.json)
![dynamics](2q_common/seed_3/dynamics.png)
![wigner](2q_common/seed_3/wigner.png)
![actuator](2q_common/seed_3/actuator.png)
![populations](2q_common/seed_3/populations.png)

### random — 4
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_4/result.json)
![dynamics](2q_common/seed_4/dynamics.png)
![wigner](2q_common/seed_4/wigner.png)
![actuator](2q_common/seed_4/actuator.png)
![populations](2q_common/seed_4/populations.png)

### random — 5
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_5/result.json)
![dynamics](2q_common/seed_5/dynamics.png)
![wigner](2q_common/seed_5/wigner.png)
![actuator](2q_common/seed_5/actuator.png)
![populations](2q_common/seed_5/populations.png)

### random — 6
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: ABNORMAL: .
[Metadati completi](2q_common/seed_6/result.json)
![dynamics](2q_common/seed_6/dynamics.png)
![wigner](2q_common/seed_6/wigner.png)
![actuator](2q_common/seed_6/actuator.png)
![populations](2q_common/seed_6/populations.png)

### random — 7
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_common/seed_7/result.json)
![dynamics](2q_common/seed_7/dynamics.png)
![wigner](2q_common/seed_7/wigner.png)
![actuator](2q_common/seed_7/actuator.png)
![populations](2q_common/seed_7/populations.png)

## 2q_independent
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9334087044991091, "probability_std_population": 0.024736641943666333, "probability_median": 0.9409645847013651, "probability_min": 0.8755242812815439, "probability_max": 0.9617811136647558, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.9273712687400184, "probability_q75": 0.9470442531822121, "selection_bias_top_only": false}.
Seed selezionato: 6. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000037.

### random — 0
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_0/result.json)
![dynamics](2q_independent/seed_0/dynamics.png)
![wigner](2q_independent/seed_0/wigner.png)
![actuator](2q_independent/seed_0/actuator.png)
![populations](2q_independent/seed_0/populations.png)

### random — 1
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_independent/seed_1/result.json)
![dynamics](2q_independent/seed_1/dynamics.png)
![wigner](2q_independent/seed_1/wigner.png)
![actuator](2q_independent/seed_1/actuator.png)
![populations](2q_independent/seed_1/populations.png)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_independent/seed_2/result.json)
![dynamics](2q_independent/seed_2/dynamics.png)
![wigner](2q_independent/seed_2/wigner.png)
![actuator](2q_independent/seed_2/actuator.png)
![populations](2q_independent/seed_2/populations.png)

### random — 3
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_independent/seed_3/result.json)
![dynamics](2q_independent/seed_3/dynamics.png)
![wigner](2q_independent/seed_3/wigner.png)
![actuator](2q_independent/seed_3/actuator.png)
![populations](2q_independent/seed_3/populations.png)

### random — 4
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_4/result.json)
![dynamics](2q_independent/seed_4/dynamics.png)
![wigner](2q_independent/seed_4/wigner.png)
![actuator](2q_independent/seed_4/actuator.png)
![populations](2q_independent/seed_4/populations.png)

### random — 5
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_independent/seed_5/result.json)
![dynamics](2q_independent/seed_5/dynamics.png)
![wigner](2q_independent/seed_5/wigner.png)
![actuator](2q_independent/seed_5/actuator.png)
![populations](2q_independent/seed_5/populations.png)

### random — 6
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_independent/seed_6/result.json)
![dynamics](2q_independent/seed_6/dynamics.png)
![wigner](2q_independent/seed_6/wigner.png)
![actuator](2q_independent/seed_6/actuator.png)
![populations](2q_independent/seed_6/populations.png)

### random — 7
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_independent/seed_7/result.json)
![dynamics](2q_independent/seed_7/dynamics.png)
![wigner](2q_independent/seed_7/wigner.png)
![actuator](2q_independent/seed_7/actuator.png)
![populations](2q_independent/seed_7/populations.png)

## 2q_normalized_common
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.3114995630159564, "probability_std_population": 0.08338771718745998, "probability_median": 0.3281714515516675, "probability_min": 0.17907951265501226, "probability_max": 0.4421750405148969, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.24820178677663307, "probability_q75": 0.3710452247545214, "selection_bias_top_only": false}.
Seed selezionato: 0. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.3635645809386664, "probability_std_population": 0.06421767344828117, "probability_median": 0.3551138776885536, "probability_min": 0.2942680109670821, "probability_max": 0.4679353878642804, "numerically_valid_count": 0, "validated_goal_count": 0, "validated_goal_fraction": 0.0, "probability_q25": 0.3027285268422588, "probability_q75": 0.39450158763307874, "selection_bias_top_only": false}.
Seed selezionato: 5. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

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
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_independent/seed_1/result.json)
![dynamics](2q_normalized_independent/seed_1/dynamics.png)
![wigner](2q_normalized_independent/seed_1/wigner.png)
![actuator](2q_normalized_independent/seed_1/actuator.png)
![populations](2q_normalized_independent/seed_1/populations.png)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
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
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
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
