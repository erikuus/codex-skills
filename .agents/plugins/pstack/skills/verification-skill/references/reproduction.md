# Reproduce and retest

Pin the symptom to a user action, the affected target and a visible or measurable failure. Reuse the smallest existing journey that reaches it. Record the revision, fixture and failing observation before editing. If a reproduction changes the data, give the second run an equivalent initial state.

Follow the request from the first incorrect observation back to the component that produced it. Choose an observation that would distinguish plausible explanations: the submitted value, response, stored row or file, or state after a reload. A passing lower-level test narrows the search to the boundaries it actually covers.

After the requested fix, repeat the original action on the same target. Show the before/after observation and the relevant regression check. For an intermittent issue, report attempts and occurrences on both revisions. If the failure could not be reproduced, give the attempted conditions and remaining uncertainty. Keep investigation-only requests read-only.
