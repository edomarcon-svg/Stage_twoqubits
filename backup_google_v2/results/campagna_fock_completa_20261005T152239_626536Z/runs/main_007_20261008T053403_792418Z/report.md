# Risultati v2

Durata fisica T = 104.7197551. T = 20 × tau_s; tau_s = pi/(2*g_ref) = 5.235987756, g_ref = 0.3.

Ogni riga usa la propagazione continua del controllo con il filtro configurato.
P_target è la probabilità target; F_root = sqrt(P_target). Il reset dei qubit, se richiesto, entra in P_target.
Una soluzione non validata non è evidenza di vantaggio fisico. La convergenza dell'ottimizzatore è distinta dalla validazione numerica.
Le statistiche e il seed selezionato riguardano solo partenze casuali; i warm start sono separati.
La banda 99% è una diagnostica del segnale finito, non un limite spettrale imposto. Le fluenze non sono calore dissipato.

| Caso | Seed | P target | F radice | Purezza | Validato | Soglia raggiunta |
|---|---:|---:|---:|---:|---|---|
| 1q | 0 | 0.99999555 | 0.99999778 | 0.999998 | True | True |
| 1q | 1 | 0.99999665 | 0.99999832 | 0.999997 | True | True |
| 1q | 2 | 0.99999651 | 0.99999826 | 0.999999 | True | True |
| 1q | 3 | 0.99999647 | 0.99999824 | 0.999998 | True | True |
| 1q | 4 | 0.99999684 | 0.99999842 | 0.999999 | True | True |
| 1q | 5 | 0.99999612 | 0.99999806 | 0.999999 | True | True |
| 1q | 6 | 0.99999622 | 0.99999811 | 0.999997 | True | True |
| 1q | 7 | 0.99999551 | 0.99999775 | 0.999997 | True | True |
| 2q_common | 0 | 0.99999759 | 0.99999880 | 0.999998 | True | True |
| 2q_common | 1 | 0.99999792 | 0.99999896 | 0.999998 | True | True |
| 2q_common | 2 | 0.99999666 | 0.99999833 | 0.999997 | True | True |
| 2q_common | 3 | 0.99999708 | 0.99999854 | 0.999997 | True | True |
| 2q_common | 4 | 0.99999792 | 0.99999896 | 0.999998 | True | True |
| 2q_common | 5 | 0.99999798 | 0.99999899 | 0.999998 | True | True |
| 2q_common | 6 | 0.99999572 | 0.99999786 | 0.999996 | True | True |
| 2q_common | 7 | 0.99999684 | 0.99999842 | 0.999998 | True | True |
| 2q_independent | 0 | 0.99999295 | 0.99999648 | 0.999989 | True | True |
| 2q_independent | 1 | 0.99999620 | 0.99999810 | 0.999995 | True | True |
| 2q_independent | 2 | 0.99999740 | 0.99999870 | 0.999998 | True | True |
| 2q_independent | 3 | 0.99999591 | 0.99999796 | 0.999997 | True | True |
| 2q_independent | 4 | 0.99999617 | 0.99999808 | 0.999996 | True | True |
| 2q_independent | 5 | 0.99999422 | 0.99999711 | 0.999991 | True | True |
| 2q_independent | 6 | 0.99999706 | 0.99999853 | 0.999997 | True | True |
| 2q_independent | 7 | 0.99999769 | 0.99999885 | 0.999998 | True | True |
| 2q_normalized_common | 0 | 0.99998242 | 0.99999121 | 0.999978 | True | True |
| 2q_normalized_common | 1 | 0.99998906 | 0.99999453 | 0.999987 | True | True |
| 2q_normalized_common | 2 | 0.99999180 | 0.99999590 | 0.999991 | True | True |
| 2q_normalized_common | 3 | 0.99999218 | 0.99999609 | 0.999990 | True | True |
| 2q_normalized_common | 4 | 0.99998302 | 0.99999151 | 0.999980 | True | True |
| 2q_normalized_common | 5 | 0.99998679 | 0.99999340 | 0.999982 | True | True |
| 2q_normalized_common | 6 | 0.99999217 | 0.99999609 | 0.999992 | True | True |
| 2q_normalized_common | 7 | 0.99998967 | 0.99999484 | 0.999987 | True | True |
| 2q_normalized_independent | 0 | 0.99999265 | 0.99999633 | 0.999991 | True | True |
| 2q_normalized_independent | 1 | 0.99999384 | 0.99999692 | 0.999993 | True | True |
| 2q_normalized_independent | 2 | 0.99999360 | 0.99999680 | 0.999992 | True | True |
| 2q_normalized_independent | 3 | 0.99999264 | 0.99999632 | 0.999991 | True | True |
| 2q_normalized_independent | 4 | 0.99998891 | 0.99999446 | 0.999983 | True | True |
| 2q_normalized_independent | 5 | 0.99999071 | 0.99999535 | 0.999987 | True | True |
| 2q_normalized_independent | 6 | 0.99999309 | 0.99999655 | 0.999990 | True | True |
| 2q_normalized_independent | 7 | 0.99999010 | 0.99999505 | 0.999988 | True | True |

## 1q
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999962340341498, "probability_std_population": 4.5789283901830465e-07, "probability_median": 0.9999963450443385, "probability_min": 0.9999955085413094, "probability_max": 0.9999968402826119, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999959780827036, "probability_q75": 0.9999965463731129, "selection_bias_top_only": false}.
Seed selezionato: 4. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000200.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_0/result.json)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_1/result.json)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_2/result.json)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_3/result.json)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_4/result.json)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_5/result.json)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](1q/seed_6/result.json)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](1q/seed_7/result.json)

## 2q_common
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.999997214322042, "probability_std_population": 7.43916483370577e-07, "probability_median": 0.9999973359117973, "probability_min": 0.999995717267359, "probability_max": 0.9999979830574746, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999967965196032, "probability_q75": 0.9999979182731884, "selection_bias_top_only": false}.
Seed selezionato: 5. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00003513.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_0/result.json)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_1/result.json)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_2/result.json)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_3/result.json)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_4/result.json)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_5/result.json)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_6/result.json)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_common/seed_7/result.json)

## 2q_independent
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999959511188277, "probability_std_population": 1.5179800309034914e-06, "probability_median": 0.9999961852022439, "probability_min": 0.999992954724984, "probability_max": 0.9999976915542179, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.999995488997645, "probability_q75": 0.9999971423090839, "selection_bias_top_only": false}.
Seed selezionato: 7. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00003513.

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
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999883893307807, "probability_std_population": 3.698245728660207e-06, "probability_median": 0.9999893646131472, "probability_min": 0.9999824163966152, "probability_max": 0.9999921768688996, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999858517791712, "probability_q75": 0.9999918948883142, "selection_bias_top_only": false}.
Seed selezionato: 3. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000001.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH.
[Metadati completi](2q_normalized_common/seed_0/result.json)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_1/result.json)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_2/result.json)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_3/result.json)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_4/result.json)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_5/result.json)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_6/result.json)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_common/seed_7/result.json)

## 2q_normalized_independent
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999919418608011, "probability_std_population": 1.686236598079415e-06, "probability_median": 0.9999926471613414, "probability_min": 0.999988913246673, "probability_max": 0.9999938370644541, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999905538368127, "probability_q75": 0.9999932169682691, "selection_bias_top_only": false}.
Seed selezionato: 1. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00000001.

### random — 0
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_0/result.json)

### random — 1
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_1/result.json)

### random — 2
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_2/result.json)

### random — 3
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_3/result.json)

### random — 4
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_4/result.json)

### random — 5
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_5/result.json)

### random — 6
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_6/result.json)

### random — 7
Controlli numerici falliti: nessuno.
CRAB: Maximum number of function evaluations has been exceeded.. GRAPE: STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
[Metadati completi](2q_normalized_independent/seed_7/result.json)
