#!/usr/bin/env python3
"""Run only local fixture tests. No live VM access is performed."""
import json
import os
from pathlib import Path
import runpy
import socket
import tempfile
import unittest
from unittest.mock import patch


def main():
    root = Path(__file__).resolve().parent.parent
    runpy.run_path(str(root/"scripts/check_python.py"))["require_python"]()
    runpy.run_path(str(root/"scripts/check_package.py"))["check"](root)
    requirements = json.loads((root/"assets/reference-requirements.json").read_text())
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.discover(str(root/"scripts/tests"), pattern="test_*.py"))
    for name in requirements["selfContainedTests"]:
        suite.addTests(unittest.defaultTestLoader.discover(str(root/"assets/kaardid-reference/ops"), pattern=name))
    with tempfile.TemporaryDirectory(prefix="skill-offline-commands-") as temporary:
        for command in ("ssh", "scp", "rsync", "sudo", "systemctl", "psql", "pg_dump", "pg_restore", "curl"):
            path = Path(temporary)/command
            path.write_text("#!/bin/sh\necho 'Live command prohibited during skill validation' >&2\nexit 97\n")
            path.chmod(0o755)
        with patch.dict(os.environ, {"PATH":temporary+os.pathsep+os.environ["PATH"]}), patch.object(
                socket.socket, "connect", side_effect=AssertionError("Network access prohibited in offline validation")):
            result = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

