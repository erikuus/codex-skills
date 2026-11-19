#!/usr/bin/env python3
"""Plan app-role SQL while preserving an existing shared operator identity."""
import argparse
import json
from pathlib import Path
import re


def plan(data):
    roles = data["roles"]
    if set(roles) != {"owner", "migrate", "app", "readonly"}:
        raise ValueError("Expected owner, migrate, app and readonly roles")
    operator = data["operator"]
    names = [operator, *roles.values()]
    if any(not isinstance(name, str) or not re.fullmatch("[a-z_][a-z0-9_]{0,62}", name) for name in names):
        raise ValueError("Invalid role identifier")
    if len(set(names)) != len(names):
        raise ValueError("Operator and app roles must be distinct")
    if any(name == "postgres" or name.startswith("pg_") for name in roles.values()):
        raise ValueError("Reserved application role")
    existing, managed = set(data["existingRoles"]), set(data["managedRoles"])
    if operator not in existing:
        raise ValueError("Prepare the personal operator login separately at host level")
    if not managed <= set(roles.values()):
        raise ValueError("Bootstrap receipt includes objects outside this app")
    if existing.intersection(roles.values()) - managed:
        raise ValueError("Existing app role has no matching ownership receipt")
    statements, created = [], []
    for kind, name in roles.items():
        if name not in existing:
            login = "LOGIN" if kind in ("migrate", "app") else "NOLOGIN"
            statements.append(f'CREATE ROLE "{name}" {login} NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;')
            created.append(name)
    statements.extend([
        f'GRANT "{roles["owner"]}" TO "{roles["migrate"]}";',
        f'GRANT "{roles["readonly"]}" TO "{operator}";',
    ])
    return {"createdRoles":created, "sql":"BEGIN;\n"+"\n".join(statements)+"\nCOMMIT;\n"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(plan(json.loads(args.inventory.read_text()))))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"App-role plan stopped: {error}\n")


if __name__ == "__main__":
    main()

