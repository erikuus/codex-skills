#!/usr/bin/env python3
"""Resolve Facebook deletion CSV rows through VAU and emit GitHub issue drafts."""

from __future__ import annotations

import argparse
import calendar
import csv
import datetime as dt
import json
import os
import re
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


MAX_API_BATCH = 500
DEFAULT_CLIENT_BASE_URL = "https://www.ra.ee/vau/index.php/et/client/view"
HEADER_NAMES = {
    "id",
    "uid",
    "userid",
    "user_id",
    "facebookid",
    "facebook_id",
    "appscopeduserid",
    "app_scoped_user_id",
}


class WorkflowError(RuntimeError):
    pass


@dataclass(frozen=True)
class SourceRow:
    path: Path
    line: int
    facebook_id: str
    received_date: dt.date | None


@dataclass
class Resolution:
    facebook_id: str
    status: str
    user_id: int | None
    sources: list[SourceRow]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve Facebook deletion CSVs and emit VAU investigation issue drafts."
    )
    parser.add_argument("csv_files", nargs="+", type=Path)
    return parser.parse_args(argv)


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise WorkflowError(f"Missing environment variable: {name}")
    return value


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9_]", "", value.strip().lower().replace(" ", "_"))


def received_date_from_path(path: Path) -> dt.date | None:
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", path.stem)
    if not match:
        return None
    try:
        return dt.date.fromisoformat(match.group(1))
    except ValueError:
        return None


def read_csv(path: Path) -> list[SourceRow]:
    if not path.is_file():
        raise WorkflowError(f"CSV file does not exist: {path}")

    rows: list[tuple[int, list[str]]] = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for line, row in enumerate(csv.reader(handle), start=1):
                if any(cell.strip() for cell in row):
                    rows.append((line, row))
    except (OSError, UnicodeError, csv.Error) as exc:
        raise WorkflowError(f"Cannot read CSV file {path}: {exc}") from exc

    if not rows:
        raise WorkflowError(f"CSV file is empty: {path}")

    first_line, first_row = rows[0]
    header_index = next(
        (
            index
            for index, value in enumerate(first_row)
            if normalize_header(value) in HEADER_NAMES
        ),
        None,
    )
    data_rows = rows[1:] if header_index is not None else rows
    received_date = received_date_from_path(path)
    result: list[SourceRow] = []

    for line, row in data_rows:
        if header_index is not None:
            value = row[header_index].strip() if header_index < len(row) else ""
        else:
            values = [cell.strip() for cell in row if cell.strip()]
            if len(values) != 1:
                raise WorkflowError(
                    f"{path}:{line} must contain exactly one Facebook ID or use a recognized ID header"
                )
            value = values[0]

        if not re.fullmatch(r"\d{1,255}", value):
            raise WorkflowError(f"{path}:{line} does not contain a valid Facebook ID")
        result.append(SourceRow(path.resolve(), line, value, received_date))

    if not result:
        raise WorkflowError(f"CSV file has no Facebook IDs: {path}")
    return result


def collect_rows(paths: Iterable[Path]) -> dict[str, list[SourceRow]]:
    collected: dict[str, list[SourceRow]] = {}
    for path in paths:
        for source in read_csv(path):
            collected.setdefault(source.facebook_id, []).append(source)
    return collected


def http_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: bytes | None = None,
) -> tuple[Any, dict[str, str]]:
    request = urllib.request.Request(url, data=body, method=method)
    request.add_header("Accept", "application/json")
    request.add_header("User-Agent", "Codex-Facebook-Deletion-Requests/1.0")
    for name, value in (headers or {}).items():
        request.add_header(name, value)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            response_headers = {name.lower(): value for name, value in response.headers.items()}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise WorkflowError(f"HTTP {exc.code} from {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise WorkflowError(f"Cannot reach {url}: {exc.reason}") from exc

    try:
        return json.loads(raw), response_headers
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"Non-JSON response from {url}") from exc


def multipart_form_data(fields: dict[str, str]) -> tuple[bytes, str]:
    boundary = f"----CodexFacebookDeletion{secrets.token_hex(16)}"
    parts: list[bytes] = []
    for name, value in fields.items():
        parts.extend(
            [
                f"--{boundary}\r\n".encode("ascii"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(
                    "ascii"
                ),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )
    parts.append(f"--{boundary}--\r\n".encode("ascii"))
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


class VauApi:
    def __init__(self) -> None:
        self.base_url = require_env("VAU_API_BASE_URL").rstrip("/")
        self.token = self._login()

    def _login(self) -> str:
        body, content_type = multipart_form_data(
            {
                "username": require_env("VAU_API_USERNAME"),
                "password": require_env("VAU_API_PASSWORD"),
            }
        )
        response, _ = http_json(
            f"{self.base_url}/user/verify",
            method="POST",
            headers={"Content-Type": content_type},
            body=body,
        )
        if not isinstance(response, dict) or response.get("responseStatus") != "ok":
            message = response.get("errorMessage") if isinstance(response, dict) else None
            raise WorkflowError(
                f"VAU API authentication failed: {message or 'unexpected response'}"
            )
        token = response.get("accessToken")
        if not isinstance(token, str) or not token:
            raise WorkflowError("VAU API authentication returned no access token")
        return token

    def resolve(self, ids: list[str], sources: dict[str, list[SourceRow]]) -> list[Resolution]:
        resolutions: list[Resolution] = []
        for start in range(0, len(ids), MAX_API_BATCH):
            chunk = ids[start : start + MAX_API_BATCH]
            query = urllib.parse.urlencode({"token": self.token})
            response, _ = http_json(
                f"{self.base_url}/ra/facebookDeletion/resolve?{query}",
                method="POST",
                headers={
                    "Content-Type": "application/json",
                },
                body=json.dumps({"facebook_ids": chunk}).encode("utf-8"),
            )
            if not isinstance(response, dict) or response.get("responseStatus") != "ok":
                message = response.get("errorMessage") if isinstance(response, dict) else None
                raise WorkflowError(f"VAU resolution failed: {message or 'unexpected response'}")
            results = response.get("results")
            if not isinstance(results, list) or len(results) != len(chunk):
                raise WorkflowError("VAU resolution response does not match the request")

            for expected_row, (facebook_id, item) in enumerate(zip(chunk, results), start=1):
                if not isinstance(item, dict) or item.get("row") != expected_row:
                    raise WorkflowError("VAU resolution response contains an invalid row number")
                status = item.get("status")
                if status not in {"found", "not_found", "ambiguous", "invalid"}:
                    raise WorkflowError("VAU resolution response contains an unknown status")
                user_id = item.get("user_id") if status == "found" else None
                if status == "found" and (not isinstance(user_id, int) or user_id <= 0):
                    raise WorkflowError("VAU resolution response contains an invalid user ID")
                resolutions.append(Resolution(facebook_id, status, user_id, sources[facebook_id]))
        return resolutions


def add_calendar_month(value: dt.date) -> dt.date:
    year = value.year + (1 if value.month == 12 else 0)
    month = 1 if value.month == 12 else value.month + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def source_description(source: SourceRow) -> str:
    description = f"`{source.path.name}`, rida {source.line}"
    if source.received_date:
        description += (
            f"; saadud {source.received_date.isoformat()}"
            f"; vastamise tähtaeg {add_calendar_month(source.received_date).isoformat()}"
        )
    return description


def build_issue(
    user_id: int,
    resolutions: list[Resolution],
    client_base_url: str,
) -> dict[str, Any]:
    client_url = f"{client_base_url}?{urllib.parse.urlencode({'id': user_id})}"
    source_rows = sorted(
        {source for resolution in resolutions for source in resolution.sources},
        key=lambda source: (source.path.name, source.line),
    )
    body_lines = [
        "Facebook on edastanud selle VAU kliendi kasutajaandmete kustutamise taotluse.",
        "",
        f"VAU klient: {client_url}",
        "",
        "Soovitus:",
        "",
        "- Kui kasutajal on muid sisselogimisviise, eemalda VAU konto seos Facebookiga.",
        "- Kui kasutaja on VAU-d kasutanud ainult Facebooki kaudu ja tema kontol ei ole olulisi andmeid, võta temaga ühendust ja/või kustuta kasutajakonto.",
        "",
        "Allikad:",
        *[f"- {source_description(source)}" for source in source_rows],
    ]
    return {
        "user_id": user_id,
        "client_url": client_url,
        "title": f"Facebooki andmete kustutamistaotlus – VAU klient {user_id}",
        "body": "\n".join(body_lines),
        "sources": [
            {
                "file": source.path.name,
                "row": source.line,
                "received_date": source.received_date.isoformat()
                if source.received_date
                else None,
            }
            for source in source_rows
        ],
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        sources = collect_rows(args.csv_files)
        ids = list(sources)
        resolutions = VauApi().resolve(ids, sources)
        counts = {
            status: sum(1 for resolution in resolutions if resolution.status == status)
            for status in ("found", "not_found", "ambiguous", "invalid")
        }
        unresolved = [resolution for resolution in resolutions if resolution.status != "found"]
        by_user: dict[int, list[Resolution]] = {}
        for resolution in resolutions:
            if resolution.status == "found" and resolution.user_id is not None:
                by_user.setdefault(resolution.user_id, []).append(resolution)

        client_base_url = os.environ.get(
            "VAU_CLIENT_BASE_URL", DEFAULT_CLIENT_BASE_URL
        ).rstrip("?")
        output = {
            "summary": {
                "file_count": len(args.csv_files),
                "row_count": sum(len(rows) for rows in sources.values()),
                "unique_facebook_id_count": len(ids),
                **{f"{status}_count": count for status, count in counts.items()},
                "issue_draft_count": len(by_user),
            },
            "issues": [
                build_issue(user_id, by_user[user_id], client_base_url)
                for user_id in sorted(by_user)
            ],
            "unresolved": [
                {
                    "status": resolution.status,
                    "sources": [
                        {"file": source.path.name, "row": source.line}
                        for source in resolution.sources
                    ],
                }
                for resolution in unresolved
            ],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 3 if unresolved else 0
    except WorkflowError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
