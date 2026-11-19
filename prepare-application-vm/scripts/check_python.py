#!/usr/bin/env python3
"""Check the interpreter before running VM setup or deployment helpers."""
import sys

MINIMUM = (3, 12)


def require_python(version=None):
    actual = tuple((version or sys.version_info)[:2])
    if actual < MINIMUM:
        raise RuntimeError("Python 3.12 or newer is required on the workstation and VM.")
    return actual


if __name__ == "__main__":
    try:
        require_python()
    except RuntimeError as error:
        raise SystemExit(str(error))
    print("Python toolchain verified: "+sys.version.split()[0])

