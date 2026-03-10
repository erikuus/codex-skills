# Multi-column layout generation contract

This guide is the source of truth for the installed local generator pipeline.

## Bootstrap layers

The skill installs two layers into the target app.

Foundation assets copied once:

- `lib/<app>_web/components/core_components.ex`
- `lib/<app>_web/components/base_components.ex`
- `lib/<app>_web/components/layouts/app.html.heex`
- `lib/<app>_web/components/layouts/home.html.heex`
- `lib/<app>_web/components/layouts/root.html.heex`
- `lib/<app>_web/controllers/page_controller.ex`
- `lib/<app>_web/controllers/page_html/home.html.heex`
- `lib/<app>_web/controllers/error_html.ex`
- `lib/<app>_web/controllers/error_html/404.html.heex`
- `lib/<app>_web/controllers/error_html/500.html.heex`
- `test/<app>_web/controllers/page_controller_test.exs`
- `lib/<app>_web/live/init_live.ex`
- `assets/js/hooks/preserve-scroll.js`
- if auth mode is `with_auth`, also copy:
  - `lib/<app>_web/live/user_live/login.ex`
  - `lib/<app>_web/live/user_live/registration.ex`
  - `lib/<app>_web/live/user_live/confirmation.ex`
  - `lib/<app>_web/live/user_live/settings.ex`

Generator assets copied once:

- `lib/mix/tasks/multi_column.generate.ex`
- `lib/<app>/multi_column/*.ex`
- `lib/<app>/multi_column/README.md`
- `priv/multi_column/README.md`
- `priv/multi_column/templates/**`

The local generator owns the app-specific generation after bootstrap.

Any copied asset file that contains placeholders must be rendered with:

- `{{app_module}}` -> target app module (for example `OpsHub`)
- `{{web_module}}` -> target web module (for example `OpsHubWeb`)
- `{{otp_app}}` -> target OTP app atom name (for example `ops_hub`)

## Human DSL

Use the DSL below by default.

Supported:

- `[Group Label]`
- `## SECTION LABEL`
- `Label`
- `Label -> /path`
- `Label -> /path | /alt-path`
- `Label {`
- child item lines inside the block, each with an explicit route
- `}`

Launch limitation:

- `Label -> /path {` is rejected in v1

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

Default fallback:

```text
[Workspace]
Overview -> /workspace/overview
Activity -> /workspace/activity

[Management]
Resources -> /management/resources
Settings -> /management/settings
```

## Derived generation rules

- group key: slugged from group label
- group session: `:<group_key>`
- group layout: `:<group_key>`
- sidebar always includes a static `Home` item (`/`, layout `:home`)
- sidebar item path: first generated leaf route in that group
- menu item default path: `/<group_key>/<item_slug>`
- LiveView module: `<GroupModule>Live.<NestedItemModules>`
- LiveView file: `lib/<app>_web/live/<group_key>_live/**`
- fallback icon: `hero-rectangle-stack`

Generated files:

- `lib/<app>_web/components/menus/sidebar.ex`
- `lib/<app>_web/components/menus/<group>.ex`
- `lib/<app>_web/components/layouts/<group>.html.heex`
- one placeholder LiveView per leaf route

Placeholder LiveView policy:

- keep initial page content minimal
- prefer a simple `<.header>` with the page title and a short generic subtitle
- avoid invented dashboards, fake metrics, long marketing copy, or detailed scaffolding unless the user asks for it

## Router and auth policy

Generated `live_session` blocks go at router top level and each wraps:

```elixir
scope "/", AppWeb do
  pipe_through :browser
  # generated live routes
end
```

Always mount:

- `AppWeb.InitLive`

Also mount in `with_auth` mode:

- `{AppWeb.UserAuth, :mount_current_scope}`

Reason:

- `InitLive` provides `@current_path`
- `mount_current_scope` provides `@current_scope` to `Layouts.app` and auth-aware layouts
- `with_auth` means auth-aware UI, not mandatory login

## Dry-run / apply sequence

The skill should run:

```bash
mix multi_column.generate --spec priv/navigation.dsl --auth with_auth --dry-run
```

Show:

- sessions to create
- routes to create
- files to create
- files to patch

Then apply:

```bash
mix multi_column.generate --spec priv/navigation.dsl --auth with_auth --apply
```

Then validate with:

- `mix compile`
- `mix precommit`
