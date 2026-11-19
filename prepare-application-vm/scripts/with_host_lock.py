#!/usr/bin/env python3
"""Serialize an already reviewed host-setup command under a private lock."""
import argparse
import fcntl
import os
from pathlib import Path
import stat
import subprocess


def run(path, command):
    descriptor = os.open(path, os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o077:
            raise ValueError("Unexpected host setup lock owner or permissions")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            return 75
        # The reviewed foreground helper keeps ownership if this wrapper exits.
        return subprocess.run(command, pass_fds=(descriptor,)).returncode
    finally:
        os.close(descriptor)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("Supply the reviewed host setup command")
    try:
        return run(args.lock, command)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Host setup stopped: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())

