#!/usr/bin/env bash
# Simulation -> verified external archive -> summary email -> optional cleanup.
# Configure archive.env (ignored by Git), see ARCHIVIAZIONE.md.
set -euo pipefail
umask 077
V2_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${QOC_ARCHIVE_ENV_FILE:-$V2_DIR/archive.env}"
if [[ -f "$ENV_FILE" ]]; then
    set -a
    # Local, user-maintained shell assignments. Never add this file to the archive.
    source "$ENV_FILE"
    set +a
fi
if [[ -n "${QOC_PYTHON:-}" ]]; then
    PYTHON_BIN="$QOC_PYTHON"
elif [[ -x "/root/stage_env/bin/python" ]]; then
    PYTHON_BIN="/root/stage_env/bin/python"
elif [[ -x "$HOME/stage_env/bin/python" ]]; then
    PYTHON_BIN="$HOME/stage_env/bin/python"
elif [[ -x "$V2_DIR/.venv/bin/python" ]]; then
    PYTHON_BIN="$V2_DIR/.venv/bin/python"
elif [[ -x "$V2_DIR/../.venv/bin/python" ]]; then
    PYTHON_BIN="$V2_DIR/../.venv/bin/python"
else
    PYTHON_BIN="python3"
fi
MODE="${QOC_RUN_MODE:-campaign}"
CONFIG="${QOC_CONFIG:-$V2_DIR/configurazione_campagna.jsonc}"
DELETE_SERVER_AFTER_DELIVERY="${DELETE_SERVER_AFTER_DELIVERY:-false}"
case "$DELETE_SERVER_AFTER_DELIVERY" in true|false) ;; *) echo 'DELETE_SERVER_AFTER_DELIVERY must be true or false' >&2; exit 1;; esac
if [[ "$DELETE_SERVER_AFTER_DELIVERY" == true ]]; then
    : "${HCLOUD_TOKEN:?Set HCLOUD_TOKEN for optional server deletion}"
fi
mkdir -p "$V2_DIR/exports"
RECEIPT="$(mktemp "$V2_DIR/exports/delivery.XXXXXXXX.json")"
args=(--mode "$MODE" --receipt "$RECEIPT")
if [[ -n "${QOC_RESUME:-}" ]]; then
    args+=(--resume "$QOC_RESUME")
else
    args+=(--config "$CONFIG")
fi
if [[ "${QOC_NO_PLOTS:-false}" == true ]]; then args+=(--no-plots); fi
if ! "$PYTHON_BIN" -u "$V2_DIR/run_and_archive.py" "${args[@]}"; then
    echo 'Simulazione/archiviazione/email non completata. Server e risultati conservati.' >&2
    echo 'Per una run già completa, riprovare publish_results.py --run <cartella>.' >&2
    exit 1
fi
"$PYTHON_BIN" "$V2_DIR/publish_results.py" --check-cleanup "$RECEIPT"
if [[ "$DELETE_SERVER_AFTER_DELIVERY" != true ]]; then
    echo "Backup verificato ed email accettata. Server conservato; ricevuta: $RECEIPT"
    exit 0
fi
# Only reached after this invocation's verified full backup AND accepted email.
SERVER_ID="$(curl --fail --silent --show-error --max-time 10 http://169.254.169.254/hetzner/v1/metadata/instance-id)"
if [[ ! "$SERVER_ID" =~ ^[0-9]+$ ]]; then
    echo 'SERVER_ID non valido: cancellazione annullata.' >&2
    exit 1
fi
curl --fail --silent --show-error --max-time 60 --request DELETE \
    --header "Authorization: Bearer $HCLOUD_TOKEN" \
    "https://api.hetzner.cloud/v1/servers/$SERVER_ID" > /dev/null
printf '%s\n' 'Richiesta di cancellazione del server accettata dopo backup verificato ed email.'
