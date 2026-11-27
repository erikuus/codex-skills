---
name: explain-codebase
description: Explain how a subsystem works, where its state belongs, or why it was designed that way. Use for code walkthroughs, historical rationale, and teaching a maintainer about a specific change.
---

# Explain a codebase

Scope the investigation to the question. A runtime question needs a traced execution path. A rationale question needs a decision record. For a teaching request, combine the two where both help the reader.

**How it works.** Pick a concrete user action or caller. Follow the actual route, event or command through dispatch, state ownership, side effects and the read that exposes the result. Resolve dynamic wiring from config and registration. Inspect one test that exercises the path and identify any fake or bypass that matters to the explanation. Cite navigable source locations. If code supports several paths, say which condition selects the one you traced.

**Why it exists.** Start with the first relevant change and inspect later revisions that altered the decision. Use focused history searches such as `git log -S`, `git log -G`, rename history and the surrounding diff. Follow an issue, review, measurement or design note when it actually bears on intent. Attribute recorded reasons to their source. Label a plausible reconstruction as inference and identify what the record leaves open.

**Teach it.** Start with the user's example and the smallest complete answer. Show what happens at the handoff most likely to surprise a maintainer. A short diagram can help when several owners share a path. End at the file, test, or decision someone would open to continue. Preserve uncertainty when simplifying. Keep an explanation request read-only.
