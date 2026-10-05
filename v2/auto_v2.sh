#!/bin/bash
# ==============================================================================
# PIPELINE AUTOMATICA v2 CON INVIO RISULTATI VIA EMAIL + FAILSAFE
# ==============================================================================
# ISTRUZIONI:
# 1. Configura le variabili qui sotto (o passale tramite variabili d'ambiente).
# 2. Per Gmail, genera una "Password per le app" da: https://myaccount.google.com/apppasswords
# ==============================================================================

# --- CONFIGURAZIONE CREDENZIALI ---
HCLOUD_TOKEN="${HCLOUD_TOKEN:-oMf48CoCOQ6QYjvS1tGeEboK1ZCUm4Gyd5w6zbneOSwSlPVYcQG9YrksiErPius6}"

# Configurazione Email
EMAIL_TO="${EMAIL_TO:-edo.marcon@gmail.com}"
SMTP_USER="${SMTP_USER:-edo.marcon@gmail.com}"
SMTP_PASSWORD="${SMTP_PASSWORD:-dofc uauy saic saqa}"
SMTP_HOST="${SMTP_HOST:-smtp.gmail.com}"
SMTP_PORT="${SMTP_PORT:-587}"

# Opzionale: Webhook Discord (se vuoi notifica o doppio canale)
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"

# Cartelle
REPO_DIR="/root/Stage_twoqubits"
V2_DIR="$REPO_DIR/v2"

cd "$V2_DIR" || exit 1
source /root/stage_env/bin/activate

echo "================================================================="
echo "=== [1/4] Avvio simulazione v2: $(date) ==="
echo "================================================================="
python -u run_simulation.py --config configurazione.jsonc --workers 8

SIM_EXIT=$?
if [ $SIM_EXIT -ne 0 ]; then
    echo "❌ ERRORE: La simulazione e' fallita con codice $SIM_EXIT."
    if [ -n "$DISCORD_WEBHOOK" ]; then
        curl -s -F "content=❌ **ERRORE CRITICO:** La simulazione v2 su Hetzner e' fallita. Il server rimane intatto per il debug." "$DISCORD_WEBHOOK"
    fi
    echo "Il server NON verra' cancellato per permetterti di analizzare i log."
    exit 1
fi

echo "================================================================="
echo "=== [2/4] Creazione pacchetto ZIP (Run + Sorgenti puliti) ==="
echo "================================================================="
# Trova la cartella della run appena completata
LATEST_RUN=$(ls -td "$V2_DIR"/results/* | head -1)
if [ -z "$LATEST_RUN" ] || [ ! -d "$LATEST_RUN" ]; then
    echo "❌ ERRORE: Cartella dei risultati non trovata in $V2_DIR/results/"
    exit 1
fi

RUN_NAME=$(basename "$LATEST_RUN")
ZIP_NAME="${RUN_NAME}_bundle.zip"
ZIP_PATH="/root/${ZIP_NAME}"

# Rimuovi eventuale zip precedente con stesso nome
rm -f "$ZIP_PATH"

# Zippa la run dei risultati E l'intero codice sorgente v2 (escludendo .venv, git e cache per non superare il limite mail)
echo "Compressione in corso escludendo ambienti virtuali e file temporanei..."
cd "$REPO_DIR" || exit 1
zip -r "$ZIP_PATH" \
    "v2/results/$RUN_NAME" \
    "v2/qoc" \
    "v2/configs" \
    "v2/run_simulation.py" \
    "v2/analyze_run.py" \
    "v2/configurazione.jsonc" \
    -x "*/.venv/*" "*__pycache__/*" "*.pyc"

ZIP_SIZE_MB=$(du -m "$ZIP_PATH" | cut -f1)
echo "Archivio creato: $ZIP_PATH (Dimensione: ~${ZIP_SIZE_MB} MB)"

echo "================================================================="
echo "=== [3/4] Invio risultati via Email ==="
echo "================================================================="
cd "$V2_DIR" || exit 1

SUBJECT="🚀 Simulazione Completata: ${RUN_NAME}"
BODY="Ciao,

La simulazione v2 su Hetzner Cloud e' terminata con successo!

- Run: ${RUN_NAME}
- Data di fine: $(date)
- Archivio allegato: ${ZIP_NAME} (~${ZIP_SIZE_MB} MB)

L'archivio contiene tutti i grafici (dynamics, wigner), i report interattivi html, i dati numerici e il codice sorgente associato.

Saluti,
Stage Twoqubits Automation"

python send_results_email.py \
    --to "$EMAIL_TO" \
    --from-email "$SMTP_USER" \
    --password "$SMTP_PASSWORD" \
    --host "$SMTP_HOST" \
    --port "$SMTP_PORT" \
    --subject "$SUBJECT" \
    --body "$BODY" \
    --file "$ZIP_PATH"

EMAIL_EXIT=$?

# Invio opzionale notifica su Discord se configurato
if [ -n "$DISCORD_WEBHOOK" ]; then
    if [ "$ZIP_SIZE_MB" -lt 10 ]; then
        curl -s -F "file=@$ZIP_PATH" \
             -F "content=🚀 **Simulazione completata con successo:** \`$RUN_NAME\`" \
             "$DISCORD_WEBHOOK"
    else
        curl -s -F "content=🚀 **Simulazione completata!** Archivio spedito via email (file > 10MB per Discord)." \
             "$DISCORD_WEBHOOK"
    fi
fi

echo "================================================================="
echo "=== [4/4] Verifica invio e gestione ciclo di vita del server ==="
echo "================================================================="
if [ $EMAIL_EXIT -eq 0 ]; then
    echo "✅ Email inviata e confermata con successo!"
    echo "Procedo con l'auto-distruzione del server Hetzner per azzerare i costi..."
    
    SERVER_ID=$(curl -s http://169.254.169.254/hetzner/v1/metadata/instance-id)
    if [ -n "$SERVER_ID" ] && [ "$HCLOUD_TOKEN" != "<TUO_API_TOKEN_HETZNER>" ]; then
        curl -s -X DELETE \
             -H "Authorization: Bearer $HCLOUD_TOKEN" \
             "https://api.hetzner.cloud/v1/servers/$SERVER_ID"
        echo "Richiesta di cancellazione server inviata."
    else
        echo "⚠️ Impossibile ricavare SERVER_ID o Token mancante. Eseguo arresto di sicurezza (poweroff)..."
        poweroff
    fi
else
    echo "❌ ATTENZIONE CRITICA: L'invio dell'email e' FALLITO (codice $EMAIL_EXIT)!"
    echo "Per salvaguardare i tuoi dati, IL SERVER NON VIENE CANCELLATO."
    echo "Eseguo spegnimento della macchina (poweroff) per fermare l'uso della CPU."
    echo "Potrai riaccendere la macchina dalla console Hetzner e scaricare i file con SCP."
    poweroff
fi
