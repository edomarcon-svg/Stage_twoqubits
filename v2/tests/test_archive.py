"""No live services: exercise packaging, corrupt transfers, SMTP failures and cleanup gates."""
from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import zipfile
from qoc.archive import (build_bundle,build_summary,S3Settings,upload_verified,verify_remote,
    download_link,atomic_json,sha256_file)
from publish_results import publish, cleanup_ready
from send_results_email import build_message,deliver_message


class MissingObject(Exception):
    response = {"Error":{"Code":"404"}}


class MemoryS3:
    def __init__(self):
        self.objects={};self.uploads=0;self.corrupt=False;self.params=None
    def head_bucket(self,**kwargs):return {}
    def head_object(self,**kwargs):
        key=kwargs["Key"]
        if key not in self.objects:raise MissingObject()
        return {"ContentLength":len(self.objects[key]),"VersionId":"version-1"}
    def upload_file(self,path,bucket,key,**kwargs):
        self.uploads+=1;self.objects[key]=Path(path).read_bytes()
    def get_object(self,**kwargs):
        self.params=kwargs
        data=self.objects[kwargs["Key"]]
        if self.corrupt:data=bytes([data[0]^1])+data[1:]
        return {"Body":io.BytesIO(data)}
    def generate_presigned_url(self,operation,**kwargs):
        self.link_args=kwargs
        return "https://storage.example/private?signature=not-a-real-token"


def fixture(base):
    run=base/"run_001";run.mkdir()
    (run/"status.json").write_text(json.dumps({"state":"complete"}))
    (run/"config.json").write_text(json.dumps({"target":{"kind":"fock","value":10},"factor_taus":20,"control":{"filter_cutoff":3}}))
    (run/"summary.json").write_text(json.dumps({"complete":True,"cases":[{"name":"1q","statistics":{
        "probability_median":.98,"validated_goal_count":0,"count":1}}]}))
    (run/"summary.csv").write_text("case,P\n1q,0.98\n")
    (run/"arrays.npz").write_bytes(b"important numerical bytes"*100)
    (run/"source_snapshot").mkdir();(run/"source_snapshot"/"model.py").write_text("saved source\n")
    return run


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name)
        self.run=fixture(self.base);self.output=self.base/"exports"
        self.settings=S3Settings(bucket="private-bucket",endpoint="https://storage.example")
    def tearDown(self):self.temp.cleanup()

    def test_full_archive_manifest_and_no_external_files(self):
        (self.base/"archive.env").write_text("SECRET=not-a-real-secret")
        bundle=build_bundle(self.run,self.output)
        with zipfile.ZipFile(bundle["archive"]) as z:
            members=json.loads(z.read("ARCHIVE_MANIFEST.json"))["files"]
            for entry in members:
                data=z.read(self.run.name+"/"+entry["path"])
                self.assertEqual(hashlib.sha256(data).hexdigest(),entry["sha256"])
            self.assertFalse(any("archive.env" in n for n in z.namelist()))
            self.assertIn("run_001/arrays.npz",z.namelist())
        self.assertEqual(sha256_file(bundle["archive"]),bundle["sha256"])
        timestamp=Path(bundle["archive"]).stat().st_mtime_ns
        build_bundle(self.run,self.output)
        self.assertEqual(Path(bundle["archive"]).stat().st_mtime_ns,timestamp)

    def test_forbids_incomplete_source_nested_output_and_symlinks(self):
        with self.assertRaises(ValueError):build_bundle(self.run,self.run/"exports")
        (self.run/"link").symlink_to(self.base/"other")
        with self.assertRaises(ValueError):build_bundle(self.run,self.output)
        (self.run/"link").unlink()
        (self.run/"status.json").write_text('{"state":"running"}')
        with self.assertRaises(ValueError):build_bundle(self.run,self.output)

    def test_summary_omits_trajectories_and_large_tables(self):
        (self.run/"seeds.csv").write_text("x"*100000)
        path=build_summary(self.run,self.output,max_bytes=90000)
        with zipfile.ZipFile(path) as z:
            self.assertIn("report.html",z.namelist())
            self.assertNotIn("arrays.npz",z.namelist())
            self.assertNotIn("seeds.csv",z.namelist())
            self.assertIn("seeds.csv",z.read("README.txt").decode())
        self.assertLess(path.stat().st_size,90000)

    def test_upload_reuses_existing_object_and_checks_real_bytes(self):
        bundle=build_bundle(self.run,self.output);client=MemoryS3()
        receipt=upload_verified(bundle,client,self.settings)
        self.assertTrue(receipt["verified"])
        self.assertEqual(client.params["VersionId"],"version-1")
        upload_verified(bundle,client,self.settings)
        self.assertEqual(client.uploads,1)
        client.corrupt=True
        with self.assertRaisesRegex(ValueError,"SHA-256"):upload_verified(bundle,client,self.settings)

    def test_local_archive_mutation_rejected(self):
        bundle=build_bundle(self.run,self.output)
        Path(bundle["archive"]).write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError,"Local archive"):upload_verified(bundle,MemoryS3(),self.settings)

    def test_size_mismatch_rejected(self):
        client=MemoryS3();client.objects["file"]=b"short"
        with self.assertRaisesRegex(ValueError,"length"):verify_remote(client,self.settings,"file",20,"bad")

    def test_delivery_gate_smtp_failure_retry_and_no_signed_link_in_receipt(self):
        client=MemoryS3()
        env={"SMTP_USER":"sender@example.org","SMTP_PASSWORD":"test-only","EMAIL_TO":"recipient@example.org"}
        with patch.dict(os.environ,env),redirect_stdout(io.StringIO()):
            with patch("publish_results.deliver_message",side_effect=RuntimeError("SMTP failure")):
                with self.assertRaises(RuntimeError):publish(self.run,self.output,self.settings,client)
            path=self.output/"delivery.json"
            receipt=json.loads(path.read_text())
            self.assertTrue(receipt["verified"]);self.assertFalse(receipt["email_accepted"])
            with self.assertRaises(ValueError):cleanup_ready(path)
            with patch("publish_results.deliver_message") as send:
                publish(self.run,self.output,self.settings,client)
                message=send.call_args.args[0]
                self.assertIn("signature=",message.get_body().get_content())
                self.assertEqual(len(list(message.iter_attachments())),1)
            self.assertEqual(client.uploads,1)
            self.assertEqual(cleanup_ready(path)["state"],"delivered")
            self.assertNotIn("signature=",path.read_text())
            self.assertNotIn("test-only",path.read_text())

    def test_corrupt_remote_never_sends_email(self):
        client=MemoryS3();client.corrupt=True
        env={"SMTP_USER":"sender@example.org","SMTP_PASSWORD":"test-only","EMAIL_TO":"recipient@example.org"}
        with patch.dict(os.environ,env),patch("publish_results.deliver_message") as send,redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):publish(self.run,self.output,self.settings,client)
            send.assert_not_called()
            with self.assertRaises(ValueError):cleanup_ready(self.output/"delivery.json")

    def test_upload_only_never_authorizes_cleanup(self):
        with redirect_stdout(io.StringIO()):publish(self.run,self.output,self.settings,MemoryS3(),send=False)
        with self.assertRaises(ValueError):cleanup_ready(self.output/"delivery.json")

    def test_settings_reject_insecure_endpoint_and_empty_bucket(self):
        for settings in [S3Settings(""),S3Settings("bucket",endpoint="http://example.org"),
                         S3Settings("bucket",endpoint="https://user:pass@example.org"),S3Settings("bucket",link_seconds=604801)]:
            with self.assertRaises(ValueError):settings.validate()

    def test_prepare_cli_requires_no_credentials(self):
        command=[sys.executable,str(Path(__file__).resolve().parents[1]/"publish_results.py"),"--prepare-only","--run",str(self.run)]
        env={k:v for k,v in os.environ.items() if not k.startswith(("AWS_","QOC_ARCHIVE_","SMTP_"))}
        result=subprocess.run(command,env=env,capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertTrue(Path(json.loads(result.stdout)["archive"]).is_file())


class MailTests(unittest.TestCase):
    def test_message_size_checked_after_encoding(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"summary.zip";path.write_bytes(b"x"*1000)
            msg=build_message("a@example.org","b@example.org","Result","Link: https://example.org",path)
            self.assertGreater(len(msg.as_bytes()),1000)
            with patch("send_results_email.MAX_MESSAGE_BYTES",100):
                with self.assertRaisesRegex(ValueError,"Encoded"):build_message("a@example.org","b@example.org","Result","body",path)

    def test_server_size_and_recipients_checked(self):
        msg=build_message("a@example.org","b@example.org","Result","body")
        server=MagicMock();server.esmtp_features={"size":"1"}
        with patch("send_results_email.smtplib.SMTP") as smtp:
            smtp.return_value.__enter__.return_value=server
            with self.assertRaisesRegex(ValueError,"SIZE"):deliver_message(msg,"smtp.example.org",587,"a@example.org","test-only")
            server.login.assert_not_called()
            server.esmtp_features={};server.send_message.return_value={"b@example.org":(550,b"no")}
            with self.assertRaises(RuntimeError):deliver_message(msg,"smtp.example.org",587,"a@example.org","test-only")

    def test_runner_failure_never_reaches_cloud_delete(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);source=Path(__file__).resolve().parents[1]/"auto_v2.sh"
            shutil.copy2(source,base/"auto_v2.sh")
            fake=base/"python-fail";fake.write_text("#!/bin/sh\nexit 1\n");fake.chmod(0o700)
            curl=base/"curl";curl.write_text(f"#!/bin/sh\ntouch '{base/'deleted'}'\n");curl.chmod(0o700)
            env=dict(os.environ,QOC_PYTHON=str(fake),QOC_ARCHIVE_ENV_FILE=str(base/"none"),
                DELETE_SERVER_AFTER_DELIVERY="true",HCLOUD_TOKEN="test-only",PATH=str(base)+os.pathsep+os.environ["PATH"])
            result=subprocess.run(["bash",str(base/"auto_v2.sh")],env=env,capture_output=True,timeout=30)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse((base/"deleted").exists())


if __name__ == "__main__":unittest.main()
