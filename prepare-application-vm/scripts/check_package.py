#!/usr/bin/env python3
"""Check the installed skill's local references and declared dependencies."""
import hashlib
import json
from pathlib import Path
import re
import runpy


def check(root):
    runpy.run_path(str(root/"scripts/check_python.py"))["require_python"]()
    for name in ("assets/dashboard/refresh-prompt.md.template",
                 "assets/runtime/refresh-dashboard",
                 "assets/runtime/run_bounded.py",
                 "assets/systemd/iipsrv.service.template",
                 "scripts/create_refresh_prompt.py"):
        if not (root/name).is_file():
            raise ValueError(f"Missing project-handover dependency: {name}")
    source = root/"assets/kaardid-reference"
    manifest = json.loads((source/"manifest.json").read_text())
    indexed = {entry["path"] for entry in manifest["files"]}
    for entry in manifest["files"]:
        path = source/entry["path"]
        if path.is_symlink() or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError(f"Missing or changed reference: {entry['path']}")
    required = {
        "protected/config/examples/environment.production.json",
        "ops/nginx/kaardid-production-preview.conf",
        "protected/commands/UpdateCommand.php",
        "protected/config/main.php",
        "protected/views/maintenance/index.php",
        "protected/views/maintenance/mnt.php",
        "composer.json", "composer.lock",
    }
    if not required <= indexed:
        raise ValueError(f"Missing required source dependencies: {required-indexed}")
    dashboard = root/"assets/dashboard/kaardid-status-overview.html"
    if hashlib.sha256(dashboard.read_bytes()).hexdigest() != manifest["dashboard"]["sourceSha256"]:
        raise ValueError("Dashboard reference checksum changed")
    requirements = json.loads((root/"assets/reference-requirements.json").read_text())
    minimum = runpy.run_path(str(root/"scripts/check_python.py"))["MINIMUM"]
    if requirements.get("toolchain", {}).get("pythonMinimum") != ".".join(map(str, minimum)):
        raise ValueError("Declared Python minimum differs from interpreter preflight")
    for group in ("selfContainedTests", "assembledApplicationTests"):
        for name in requirements[group]:
            if not (source/"ops"/name).is_file():
                raise ValueError(f"Missing declared test: {name}")
    composer = next(item for item in requirements["dependencies"] if item["id"] == "composer-phar")
    if composer["sourceCommit"] != manifest["sourceCommit"] or not re.fullmatch("[a-f0-9]{64}", composer["sha256"]):
        raise ValueError("Composer acquisition provenance is incomplete")
    for document in [root/"SKILL.md", *(root/"references").glob("*.md")]:
        for link in re.findall(r"\]\(([^)]+)\)", document.read_text()):
            if not link.startswith(("https:", "http:", "#")) and not (document.parent/link.split("#")[0]).exists():
                raise ValueError(f"Broken skill link in {document.name}: {link}")
    policy = (root/"agents/openai.yaml").read_text()
    if not re.search(r"(?m)^  allow_implicit_invocation: false$", policy):
        raise ValueError("Explicit invocation policy changed")
    validate = runpy.run_path(str(root/"scripts/check_topology.py"))["validate"]
    validate(json.loads((root/"assets/topology.example.json").read_text()))
    return len(indexed), len(requirements["dependencies"])


if __name__ == "__main__":
    try:
        count, dependencies = check(Path(__file__).resolve().parent.parent)
        print(f"Verified {count} source references and {dependencies} declared external runtime dependency groups.")
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit(f"Package check failed: {error}")

