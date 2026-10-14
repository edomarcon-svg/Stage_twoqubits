#!/usr/bin/env python3
"""Archive one explicit completed run/campaign to private S3, verify it and email a link."""
import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sys
from qoc.archive import (S3Settings, s3_client, check_storage, completed_run, build_bundle,
                         build_summary, upload_verified, download_link, atomic_json, utc_now,
                         verify_remote)
from send_results_email import build_message, deliver_message


def mail_settings():
    names = ["SMTP_USER","SMTP_PASSWORD","EMAIL_TO"]
    missing = [name for name in names if not os.environ.get(name)]
    if missing: raise ValueError("Missing environment variables: "+", ".join(missing))
    return {"sender":os.environ["SMTP_USER"],"password":os.environ["SMTP_PASSWORD"],
        "recipient":os.environ["EMAIL_TO"],"host":os.environ.get("SMTP_HOST","smtp.gmail.com"),
        "port":int(os.environ.get("SMTP_PORT","587"))}


def publish(run, output=None, settings=None, client=None, send=True, receipt_path=None):
    run = completed_run(run)
    settings = settings or S3Settings.from_env()
    client = client or s3_client(settings)
    mail = mail_settings() if send else None
    check_storage(client,settings)
    output = Path(output).resolve() if output else run.parent/"exports"/run.name
    if output == run or run in output.parents: raise ValueError("Export destination must be outside the run")
    receipt_path = Path(receipt_path).resolve() if receipt_path else output/"delivery.json"
    if receipt_path == run or run in receipt_path.parents: raise ValueError("Receipt must be outside the run")
    # Reset eligibility before any retry so stale SMTP success cannot authorize cleanup.
    atomic_json(receipt_path,{"run":str(run),"verified":False,"email_accepted":False,"state":"preparing"})
    try:
        bundle = build_bundle(run,output)
        summary = build_summary(run,output)
        print(f"Archivio locale: {bundle['bytes']/1024**2:.2f} MiB; riepilogo: {summary.stat().st_size/1024**2:.2f} MiB",flush=True)
        receipt = upload_verified(bundle,client,settings)
        receipt.update(state="verified",email_accepted=False,summary=str(summary))
        atomic_json(receipt_path,receipt)
        if send:
            link = download_link(client,settings,receipt)
            expires = datetime.now(timezone.utc)+timedelta(seconds=settings.link_seconds)
            body = (f"Simulazione completata: {run.name}\n\n"
                "In allegato il riepilogo leggero. La fine del calcolo non implica successo fisico di ogni tentativo: consultare le validazioni.\n\n"
                f"Archivio completo (dati, grafici e snapshot del codice):\n{link}\n\n"
                f"Scadenza massima del link: {expires.isoformat()} (UTC; credenziali temporanee possono farlo scadere prima).\n"
                f"Posizione persistente: s3://{receipt['bucket']}/{receipt['key']}\n"
                f"Dimensione: {receipt['bytes']} byte\nSHA-256: {receipt['sha256']}\n"
                "Verifica: archivio riletto integralmente dallo storage e checksum confrontato.\n"
                "La scadenza del link non elimina l'archivio. Un nuovo link può essere generato dallo storage.\n")
            msg = build_message(mail["sender"],mail["recipient"],f"Risultati: {run.name}",body,summary)
            deliver_message(msg,mail["host"],mail["port"],mail["sender"],mail["password"])
            receipt.update(email_accepted=True,email_accepted_at=utc_now(),state="delivered",link_expires_no_later_than=expires.isoformat())
            atomic_json(receipt_path,receipt)
        print(f"Archivio remoto verificato. Ricevuta: {receipt_path}",flush=True)
        return receipt
    except BaseException as exc:
        status = json.loads(receipt_path.read_text())
        status.update(state="failed",email_accepted=False,error_type=type(exc).__name__)
        atomic_json(receipt_path,status)
        raise


def cleanup_ready(receipt_path):
    receipt = json.loads(Path(receipt_path).read_text())
    required = (receipt.get("state") == "delivered" and receipt.get("verified") is True
                and receipt.get("verification") == "full_remote_read_sha256" and receipt.get("email_accepted") is True)
    if not required: raise ValueError("Cleanup refused: external verification and email acceptance are both required")
    return receipt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run",type=Path,help="Exact run or campaign directory; never guesses the latest result")
    p.add_argument("--output",type=Path)
    p.add_argument("--receipt",type=Path)
    p.add_argument("--prepare-only",action="store_true",help="Create local full and summary bundles, no network or mail")
    p.add_argument("--check-storage",action="store_true",help="Read-only access check to the configured bucket")
    p.add_argument("--upload-only",action="store_true",help="Upload and verify, do not send email or permit server cleanup")
    p.add_argument("--refresh-link",type=Path,help="Use an existing delivery receipt to generate a new private download link")
    p.add_argument("--link-file",type=Path,help="Private output file for --refresh-link; URL is never printed to logs")
    p.add_argument("--check-cleanup",type=Path,help="Check delivery receipt; does not delete anything")
    args = p.parse_args()
    try:
        if args.check_cleanup:
            cleanup_ready(args.check_cleanup);print("Receipt eligible for configured cleanup.");return 0
        if args.prepare_only:
            if not args.run: p.error("--prepare-only requires --run")
            run = completed_run(args.run)
            output = args.output or run.parent/"exports"/run.name
            bundle = build_bundle(run,output);summary = build_summary(run,output)
            print(json.dumps({"archive":bundle["archive"],"bytes":bundle["bytes"],"sha256":bundle["sha256"],"summary":str(summary)}))
            return 0
        if args.refresh_link:
            if not args.link_file: p.error("--refresh-link requires --link-file")
            receipt = json.loads(args.refresh_link.read_text())
            settings = S3Settings(bucket=receipt["bucket"],endpoint=receipt["endpoint"],region=receipt["region"],
                addressing_style=receipt.get("addressing_style","auto"),
                link_seconds=int(os.environ.get("QOC_ARCHIVE_LINK_SECONDS","604800"))).validate()
            client = s3_client(settings)
            verify_remote(client,settings,receipt["key"],receipt["bytes"],receipt["sha256"])
            atomic_json(args.link_file,{"download_url":download_link(client,settings,receipt),"created_at":utc_now()})
            print(f"Private download link saved to {args.link_file}");return 0
        settings = S3Settings.from_env();client = s3_client(settings)
        if args.check_storage:
            check_storage(client,settings);print("Bucket access verified (read-only; upload permission is checked during transfer).");return 0
        if not args.run: p.error("Supply --run, --check-storage or --refresh-link")
        publish(args.run,args.output,settings,client,not args.upload_only,args.receipt)
        return 0
    except Exception as exc:
        # SDK messages can contain URLs/headers. Keep ordinary logs free of credentials and signed links.
        print(f"Archiviazione non completata ({type(exc).__name__}). Dati locali e server da conservare.",file=sys.stderr)
        if isinstance(exc,(ValueError,FileNotFoundError,RuntimeError)): print(str(exc),file=sys.stderr)
        return 1


if __name__ == "__main__": sys.exit(main())
