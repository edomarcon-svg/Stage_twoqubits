# Risultati v2

Durata fisica T = 104.7197551. T = 20 × tau_s; tau_s = pi/(2*g_ref) = 5.235987756, g_ref = 0.3.

Ogni riga usa la propagazione continua del controllo con il filtro configurato.
P_target è la probabilità target; F_root = sqrt(P_target). Il reset dei qubit, se richiesto, entra in P_target.
Una soluzione non validata non è evidenza di vantaggio fisico. La convergenza dell'ottimizzatore è distinta dalla validazione numerica.
Le statistiche e il seed selezionato riguardano solo partenze casuali; i warm start sono separati.
La banda 99% è una diagnostica del segnale finito, non un limite spettrale imposto. Le fluenze non sono calore dissipato.

| Caso | Seed | P target | F radice | Purezza | Validato | Soglia raggiunta |
|---|---:|---:|---:|---:|---|---|
| 1q | 0 | 0.00000001 | 0.00010000 | 0.958522 | True | False |
| 1q | 1 | 0.00000002 | 0.00012821 | 0.990033 | True | False |
| 1q | 2 | 0.00000002 | 0.00014431 | 0.981247 | True | False |
| 1q | 3 | 0.00000005 | 0.00022048 | 0.987262 | True | False |
| 1q | 4 | 0.00000000 | 0.00002367 | 0.985800 | True | False |
| 1q | 5 | 0.00000001 | 0.00010983 | 0.981025 | True | False |
| 1q | 6 | 0.00000001 | 0.00009134 | 0.986963 | True | False |
| 1q | 7 | 0.00000001 | 0.00009727 | 0.986590 | True | False |
| 2q_independent_normalized | 0 | 0.00000000 | 0.00003116 | 0.993477 | True | False |
| 2q_independent_normalized | 1 | 0.00000000 | 0.00003307 | 0.986872 | True | False |
| 2q_independent_normalized | 2 | 0.00000000 | 0.00002169 | 0.993296 | True | False |
| 2q_independent_normalized | 3 | 0.00000000 | 0.00002422 | 0.986741 | True | False |
| 2q_independent_normalized | 4 | 0.00000000 | 0.00001569 | 0.988936 | True | False |
| 2q_independent_normalized | 5 | 0.00000000 | 0.00005002 | 0.990941 | True | False |
| 2q_independent_normalized | 6 | 0.00000000 | 0.00005626 | 0.994035 | True | False |
| 2q_independent_normalized | 7 | 0.00000000 | 0.00001392 | 0.989616 | True | False |
| 2q_independent | 0 | 0.99997464 | 0.99998732 | 0.999968 | False | True |
| 2q_independent | 1 | 0.99995569 | 0.99997785 | 0.999946 | False | True |
| 2q_independent | 2 | 0.99995100 | 0.99997550 | 0.999923 | False | True |
| 2q_independent | 3 | 0.99994712 | 0.99997356 | 0.999919 | False | True |
| 2q_independent | 4 | 0.99995519 | 0.99997760 | 0.999930 | False | True |
| 2q_independent | 5 | 0.99995487 | 0.99997743 | 0.999937 | False | True |
| 2q_independent | 6 | 0.99996596 | 0.99998298 | 0.999952 | False | True |
| 2q_independent | 7 | 0.99993312 | 0.99996656 | 0.999890 | False | True |
| 2q_common | 0 | 0.99997065 | 0.99998533 | 0.999960 | False | True |
| 2q_common | 1 | 0.99992338 | 0.99996169 | 0.999904 | False | True |
| 2q_common | 2 | 0.99995161 | 0.99997581 | 0.999924 | False | True |
| 2q_common | 3 | 0.99994019 | 0.99997010 | 0.999931 | False | True |
| 2q_common | 4 | 0.99996056 | 0.99998028 | 0.999937 | False | True |
| 2q_common | 5 | 0.99997041 | 0.99998520 | 0.999960 | False | True |
| 2q_common | 6 | 0.99993485 | 0.99996742 | 0.999943 | False | True |
| 2q_common | 7 | 0.99993560 | 0.99996780 | 0.999905 | False | True |

## 1q
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 1.578774666514555e-08, "probability_std_population": 1.35916562392758e-08, "probability_median": 1.1031514324443324e-08, "probability_min": 5.601796731534793e-10, "probability_max": 4.861100892453933e-08, "numerically_valid_count": 8, "validated_goal_count": 0, "selection_bias_top_only": false}.
Seed selezionato: 3. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](1q/seed_0/result.json)
![dynamics](1q/seed_0/dynamics.png)
![wigner](1q/seed_0/wigner.png)
![actuator](1q/seed_0/actuator.png)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](1q/seed_1/result.json)
![dynamics](1q/seed_1/dynamics.png)
![wigner](1q/seed_1/wigner.png)
![actuator](1q/seed_1/actuator.png)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](1q/seed_2/result.json)
![dynamics](1q/seed_2/dynamics.png)
![wigner](1q/seed_2/wigner.png)
![actuator](1q/seed_2/actuator.png)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_3/result.json)
![dynamics](1q/seed_3/dynamics.png)
![wigner](1q/seed_3/wigner.png)
![actuator](1q/seed_3/actuator.png)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](1q/seed_4/result.json)
![dynamics](1q/seed_4/dynamics.png)
![wigner](1q/seed_4/wigner.png)
![actuator](1q/seed_4/actuator.png)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](1q/seed_5/result.json)
![dynamics](1q/seed_5/dynamics.png)
![wigner](1q/seed_5/wigner.png)
![actuator](1q/seed_5/actuator.png)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](1q/seed_6/result.json)
![dynamics](1q/seed_6/dynamics.png)
![wigner](1q/seed_6/wigner.png)
![actuator](1q/seed_6/actuator.png)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](1q/seed_7/result.json)
![dynamics](1q/seed_7/dynamics.png)
![wigner](1q/seed_7/wigner.png)
![actuator](1q/seed_7/actuator.png)

## 2q_independent_normalized
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 1.1534912444378646e-09, "probability_std_population": 1.0266916525835692e-09, "probability_median": 7.786762024504657e-10, "probability_min": 1.9371279718848282e-10, "probability_max": 3.164787451413314e-09, "numerically_valid_count": 8, "validated_goal_count": 0, "selection_bias_top_only": false}.
Seed selezionato: 6. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000000.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](2q_independent_normalized/seed_0/result.json)
![dynamics](2q_independent_normalized/seed_0/dynamics.png)
![wigner](2q_independent_normalized/seed_0/wigner.png)
![actuator](2q_independent_normalized/seed_0/actuator.png)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](2q_independent_normalized/seed_1/result.json)
![dynamics](2q_independent_normalized/seed_1/dynamics.png)
![wigner](2q_independent_normalized/seed_1/wigner.png)
![actuator](2q_independent_normalized/seed_1/actuator.png)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](2q_independent_normalized/seed_2/result.json)
![dynamics](2q_independent_normalized/seed_2/dynamics.png)
![wigner](2q_independent_normalized/seed_2/wigner.png)
![actuator](2q_independent_normalized/seed_2/actuator.png)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](2q_independent_normalized/seed_3/result.json)
![dynamics](2q_independent_normalized/seed_3/dynamics.png)
![wigner](2q_independent_normalized/seed_3/wigner.png)
![actuator](2q_independent_normalized/seed_3/actuator.png)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](2q_independent_normalized/seed_4/result.json)
![dynamics](2q_independent_normalized/seed_4/dynamics.png)
![wigner](2q_independent_normalized/seed_4/wigner.png)
![actuator](2q_independent_normalized/seed_4/actuator.png)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](2q_independent_normalized/seed_5/result.json)
![dynamics](2q_independent_normalized/seed_5/dynamics.png)
![wigner](2q_independent_normalized/seed_5/wigner.png)
![actuator](2q_independent_normalized/seed_5/actuator.png)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](2q_independent_normalized/seed_6/result.json)
![dynamics](2q_independent_normalized/seed_6/dynamics.png)
![wigner](2q_independent_normalized/seed_6/wigner.png)
![actuator](2q_independent_normalized/seed_6/actuator.png)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL.
[Metadati completi](2q_independent_normalized/seed_7/result.json)
![dynamics](2q_independent_normalized/seed_7/dynamics.png)
![wigner](2q_independent_normalized/seed_7/wigner.png)
![actuator](2q_independent_normalized/seed_7/actuator.png)

## 2q_independent
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999546980760177, "probability_std_population": 1.1524817755869309e-05, "probability_median": 0.9999550315671741, "probability_min": 0.9999331167261921, "probability_max": 0.9999746361773092, "numerically_valid_count": 0, "validated_goal_count": 0, "selection_bias_top_only": false}.
Seed selezionato: 0. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000096.

### random — 0
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_0/result.json)
![dynamics](2q_independent/seed_0/dynamics.png)
![wigner](2q_independent/seed_0/wigner.png)
![actuator](2q_independent/seed_0/actuator.png)

### random — 1
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_1/result.json)
![dynamics](2q_independent/seed_1/dynamics.png)
![wigner](2q_independent/seed_1/wigner.png)
![actuator](2q_independent/seed_1/actuator.png)

### random — 2
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_2/result.json)
![dynamics](2q_independent/seed_2/dynamics.png)
![wigner](2q_independent/seed_2/wigner.png)
![actuator](2q_independent/seed_2/actuator.png)

### random — 3
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_3/result.json)
![dynamics](2q_independent/seed_3/dynamics.png)
![wigner](2q_independent/seed_3/wigner.png)
![actuator](2q_independent/seed_3/actuator.png)

### random — 4
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_4/result.json)
![dynamics](2q_independent/seed_4/dynamics.png)
![wigner](2q_independent/seed_4/wigner.png)
![actuator](2q_independent/seed_4/actuator.png)

### random — 5
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_5/result.json)
![dynamics](2q_independent/seed_5/dynamics.png)
![wigner](2q_independent/seed_5/wigner.png)
![actuator](2q_independent/seed_5/actuator.png)

### random — 6
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_6/result.json)
![dynamics](2q_independent/seed_6/dynamics.png)
![wigner](2q_independent/seed_6/wigner.png)
![actuator](2q_independent/seed_6/actuator.png)

### random — 7
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_independent/seed_7/result.json)
![dynamics](2q_independent/seed_7/dynamics.png)
![wigner](2q_independent/seed_7/wigner.png)
![actuator](2q_independent/seed_7/actuator.png)

## 2q_common
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999484067249198, "probability_std_population": 1.6501968818842466e-05, "probability_median": 0.9999459026420674, "probability_min": 0.9999233799219465, "probability_max": 0.9999706528420098, "numerically_valid_count": 0, "validated_goal_count": 0, "selection_bias_top_only": false}.
Seed selezionato: 0. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000096.

### random — 0
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_0/result.json)
![dynamics](2q_common/seed_0/dynamics.png)
![wigner](2q_common/seed_0/wigner.png)
![actuator](2q_common/seed_0/actuator.png)

### random — 1
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_1/result.json)
![dynamics](2q_common/seed_1/dynamics.png)
![wigner](2q_common/seed_1/wigner.png)
![actuator](2q_common/seed_1/actuator.png)

### random — 2
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_2/result.json)
![dynamics](2q_common/seed_2/dynamics.png)
![wigner](2q_common/seed_2/wigner.png)
![actuator](2q_common/seed_2/actuator.png)

### random — 3
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_3/result.json)
![dynamics](2q_common/seed_3/dynamics.png)
![wigner](2q_common/seed_3/wigner.png)
![actuator](2q_common/seed_3/actuator.png)

### random — 4
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_4/result.json)
![dynamics](2q_common/seed_4/dynamics.png)
![wigner](2q_common/seed_4/wigner.png)
![actuator](2q_common/seed_4/actuator.png)

### random — 5
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_5/result.json)
![dynamics](2q_common/seed_5/dynamics.png)
![wigner](2q_common/seed_5/wigner.png)
![actuator](2q_common/seed_5/actuator.png)

### random — 6
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_6/result.json)
![dynamics](2q_common/seed_6/dynamics.png)
![wigner](2q_common/seed_6/wigner.png)
![actuator](2q_common/seed_6/actuator.png)

### random — 7
Controlli numerici falliti: dimension, norm, parity.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_7/result.json)
![dynamics](2q_common/seed_7/dynamics.png)
![wigner](2q_common/seed_7/wigner.png)
![actuator](2q_common/seed_7/actuator.png)
