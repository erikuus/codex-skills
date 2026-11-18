#!/usr/bin/env python3
"""Probe archive storage in an isolated worker with a full-operation deadline."""
import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys

if sys.version_info < (3, 12):
    raise SystemExit("Storage checks require Python 3.12 or newer.")


def _inspect(mount, source, fstype, known_file):
    """All potentially blocking filesystem operations belong in this worker."""
    mount = Path(mount)
    if not mount.is_absolute() or mount.is_symlink():
        raise ValueError("Expected an absolute ordinary mountpoint")
    probe = subprocess.run(["findmnt","--json","--target",str(mount),
                            "--output","SOURCE,TARGET,FSTYPE,OPTIONS"],
                           text=True,capture_output=True,timeout=5,check=True)
    records = json.loads(probe.stdout)["filesystems"]
    if not isinstance(records, list) or len(records) != 1 or not isinstance(records[0], dict):
        raise ValueError("Ambiguous storage mount")
    record = records[0]
    if record["source"] != source or record["target"] != str(mount) or record["fstype"] != fstype:
        raise ValueError("Expected archive mount is unavailable")
    if "ro" not in record["options"].split(","):
        raise ValueError("Expected a read-only archive mount")
    known_file = Path(known_file)
    if not known_file.is_absolute():
        known_file = mount/known_file
    if not known_file.resolve().is_relative_to(mount.resolve()):
        raise ValueError("Known-file probe escapes the archive mount")
    if not stat.S_ISREG(known_file.lstat().st_mode):
        raise ValueError("Known archive file must be regular")
    descriptor = os.open(known_file, os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError("Known archive file must be regular")
        if not os.read(descriptor, 1):
            raise ValueError("Known archive file is empty")
    finally:
        os.close(descriptor)
    return {"mountVerified":True,"knownFileReadable":True}


def _retire(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=0.2)
    except subprocess.TimeoutExpired:
        # Kernel-blocked network I/O may finish later. The caller stays bounded.
        pass
    if process.stdout:
        process.stdout.close()


def verify(mount, source, fstype, known_file, timeout=5):
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Storage probe deadline must be finite and positive")
    command = [sys.executable, str(Path(__file__).resolve()), "--worker",
               "--mount", str(mount), "--source", source, "--fstype", fstype,
               "--known-file", str(known_file)]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                               text=True, start_new_session=True)
    try:
        try:
            output, _ = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            raise ValueError("Archive storage probe deadline exceeded") from None
        if process.returncode != 0:
            raise ValueError("Archive storage is unavailable or unverified")
        result = json.loads(output)
        if not isinstance(result, dict) or result.get("mountVerified") is not True or result.get("knownFileReadable") is not True:
            raise ValueError("Invalid storage probe receipt")
        result["checkedAt"] = datetime.now(timezone.utc).isoformat()
        return result
    finally:
        _retire(process)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mount", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--fstype", required=True)
    parser.add_argument("--known-file", required=True)
    parser.add_argument("--timeout", type=float, default=5)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    attempted = datetime.now(timezone.utc).isoformat()
    try:
        if args.worker:
            result = _inspect(args.mount,args.source,args.fstype,args.known_file)
        else:
            result = verify(args.mount,args.source,args.fstype,args.known_file,args.timeout)
        print(json.dumps(result))
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError):
        print(json.dumps({"mountVerified":False,"knownFileReadable":None,"attemptedAt":attempted}))
        print("Archive storage is unavailable or unverified.",file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

