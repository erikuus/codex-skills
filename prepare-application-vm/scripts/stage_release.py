#!/usr/bin/env python3
"""Stage a verified first-release artifact as its deployment owner."""
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
import grp
import pwd
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tarfile
import tempfile
import sys

if sys.version_info < (3, 12):
    raise SystemExit("First-release staging requires Python 3.12 or newer.")


def owned(path, directory=False):
    info = path.lstat()
    expected = stat.S_ISDIR if directory else stat.S_ISREG
    if not expected(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o022:
        raise ValueError(f"Unexpected path ownership/type/permissions: {path}")
    return info


def shared_directory(path, policy):
    """Check declared runtime identity/mode independently from immutable code."""
    if set(policy) != {"target", "owner", "group", "mode"}:
        raise ValueError("Shared policy requires target, owner, group and mode")
    if not isinstance(policy["mode"], str) or not re.fullmatch("[02][0-7]{3}", policy["mode"]):
        raise ValueError("Shared mode must be a four-digit directory mode")
    mode = int(policy["mode"], 8)
    if mode & 0o002 or mode & 0o700 != 0o700:
        raise ValueError("Shared mode must permit owner access and prevent world writes")
    try:
        uid = pwd.getpwnam(policy["owner"]).pw_uid
        gid = grp.getgrnam(policy["group"]).gr_gid
    except (KeyError, TypeError):
        raise ValueError("Expected shared owner/group is unavailable") from None
    info = path.lstat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != uid or info.st_gid != gid
            or stat.S_IMODE(info.st_mode) != mode):
        raise ValueError(f"Unexpected shared directory identity/mode: {path}")


def relative(value):
    if not isinstance(value, str):
        raise ValueError("Expected a relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or str(path) != value or not value or ".." in path.parts or value == ".":
        raise ValueError("Unsafe relative path")
    return path


@contextmanager
def lock(target):
    fd = os.open(target/".bootstrap.lock", os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o077:
            raise ValueError("Unsafe bootstrap lock")
        fcntl.flock(fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
        yield
    finally:
        os.close(fd)


def prepare(target, archive, manifest_path, mappings):
    if os.geteuid() == 0:
        raise ValueError("Stage releases as the deployment owner")
    target = Path(target).absolute()
    owned(target, True)
    target = target.resolve(strict=True)
    releases, shared = target/"releases", target/"shared"
    owned(releases, True)
    owned(shared, True)
    if not isinstance(mappings, dict):
        raise ValueError("Expected a shared-map object")
    mapped = {}
    for source, destination in mappings.items():
        if isinstance(destination, dict):
            destination_path = relative(destination.get("target"))
        else:
            destination_path = relative(destination)
        source_path = relative(source)
        for existing in mapped:
            if source_path in existing.parents or existing in source_path.parents:
                raise ValueError("Overlapping shared placeholders")
        shared_target = shared/str(destination_path)
        if shared_target.resolve() != shared_target:
            raise ValueError("Shared target contains a symlink")
        if isinstance(destination, dict):
            shared_directory(shared_target, destination)
        else:
            # Legacy strings retain their deployer-owned, immutable-mode contract.
            owned(shared_target, True)
        mapped[source_path] = shared_target
    owned(manifest_path)
    owned(archive)
    manifest = json.loads(Path(manifest_path).read_text())
    sha = manifest.get("commit", "")
    if not isinstance(sha, str) or not re.fullmatch("[a-f0-9]{40}", sha):
        raise ValueError("Invalid artifact commit")
    expected_hash = manifest.get("artifact_sha256")
    with Path(archive).open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != expected_hash:
            raise ValueError("Artifact checksum mismatch")
    with lock(target), tarfile.open(archive) as bundle:
        if (target/"rehearsal").exists() or (target/"rehearsal").is_symlink():
            raise ValueError("Rehearsal is already initialized; use routine deployment")
        entries, names = [], set()
        for entry in bundle.getmembers():
            name = relative(entry.name)
            if (name.parts[0] != sha or str(name) in names
                    or not (entry.isdir() or entry.isfile())):
                raise ValueError("Unsafe or duplicate archive entry")
            names.add(str(name))
            entries.append(entry)
        if not entries:
            raise ValueError("Empty release artifact")
        for source in mapped:
            placeholder = f"{sha}/{source}"
            if placeholder not in names or not bundle.getmember(placeholder).isdir():
                raise ValueError("Shared placeholder must be an archive directory")
            if any(name.startswith(placeholder+"/") for name in names):
                raise ValueError("Shared placeholder contains immutable content")
        expected = {str(PurePosixPath(e.name).relative_to(sha)) for e in entries}
        expected.discard(".")
        release = releases/sha
        def verify(directory):
            owned(directory, True)
            actual = {str(p.relative_to(directory)) for p in directory.rglob("*")}
            if actual != expected:
                raise ValueError("Release has missing or extra paths")
            for entry in entries:
                rel = PurePosixPath(entry.name).relative_to(sha)
                path = directory/str(rel)
                if rel in mapped:
                    if not path.is_symlink() or os.readlink(path) != str(mapped[rel]):
                        raise ValueError("Unexpected shared link")
                elif entry.isdir():
                    owned(path, True)
                else:
                    owned(path)
                    with path.open("rb") as stream, bundle.extractfile(entry) as source:
                        if hashlib.file_digest(stream, "sha256").digest() != hashlib.file_digest(source, "sha256").digest():
                            raise ValueError("Existing release content differs")
                    if bool(path.stat().st_mode & 0o111) != bool(entry.mode & 0o111):
                        raise ValueError("Existing release executable mode differs")
        if release.exists() or release.is_symlink():
            verify(release)
            return {"release":str(release), "reused":True}
        stage = Path(tempfile.mkdtemp(prefix=".bootstrap-"+sha[:12]+"-", dir=releases))
        try:
            for entry in entries:
                rel = PurePosixPath(entry.name).relative_to(sha)
                destination = stage/str(rel)
                if entry.isdir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with bundle.extractfile(entry) as source, destination.open("xb") as output:
                        shutil.copyfileobj(source, output)
                    destination.chmod(0o750 if entry.mode & 0o111 else 0o640)
            for source, destination in mapped.items():
                placeholder = stage/str(source)
                placeholder.rmdir()
                placeholder.symlink_to(destination, target_is_directory=True)
            for item in [stage, *stage.rglob("*")]:
                if not item.is_symlink():
                    os.chown(item, -1, releases.stat().st_gid)
                    if item.is_dir():
                        item.chmod(0o2750)
            verify(stage)
            os.rename(stage, release)
        except BaseException:
            # Preserve this private, identified attempt for diagnosis.
            raise
        return {"release":str(release), "reused":False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("target", "archive", "manifest", "shared-map"):
        parser.add_argument("--"+name, type=Path, required=True)
    args = parser.parse_args()
    try:
        result = prepare(args.target, args.archive, args.manifest,
                         json.loads(args.shared_map.read_text()))
    except (OSError, ValueError, tarfile.TarError) as error:
        parser.exit(1, f"First-release staging stopped: {error}\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()

