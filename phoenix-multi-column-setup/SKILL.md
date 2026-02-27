---
name: phoenix-multi-column-setup
description: Create and bootstrap Phoenix LiveView apps with multi-column layout pattern. Automatically sets up the project, removes Daisy UI, and implements the complete multi-column layout (narrow sidebar + vertical navigation + preserve-scroll hook) with current_layout/current_path assigns and InitLive routing.
---

# Phoenix Multi Column Setup

## Overview

This skill creates production-ready Phoenix LiveView apps with a professional multi-column layout pattern. It executes a complete workflow: sets up the Phoenix project, removes Daisy UI to avoid conflicts, installs shared components, and wires the multi-column layout with narrow sidebar, vertical navigation, and preserve-scroll functionality.

Use this skill when asked to create a multi-column LiveView app or set up a Phoenix app with multi-column layout.

## Step 0: Collect Navigation Spec (custom or default)

Before creating any multi-column files, ask user to choose:

- provide a custom Navigation Spec (human-friendly DSL), or
- use the built-in default Navigation Spec

If custom spec is selected, default to human-friendly DSL input (see `references/multi-column-layout.md`).

Optional advanced mode: accept YAML when user explicitly prefers machine-readable format.

Custom spec must define:

- authentication intent in prompt (`with authentication` or `without authentication`)
  - if missing, ask one clarification question before generation
- `groups`: list of level-1 sidebar groups
  - each group must include label/name and menu items (AI derives keys)
- `menu_items`: list of level-2 items per group
  - each item must include label
  - path, aliases, and section are optional

AI should auto-pick fitting Heroicons from labels and infer missing keys/paths/module names.
Users can adjust icons and naming later in generated code.

If user omits custom spec, use the default fallback spec from `references/multi-column-layout.md`.

Do not infer any other missing groups, routes, or page modules beyond the selected custom/default spec.

Before writing files, show the derived plan (sessions, routes, layouts, menus, and LiveViews) and require explicit user confirmation.

## Step 1: Set up Phoenix app

- Follow `references/setup-phx-project.md`.
- Add `.vscode/settings.json` with Tailwind v4 lint/association settings to silence false warnings.

```json
{
  "css.lint.unknownAtRules": "ignore",
  "scss.lint.unknownAtRules": "ignore",
  "less.lint.unknownAtRules": "ignore",
  "files.associations": {
    "app.css": "tailwindcss"
  }
}
```

## Step 2: Remove Daisy UI

- Follow `references/remove-daisyui.md`.
- Do not add alternative Tailwind plugins unless explicitly requested.

## Step 3: Install shared components

Copy/overwrite components (after template rendering):

- Resolve template placeholders in all copied `.ex` assets: replace `{{web_module}}` with the target web module (example: `LivePlaygroundWeb`).
- Overwrite `lib/<app>_web/components/core_components.ex` with rendered `assets/components/core_components.ex`.
- Copy rendered `assets/components/more_components.ex` to `lib/<app>_web/components/more_components.ex` and import it in `my_app_web.ex` so it is available to LiveViews, components, and templates.
- Overwrite `lib/<app>_web/components/layouts/app.html.heex` with `assets/components/layouts/app.html.heex` to centralize flash and optional auth-header rendering in `Layouts.app`.

Example `my_app_web.ex` import:

```elixir
def html_helpers do
  quote do
    use Phoenix.Component

    import Phoenix.HTML

    import MyAppWeb.CoreComponents
    import MyAppWeb.MoreComponents
    import MyAppWeb.Gettext

    alias Phoenix.LiveView.JS
  end
end
```

## Step 4: Implement multi-column layout

Follow `references/multi-column-layout.md` as the single source of truth for this step.

Execution summary:

- Install fixed generic parts first (`InitLive`, `PreserveScroll`).
- Resolve `{{web_module}}` placeholders in all copied/generated `.ex` files before writing them into the target app.
- Define app-specific 2-level navigation from the selected Navigation Spec (custom or default).
- Pick templates from global `auth_mode` (`with_auth` or `without_auth`), then generate sidebar/menu/layout modules with app-specific naming.
- Mount `InitLive` in each relevant `live_session` and keep auth/current_scope mounts.
- Use `Layouts.app` as the outer wrapper and `.multi_column_layout` for each group layout.
- Keep `<.flash_group ...>` usage inside `app.html.heex` only.
- Ensure every menu item route has a destination LiveView.
- Require explicit confirmation on the derived generation plan before file writes.

Do not duplicate or override detailed rules from the reference file in this step.

## Resources

### references/

- `setup-phx-project.md`: setup workflow for Phoenix apps
- `remove-daisyui.md`: Daisy UI removal steps
- `multi-column-layout.md`: wiring details, assigns, and file list

### assets/

- Reusable Phoenix components, layouts, and JS hook for the multi-column layout
