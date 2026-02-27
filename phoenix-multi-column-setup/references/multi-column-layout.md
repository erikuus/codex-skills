# Multi-column layout implementation guide

This guide defines a reliable implementation order for the multi-column architecture:

- Narrow sidebar (level 1 navigation)
- Vertical menu (level 2 navigation)
- Main content area (LiveView pages)
- Persistent desktop menu scroll (`PreserveScroll`)
- Active menu state from `@current_path` (`InitLive`)

## 1) Fixed generic parts (copy as-is in every app)

These pieces are generic but `.ex` templates require module placeholder rendering before copy:

- Render every copied `.ex` asset by replacing `{{web_module}}` with the target app web module (example: `LivePlaygroundWeb`).
- `assets/live/init_live.ex` -> `lib/<app>_web/live/init_live.ex`
- `assets/js/hooks/preserve-scroll.js` -> `assets/js/hooks/preserve-scroll.js`

### `InitLive` contract

`InitLive` is generic. It attaches a `:handle_params` hook and assigns `current_path` from URL path.

Once mounted in a `live_session`, all LiveViews in that session can use `@current_path` in layouts/menu components.

### `PreserveScroll` contract

1. Place hook file under `assets/js/hooks/`.
2. Register it in `assets/js/app.js` and pass via `LiveSocket` hooks.
3. Use it on `:desktop_menu` slot in every `.multi_column_layout` usage.

## 2) App-specific parts (must be generated per app)

Use app-domain naming for groups and modules.

### 2.1 Navigation Spec (input gate)

At project start, the app usually has no domain navigation yet. Do not guess it.

Ask user to choose one of:

- provide a custom Navigation Spec (human-friendly DSL), or
- use the built-in default Navigation Spec

#### Primary format (human-friendly DSL)

Use this as the default input mode. It is easier to write than YAML.

Rules:

- Auth mode is derived from prompt intent (`with authentication` or `without authentication`).
- If auth mode is unclear, ask one clarification question before parsing DSL.
- Sidebar group: `[Group Label]`
- Section in group menu: `## SECTION LABEL`
- Menu item: `Label`
- Menu item with path override: `Label -> /path`
- Menu item with active aliases: `Label -> /path | /alt-path`
- Expandable block:
  - `Label {` or `Label -> /path {`
  - child items on separate indented lines, each with explicit route
  - `}`

Example:

```text
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

Notes:

- AI auto-selects a fitting Heroicon from label text (user can adjust later in code).
- If path is omitted, AI derives it from label (slug path).
- If aliases are omitted, active matching uses the primary path only.
- Auth mode is not part of DSL text; it comes from prompt intent or one clarification answer.

#### Optional format (advanced YAML)

Use only if user prefers explicit machine-readable input.

```yaml
auth_mode: with_auth
groups:
  - key: workspace
    label: Workspace
    icon: hero-squares-2x2
    menu_items:
      - key: overview
        label: Overview
        path: /workspace/overview
        liveview: WorkspaceLive.Overview
      - key: activity
        label: Activity
        path: /workspace/activity
        liveview: WorkspaceLive.Activity

  - key: management
    label: Management
    icon: hero-briefcase
    menu_items:
      - key: resources
        label: Resources
        path: /management/resources
        liveview: ManagementLive.Resources
        section: Operations
      - key: settings
        label: Settings
        path: /management/settings
        liveview: ManagementLive.Settings
      - key: guides
        label: Guides
        path: /management/guides
        liveview: ManagementLive.Guides
        expandable_items:
          - key: getting_started
            label: Getting Started
            path: /management/guides/getting-started
            liveview: ManagementLive.Guides.GettingStarted
          - key: best_practices
            label: Best Practices
            path: /management/guides/best-practices
            liveview: ManagementLive.Guides.BestPractices
```

Default fallback spec (if user omits custom spec):

```yaml
auth_mode: without_auth
groups:
  - key: workspace
    label: Workspace
    icon: hero-squares-2x2
    menu_items:
      - key: overview
        label: Overview
        path: /workspace/overview
        liveview: WorkspaceLive.Overview
      - key: activity
        label: Activity
        path: /workspace/activity
        liveview: WorkspaceLive.Activity

  - key: management
    label: Management
    icon: hero-briefcase
    menu_items:
      - key: resources
        label: Resources
        path: /management/resources
        liveview: ManagementLive.Resources
      - key: settings
        label: Settings
        path: /management/settings
        liveview: ManagementLive.Settings
```

Define:

- Level 1 (sidebar groups): atoms like `:clients`, `:orders`, `:products`
- Level 2 (menu items): routes/LiveViews under each sidebar group

Generate per app:

- `lib/<app>_web/components/menus/sidebar.ex` (icons + top-level active state via `current_layout`)
- `lib/<app>_web/components/menus/<group>.ex` for each group (uses `current_path`)
- `lib/<app>_web/components/layouts/<group>.html.heex` for each group layout
- LiveView module for each menu item route (minimum viable page with header)

Use these assets only as templates (render `{{web_module}}` first for `.ex` files):

- Sidebar:
  - `assets/components/menus/sidebar_with_auth.ex`
  - `assets/components/menus/sidebar_without_auth.ex`
- Menus:
  - `assets/components/menus/group_with_auth.ex`
  - `assets/components/menus/group_without_auth.ex`
- Layouts:
  - `assets/components/layouts/app.html.heex`
  - `assets/components/layouts/group_with_auth.html.heex`
  - `assets/components/layouts/group_without_auth.html.heex`

Template selection rule:

- If the app uses authenticated routes (`current_scope`, user auth mounts), start from all `*_with_auth` templates (sidebar, group menu, group layout).
- If the app has no authentication, start from all `*_without_auth` templates (sidebar, group menu, group layout).

### 2.2 Mapping rules from spec to generated files

Mapping from human DSL:

- `[Group Label]` -> group key (slug), sidebar item, `live_session :<group_key>`, layout `<group_key>`, menu module `<group_key>.ex`
- `## SECTION LABEL` -> section block for vertical navigation
- `Label` -> simple menu item (icon auto-picked, path auto-derived)
- `Label -> /path | /alt-path` -> menu item with explicit path and active aliases
- `Label { ... }` -> expandable block with generated stable `id` from label and child items as `expandable_items`

- Group `key` maps to:
  - `live_session :<key>`
  - layout name `<key>` (for `layout: {YourAppWeb.Layouts, :<key>}`)
  - `current_layout` atom `:<key>` in sidebar calls
  - menu module file `lib/<app>_web/components/menus/<key>.ex`
  - layout template file `lib/<app>_web/components/layouts/<key>.html.heex`
- Menu item maps to:
  - one LiveView route in router
  - one destination LiveView module
  - one navigation item in `<key>.ex` menu module

AI defaults:

- Icon defaults: choose best-match Heroicon by keywords from label text; fallback `hero-rectangle-stack`.
- Path defaults: `/<group_key>/<item_slug>` unless overridden.
- LiveView defaults: `<GroupModule>Live.<ItemModule>` from group/item labels.
- Expandable id defaults: slug from expandable label.

Before writing files, show these inferred values and require explicit user confirmation.

## 3) Router wiring pattern

Mount `InitLive` in each relevant `live_session`.
Session name depends on your top-level group and should not be assumed.

```elixir
live_session :orders,
  layout: {YourAppWeb.Layouts, :orders},
  on_mount: [
    YourAppWeb.InitLive,
    {YourAppWeb.UserAuth, :mount_current_scope}
  ] do
  scope "/", YourAppWeb do
    pipe_through :browser
    # live routes for orders menu items...
  end
end
```

Repeat for other groups (`:clients`, `:products`, etc.) as needed.

Before writing router/layout/menu files, show a derived plan and require explicit user confirmation.

## 4) Layout wiring pattern (`.multi_column_layout`)

Use `Layouts.app` as the outer contract and render the multi-column shell inside it:

```heex
<Layouts.app
  flash={@flash}
  current_scope={@current_scope}
  show_auth_menu={true}
  auth_menu_class="hidden lg:flex justify-end px-6 lg:px-8 py-4"
>
  <.multi_column_layout>
    <:narrow_sidebar>
      <Sidebar.menu current_layout={:orders} current_scope={@current_scope} />
    </:narrow_sidebar>
    <:mobile_menu>
      <Orders.menu id="orders-mobile-menu" current_path={@current_path} />
    </:mobile_menu>
    <:desktop_menu hook="PreserveScroll">
      <Orders.menu id="orders-desktop-menu" current_path={@current_path} />
    </:desktop_menu>
    {@inner_content}
  </.multi_column_layout>
</Layouts.app>
```

Notes:

- `current_layout` drives active state in sidebar icons.
- `current_path` drives active state in vertical navigation menu.
- `PreserveScroll` belongs on `:desktop_menu`.
- Ensure pages begin with `<Layouts.app ...>` and keep `<.flash_group ...>` in `app.html.heex` only.
- `show_auth_menu` defaults to `false`; set it to `true` in layouts that should render the guest auth header.

If using no-auth templates, use `<Layouts.app flash={@flash}>` and omit auth-specific assigns/components.
For no-auth layouts, omit `show_auth_menu` unless explicitly needed.

For no-auth sidebars, omit `current_scope` in `<Sidebar.menu ...>`.

## 5) Minimum page scaffolding rule

For every level-2 menu item, create a destination LiveView so navigation is valid.

Minimum render requirement per page:

- A root container
- A `<.header>` title reflecting that page

This guarantees the generated navigation is testable and non-broken immediately after setup.

## 6) Implementation checklist

- Validate Navigation Spec before generation:
  - user chose custom spec or default spec
  - DSL/YAML parsed successfully
  - group keys unique
  - menu item keys unique within group
  - route paths unique globally
  - each menu item has a LiveView target
- Copy `InitLive` and `PreserveScroll` first (fixed parts).
- Register `PreserveScroll` in `assets/js/app.js`.
- Define sidebar groups and menu items from the approved selected spec (custom or default).
- Pick template mode from global `auth_mode` (`with_auth` or `without_auth`).
- Create sidebar/menu/layout modules for each top-level group.
- Install `app.html.heex` layout contract from skill assets before wiring group layouts.
- Mount `InitLive` in every matching `live_session`.
- Pass `current_scope`, `current_layout`, and `current_path` through layouts/menus.
- Keep `<.flash_group ...>` usage only in `app.html.heex`; group layouts should call `<Layouts.app ...>` and never call `<.flash_group>` directly.
- Ensure every menu item points to an existing LiveView.
- Show generated routes/sessions/files summary and get explicit user confirmation before file writes.
