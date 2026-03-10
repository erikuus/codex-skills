---
name: phoenix-multi-column-setup
description: Create and bootstrap Phoenix LiveView apps with a multi-column layout pattern. Automatically sets up the app, installs shared layout assets, bootstraps a local `mix multi_column.generate` pipeline, and generates auth-aware or no-auth navigation shells from a DSL spec.
---

# Phoenix Multi Column Setup

Use this skill when the user wants to create a new Phoenix LiveView app, or retrofit an existing one, with:

- narrow sidebar + vertical menu multi-column layout
- `InitLive` + `PreserveScroll`
- group-based `live_session` routing
- auth-aware or no-auth layout mode
- a local `mix multi_column.generate` command driven by a navigation DSL

## Default behavior

- Treat `mix compile` and `mix precommit` as part of the skill. Do not ask the user whether to run them.
- Default to the human DSL spec format.
- Always show the generator dry-run plan before writing generated files, unless the user explicitly asks to skip the preview.
- Keep the generator honest: managed blocks plus fail-on-conflict, not best-effort router surgery.

## Inputs to collect

Before changing files, determine:

- app name
- whether this is a fresh app in an empty folder or an existing app
- auth mode: `with_auth` or `without_auth`
- navigation DSL

If the user does not provide a DSL, use the default fallback spec from `references/multi-column-layout.md`.

## Fresh app workflow

When the user starts from an empty folder:

1. Follow `references/setup-phx-project.md`.
2. Create the Phoenix app.
3. Run `mix setup`.
4. Run `mix assets.build`.
5. If auth was requested and auth is not already present, run `mix phx.gen.auth Accounts User users`, then `mix ecto.migrate`.
6. Remove DaisyUI only if it is present. Follow `references/remove-daisyui.md`.
7. Install shared foundation assets:
   - `assets/components/core_components.ex`
   - `assets/components/base_components.ex`
   - `assets/components/layouts/app.html.heex`
   - `assets/components/layouts/home.html.heex`
   - `assets/components/layouts/root.html.heex`
   - `assets/controllers/page_controller.ex`
   - `assets/controllers/page_html/home.html.heex`
   - `assets/controllers/error_html.ex`
   - `assets/controllers/error_html/404.html.heex`
   - `assets/controllers/error_html/500.html.heex`
   - `assets/test/page_controller_test.exs`
   - `assets/live/init_live.ex`
   - `assets/js/hooks/preserve-scroll.js`
   - If auth mode is `with_auth`, also install auth LiveView style overrides:
     - `assets/live/user_live/login.ex`
     - `assets/live/user_live/registration.ex`
     - `assets/live/user_live/confirmation.ex`
     - `assets/live/user_live/settings.ex`
8. Install the local generator pipeline into the target app:
   - copy `assets/generator/lib/mix/tasks/multi_column.generate.ex` to `lib/mix/tasks/multi_column.generate.ex`
   - copy rendered `assets/generator/lib/app/multi_column/*.ex` to `lib/<app>/multi_column/*.ex`
   - copy `assets/generator/lib/app/multi_column/README.md` to `lib/<app>/multi_column/README.md`
   - copy `assets/generator/priv/multi_column/README.md` to `priv/multi_column/README.md`
   - copy rendered `assets/generator/priv/multi_column/templates/**` to `priv/multi_column/templates/**`
9. Render every copied `.ex`, `.exs`, `.heex`, or `.eex` asset that contains placeholders:
   - replace `{{app_module}}` with the target app module, for example `OpsHub`
   - replace `{{web_module}}` with the target web module, for example `OpsHubWeb`
   - replace `{{otp_app}}` with the target OTP app atom name, for example `ops_hub`
10. Ensure `lib/<app>_web.ex` imports `BaseComponents`.
11. Run the generator dry-run:
   - `mix multi_column.generate --spec priv/navigation.dsl --auth <mode> --dry-run`
12. Show the plan.
13. If the task is to build the app, run:
   - `mix multi_column.generate --spec priv/navigation.dsl --auth <mode> --apply`
14. Run `mix compile`.
15. Run `mix precommit`.

## Existing app workflow

When the target app already exists:

1. Inspect the app first:
   - `router.ex`
   - `assets/js/app.js`
   - `lib/<app>_web.ex`
   - auth presence (`user_auth.ex`, auth routes, `mount_current_scope`)
2. Install the shared foundation assets only if missing or stale.
   - If auth mode is `with_auth`, also install or refresh `assets/live/user_live/*.ex` overrides so auth pages use the shared auth layout pattern.
3. Install the local generator pipeline if missing.
4. Run generator dry-run.
5. Review the plan and fail on conflicts instead of hand-waving them away.
6. Apply only after the plan is acceptable.
7. Run `mix compile`.
8. Run `mix precommit`.

## Generator contract

The installed local command is:

```bash
mix multi_column.generate --spec priv/navigation.dsl --auth with_auth --dry-run
mix multi_column.generate --spec priv/navigation.dsl --auth with_auth --apply
```

The generator is responsible for:

- parsing and validating the DSL
- deriving app and web modules from the target app
- generating sidebar, group menus, group layouts, and placeholder LiveViews
- ensuring generated sidebar includes a `Home` item pointing to `/` (layout `:home`)
- keeping initial generated page content intentionally minimal so placeholder pages do not invent detailed product copy or fake data
- patching `router.ex` with managed `live_session` blocks
- patching `assets/js/app.js` to register `PreserveScroll` once
- patching `lib/<app>_web.ex` to import `BaseComponents` once

The generator is not responsible for:

- creating the Phoenix app itself
- adding auth from scratch
- copying the shared foundation assets into the project for the first time

Those bootstrap steps stay in the skill workflow. The generator owns the fragile cross-file generation and patching after bootstrap.

## Router policy

Generated routes must go inside top-level `live_session` blocks that each wrap:

- `scope "/", AppWeb`
- `pipe_through :browser`

Reason:

- these are browser LiveViews
- `InitLive` needs to mount for `@current_path`
- in `with_auth` mode, layouts need `@current_scope`

For `with_auth`, mount:

- `AppWeb.InitLive`
- `{AppWeb.UserAuth, :mount_current_scope}`

Do not put generated sections under `:require_authenticated_user` unless the user explicitly asks for protected-only navigation. `with_auth` means auth-aware UI and `current_scope`, not mandatory login.

## DSL notes

Use the human DSL from `references/multi-column-layout.md`.

Supported in this launch version:

- `[Group]`
- `## SECTION`
- `Label`
- `Label -> /path`
- `Label -> /path | /alias`
- `Label { ... }`

Current limitation:

- expandable parents with their own route (`Label -> /path {`) are not supported in this launch version; fail clearly if encountered

## Prompt shape

Good prompts look like:

```text
Create a new Phoenix LiveView app named ops_hub in this empty folder with a multi-column layout and authentication.
Use the following navigation schema:

[Workspace]
Overview -> /workspace/overview
Activity -> /workspace/activity

[Management]
## OPERATIONS
Resources -> /management/resources
Settings -> /management/settings
Guides {
  Getting Started -> /management/guides/getting-started
  Best Practices -> /management/guides/best-practices
}
```

or:

```text
Create a new Phoenix LiveView app named docs_portal in this empty folder with a multi-column layout and no authentication.
Use the following navigation schema:

[Workspace]
Overview -> /workspace/overview
Updates -> /workspace/updates

[Guides]
Getting Started -> /guides/getting-started
Reference -> /guides/reference
```

## Resources

- `references/setup-phx-project.md`: fresh-app bootstrap order
- `references/remove-daisyui.md`: DaisyUI cleanup
- `references/multi-column-layout.md`: DSL and generated file contract
- `assets/`: shared components, layouts, JS hook, and generator payload
