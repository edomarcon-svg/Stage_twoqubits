#!/usr/bin/env python3
"""Run the configured experiment and publish its EXACT returned directory."""
import argparse
import json
from pathlib import Path
import sys
from qoc.archive import S3Settings, s3_client, check_storage
from publish_results import mail_settings, publish


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode",choices=["campaign","single"],default="campaign")
    p.add_argument("--config",type=Path)
    p.add_argument("--resume",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--receipt",type=Path,required=True)
    p.add_argument("--no-plots",action="store_true")
    args = p.parse_args()
    if not args.config and not args.resume: p.error("Supply --config or --resume")
    try:
        settings = S3Settings.from_env();client = s3_client(settings)
        mail_settings();check_storage(client,settings)
        if args.mode == "campaign":
            from qoc.campaign import load_campaign, run_campaign
            spec = load_campaign(args.config or args.resume/"campaign.json")
            root = run_campaign(spec,args.output,args.resume,plots=not args.no_plots)
        else:
            from qoc.config import load_config
            from qoc.pipeline import run_experiment
            cfg = load_config(args.config or args.resume/"config.json")
            root = run_experiment(cfg,args.output,args.resume,plots=not args.no_plots)
        publish(root,settings=settings,client=client,receipt_path=args.receipt)
        return 0
    except Exception as exc:
        print(f"Pipeline fermata ({type(exc).__name__}); nessuna cancellazione del server.",file=sys.stderr)
        if isinstance(exc,(ValueError,FileNotFoundError,RuntimeError)): print(str(exc),file=sys.stderr)
        return 1


if __name__ == "__main__": sys.exit(main())
