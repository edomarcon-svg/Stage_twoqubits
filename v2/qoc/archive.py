"""Complete immutable run bundles, compact email summaries and verified S3 upload.

Credentials are supplied by the SDK environment/profile, never stored in receipts.
Verification reads the remote object back and hashes its bytes, including multipart
uploads: neither ETag nor user-provided metadata is treated as proof of integrity.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urlparse
import zipfile

CHUNK = 4 * 1024 * 1024


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=path.name+".",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=2,ensure_ascii=False,allow_nan=False)
            f.write("\n")
        os.replace(temp,path)
    finally:
        if os.path.exists(temp): os.unlink(temp)


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while block := f.read(CHUNK): h.update(block)
    return h.hexdigest()


def completed_run(run):
    run = Path(run).resolve()
    marker = run/("state.json" if (run/"campaign.json").exists() else "status.json")
    if not marker.is_file() or json.loads(marker.read_text()).get("state") != "complete":
        raise ValueError("Archive requires a completed run/campaign; interrupted or pilot-only runs are not eligible")
    if not (run/"summary.json").is_file() or not (run/"config.json").is_file():
        raise ValueError("Run is missing summary.json or config.json")
    return run


def _inventory(run):
    entries = []
    for path in sorted(run.rglob("*")):
        if path.is_symlink(): raise ValueError(f"Symlink not allowed in complete archive: {path.relative_to(run)}")
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc": continue
        stat = path.stat()
        entries.append((path.relative_to(run).as_posix(),stat.st_size,stat.st_mtime_ns))
    return entries


def build_bundle(run, output):
    run = completed_run(run)
    output = Path(output).resolve()
    if output == run or run in output.parents:
        raise ValueError("Archive output must be outside the source run")
    output.mkdir(parents=True,exist_ok=True)
    archive = output/(run.name+"_complete.zip")
    manifest_path = output/"bundle.json"
    inventory = _inventory(run)
    # Reuse a previously prepared bundle only after checking source inventory and local hash.
    if manifest_path.exists() and archive.exists():
        old = json.loads(manifest_path.read_text())
        if old.get("inventory") == [list(x) for x in inventory] and old.get("run") == str(run) and sha256_file(archive) == old.get("sha256"):
            return old
    temp = archive.with_suffix(".zip.tmp")
    members = []
    try:
        with zipfile.ZipFile(temp,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
            for relative,size,mtime in inventory:
                path = run/relative
                digest = hashlib.sha256()
                # One read supplies both ZIP and per-file hash. Zip64 supports large trajectories.
                info = zipfile.ZipInfo.from_file(path,arcname=run.name+"/"+relative)
                info.compress_type = zipfile.ZIP_STORED if path.suffix in {".npz",".png",".zip",".jpg"} else zipfile.ZIP_DEFLATED
                with path.open("rb") as source,z.open(info,"w",force_zip64=True) as target:
                    while block := source.read(CHUNK):
                        digest.update(block);target.write(block)
                members.append({"path":relative,"bytes":size,"sha256":digest.hexdigest()})
            z.writestr("ARCHIVE_MANIFEST.json",json.dumps({"run_name":run.name,"files":members},indent=2))
        completed_run(run)
        if _inventory(run) != inventory:
            raise ValueError("Run changed while archiving; archive discarded, retry when idle")
        os.replace(temp,archive)
    finally:
        temp.unlink(missing_ok=True)
    result = {"run":str(run),"archive":str(archive),"bytes":archive.stat().st_size,
        "sha256":sha256_file(archive),"inventory":inventory,"files":len(members),"created_at":utc_now()}
    atomic_json(manifest_path,result)
    return result


def build_summary(run, output, max_bytes=10*1024*1024):
    """Independent report without broken links to omitted full-run images/files."""
    run = completed_run(run)
    output = Path(output);output.mkdir(parents=True,exist_ok=True)
    dest = output/(run.name+"_summary.zip")
    summary = json.loads((run/"summary.json").read_text())
    rows = []
    if "experiments" in summary:
        for c in summary["experiments"]:
            rows.append([c.get("stage"),c.get("target"),c.get("factor_taus"),c.get("filter_cutoff"),c.get("case"),
                c.get("probability_median"),f"{c.get('validated_goal_count')}/{c.get('count')}"])
    else:
        cfg = json.loads((run/"config.json").read_text())
        for c in summary.get("cases",[]):
            stats = c["statistics"]
            rows.append(["run",json.dumps(cfg["target"]),cfg.get("factor_taus"),cfg["control"]["filter_cutoff"],c["name"],
                stats.get("probability_median"),f"{stats.get('validated_goal_count')}/{stats.get('count')}"])
    report = "<!doctype html><html lang='it'><meta charset='utf-8'><title>Riepilogo simulazione</title><body>"
    report += f"<h1>{html.escape(run.name)}</h1><p>Archivio completo disponibile al link nell'email. P indica la probabilità, non la fedeltà radice. Successo = soglia raggiunta e validazione superata.</p>"
    report += "<table border='1'><tr>"+"".join(f"<th>{x}</th>" for x in ["Fase","Target","T/tau_s","Filtro","Caso","P mediana","Successi validati"])+"</tr>"
    for row in rows: report += "<tr>"+"".join(f"<td>{html.escape(str(x))}</td>" for x in row)+"</tr>"
    report += "</table></body></html>"
    # Budget is on uncompressed payload (conservative) with margin for ZIP headers.
    used = len(report.encode())
    omitted, included = [], []
    if used > max_bytes//2: raise ValueError("Summary table alone exceeds size budget")
    with zipfile.ZipFile(dest,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        z.writestr("report.html",report)
        for name in ["summary.csv","seeds.csv","config.json","campaign.json","pilot_selection.json"]:
            path = run/name
            if not path.is_file(): continue
            if used + path.stat().st_size > max_bytes - 65536:
                omitted.append(name);continue
            z.write(path,name);used += path.stat().st_size;included.append(name)
        z.writestr("README.txt","Riepilogo leggero. Tutti gli array, grafici, metadati e sorgenti sono nell'archivio completo esterno.\n"
                   +"File inclusi: "+", ".join(included)+"\nFile esclusi per dimensione: "+", ".join(omitted)+"\n")
    if dest.stat().st_size > max_bytes: raise ValueError("Summary ZIP exceeds attachment budget")
    return dest


@dataclass(frozen=True)
class S3Settings:
    bucket: str
    endpoint: str | None = None
    region: str = "us-east-1"
    prefix: str = "twoqubits"
    link_seconds: int = 604800
    addressing_style: str = "auto"

    def validate(self):
        if not re.fullmatch(r"[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]",self.bucket):
            raise ValueError("Set QOC_ARCHIVE_BUCKET to the existing private S3 bucket name")
        if self.endpoint:
            url = urlparse(self.endpoint)
            if url.scheme != "https" or not url.hostname or url.username or url.password or url.query or url.fragment:
                raise ValueError("QOC_ARCHIVE_ENDPOINT must be an HTTPS endpoint without credentials/query")
        if not 60 <= self.link_seconds <= 604800: raise ValueError("Link lifetime must be between 60 and 604800 seconds")
        if self.addressing_style not in {"auto","path","virtual"}: raise ValueError("Invalid S3 addressing style")
        if any(c in self.prefix for c in "\r\n") or any(x in {".",".."} for x in self.prefix.split("/")):
            raise ValueError("Invalid object prefix")
        return self

    @classmethod
    def from_env(cls):
        return cls(bucket=os.environ.get("QOC_ARCHIVE_BUCKET",""),endpoint=os.environ.get("QOC_ARCHIVE_ENDPOINT") or None,
            region=os.environ.get("AWS_DEFAULT_REGION","us-east-1"),prefix=os.environ.get("QOC_ARCHIVE_PREFIX","twoqubits"),
            link_seconds=int(os.environ.get("QOC_ARCHIVE_LINK_SECONDS","604800")),
            addressing_style=os.environ.get("QOC_ARCHIVE_ADDRESSING_STYLE","auto")).validate()


def s3_client(settings):
    try:
        import boto3
        from botocore.config import Config
    except ImportError as exc:
        raise RuntimeError("Install optional archive dependencies: pip install -r requirements-archive.txt") from exc
    return boto3.client("s3",endpoint_url=settings.endpoint,region_name=settings.region,
        config=Config(signature_version="s3v4",retries={"max_attempts":5,"mode":"standard"},
            connect_timeout=20,read_timeout=120,s3={"addressing_style":settings.addressing_style},
            request_checksum_calculation="when_required",response_checksum_validation="when_required"))


def check_storage(client, settings):
    # Read-only preflight; creation/policy changes belong to the storage administrator.
    client.head_bucket(Bucket=settings.bucket)


def verify_remote(client, settings, key, size, digest):
    head = client.head_object(Bucket=settings.bucket,Key=key)
    if head["ContentLength"] != size: raise ValueError("Remote archive length mismatch")
    params = {"Bucket":settings.bucket,"Key":key}
    if head.get("VersionId"): params["VersionId"] = head["VersionId"]
    remote = client.get_object(**params)
    count, actual = 0, hashlib.sha256()
    body = remote["Body"]
    try:
        while block := body.read(CHUNK): count += len(block);actual.update(block)
    finally:
        body.close()
    if count != size or actual.hexdigest() != digest:
        raise ValueError("Remote archive SHA-256 verification failed; keep local data/server")
    return {"verified":True,"verification":"full_remote_read_sha256","verified_at":utc_now(),
        "version_id":head.get("VersionId"),"bytes":count,"sha256":actual.hexdigest()}


def upload_verified(bundle, client, settings):
    settings.validate()
    archive = Path(bundle["archive"])
    if archive.stat().st_size != bundle["bytes"] or sha256_file(archive) != bundle["sha256"]:
        raise ValueError("Local archive changed since packaging")
    key = "/".join(x for x in [settings.prefix.strip("/"),Path(bundle["run"]).name,bundle["sha256"]+".zip"] if x)
    # If a previous upload succeeded but SMTP failed, reuse it after FULL re-verification.
    try:
        existing = client.head_object(Bucket=settings.bucket,Key=key)
    except Exception as exc:
        code = str(getattr(exc,"response",{}).get("Error",{}).get("Code",""))
        if code not in {"404","NoSuchKey","NotFound"}: raise
        existing = None
    if existing is None:
        from boto3.s3.transfer import TransferConfig
        client.upload_file(str(archive),settings.bucket,key,
            ExtraArgs={"ContentType":"application/zip","Metadata":{"sha256":bundle["sha256"]}},
            Config=TransferConfig(multipart_threshold=64*1024*1024,multipart_chunksize=64*1024*1024,max_concurrency=4))
    verified = verify_remote(client,settings,key,bundle["bytes"],bundle["sha256"])
    return {**verified,"bucket":settings.bucket,"key":key,"endpoint":settings.endpoint,"region":settings.region,
        "addressing_style":settings.addressing_style,"run":bundle["run"],"local_archive":str(archive)}


def download_link(client, settings, receipt):
    params = {"Bucket":settings.bucket,"Key":receipt["key"],
        "ResponseContentDisposition":'attachment; filename="'+Path(receipt["run"]).name+'_complete.zip"'}
    if receipt.get("version_id"): params["VersionId"] = receipt["version_id"]
    return client.generate_presigned_url("get_object",Params=params,ExpiresIn=settings.link_seconds)
