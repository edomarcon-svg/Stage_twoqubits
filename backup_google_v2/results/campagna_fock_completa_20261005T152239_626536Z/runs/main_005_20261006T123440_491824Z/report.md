# Risultati v2

Durata fisica T = 104.7197551. T = 20 × tau_s; tau_s = pi/(2*g_ref) = 5.235987756, g_ref = 0.3.

Ogni riga usa la propagazione continua del controllo con il filtro configurato.
P_target è la probabilità target; F_root = sqrt(P_target). Il reset dei qubit, se richiesto, entra in P_target.
Una soluzione non validata non è evidenza di vantaggio fisico. La convergenza dell'ottimizzatore è distinta dalla validazione numerica.
Le statistiche e il seed selezionato riguardano solo partenze casuali; i warm start sono separati.
La banda 99% è una diagnostica del segnale finito, non un limite spettrale imposto. Le fluenze non sono calore dissipato.

| Caso | Seed | P target | F radice | Purezza | Validato | Soglia raggiunta |
|---|---:|---:|---:|---:|---|---|
| 1q | 0 | 0.99999700 | 0.99999850 | 0.999999 | True | True |
| 1q | 1 | 0.99999816 | 0.99999908 | 1.000000 | True | True |
| 1q | 2 | 0.99999802 | 0.99999901 | 1.000000 | True | True |
| 1q | 3 | 0.99999847 | 0.99999923 | 1.000000 | True | True |
| 1q | 4 | 0.99999803 | 0.99999901 | 1.000000 | True | True |
| 1q | 5 | 0.99999779 | 0.99999890 | 0.999999 | True | True |
| 1q | 6 | 0.99999758 | 0.99999879 | 0.999999 | True | True |
| 1q | 7 | 0.99999814 | 0.99999907 | 0.999999 | True | True |
| 2q_common | 0 | 0.99999863 | 0.99999931 | 0.999999 | True | True |
| 2q_common | 1 | 0.99999876 | 0.99999938 | 0.999999 | True | True |
| 2q_common | 2 | 0.99999728 | 0.99999864 | 0.999998 | True | True |
| 2q_common | 3 | 0.99999951 | 0.99999975 | 1.000000 | True | True |
| 2q_common | 4 | 0.99999806 | 0.99999903 | 0.999999 | True | True |
| 2q_common | 5 | 0.99999953 | 0.99999977 | 1.000000 | True | True |
| 2q_common | 6 | 0.99999915 | 0.99999958 | 1.000000 | True | True |
| 2q_common | 7 | 0.99999940 | 0.99999970 | 1.000000 | True | True |
| 2q_independent | 0 | 0.99999858 | 0.99999929 | 0.999999 | True | True |
| 2q_independent | 1 | 0.99999890 | 0.99999945 | 0.999999 | True | True |
| 2q_independent | 2 | 0.99999904 | 0.99999952 | 1.000000 | True | True |
| 2q_independent | 3 | 0.99999859 | 0.99999929 | 0.999999 | True | True |
| 2q_independent | 4 | 0.99999870 | 0.99999935 | 0.999999 | True | True |
| 2q_independent | 5 | 0.99999925 | 0.99999962 | 1.000000 | True | True |
| 2q_independent | 6 | 0.99999856 | 0.99999928 | 0.999999 | True | True |
| 2q_independent | 7 | 0.99999883 | 0.99999941 | 1.000000 | True | True |
| 2q_normalized_common | 0 | 0.99999731 | 0.99999866 | 0.999998 | True | True |
| 2q_normalized_common | 1 | 0.99999789 | 0.99999895 | 0.999999 | True | True |
| 2q_normalized_common | 2 | 0.99999710 | 0.99999855 | 0.999998 | True | True |
| 2q_normalized_common | 3 | 0.99999699 | 0.99999850 | 0.999997 | True | True |
| 2q_normalized_common | 4 | 0.99999671 | 0.99999835 | 0.999997 | True | True |
| 2q_normalized_common | 5 | 0.99999615 | 0.99999807 | 0.999997 | True | True |
| 2q_normalized_common | 6 | 0.99999603 | 0.99999802 | 0.999997 | True | True |
| 2q_normalized_common | 7 | 0.99999476 | 0.99999738 | 0.999994 | True | True |
| 2q_normalized_independent | 0 | 0.99999699 | 0.99999849 | 0.999998 | True | True |
| 2q_normalized_independent | 1 | 0.99999682 | 0.99999841 | 0.999998 | True | True |
| 2q_normalized_independent | 2 | 0.99999712 | 0.99999856 | 0.999998 | True | True |
| 2q_normalized_independent | 3 | 0.99999705 | 0.99999852 | 0.999998 | True | True |
| 2q_normalized_independent | 4 | 0.99999772 | 0.99999886 | 0.999999 | True | True |
| 2q_normalized_independent | 5 | 0.99999742 | 0.99999871 | 0.999999 | True | True |
| 2q_normalized_independent | 6 | 0.99999711 | 0.99999856 | 0.999998 | True | True |
| 2q_normalized_independent | 7 | 0.99999736 | 0.99999868 | 0.999998 | True | True |

## 1q
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.999997898343724, "probability_std_population": 4.193684805234531e-07, "probability_median": 0.9999980248481051, "probability_min": 0.9999969991343727, "probability_max": 0.9999984658282279, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999977384534087, "probability_q75": 0.9999981482394129, "selection_bias_top_only": false}.
Seed selezionato: 3. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00047005.

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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999987910381078, "probability_std_population": 7.415298908233273e-07, "probability_median": 0.9999989596602782, "probability_min": 0.9999972842758155, "probability_max": 0.999999531835341, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999984841397052, "probability_q75": 0.9999994278715598, "selection_bias_top_only": false}.
Seed selezionato: 5. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.01035578.

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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.999998804624609, "probability_std_population": 2.313763541388586e-07, "probability_median": 0.9999987634837781, "probability_min": 0.999998564865898, "probability_max": 0.999999248236962, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999985835738334, "probability_q75": 0.9999989315424683, "selection_bias_top_only": false}.
Seed selezionato: 5. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.01035578.

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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999966179393222, "probability_std_population": 9.00038202612077e-07, "probability_median": 0.9999968498613137, "probability_min": 0.9999947646193844, "probability_max": 0.9999978919844967, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999961178164223, "probability_q75": 0.9999971503094658, "selection_bias_top_only": false}.
Seed selezionato: 1. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00702136.

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
Distribuzione sulle 8 pipeline raffinate: {"count": 8, "probability_mean": 0.9999971985007039, "probability_std_population": 2.651297707510657e-07, "probability_median": 0.99999711943216, "probability_min": 0.9999968203924847, "probability_max": 0.9999977152339085, "numerically_valid_count": 8, "validated_goal_count": 8, "validated_goal_fraction": 1.0, "probability_q25": 0.9999970333691541, "probability_q75": 0.9999973739263956, "selection_bias_top_only": false}.
Seed selezionato: 4. Selezione per costo continuo, dando precedenza alle soluzioni validate.
Probabilità target senza modulazione: 0.00702136.

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
