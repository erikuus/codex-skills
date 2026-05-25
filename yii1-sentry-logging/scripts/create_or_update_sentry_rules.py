#!/usr/bin/env python3
"""Create or update the two recommended Sentry issue alert rules."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional


BASE_URL = "https://sentry.io/api/0"


def build_rule1_name(email: str, environment: str) -> str:
    return f"Notify {email}: new {environment} issue"


def build_rule2_name(email: str, environment: str) -> str:
    return f"Notify {email}: persistent {environment} issue"


def api_request(
    token: str,
    method: str,
    url: str,
    payload: Optional[Dict[str, Any]] = None,
) -> Any:
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"{method} {url} failed with {exc.code}: {body}"
        ) from exc


def list_rules(token: str, base_url: str, org: str, project: str) -> List[Dict[str, Any]]:
    url = f"{base_url}/projects/{urllib.parse.quote(org)}/{urllib.parse.quote(project)}/rules/"
    return api_request(token, "GET", url)


def create_rule(
    token: str,
    base_url: str,
    org: str,
    project: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    url = f"{base_url}/projects/{urllib.parse.quote(org)}/{urllib.parse.quote(project)}/rules/"
    return api_request(token, "POST", url, payload)


def update_rule(
    token: str,
    base_url: str,
    org: str,
    project: str,
    rule_id: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    url = (
        f"{base_url}/projects/{urllib.parse.quote(org)}/"
        f"{urllib.parse.quote(project)}/rules/{urllib.parse.quote(rule_id)}/"
    )
    return api_request(token, "PUT", url, payload)


def find_rule_by_name(rules: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
    for rule in rules:
        if rule.get("name") == name:
            return rule
    return None


def build_rule1_payload(name: str, environment: str, member_id: str) -> Dict[str, Any]:
    return {
        "name": name,
        "actionMatch": "all",
        "filterMatch": "all",
        "frequency": 5,
        "conditions": [
            {
                "id": "sentry.rules.conditions.first_seen_event.FirstSeenEventCondition",
            }
        ],
        "filters": [],
        "actions": [
            {
                "id": "sentry.mail.actions.NotifyEmailAction",
                "targetType": "Member",
                "targetIdentifier": member_id,
                "fallthroughType": "ActiveMembers",
            }
        ],
        "environment": environment,
    }


def build_rule2_payload(name: str, environment: str, member_id: str) -> Dict[str, Any]:
    return {
        "name": name,
        "actionMatch": "all",
        "filterMatch": "all",
        "frequency": 480,
        "conditions": [
            {
                "id": "sentry.rules.conditions.event_frequency.EventFrequencyCondition",
                "value": 4,
                "interval": "1h",
            }
        ],
        "filters": [],
        "actions": [
            {
                "id": "sentry.mail.actions.NotifyEmailAction",
                "targetType": "Member",
                "targetIdentifier": member_id,
                "fallthroughType": "ActiveMembers",
            }
        ],
        "environment": environment,
    }


def ensure_rule(
    token: str,
    base_url: str,
    org: str,
    project: str,
    rules: List[Dict[str, Any]],
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    existing = find_rule_by_name(rules, payload["name"])
    if existing is None:
        return create_rule(token, base_url, org, project, payload)
    return update_rule(token, base_url, org, project, str(existing["id"]), payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create or update the recommended Rule 1 and Rule 2 issue alerts."
    )
    parser.add_argument("--org", required=True, help="Sentry organization slug")
    parser.add_argument("--project", required=True, help="Sentry project slug")
    parser.add_argument("--member-id", required=True, help="Sentry member identifier")
    parser.add_argument("--email", required=True, help="Maintainer email used in rule names")
    parser.add_argument(
        "--environment",
        default="prod",
        help="Environment to scope the rules to (default: prod)",
    )
    parser.add_argument(
        "--base-url",
        default=BASE_URL,
        help=f"Sentry API base URL (default: {BASE_URL})",
    )
    parser.add_argument(
        "--token-env",
        default="SENTRY_AUTH_TOKEN",
        help="Environment variable that contains the Sentry auth token",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get(args.token_env)
    if not token:
        print(
            f"Missing {args.token_env}. Export a Sentry auth token before running this script.",
            file=sys.stderr,
        )
        return 2

    rule1_name = build_rule1_name(args.email, args.environment)
    rule2_name = build_rule2_name(args.email, args.environment)

    try:
        existing_rules = list_rules(token, args.base_url, args.org, args.project)
        rule1 = ensure_rule(
            token,
            args.base_url,
            args.org,
            args.project,
            existing_rules,
            build_rule1_payload(rule1_name, args.environment, args.member_id),
        )
        refreshed_rules = list_rules(token, args.base_url, args.org, args.project)
        rule2 = ensure_rule(
            token,
            args.base_url,
            args.org,
            args.project,
            refreshed_rules,
            build_rule2_payload(rule2_name, args.environment, args.member_id),
        )
        final_rules = list_rules(token, args.base_url, args.org, args.project)
    except RuntimeError as exc:
        message = str(exc)
        if "environment" in message.lower():
            print(message, file=sys.stderr)
            print(
                "Hint: seed one event into this environment first so Sentry knows it exists.",
                file=sys.stderr,
            )
            return 1
        print(message, file=sys.stderr)
        return 1

    result = {
        "project": args.project,
        "environment": args.environment,
        "rule1_name": rule1_name,
        "rule2_name": rule2_name,
        "rule1_id": rule1.get("id"),
        "rule2_id": rule2.get("id"),
        "rules": [
            rule
            for rule in final_rules
            if rule.get("name") in {rule1_name, rule2_name}
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
