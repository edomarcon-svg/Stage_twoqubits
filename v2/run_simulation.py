#!/usr/bin/env python3
"""Standalone command line for v2; never imports modules from the parent folder."""
import argparse
import json
from pathlib import Path
from qoc.config import load_config
from qoc.pipeline import run_experiment
from qoc.reporting import write_reports


def main():
    parser = argparse.ArgumentParser(description="Cavità + 1/2 qubit: CRAB, GRAPE esatto, attuatore e validazione")
    parser.add_argument("--config",type=Path,help="Configurazione JSON; default configs/smoke.json")
    parser.add_argument("--output",type=Path,help="Directory BASE per una nuova run; mai sovrascrive run precedenti")
    parser.add_argument("--resume",type=Path,help="Riprende una run compatibile, verificando codice, dipendenze e config")
    parser.add_argument("--report-only",type=Path,help="Rigenera i report di una run senza ottimizzare")
    parser.add_argument("--case",action="append",help="Seleziona uno o più nomi di caso presenti nella configurazione")
    parser.add_argument("--duration",type=float,help="Tempo T esplicito, stessa unità 1/frequenza per tutti i casi")
    parser.add_argument("--intervals",type=int,help="Numero di intervalli di propagazione (dt=T/N)")
    parser.add_argument("--workers",type=int,help="Numero massimo di processi per i seed")
    parser.add_argument("--no-plots",action="store_true",help="Salva dati e tabelle; figure rigenerabili con --report-only")
    parser.add_argument("--validate-config",action="store_true",help="Stampa config risolta e controlla modelli/target senza ottimizzare")
    args = parser.parse_args()
    if args.report_only:
        write_reports(args.report_only)
        print(args.report_only/"report.html")
        return
    config_path = args.config or ((args.resume/"config.json") if args.resume else Path(__file__).resolve().parent/"configs"/"smoke.json")
    cfg = load_config(config_path)
    if args.case:
        if set(args.case)-{x.name for x in cfg.cases}:
            parser.error("Nome caso inesistente")
        cfg.cases = [c for c in cfg.cases if c.name in args.case]
    for attr in ["duration","intervals"]:
        if getattr(args,attr) is not None:
            setattr(cfg,attr,getattr(args,attr))
    if args.workers is not None:
        cfg.optimization.workers = args.workers
    cfg.validate()
    if args.validate_config:
        from qoc.models import build_model
        for c in cfg.cases:
            build_model(cfg,c)
        print(json.dumps(cfg.to_dict(),indent=2))
        return
    root = run_experiment(cfg,args.output,args.resume,plots=not args.no_plots)
    print(f"Report: {root/'report.html'}")
    print("Consultare separatamente validazione numerica e soglia target; una run completata può non averle superate.")


if __name__ == "__main__":
    main()
