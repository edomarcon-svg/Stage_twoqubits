# Campagna sui vincoli dell'attuatore (filtro, ampiezza, slew rate) e stato iniziale vestito (`ground`)

La configurazione `configurazione_campagna.jsonc` prepara **44 esperimenti principali** (**1056 pipeline**: 3 sistemi fisici `1q`, `2q_common`, `2q_independent` × 8 seed per esperimento), omettendo i casi normalizzati (`2q_normalized_*`, il cui ruolo è già stato caratterizzato nelle due campagne precedenti) e mantenendo il collaudo disattivato (`pilot.enabled: false`, con profilo `root` e `crab_initial_std = 0.1`).

## Avvio

Dalla radice del repository, con l'ambiente locale già disponibile:

```bash
.venv/bin/python v2/run_campaign.py --config v2/configurazione_campagna.jsonc --validate-config
.venv/bin/python -u v2/run_campaign.py --config v2/configurazione_campagna.jsonc
```

Su un server dove l'ambiente è già attivato, dalla cartella `v2`:

```bash
python -u run_campaign.py --config configurazione_campagna.jsonc
```

Per continuare dopo un'interruzione:

```bash
python -u run_campaign.py --resume results/campagna_vincoli_filtro_ampiezza_slew_ground_TIMESTAMP
```

## Disegno dei 4 studi della campagna

| Studio | Blocco | ID run | Target | Stato iniz. | $\text{dim}$ ($\to \text{val}$) | Durate ($T/\tau_s$) | Filtro $\omega_{\text{cut}}$ | Bounds / Slew | Esperimenti (Pipeline) |
| --- | --- | --- | --- | :---: | :---: | :---: | :---: | --- | :---: |
| **1. Banda filtro** | `fock6_t10_cutoff_scan` | `main_000`–`004` | Fock 6 | `bare` | $60 \to 80$ | 10 | `1.0`, `1.5`, `2.0`, `4.5`, `6.0` | `[0.5, 3.0]` | 5 (120) |
| **1. Banda filtro** | `fock10_t10_cutoff_scan` | `main_005`–`008` | Fock 10 | `bare` | $60 \to 80$ | 10 | `4.0`, `5.0`, `6.5`, `8.0` | `[0.5, 3.0]` | 4 (96) |
| **1. Banda filtro** | `fock10_t15_cutoff_scan` | `main_009`–`012` | Fock 10 | `bare` | $60 \to 80$ | 15 | `1.5`, `2.0`, `4.5`, `null` | `[0.5, 3.0]` | 4 (96) |
| **1. Banda filtro** | `cat2_t10_cutoff_scan` | `main_013`–`017` | Cat $\alpha=2.0$ | `bare` | $48 \to 68$ | 10 | `1.0`, `1.5`, `2.0`, `4.5`, `6.0` | `[0.5, 3.0]` | 5 (120) |
| **2. Ampiezza** | `fock6_t10_bounds_scan` | `main_018`–`020` | Fock 6 | `bare` | $60 \to 80$ | 10 | `3.0` | `[1.0, 3.0]`, `[1.25, 2.75]`, `[1.5, 2.5]` | 3 (72) |
| **2. Ampiezza** | `fock10_t15_bounds_scan` | `main_021`–`023` | Fock 10 | `bare` | $60 \to 80$ | 15 | `3.0` | `[1.0, 3.0]`, `[1.25, 2.75]`, `[1.5, 2.5]` | 3 (72) |
| **2. Ampiezza** | `cat2_t10_bounds_scan` | `main_024`–`026` | Cat $\alpha=2.0$ | `bare` | $48 \to 68$ | 10 | `3.0` | `[1.0, 3.0]`, `[1.25, 2.75]`, `[1.5, 2.5]` | 3 (72) |
| **3. Slew rate** | `fock6_t10_slew_scan` | `main_027`–`031` | Fock 6 | `bare` | $60 \to 80$ | 10 | `3.0` | `slew_weight`: `1e-4`, `5e-4`, `2e-3`; `max_slew`: `2.5`, `1.5` | 5 (120) |
| **3. Slew rate** | `fock10_t15_slew_scan` | `main_032`–`036` | Fock 10 | `bare` | $60 \to 80$ | 15 | `3.0` | `slew_weight`: `1e-4`, `5e-4`, `2e-3`; `max_slew`: `2.5`, `1.5` | 5 (120) |
| **4. Stato vestito** | `ground_init_fock6` | `main_037`–`038` | Fock 6 | `ground` | $60 \to 80$ | 10, 20 | `3.0` | `[0.5, 3.0]` | 2 (48) |
| **4. Stato vestito** | `ground_init_fock10` | `main_039`–`041` | Fock 10 | `ground` | $60 \to 80$ | 10, 15, 20 | `3.0` | `[0.5, 3.0]` | 3 (72) |
| **4. Stato vestito** | `ground_init_cat2` | `main_042`–`043` | Cat $\alpha=2.0$ | `ground` | $48 \to 68$ | 10, 15 | `3.0` | `[0.5, 3.0]` | 2 (48) |

## Analisi a posteriori su stato iniziale (`--initial-state-check`) e filtro (`--cutoffs`)

Oltre ai blocchi di ri-ottimizzazione nativa con `"initial_state": "ground"`, lo script `analyze_run.py` permette di valutare a posteriori qualsiasi run già completata (sia sul singolo seed selezionato sia su tutti gli 8 seed con `--all-seeds`):

```bash
# Confronto stato iniziale bare vs ground vestito (sovrapposizione, fotoni virtuali e cross-evaluation dell'impulso)
.venv/bin/python v2/analyze_run.py <cartella_run> --all-seeds --initial-state-check

# Scansione del filtro a posteriori senza ri-ottimizzare
.venv/bin/python v2/analyze_run.py <cartella_run> --all-seeds --cutoffs 0.5 1.0 1.5 2.0 3.0 4.0 5.0 6.0 8.0 10.0
```
