#!/usr/bin/env python3
"""Print the expected two-email verification checkpoints for XSentryLogRoute."""

from __future__ import annotations

import argparse
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Describe the expected event and email progression for the fixed-window Sentry route."
    )
    parser.add_argument("--window-seconds", type=int, default=900)
    parser.add_argument("--max-initial-events", type=int, default=1)
    parser.add_argument("--summary-threshold", type=int, default=25)
    parser.add_argument("--rule2-seen-more-than", type=int, default=4)
    parser.add_argument("--rule2-interval", default="1h")
    parser.add_argument("--rule2-frequency-minutes", type=int, default=480)
    parser.add_argument("--environment", default="prod")
    parser.add_argument("--marker", default="YII1_SENTRY_RULE_TEST_YYYYMMDD_A")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    checkpoints = [
        {
            "event": 1,
            "raw_occurrence": 1,
            "window": 1,
            "effect_in_sentry": "creates the issue",
            "issue_event_count": 1,
            "email_expected": "Rule 1 sends email 1",
        },
        {
            "event": 2,
            "raw_occurrence": args.summary_threshold,
            "window": 1,
            "effect_in_sentry": "same issue, summary event",
            "issue_event_count": 2,
            "email_expected": "no new email yet",
        },
        {
            "event": 3,
            "raw_occurrence": 1,
            "window": 2,
            "effect_in_sentry": "same issue, first occurrence in next fixed window",
            "issue_event_count": 3,
            "email_expected": "no new email yet",
        },
        {
            "event": 4,
            "raw_occurrence": args.summary_threshold,
            "window": 2,
            "effect_in_sentry": "same issue, summary event in next window",
            "issue_event_count": 4,
            "email_expected": "no new email yet",
        },
        {
            "event": 5,
            "raw_occurrence": 1,
            "window": 3,
            "effect_in_sentry": "same issue, first occurrence in third fixed window",
            "issue_event_count": 5,
            "email_expected": "Rule 2 sends email 2",
        },
    ]

    payload = {
        "environment": args.environment,
        "marker": args.marker,
        "fixed_window_seconds": args.window_seconds,
        "max_initial_events": args.max_initial_events,
        "summary_threshold": args.summary_threshold,
        "rule2": {
            "condition": f"issue is seen more than {args.rule2_seen_more_than} times in {args.rule2_interval}",
            "frequency_minutes": args.rule2_frequency_minutes,
        },
        "notes": [
            "This assumes fixed-window throttling, not sliding-window throttling.",
            "Only event 1 creates the Sentry issue in the feed.",
            "Later events stay on the same issue and only increase issue event count.",
            "Verify Rule 2 against issue event count, not against new issue count.",
            "Expected Gmail pattern: one email after event 1, still one after event 2, two after event 5.",
        ],
        "checkpoints": checkpoints,
    }

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
