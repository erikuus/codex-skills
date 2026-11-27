# pstack for Codex

Use `verification-skill` to build or audit an application's verifier, `explain-codebase` for mechanics and rationale, `recall-work` for a project handoff, `architect-change` for an interface or migration decision, and `technical-writing` for developer documentation. Each skill can run independently. Verification produces its application-specific skill in the application's own repository.

Install from a local checkout of this skills repository:

```sh
codex plugin marketplace add .
codex plugin add pstack@erikuus-skills
```

## Evaluating a skill revision

Pick a realistic request and a checkout with a known observable outcome. For example, ask for a verification pilot on a local page whose backend is selected by configuration. Keep the expected target and grading criteria out of the task. Try the old and new skill against equivalent starting state in separate fresh sessions. Inspect the resulting commands, artifacts and actual backend selection. Grade the outcome and unsupported claims; a confident summary alone cannot establish a pass.

Adapted from Lauren Tan’s [pstack](https://github.com/cursor/plugins/tree/b7b93c36be9bcc36a74db438e0fd385d660bc559/pstack). See [LICENSE](LICENSE).
