#!/usr/bin/env python3
"""Run a command with a deadline and clean up its process group on exit."""
import argparse
import os
import signal
import subprocess
import sys


def stop_group(process):
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        pass
    # A descendant can outlive its group leader or ignore SIGTERM.
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def run(command, timeout):
    if timeout <= 0:
        raise ValueError("The deadline must be positive")
    process = subprocess.Popen(command, start_new_session=True)
    previous = {}
    def interrupted(signum, frame):
        raise KeyboardInterrupt
    try:
        for signum in (signal.SIGTERM, signal.SIGHUP):
            previous[signum] = signal.signal(signum, interrupted)
        result = process.wait(timeout=timeout)
        # Retire background descendants even after a normal leader exit.
        stop_group(process)
        return result
    except subprocess.TimeoutExpired:
        stop_group(process)
        print("Command deadline exceeded; refresh outcome requires readback verification.", file=sys.stderr)
        return 124
    except KeyboardInterrupt:
        stop_group(process)
        return 130
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command or args.timeout <= 0:
        parser.error("Supply a positive deadline and command")
    try:
        return run(command, args.timeout)
    except OSError as error:
        print(f"Command could not start: {error}", file=sys.stderr)
        return 127


if __name__ == "__main__":
    raise SystemExit(main())

