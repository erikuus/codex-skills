# Pinned autoreview dependency

Use the complete upstream `autoreview` skill as the review engine for `review-to-pr`.

- Source: `https://github.com/openclaw/agent-skills`
- Upstream path: `skills/autoreview`
- Pinned commit: `fe588b1a6267eb47f785d0c748db9f6f3e9a3b4f`
- Installed sibling: `/Users/erikuus/.agents/skills/autoreview`
- `SKILL.md` SHA-256: `ebc732cd3df231ec5a29fafb798ef27a9178ca3fbc1070ab32684df2c2299f41`
- `scripts/autoreview` SHA-256: `14945b1b44104bf7e05cf4b9e6b50d5d064228927a3b3bf5aa73de89ad1d4de8`

Do not patch the installed copy. To update it, select a new reviewed upstream commit, replace the entire `skills/autoreview` directory, update this provenance record and hashes, run the upstream smoke/self-tests, and validate `review-to-pr` again. Do not point the dependency at a moving `main` checkout.
