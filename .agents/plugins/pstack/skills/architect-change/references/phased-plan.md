# Plan a migration

Use the existing project plan when it owns the work. State the target and compatibility period, then order the slices by dependency. Identify any steps that can safely land independently and any shared state that requires serialization.

For each slice name the owner or caller it changes, what remains usable at its boundary, how to exercise it, and the observable pass condition. Include backfill, retry, rollback or cutover details where the actual data and release process require them. Choose appropriate proof for each slice. Reserve performance budgets for claims involving performance.

Identify the first shippable slice and the evidence required to retire a legacy path. Follow the repository's release and review arrangements. Deliver a plan when the request is planning only.
