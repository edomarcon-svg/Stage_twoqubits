"""Atomic metadata, versioned schemas and reproducible source snapshots."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from . import __version__

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 2


def save_json(path, data):
    path = Path(path)
    tmp = path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    os.replace(tmp,path)


def config_digest(cfg):
    return hashlib.sha256(json.dumps(cfg.to_dict(),sort_keys=True,allow_nan=False).encode()).hexdigest()


def source_hashes():
    paths = list((ROOT/"qoc").glob("*.py")) + list(ROOT.glob("*.py")) + [ROOT/"requirements.txt",ROOT/"requirements-tested.txt",ROOT/"requirements-archive.txt",ROOT/"pyproject.toml"]
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths) if p.is_file()}


def provenance(cfg):
    versions = {}
    for name in ["numpy","scipy","qutip","matplotlib","threadpoolctl"]:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    # A copied v2 works without Git; hashes and the source snapshot are authoritative.
    try:
        commit = subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
    except (OSError,subprocess.CalledProcessError):
        commit = None
    return {"schema_version":SCHEMA_VERSION,"qoc_version":__version__,"created_utc":datetime.now(timezone.utc).isoformat(),
            "python":sys.version,"platform":platform.platform(),"packages":versions,"git_commit":commit,
            "source_hashes":source_hashes(),"config_sha256":config_digest(cfg)}


def prepare_run(cfg, destination=None, resume=None):
    if resume:
        root = Path(resume).resolve()
        saved = json.loads((root/"provenance.json").read_text())
        if saved["config_sha256"]!=config_digest(cfg):
            raise ValueError("Resume refused: configuration differs from saved run")
        if saved["source_hashes"]!=source_hashes():
            raise ValueError("Resume refused: numerical source differs; start a new run")
        current = provenance(cfg)
        if saved["packages"]!=current["packages"]:
            raise ValueError("Resume refused: dependency versions differ; start a new run")
        return root
    base = Path(destination).resolve() if destination else ROOT/"results"
    base.mkdir(parents=True,exist_ok=True)
    name = "".join(c if c.isalnum() or c in "_-" else "_" for c in cfg.name)
    root = base/(name+"_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ"))
    root.mkdir()
    save_json(root/"config.json",cfg.to_dict())
    meta = provenance(cfg)
    save_json(root/"provenance.json",meta)
    snapshot = root/"source_snapshot"
    snapshot.mkdir()
    for relative in meta["source_hashes"]:
        target = snapshot/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/relative,target)
    save_json(snapshot/"resolved_config.json",cfg.to_dict())
    return root
