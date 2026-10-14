# Risultati v2

Durata fisica T = 104.7197551. T = 20 × tau_s; tau_s = pi/(2*g_ref) = 5.235987756, g_ref = 0.3.

Ogni riga usa la propagazione continua del controllo con il filtro configurato.
P_target è la probabilità target; F_root = sqrt(P_target). Il reset dei qubit, se richiesto, entra in P_target.
Una soluzione non validata non è evidenza di vantaggio fisico. La convergenza dell'ottimizzatore è distinta dalla validazione numerica.
Le statistiche e il seed selezionato riguardano solo partenze casuali; i warm start sono separati.
La banda 99% è una diagnostica del segnale finito, non un limite spettrale imposto. Le fluenze non sono calore dissipato.

| Caso | Seed | P target | F radice | Purezza | Validato | Soglia raggiunta |
|---|---:|---:|---:|---:|---|---|
| 1q | 0 | 0.99998993 | 0.99999497 | 0.999992 | True | True |
| 1q | 1 | 0.99998396 | 0.99999198 | 0.999979 | True | True |
| 1q | 2 | 0.99999184 | 0.99999592 | 0.999993 | True | True |
| 1q | 3 | 0.99999476 | 0.99999738 | 0.999995 | True | True |
| 1q | 4 | 0.99999354 | 0.99999677 | 0.999995 | True | True |
| 1q | 5 | 0.99998219 | 0.99999110 | 0.999980 | True | True |
| 1q | 6 | 0.99999274 | 0.99999637 | 0.999992 | True | True |
| 1q | 7 | 0.99999304 | 0.99999652 | 0.999996 | True | True |
| 2q_common | 0 | 0.99999731 | 0.99999866 | 0.999997 | True | True |
| 2q_common | 1 | 0.99999481 | 0.99999740 | 0.999995 | True | True |
| 2q_common | 2 | 0.99999474 | 0.99999737 | 0.999995 | True | True |
| 2q_common | 3 | 0.99999578 | 0.99999789 | 0.999995 | True | True |
| 2q_common | 4 | 0.99999591 | 0.99999796 | 0.999995 | True | True |
| 2q_common | 5 | 0.99999617 | 0.99999808 | 0.999995 | True | True |
| 2q_common | 6 | 0.99999400 | 0.99999700 | 0.999993 | True | True |
| 2q_common | 7 | 0.99999548 | 0.99999774 | 0.999995 | True | True |
| 2q_independent | 0 | 0.99999521 | 0.99999760 | 0.999995 | True | True |
| 2q_independent | 1 | 0.99999014 | 0.99999507 | 0.999986 | True | True |
| 2q_independent | 2 | 0.99999503 | 0.99999751 | 0.999994 | True | True |
| 2q_independent | 3 | 0.99999425 | 0.99999712 | 0.999992 | True | True |
| 2q_independent | 4 | 0.99999543 | 0.99999772 | 0.999994 | True | True |
| 2q_independent | 5 | 0.99999253 | 0.99999627 | 0.999991 | True | True |
| 2q_independent | 6 | 0.99999382 | 0.99999691 | 0.999991 | True | True |
| 2q_independent | 7 | 0.99999181 | 0.99999590 | 0.999989 | True | True |
| 2q_normalized_common | 0 | 0.99997279 | 0.99998639 | 0.999966 | True | True |
| 2q_normalized_common | 1 | 0.99993867 | 0.99996933 | 0.999919 | True | True |
| 2q_normalized_common | 2 | 0.97517777 | 0.98751089 | 0.974051 | False | False |
| 2q_normalized_common | 3 | 0.99997764 | 0.99998882 | 0.999977 | True | True |
| 2q_normalized_common | 4 | 0.99998526 | 0.99999263 | 0.999979 | True | True |
| 2q_normalized_common | 5 | 0.97281077 | 0.98631170 | 0.973745 | False | False |
| 2q_normalized_common | 6 | 0.99989959 | 0.99994980 | 0.999861 | True | True |
| 2q_normalized_common | 7 | 0.99997996 | 0.99998998 | 0.999974 | True | True |
| 2q_normalized_independent | 0 | 0.99999055 | 0.99999527 | 0.999986 | True | True |
| 2q_normalized_independent | 1 | 0.99998536 | 0.99999268 | 0.999978 | True | True |
| 2q_normalized_independent | 2 | 0.99998841 | 0.99999420 | 0.999983 | True | True |
| 2q_normalized_independent | 3 | 0.99999286 | 0.99999643 | 0.999990 | True | True |
| 2q_normalized_independent | 4 | 0.99998465 | 0.99999233 | 0.999978 | True | True |
| 2q_normalized_independent | 5 | 0.99998720 | 0.99999360 | 0.999983 | True | True |
| 2q_normalized_independent | 6 | 0.99998446 | 0.99999223 | 0.999977 | True | True |
| 2q_normalized_independent | 7 | 0.99998383 | 0.99999192 | 0.999975 | True | True |

## 1q
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999902507772411, "probability_std_population": 4.361956217235183e-06, "probability_median": 0.9999922880008898, "probability_min": 0.999982193598956, "probability_max": 0.9999947637867214, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999884389166934, "probability_q75": 0.999993162933595, "selection_bias_top_only": false}.
Seed selezionato: 3. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_0/result.json)
![dynamics](1q/seed_0/dynamics.png)
![wigner](1q/seed_0/wigner.png)
![actuator](1q/seed_0/actuator.png)
![populations](1q/seed_0/populations.png)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_1/result.json)
![dynamics](1q/seed_1/dynamics.png)
![wigner](1q/seed_1/wigner.png)
![actuator](1q/seed_1/actuator.png)
![populations](1q/seed_1/populations.png)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_2/result.json)
![dynamics](1q/seed_2/dynamics.png)
![wigner](1q/seed_2/wigner.png)
![actuator](1q/seed_2/actuator.png)
![populations](1q/seed_2/populations.png)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_3/result.json)
![dynamics](1q/seed_3/dynamics.png)
![wigner](1q/seed_3/wigner.png)
![actuator](1q/seed_3/actuator.png)
![populations](1q/seed_3/populations.png)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_4/result.json)
![dynamics](1q/seed_4/dynamics.png)
![wigner](1q/seed_4/wigner.png)
![actuator](1q/seed_4/actuator.png)
![populations](1q/seed_4/populations.png)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_5/result.json)
![dynamics](1q/seed_5/dynamics.png)
![wigner](1q/seed_5/wigner.png)
![actuator](1q/seed_5/actuator.png)
![populations](1q/seed_5/populations.png)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_6/result.json)
![dynamics](1q/seed_6/dynamics.png)
![wigner](1q/seed_6/wigner.png)
![actuator](1q/seed_6/actuator.png)
![populations](1q/seed_6/populations.png)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_7/result.json)
![dynamics](1q/seed_7/dynamics.png)
![wigner](1q/seed_7/wigner.png)
![actuator](1q/seed_7/actuator.png)
![populations](1q/seed_7/populations.png)

## 2q_common
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999955253226189, "probability_std_population": 9.530149060977817e-07, "probability_median": 0.9999956301209365, "probability_min": 0.9999940003161687, "probability_max": 0.9999973102449298, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999947922207844, "probability_q75": 0.9999959774518874, "selection_bias_top_only": false}.
Seed selezionato: 0. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000096.

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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999935269944844, "probability_std_population": 1.7580701302655927e-06, "probability_median": 0.9999940338579822, "probability_min": 0.9999901416538093, "probability_max": 0.9999954310979026, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999923503462796, "probability_q75": 0.9999950739220832, "selection_bias_top_only": false}.
Seed selezionato: 4. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000096.

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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9934678043002435, "probability_std_population": 0.011258644937650424, "probability_median": 0.999955726676655, "probability_min": 0.9728107677603172, "probability_max": 0.9999852572372905, "numerically_valid_count": 6, "validated_goal_count": 6, "validated_goal_fraction": 0.75, "probability_q25": 0.9937191363650195, "probability_q75": 0.9999782190375827, "selection_bias_top_only": false}.
Seed selezionato: 4. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_0/result.json)
![dynamics](2q_normalized_common/seed_0/dynamics.png)
![wigner](2q_normalized_common/seed_0/wigner.png)
![actuator](2q_normalized_common/seed_0/actuator.png)
![populations](2q_normalized_common/seed_0/populations.png)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_1/result.json)
![dynamics](2q_normalized_common/seed_1/dynamics.png)
![wigner](2q_normalized_common/seed_1/wigner.png)
![actuator](2q_normalized_common/seed_1/actuator.png)
![populations](2q_normalized_common/seed_1/populations.png)

### random — 2
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_2/result.json)
![dynamics](2q_normalized_common/seed_2/dynamics.png)
![wigner](2q_normalized_common/seed_2/wigner.png)
![actuator](2q_normalized_common/seed_2/actuator.png)
![populations](2q_normalized_common/seed_2/populations.png)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_3/result.json)
![dynamics](2q_normalized_common/seed_3/dynamics.png)
![wigner](2q_normalized_common/seed_3/wigner.png)
![actuator](2q_normalized_common/seed_3/actuator.png)
![populations](2q_normalized_common/seed_3/populations.png)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_4/result.json)
![dynamics](2q_normalized_common/seed_4/dynamics.png)
![wigner](2q_normalized_common/seed_4/wigner.png)
![actuator](2q_normalized_common/seed_4/actuator.png)
![populations](2q_normalized_common/seed_4/populations.png)

### random — 5
Controlli numerici falliti: time_grid.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_5/result.json)
![dynamics](2q_normalized_common/seed_5/dynamics.png)
![wigner](2q_normalized_common/seed_5/wigner.png)
![actuator](2q_normalized_common/seed_5/actuator.png)
![populations](2q_normalized_common/seed_5/populations.png)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_6/result.json)
![dynamics](2q_normalized_common/seed_6/dynamics.png)
![wigner](2q_normalized_common/seed_6/wigner.png)
![actuator](2q_normalized_common/seed_6/actuator.png)
![populations](2q_normalized_common/seed_6/populations.png)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_7/result.json)
![dynamics](2q_normalized_common/seed_7/dynamics.png)
![wigner](2q_normalized_common/seed_7/wigner.png)
![actuator](2q_normalized_common/seed_7/actuator.png)
![populations](2q_normalized_common/seed_7/populations.png)

## 2q_normalized_independent
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999871637235724, "probability_std_population": 3.0280212058198138e-06, "probability_median": 0.9999862772933863, "probability_min": 0.999983830619265, "probability_max": 0.9999928570657491, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999846057901948, "probability_q75": 0.9999889406022933, "selection_bias_top_only": false}.
Seed selezionato: 3. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_0/result.json)
![dynamics](2q_normalized_independent/seed_0/dynamics.png)
![wigner](2q_normalized_independent/seed_0/wigner.png)
![actuator](2q_normalized_independent/seed_0/actuator.png)
![populations](2q_normalized_independent/seed_0/populations.png)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_1/result.json)
![dynamics](2q_normalized_independent/seed_1/dynamics.png)
![wigner](2q_normalized_independent/seed_1/wigner.png)
![actuator](2q_normalized_independent/seed_1/actuator.png)
![populations](2q_normalized_independent/seed_1/populations.png)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_2/result.json)
![dynamics](2q_normalized_independent/seed_2/dynamics.png)
![wigner](2q_normalized_independent/seed_2/wigner.png)
![actuator](2q_normalized_independent/seed_2/actuator.png)
![populations](2q_normalized_independent/seed_2/populations.png)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_3/result.json)
![dynamics](2q_normalized_independent/seed_3/dynamics.png)
![wigner](2q_normalized_independent/seed_3/wigner.png)
![actuator](2q_normalized_independent/seed_3/actuator.png)
![populations](2q_normalized_independent/seed_3/populations.png)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_4/result.json)
![dynamics](2q_normalized_independent/seed_4/dynamics.png)
![wigner](2q_normalized_independent/seed_4/wigner.png)
![actuator](2q_normalized_independent/seed_4/actuator.png)
![populations](2q_normalized_independent/seed_4/populations.png)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_5/result.json)
![dynamics](2q_normalized_independent/seed_5/dynamics.png)
![wigner](2q_normalized_independent/seed_5/wigner.png)
![actuator](2q_normalized_independent/seed_5/actuator.png)
![populations](2q_normalized_independent/seed_5/populations.png)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_6/result.json)
![dynamics](2q_normalized_independent/seed_6/dynamics.png)
![wigner](2q_normalized_independent/seed_6/wigner.png)
![actuator](2q_normalized_independent/seed_6/actuator.png)
![populations](2q_normalized_independent/seed_6/populations.png)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_7/result.json)
![dynamics](2q_normalized_independent/seed_7/dynamics.png)
![wigner](2q_normalized_independent/seed_7/wigner.png)
![actuator](2q_normalized_independent/seed_7/actuator.png)
![populations](2q_normalized_independent/seed_7/populations.png)
