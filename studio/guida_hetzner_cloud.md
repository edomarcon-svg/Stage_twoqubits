# Guida Completa all'Esecuzione di Simulazioni su Hetzner Cloud

Questa guida riassume tutti i passaggi, i comandi e le best practice per eseguire le simulazioni quantistiche (CRAB, GRAPE, analisi di fedeltà e validazione) del progetto `Stage_twoqubits` (in particolare della versione **`v2`**) su una macchina virtuale remota ad alte prestazioni su **Hetzner Cloud**, permettendo di spegnere il proprio PC durante il calcolo.

---

## 📌 Indice dei Contenuti
1. [Il Trucco Pro: Lo Snapshot per Saltare i Setup Futuri](#-il-trucco-pro-lo-snapshot-per-saltare-i-setup-futuri)
2. [Fase 1: Creazione del Server su Hetzner](#fase-1-creazione-del-server-su-hetzner)
3. [Fase 2: Setup Iniziale del Server (Macchina Nuova)](#fase-2-setup-iniziale-del-server-macchina-nuova)
4. [Fase 3: Esecuzione della Simulazione (v2)](#fase-3-esecuzione-della-simulazione-v2)
   - [Opzione A: Modalità Interattiva con tmux](#opzione-a-modalità-interattiva-con-tmux)
   - [Opzione B: Modalità Automatica (Discord + Auto-distruzione)](#opzione-b-modalità-automatica-discord--auto-distruzione)
5. [Fase 4: Cheat Sheet Comandi Veloci dal PC Locale (PowerShell)](#fase-4-cheat-sheet-comandi-veloci-dal-pc-locale-powershell)
6. [Fase 5: Scaricamento Manuale dei Risultati](#fase-5-scaricamento-manuale-dei-risultati)
7. [Note Importanti sulla Fatturazione Hetzner](#note-importanti-sulla-fatturazione-hetzner)

---

## 💡 Il Trucco Pro: Lo Snapshot per Saltare i Setup Futuri

Su Hetzner Cloud, puoi salvare una fotografia esatta del disco del server (*Snapshot*):
1. Nella console Hetzner, seleziona il server $\rightarrow$ scheda **Snapshots** $\rightarrow$ **Take Snapshot** (costa appena ~0,05 €/mese).
2. **Perché è utilissimo**: Quando vorrai lanciare una nuova simulazione in futuro, cliccando su *"Create Server from Snapshot"*, avrai una macchina nuova con **Python, l'ambiente virtuale, QuTiP, NumPy, SciPy e `threadpoolctl` già tutti installati e configurati in 20 secondi**, saltando interamente la Fase 2!

---

## Fase 1: Creazione del Server su Hetzner

1. Accedi alla [Console Hetzner Cloud](https://console.hetzner.cloud) ed entra nel tuo progetto.
2. Clicca su **Add Server**.
3. **Location**: Falkenstein o Nuremberg (Germania, ottima latenza ed economica).
4. **Image**: Ubuntu 24.04 LTS *(oppure il tuo Snapshot se ne hai salvato uno)*.
5. **Type**: Scegli **Shared vCPU** $\rightarrow$ serie **CPX (AMD)**:
   - **CPX31**: 4 vCPU, 8 GB RAM (~0,014 €/ora)
   - **CPX41**: 8 vCPU, 16 GB RAM (~0,026 €/ora — *consigliato per run pesanti a 8 workers*)
6. **SSH Keys**: Spunta la tua chiave SSH creata dal PC.
7. Clicca su **Create & Buy now**.
8. Prendi nota dell'**indirizzo IPv4** assegnato (es. `2.28.xxx.xxx`).

---

## Fase 2: Setup Iniziale del Server (Macchina Nuova)

> *Nota: Se crei il server da uno Snapshot preesistente, puoi saltare questo passaggio e andare direttamente alla Fase 3.*

Apri **PowerShell** sul tuo PC locale e connettiti al server:
```powershell
ssh root@<IP_SERVER>
```

Una volta dentro il terminale Linux del server, esegui i seguenti comandi:

```bash
# 1. Aggiorna il sistema e installa i pacchetti di base
apt update && apt upgrade -y
apt install -y python3-pip python3-venv git tmux htop zip

# 2. Crea l'ambiente virtuale dedicato
python3 -m venv ~/stage_env
source ~/stage_env/bin/activate
```

### Copiare il codice del progetto sul server:

- **Opzione con Git (Consigliata se il repo è online)**:
  ```bash
  git clone <URL_TUO_REPOSITORY> ~/Stage_twoqubits
  ```
- **Opzione con SCP (da una nuova finestra PowerShell sul tuo PC locale)**:
  ```powershell
  scp -r C:\Users\edoma\Desktop\Stage_twoqubits root@<IP_SERVER>:~/Stage_twoqubits
  ```

### Installare le dipendenze per `v2`:
Sul server, entra nella cartella `v2` e installa i requisiti (incluso `threadpoolctl` necessario per il controllo dei thread BLAS):
```bash
cd ~/Stage_twoqubits/v2
source ~/stage_env/bin/activate
pip install -r requirements.txt
pip install threadpoolctl
```

---

## Fase 3: Esecuzione della Simulazione (v2)

### Opzione A: Modalità Interattiva con `tmux`
Ideale se vuoi seguire l'avanzamento, controllare i seed e verificare il log.

```bash
# 1. Crea una sessione persistente
tmux new -s simulazione

# 2. Entra nella cartella di v2 e attiva l'ambiente
cd ~/Stage_twoqubits/v2
source ~/stage_env/bin/activate

# 3. Lancia la simulazione salvando il log
python -u run_simulation.py --config configurazione.jsonc --workers 8 2>&1 | tee simulation.log
```

- **Per disconnetterti senza interrompere il calcolo**:
  Premi **`Ctrl + B`**, rilascia i tasti, e poi premi **`D`** (*Detach*).
  Vedrai la scritta `[detached]`. Ora puoi chiudere il terminale e spegnere il tuo PC!
- **Per ricollegarti alla schermata in seguito**:
  ```bash
  ssh root@<IP_SERVER>
  tmux attach -t simulazione
  ```

---

### Opzione B: Modalità Automatica (Discord + Auto-distruzione)
Ideale per il pattern *"Fire-and-Forget"*: lanci la simulazione, spegni subito il PC, ricevi l'archivio ZIP su Discord appena finisce e il server si auto-elimina da solo per azzerare la spesa.

1. **Crea lo script di automazione sul server**:
   ```bash
   nano ~/Stage_twoqubits/v2/auto_v2.sh
   ```

2. **Incolla il seguente contenuto** (sostituisci il token Hetzner e il webhook Discord):
   ```bash
   #!/bin/bash
   # ==============================================================================
   # PIPELINE AUTOMATICA v2: CALCOLO -> ZIP -> DISCORD -> AUTO-DISTRUZIONE
   # ==============================================================================
   HCLOUD_TOKEN="<TUO_API_TOKEN_HETZNER>"
   DISCORD_WEBHOOK="<TUO_WEBHOOK_DISCORD>"

   cd ~/Stage_twoqubits/v2
   source ~/stage_env/bin/activate

   echo "=== [1/4] Avvio simulazione v2: $(date) ==="
   python -u run_simulation.py --config configurazione.jsonc --workers 8

   EXIT_CODE=$?
   if [ $EXIT_CODE -ne 0 ]; then
       curl -F "content=❌ **ERRORE:** La simulazione v2 è fallita! Il server non è stato eliminato per permetterti di controllare i log." \
            "$DISCORD_WEBHOOK"
       exit 1
   fi

   echo "=== [2/4] Creazione archivio ZIP della run più recente ==="
   LATEST_RUN=$(ls -td results/* | head -1)
   RUN_NAME=$(basename "$LATEST_RUN")
   ZIP_PATH="/root/${RUN_NAME}.zip"

   zip -r "$ZIP_PATH" "$LATEST_RUN"

   echo "=== [3/4] Invio file su Discord ==="
   curl -F "file=@$ZIP_PATH" \
        -F "content=🚀 **Simulazione v2 completata!** Ecco i risultati: \`$RUN_NAME\`" \
        "$DISCORD_WEBHOOK"

   echo "=== [4/4] Auto-distruzione del server Hetzner ==="
   # Ottiene l'ID del server dai metadati interni di Hetzner
   SERVER_ID=$(curl -s http://169.254.169.254/hetzner/v1/metadata/instance-id)

   # Chiama le API Hetzner per cancellare definitivamente il server
   curl -s -X DELETE \
        -H "Authorization: Bearer $HCLOUD_TOKEN" \
        "https://api.hetzner.cloud/v1/servers/$SERVER_ID"
   ```

3. **Rendi lo script eseguibile**:
   ```bash
   chmod +x ~/Stage_twoqubits/v2/auto_v2.sh
   ```

4. **Avvia il processo in background ed esci**:
   ```bash
   nohup ~/Stage_twoqubits/v2/auto_v2.sh > ~/v2_execution.log 2>&1 &
   exit
   ```
   *Puoi spegnere il computer: riceverai i risultati direttamente sul tuo canale Discord.*

---

## Fase 4: Cheat Sheet Comandi Veloci dal PC Locale (PowerShell)

Tutti questi comandi possono essere lanciati direttamente da **PowerShell di Windows**:

| Azione desiderata | Comando PowerShell |
| :--- | :--- |
| **Vedere il log live di `v2`** | `ssh root@<IP_SERVER> "tail -n 25 -f ~/Stage_twoqubits/v2/simulation.log"` |
| **Leggere tutto il log di auto-run** | `ssh root@<IP_SERVER> "cat ~/v2_execution.log"` |
| **Controllare l'uso della CPU live** | `ssh root@<IP_SERVER> "htop"` |
| **Ricollegarsi alla schermata tmux** | `ssh root@<IP_SERVER>` e poi `tmux attach -t simulazione` |
| **Staccarsi da tmux senza fermare** | Premi `Ctrl + B`, poi `D` |

---

## Fase 5: Scaricamento Manuale dei Risultati

Se non usi la cancellazione automatica e vuoi scaricare a mano i file generati dalla simulazione (grafici `dynamics.png`, `wigner.png`, report interattivo `report.html`, matrici `arrays.npz`):

Dalla cartella principale del progetto sul tuo **PC Windows** (in PowerShell):
```powershell
scp -r root@<IP_SERVER>:~/Stage_twoqubits/v2/results/* C:\Users\edoma\Desktop\Stage_twoqubits\v2\results\
```

---

## Note Importanti sulla Fatturazione Hetzner

> [!CAUTION]
> **Attenzione**: Su Hetzner Cloud il comando `Power Off` (spegnimento) **NON** ferma i costi, perché la CPU, l'indirizzo IP pubblico e lo spazio disco rimangono riservati a te.
> 
> Per fermare al 100% la fatturazione devi:
> 1. Salvare i risultati sul PC o su Discord/Drive.
> 2. Selezionare **Delete Server** nella console Hetzner (oppure lasciare che lo script `auto_v2.sh` chiami l'API di cancellazione con il token in modalità *Read & Write*).
