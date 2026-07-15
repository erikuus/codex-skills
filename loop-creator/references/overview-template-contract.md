# Overview Template Contract

Use `assets/overview.html.template` as the source for every generated loop overview. Copy it to project-root `overview.template.html`, adapt only loop-specific nouns or optional detail rendering, and have the deterministic CLI render project-root `overview.html` from it.

## Replacement contract

The template contains exactly two replacement tokens:

- `__LOOP_TITLE__`: replace every occurrence with the HTML-escaped loop name.
- `__OVERVIEW_DATA_JSON__`: replace its single occurrence with compact JSON encoded with `ensure_ascii=False` and `sort_keys=True`, then replace every `</` with `<\/` so candidate text cannot close the JSON script element.

Assert after rendering that neither token remains. Write the final page atomically.

Python standard-library pattern:

```python
import html
import json

template = overview_template_path.read_text(encoding="utf-8")
payload = json.dumps(data, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
rendered = template.replace("__LOOP_TITLE__", html.escape(loop_name)).replace(
    "__OVERVIEW_DATA_JSON__", payload
)
if "__LOOP_TITLE__" in rendered or "__OVERVIEW_DATA_JSON__" in rendered:
    raise RuntimeError("overview template token replacement failed")
```

## Payload schema

Emit this normalized shape. Extra fields are allowed; missing optional fields must not break the page.

```json
{
  "schema_version": 1,
  "loop_name": "Example Loop",
  "candidate_noun": "candidate",
  "generated_at": "2026-07-15T12:00:00+00:00",
  "input_hash": "full sha256",
  "criteria_hash": "full sha256",
  "selection_mode": "single-winner",
  "winner_id": "cand-abc123",
  "shortlist_ids": [],
  "counts": {
    "pending": 1,
    "evaluated": 4,
    "invalid": 1,
    "stale": 1
  },
  "candidates": [
    {
      "candidate_id": "cand-abc123",
      "title": "Candidate title or concise excerpt",
      "status": "evaluated",
      "submitted_at": "2026-07-15T11:30:00+00:00",
      "score": 84,
      "verdict": "promote",
      "is_winner": true,
      "in_shortlist": false,
      "dimension_scores": {"clarity": 90, "novelty": 78},
      "rationale_excerpt": "Why the evaluator scored it this way.",
      "content": "# Candidate\n\nMarkdown body",
      "candidate_path": "candidates/archive/cand-abc123.md",
      "evaluation_path": "evaluations/cand-abc123.json",
      "stale_reason": null,
      "evaluation": {}
    }
  ],
  "recent_activity": [
    {
      "at": "2026-07-15T11:31:00+00:00",
      "label": "Evaluation recorded",
      "detail": "cand-abc123 scored 84"
    }
  ]
}
```

Allowed candidate statuses are `pending`, `submitted`, `evaluated`, `invalid`, and `stale`. Normalize internal state names to these display values. Set `score` to an integer on the loop's declared scale or `null`; the template defaults the visible scale maximum to `100`. If another maximum is required, emit `score_max` at the top level.

For a single-winner loop, emit `winner_id` and set the matching candidate's `is_winner`. For a shortlist loop, emit ordered `shortlist_ids` and set `in_shortlist` on each matching candidate. Keep both forms consistent so the page can explain current selection without deriving state from scores.

## Required behavior

Preserve these template behaviors:

- initialize selection to the winner, then the first shortlist member, then the newest candidate
- filter by title, ID, status, verdict, and rationale
- sort by newest or score, with deterministic ID tie-breaking
- select candidates without page navigation
- display score dimensions, prose, rationale, warnings, file paths, and raw evaluation detail
- show full input and criteria hashes plus counts in the loop metadata popover
- show recent activity in the metadata popover
- refresh from the current page every 30 seconds without changing scroll position or selection; ignore refresh failures
- collapse to a single-column list/reader layout below `800px`
- support empty candidate lists and empty search results

Keep the page dependency-free. Do not load fonts, scripts, stylesheets, or telemetry from the network.
Emit candidate and evaluation paths as absolute local paths, `file:` URLs, or relative paths. The template rejects other URL schemes.

## Minimum renderer tests

Test all of the following:

1. Both template tokens are replaced and absent from final HTML.
2. A loop title containing `<`, `>`, `&`, quotes, and apostrophes is HTML-escaped.
3. Candidate content containing `</script>` is encoded as `<\/script>` in the embedded JSON.
4. Winner or shortlist state, full hashes, pending/invalid/stale statuses, score, verdict, rationale, paths, and recent activity appear in the embedded payload.
5. Final HTML retains the `overview-data`, `search`, `sortControl`, `candidateList`, `detail`, and `loopInfo` elements.
6. An empty candidate list renders without a JavaScript error.
7. The page has the `max-width: 800px` responsive rule and no external resource references.
8. Candidate/evaluation links reject non-file URL schemes such as `javascript:`.
