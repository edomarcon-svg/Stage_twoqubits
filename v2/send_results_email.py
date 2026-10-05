#!/usr/bin/env python3
"""
Script per l'invio via email dei risultati delle simulazioni quantistiche (v2).
Usa esclusivamente la libreria standard di Python (smtplib, email) senza dipendenze esterne.

Supporta:
- Server SMTP con autenticazione TLS (es. Gmail con 'Password per le app')
- Controllo preventivo della dimensione del file allegato (max ~20-22 MB per non eccedere il limite SMTP)
- Parametri da riga di comando o variabili d'ambiente per massima sicurezza
"""

import os
import sys
import argparse
import smtplib
import ssl
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


MAX_SAFE_ATTACHMENT_MB = 22.0  # Limite di sicurezza (Gmail accetta fino a 25MB incluso Base64)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Invia i risultati della simulazione via email con allegato ZIP."
    )
    parser.add_argument(
        "--to",
        required=True,
        help="Indirizzo email del destinatario."
    )
    parser.add_argument(
        "--from-email",
        default=os.environ.get("SMTP_USER"),
        help="Indirizzo email del mittente (default: variabile d'ambiente SMTP_USER)."
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("SMTP_PASSWORD"),
        help="Password per le app dell'account SMTP (default: variabile d'ambiente SMTP_PASSWORD)."
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        help="Host del server SMTP (default: smtp.gmail.com)."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("SMTP_PORT", 587)),
        help="Porta SMTP TLS (default: 587)."
    )
    parser.add_argument(
        "--subject",
        default="Risultati Simulazione Quantistica - Hetzner Cloud",
        help="Oggetto dell'email."
    )
    parser.add_argument(
        "--body",
        default=None,
        help="Testo del corpo dell'email."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Percorso dell'archivio (es. .zip) da allegare."
    )
    return parser.parse_args()


def send_email():
    args = parse_args()

    sender_email = args.from_email
    recipient_email = args.to
    password = args.password
    file_path = Path(args.file)

    if not sender_email:
        print("[ERRORE] Indirizzo mittente mancante. Specifica --from-email o imposta SMTP_USER.", file=sys.stderr)
        sys.exit(1)

    if not password:
        print("[ERRORE] Password SMTP mancante. Specifica --password o imposta SMTP_PASSWORD.", file=sys.stderr)
        sys.exit(1)

    if not file_path.is_file():
        print(f"[ERRORE] Il file allegato non esiste: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Controllo dimensione file
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    print(f"[*] Dimensione file da allegare: {file_size_mb:.2f} MB")

    if file_size_mb > MAX_SAFE_ATTACHMENT_MB:
        print(
            f"[ERRORE CRITICO] Il file ({file_size_mb:.2f} MB) supera il limite massimo per gli allegati email "
            f"({MAX_SAFE_ATTACHMENT_MB:.0f} MB). I server di posta rifiuterebbero il messaggio.",
            file=sys.stderr
        )
        print("Suggerimento: escludi cartelle pesanti (.venv, .git) o vecchi risultati prima di creare lo zip.", file=sys.stderr)
        sys.exit(2)

    # Costruzione messaggio email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = args.subject

    body_text = args.body or (
        f"Ciao,\n\n"
        f"La simulazione su Hetzner Cloud e' terminata con successo.\n"
        f"In allegato trovi l'archivio compresso con i risultati e il codice: {file_path.name} ({file_size_mb:.2f} MB).\n\n"
        f"-- Invio automatico Stage_twoqubits"
    )
    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    # Lettura e codifica dell'allegato
    print(f"[*] Lettura e preparazione dell'allegato '{file_path.name}'...")
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={file_path.name}",
    )
    msg.attach(part)

    # Connessione SMTP e invio
    print(f"[*] Connessione al server SMTP {args.host}:{args.port}...")
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(args.host, args.port, timeout=60) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            print("[*] Autenticazione in corso...")
            server.login(sender_email, password)
            print(f"[*] Invio dell'email a {recipient_email} in corso...")
            server.send_message(msg)
        print(f"[OK] Email inviata con successo a {recipient_email}!")
        sys.exit(0)
    except Exception as e:
        print(f"[ERRORE] Invio fallito: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    send_email()
