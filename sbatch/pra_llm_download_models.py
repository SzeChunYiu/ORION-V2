#!/usr/bin/env python3
"""Pre-download frozen models into HF_HOME and record resolved commit hashes.

Usage: pra_llm_download_models.py [--out NAME.json] [REPO ...]
Default (no repos): the Design V1 pair -> HF_HOME/RESOLVED_REVISIONS.json.
Design V2 pair:     --out RESOLVED_REVISIONS_V2.json Qwen/Qwen2.5-32B-Instruct mistralai/Mistral-Small-24B-Instruct-2501
Only HF-format shards are fetched (consolidated.safetensors / *.pth / *.bin are skipped).
"""
import argparse
import json
import os
from pathlib import Path

from huggingface_hub import HfApi, snapshot_download

V1_REPOS = ["Qwen/Qwen2.5-7B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3"]
ap = argparse.ArgumentParser()
ap.add_argument("--out", default="RESOLVED_REVISIONS.json", help="file name written under HF_HOME")
ap.add_argument("repos", nargs="*", default=V1_REPOS)
args = ap.parse_args()
hf_home = Path(os.environ["HF_HOME"])
api = HfApi()
out = {}
for repo in args.repos:
    info = api.model_info(repo)
    sha = info.sha
    path = snapshot_download(
        repo,
        revision=sha,
        allow_patterns=["*.json", "*.safetensors", "*.model", "*.txt", "*.py", "tokenizer*", "*.jinja"],
        ignore_patterns=["consolidated*", "*.pth", "*.bin"],
    )
    size = sum(p.stat().st_size for p in Path(path).rglob("*") if p.is_file())
    out[repo] = {"revision": sha, "local_path": path, "gated": bool(getattr(info, "gated", False)), "snapshot_bytes": size}
    print(repo, sha, path, f"{size / 1e9:.1f} GB", flush=True)
json.dump(out, open(hf_home / args.out, "w"), indent=2)
print("MODELS_READY", flush=True)
