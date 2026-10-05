#!/usr/bin/env python3
"""Send a small result summary via TLS SMTP; large archives belong in external storage."""
import argparse
from email.message import EmailMessage
from email.policy import SMTP
import os
from pathlib import Path
import smtplib
import ssl
import sys

MAX_SAFE_ATTACHMENT_MB = 15.0
MAX_MESSAGE_BYTES = 23_000_000


def build_message(sender, recipient, subject, body, attachment=None):
    if not sender or not recipient: raise ValueError("SMTP sender and recipient are required")
    msg = EmailMessage(policy=SMTP)
    msg["From"],msg["To"],msg["Subject"] = sender,recipient,subject
    msg.set_content(body)
    if attachment:
        path = Path(attachment)
        if not path.is_file(): raise ValueError("Attachment does not exist")
        if path.stat().st_size > MAX_SAFE_ATTACHMENT_MB*1024*1024:
            raise ValueError("Attachment exceeds 15 MiB; send a summary and an external download link")
        msg.add_attachment(path.read_bytes(),maintype="application",subtype="zip" if path.suffix == ".zip" else "octet-stream",filename=path.name)
    if len(msg.as_bytes()) > MAX_MESSAGE_BYTES:
        raise ValueError("Encoded SMTP message exceeds conservative size limit")
    return msg


def deliver_message(msg, host, port, sender, password):
    if not password: raise ValueError("Set SMTP_PASSWORD")
    encoded = len(msg.as_bytes())
    with smtplib.SMTP(host,port,timeout=60) as server:
        server.ehlo();server.starttls(context=ssl.create_default_context());server.ehlo()
        limit = server.esmtp_features.get("size","").split()
        if limit and limit[0].isdigit() and encoded > int(limit[0]):
            raise ValueError("Message exceeds this SMTP server's advertised SIZE")
        server.login(sender,password)
        refused = server.send_message(msg)
        if refused: raise RuntimeError("SMTP server refused a recipient")


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--to",required=True)
    p.add_argument("--from-email",default=os.environ.get("SMTP_USER"))
    p.add_argument("--password",default=os.environ.get("SMTP_PASSWORD"),help="Prefer SMTP_PASSWORD in the environment")
    p.add_argument("--host",default=os.environ.get("SMTP_HOST","smtp.gmail.com"))
    p.add_argument("--port",type=int,default=int(os.environ.get("SMTP_PORT","587")))
    p.add_argument("--subject",default="Risultati simulazione")
    text = p.add_mutually_exclusive_group()
    text.add_argument("--body")
    text.add_argument("--body-file",type=Path)
    p.add_argument("--file",type=Path,help="Optional small summary attachment")
    return p.parse_args()


def send_email():
    args = parse_args()
    try:
        body = args.body_file.read_text() if args.body_file else args.body or "Riepilogo della simulazione in allegato."
        msg = build_message(args.from_email,args.to,args.subject,body,args.file)
        deliver_message(msg,args.host,args.port,args.from_email,args.password)
    except (ValueError,OSError,smtplib.SMTPException,RuntimeError) as exc:
        print(f"Invio fallito ({type(exc).__name__}); conservare i dati locali.",file=sys.stderr)
        return 1
    print("Email accettata dal server SMTP.")
    return 0


if __name__ == "__main__": sys.exit(send_email())
