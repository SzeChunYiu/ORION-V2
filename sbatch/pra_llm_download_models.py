#!/usr/bin/env python3
"""Pre-download the two frozen models into HF_HOME and record resolved commit hashes."""
import json
import os
from pathlib import Path

from huggingface_hub import HfApi, snapshot_download

REPOS = ["Qwen/Qwen2.5-7B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3"]
hf_home = Path(os.environ["HF_HOME"])
api = HfApi()
out = {}
for repo in REPOS:
    sha = api.model_info(repo).sha
    path = snapshot_download(
        repo,
        revision=sha,
        allow_patterns=["*.json", "*.safetensors", "*.model", "*.txt", "*.py", "tokenizer*", "*.jinja"],
        ignore_patterns=["consolidated*", "*.pth", "*.bin"],
    )
    out[repo] = {"revision": sha, "local_path": path}
    print(repo, sha, path, flush=True)
json.dump(out, open(hf_home / "RESOLVED_REVISIONS.json", "w"), indent=2)
print("MODELS_READY", flush=True)
