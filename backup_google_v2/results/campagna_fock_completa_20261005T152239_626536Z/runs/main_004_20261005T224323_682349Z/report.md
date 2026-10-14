# Risultati v2

Durata fisica T = 52.35987756. T = 10 × tau_s; tau_s = pi/(2*g_ref) = 5.235987756, g_ref = 0.3.

Ogni riga usa la propagazione continua del controllo con il filtro configurato.
P_target è la probabilità target; F_root = sqrt(P_target). Il reset dei qubit, se richiesto, entra in P_target.
Una soluzione non validata non è evidenza di vantaggio fisico. La convergenza dell'ottimizzatore è distinta dalla validazione numerica.
Le statistiche e il seed selezionato riguardano solo partenze casuali; i warm start sono separati.
La banda 99% è una diagnostica del segnale finito, non un limite spettrale imposto. Le fluenze non sono calore dissipato.

| Caso | Seed | P target | F radice | Purezza | Validato | Soglia raggiunta |
|---|---:|---:|---:|---:|---|---|
| 1q | 0 | 0.99999643 | 0.99999822 | 0.999998 | True | True |
| 1q | 1 | 0.99999777 | 0.99999889 | 0.999999 | True | True |
| 1q | 2 | 0.99999610 | 0.99999805 | 0.999997 | True | True |
| 1q | 3 | 0.99999688 | 0.99999844 | 0.999999 | True | True |
| 1q | 4 | 0.99999799 | 0.99999899 | 0.999999 | True | True |
| 1q | 5 | 0.99999671 | 0.99999835 | 0.999999 | True | True |
| 1q | 6 | 0.99999709 | 0.99999855 | 0.999999 | True | True |
| 1q | 7 | 0.99999600 | 0.99999800 | 0.999998 | True | True |
| 2q_common | 0 | 0.99999585 | 0.99999792 | 0.999997 | True | True |
| 2q_common | 1 | 0.99999569 | 0.99999785 | 0.999996 | True | True |
| 2q_common | 2 | 0.99999329 | 0.99999664 | 0.999992 | True | True |
| 2q_common | 3 | 0.99999746 | 0.99999873 | 0.999998 | True | True |
| 2q_common | 4 | 0.99999663 | 0.99999832 | 0.999997 | True | True |
| 2q_common | 5 | 0.99999746 | 0.99999873 | 0.999999 | True | True |
| 2q_common | 6 | 0.99999615 | 0.99999808 | 0.999996 | True | True |
| 2q_common | 7 | 0.99999760 | 0.99999880 | 0.999998 | True | True |
| 2q_independent | 0 | 0.99999765 | 0.99999882 | 0.999998 | True | True |
| 2q_independent | 1 | 0.99999710 | 0.99999855 | 0.999996 | True | True |
| 2q_independent | 2 | 0.99999639 | 0.99999819 | 0.999996 | True | True |
| 2q_independent | 3 | 0.99999831 | 0.99999916 | 0.999999 | True | True |
| 2q_independent | 4 | 0.99999620 | 0.99999810 | 0.999997 | True | True |
| 2q_independent | 5 | 0.99999734 | 0.99999867 | 0.999998 | True | True |
| 2q_independent | 6 | 0.99999797 | 0.99999899 | 0.999998 | True | True |
| 2q_independent | 7 | 0.99999753 | 0.99999876 | 0.999998 | True | True |
| 2q_normalized_common | 0 | 0.99999273 | 0.99999636 | 0.999994 | True | True |
| 2q_normalized_common | 1 | 0.99999325 | 0.99999662 | 0.999994 | True | True |
| 2q_normalized_common | 2 | 0.99999575 | 0.99999787 | 0.999996 | True | True |
| 2q_normalized_common | 3 | 0.99998977 | 0.99999488 | 0.999989 | True | True |
| 2q_normalized_common | 4 | 0.99969300 | 0.99984649 | 0.999656 | True | True |
| 2q_normalized_common | 5 | 0.99998676 | 0.99999338 | 0.999992 | True | True |
| 2q_normalized_common | 6 | 0.99998704 | 0.99999352 | 0.999982 | True | True |
| 2q_normalized_common | 7 | 0.99999099 | 0.99999550 | 0.999989 | True | True |
| 2q_normalized_independent | 0 | 0.99999540 | 0.99999770 | 0.999995 | True | True |
| 2q_normalized_independent | 1 | 0.99999586 | 0.99999793 | 0.999996 | True | True |
| 2q_normalized_independent | 2 | 0.99999338 | 0.99999669 | 0.999995 | True | True |
| 2q_normalized_independent | 3 | 0.99999125 | 0.99999563 | 0.999990 | True | True |
| 2q_normalized_independent | 4 | 0.99999184 | 0.99999592 | 0.999989 | True | True |
| 2q_normalized_independent | 5 | 0.99999647 | 0.99999824 | 0.999996 | True | True |
| 2q_normalized_independent | 6 | 0.99999279 | 0.99999640 | 0.999993 | True | True |
| 2q_normalized_independent | 7 | 0.99999571 | 0.99999785 | 0.999994 | True | True |

## 1q
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999968714275845, "probability_std_population": 6.778981620733381e-07, "probability_median": 0.9999967938205561, "probability_min": 0.9999959963634417, "probability_max": 0.9999979870185755, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999963500079379, "probability_q75": 0.9999972622367572, "selection_bias_top_only": false}.
Seed selezionato: 4. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00284484.

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
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
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
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999962664821798, "probability_std_population": 1.3295012639644844e-06, "probability_median": 0.9999963916877042, "probability_min": 0.9999932878959198, "probability_max": 0.9999975979453213, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.999995809975042, "probability_q75": 0.9999974583883839, "selection_bias_top_only": false}.
Seed selezionato: 7. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.02429214.

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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.999997311302957, "probability_std_population": 6.830041083405549e-07, "probability_median": 0.9999974356102248, "probability_min": 0.9999962006831494, "probability_max": 0.999998312122953, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999969235576494, "probability_q75": 0.9999977279051119, "selection_bias_top_only": false}.
Seed selezionato: 3. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.02429214.

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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999536593934006, "probability_std_population": 9.856286246925284e-05, "probability_median": 0.999990377818742, "probability_min": 0.999692996843959, "probability_max": 0.9999957480499008, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999869700007129, "probability_q75": 0.9999928579366278, "selection_bias_top_only": false}.
Seed selezionato: 2. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00248696.

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
Controlli numerici falliti: nessuno.
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
Controlli numerici falliti: nessuno.
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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999940889258456, "probability_std_population": 1.8855148472327491e-06, "probability_median": 0.9999943910148629, "probability_min": 0.999991254110123, "probability_max": 0.9999964739301321, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999925559645835, "probability_q75": 0.9999957465308036, "selection_bias_top_only": false}.
Seed selezionato: 5. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00248696.

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
