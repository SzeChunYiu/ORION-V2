"""Verify this additive package and its unchanged upstream contract inputs."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]


def verify():
    manifest = json.loads((ROOT / "SOURCE_BINDING.json").read_text())
    for item in manifest["files"] + manifest["read_only_contracts"]:
        target = REPO / item["path"]
        relative = Path(item["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("invalid_source_path")
        cursor = REPO
        for part in relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ValueError("source_symlink:" + item["path"])
        content = target.read_bytes()
        if hashlib.sha256(content).hexdigest() != item["sha256"]:
            raise ValueError("source_digest_mismatch:" + item["path"])
        blob = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        if blob != item["git_blob_sha1"]:
            raise ValueError("source_git_blob_mismatch:" + item["path"])
    authored = {p.relative_to(REPO).as_posix() for p in ROOT.rglob("*")
                if p.is_file() and "__pycache__" not in p.parts and p.name != "SOURCE_BINDING.json"}
    bound = {x["path"] for x in manifest["files"] if x["path"].startswith(ROOT.relative_to(REPO).as_posix())}
    if authored != bound:
        raise ValueError("authored_inventory_mismatch")
    tree = ast.parse((ROOT / "adapter.py").read_text())
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        if any("orion" in name.lower() for name in names):
            raise ValueError("orion_import_in_parent_arm")
    return {"status": "SOURCE_BINDINGS_VALID", "authored_files": len(manifest["files"]),
            "read_only_contracts": len(manifest["read_only_contracts"]),
            "manifest_sha256": hashlib.sha256((ROOT / "SOURCE_BINDING.json").read_bytes()).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
