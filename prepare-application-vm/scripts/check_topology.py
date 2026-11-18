#!/usr/bin/env python3
"""Validate declared host/app allocations without contacting a server."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import urlsplit

NAME = re.compile(r"[a-z][a-z0-9-]{0,47}")
ROLE = re.compile(r"[a-z_][a-z0-9_]{0,62}")
USER = re.compile(r"[a-z_][a-z0-9_-]{0,31}")
ALIAS = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")
UNIT = re.compile(r"[a-zA-Z0-9_-]+\.(?:service|timer|socket)")
RESERVED_USERS = {"root", "postgres", "www-data", "nginx", "nobody", "daemon", "systemd-network"}


def object_fields(value, required, optional, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    missing = set(required) - value.keys()
    unknown = value.keys() - set(required) - set(optional)
    if missing or unknown:
        raise ValueError(f"{label}: missing {sorted(missing)}, unknown {sorted(unknown)}")


def text(value, label, pattern=None):
    if not isinstance(value, str) or not value.strip() or (pattern and not pattern.fullmatch(value)):
        raise ValueError(f"Invalid {label}")
    return value


def path(value, label):
    value = text(value, label)
    result = PurePosixPath(value)
    if not result.is_absolute() or result == PurePosixPath("/") or str(result) != value or ".." in result.parts:
        raise ValueError(f"{label} must be a normalized absolute path")
    return result


def allocated_path(value, label, kind):
    result = path(value, label)
    if kind == "root":
        valid = (result.parts[:2] == ("/", "srv") and len(result.parts) >= 3
                 or result.parts[:3] == ("/", "var", "www") and len(result.parts) >= 4)
    elif kind == "setup":
        valid = (result.parts[:2] == ("/", "home") and len(result.parts) >= 5
                 or result.parts[:2] == ("/", "srv") and len(result.parts) >= 3)
    else:
        valid = (result.parts[:2] == ("/", "run") and len(result.parts) >= 4
                 or result.parts[:3] == ("/", "var", "run") and len(result.parts) >= 5)
    if not valid:
        raise ValueError(f"{label} is outside the supported app allocation paths")
    return result


def unique(seen, key, label):
    if key in seen:
        raise ValueError(f"Duplicate {label}: {key}")
    seen.add(key)


def overlaps(first, second):
    return first == second or first in second.parents or second in first.parents


def port(value, label):
    if type(value) is not int or not 1024 <= value <= 65535:
        raise ValueError(f"{label} must be an unprivileged TCP port")
    return value


def validate(data):
    object_fields(data, ("schemaVersion", "hosts", "apps"), ("notes",), "inventory")
    if type(data["schemaVersion"]) is not int or data["schemaVersion"] != 1:
        raise ValueError("Expected schemaVersion 1")
    if not isinstance(data["hosts"], list) or not data["hosts"] or not isinstance(data["apps"], list) or not data["apps"]:
        raise ValueError("hosts and apps must be nonempty arrays")
    host_ids, aliases = set(), set()
    for host in data["hosts"]:
        object_fields(host, ("id", "sshAlias", "setupLock"), ("capacity", "operatorRole", "notes"), "host")
        unique(host_ids, text(host["id"], "host id", NAME), "host id")
        unique(aliases, text(host["sshAlias"], "SSH alias", ALIAS), "SSH alias")
        lock = path(host["setupLock"], "host setup lock")
        if lock.parts[:3] != ("/", "run", "lock") or len(lock.parts) != 4:
            raise ValueError("Host setup lock must be a named file under /run/lock")
        if host.get("operatorRole") is not None:
            text(host["operatorRole"], "operator role", ROLE)
        if host.get("capacity") is not None:
            object_fields(host["capacity"], ("vcpu", "ramGiB"), (), "capacity")
            for field, value in host["capacity"].items():
                if type(value) not in (int, float) or not 0 < value < 1000000:
                    raise ValueError(f"Invalid capacity {field}")

    app_ids, repositories, origins = set(), set(), set()
    ports, local_ports, sockets, users, databases, roles, units = set(), set(), set(), set(), set(), set(), set()
    directories, socket_paths = [], []
    for app in data["apps"]:
        object_fields(app, ("id", "host", "repository", "framework", "publicOrigin", "environments"), ("notes",), "app")
        app_id = text(app["id"], "app id", NAME)
        unique(app_ids, app_id, "app id")
        host_id = text(app["host"], "app host", NAME)
        if host_id not in host_ids:
            raise ValueError(f"{app_id} references an unknown host")
        unique(repositories, str(path(app["repository"], "repository")), "repository")
        if app["framework"] not in ("yii1", "standalone-php", "custom"):
            raise ValueError("framework must be yii1, standalone-php or custom")
        if app["publicOrigin"] is not None:
            origin = urlsplit(text(app["publicOrigin"], "publicOrigin"))
            if (origin.scheme != "https" or not origin.hostname or origin.username or origin.password
                    or origin.path not in ("", "/") or origin.query or origin.fragment):
                raise ValueError("publicOrigin must be an HTTPS origin")
            unique(origins, (origin.hostname.lower(), origin.port or 443), "public origin")
        object_fields(app["environments"], ("rehearsal", "production"), (), "environments")
        for name, environment in app["environments"].items():
            label = f"{app_id}/{name}"
            object_fields(environment,
                          ("root", "setupRoot", "serviceUser", "fpmSocket", "probePort", "database", "unitNames"),
                          ("webTunnelPort", "dbTunnelPort", "notes"), label)
            for key, kind in (("root", "root"), ("setupRoot", "setup")):
                allocated = allocated_path(environment[key], f"{label} {key}", kind)
                for other_host, other_path, other_label in directories:
                    if host_id == other_host and overlaps(allocated, other_path):
                        raise ValueError(f"Overlapping directories: {label}/{key} and {other_label}")
                directories.append((host_id, allocated, f"{label}/{key}"))
            user = text(environment["serviceUser"], f"{label} serviceUser", USER)
            if user in RESERVED_USERS:
                raise ValueError(f"Reserved application service user: {user}")
            unique(users, (host_id, user), "service user")
            sock = allocated_path(environment["fpmSocket"], f"{label} FPM socket", "socket")
            unique(sockets, (host_id, str(sock)), "FPM socket")
            socket_paths.append((host_id, sock))
            unique(ports, (host_id, port(environment["probePort"], label)), "probe port")
            for key in ("webTunnelPort", "dbTunnelPort"):
                if environment.get(key) is not None:
                    unique(local_ports, port(environment[key], key), "local tunnel port")
            if not isinstance(environment["unitNames"], list):
                raise ValueError("unitNames must be an array")
            for unit in environment["unitNames"]:
                unique(units, (host_id, text(unit, "unit name", UNIT)), "unit name")
            db = environment["database"]
            if db is None:
                if environment.get("dbTunnelPort") is not None:
                    raise ValueError("Database-free environment cannot declare a local DB tunnel")
                continue
            object_fields(db, ("cluster", "name", "ownerRole", "migrationRole", "appRole"), (), "database")
            cluster = text(db["cluster"], "cluster")
            unique(databases, (host_id, cluster, text(db["name"], "database name", ROLE)), "database")
            for key in ("ownerRole", "migrationRole", "appRole"):
                role = text(db[key], key, ROLE)
                if role in ("postgres", "root") or role.startswith("pg_"):
                    raise ValueError(f"Reserved application DB role: {role}")
                unique(roles, (host_id, cluster, role), "database role")
    for host, sock in socket_paths:
        for other_host, directory, label in directories:
            if host == other_host and overlaps(sock, directory):
                raise ValueError(f"Socket overlaps application directory {label}")
    return len(data["hosts"]), len(data["apps"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    try:
        counts = validate(json.loads(args.inventory.read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError) as error:
        parser.exit(1, f"Invalid topology: {error}\n")
    print(f"Valid allocations for {counts[1]} app(s) on {counts[0]} host(s). Verify live occupancy separately.")


if __name__ == "__main__":
    main()

