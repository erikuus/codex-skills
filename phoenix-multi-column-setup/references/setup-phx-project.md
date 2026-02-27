# Phoenix app setup workflow

Use the following steps after creating or cloning a Phoenix LiveView app.

0. Run the project setup alias first:
   - Run `mix setup`.
   - If the project has no `setup` alias, run steps 1-3 instead.

1. Fetch and compile dependencies:
   - `mix deps.get`
   - `mix compile`

2. Set up the database:
   - `mix ecto.setup`

3. Install/setup frontend tooling and build assets:
   - Run:
     - `mix assets.setup`
     - `mix assets.build`
   - If you successfully ran `mix setup`, still run `mix assets.build` once to ensure fresh built assets.

4. Generate authentication only when requested in prompt:
   - If prompt says app should include authentication, ensure auth is present.
   - If auth is missing, run:
     - `mix phx.gen.auth Accounts User users`
     - `mix ecto.migrate`
   - If auth already exists (for example `user_auth.ex`, auth routes, and `mount_current_scope` are already present), skip generation.
   - For multi-column setup, later mount both `InitLive` and `{YourAppWeb.UserAuth, :mount_current_scope}` in relevant `live_session` blocks.

5. Launch the Phoenix server in the background:
   - `mix phx.server`
   - If port 4000 is in use, retry with `PORT=4001 mix phx.server`
   - If 4001 is in use, increment (`PORT=4002`, `PORT=4003`, ...)

6. Verify the server:
   - Wait for the chosen port, request `http://localhost:<port>`
   - If HTTP 200/30x, report success and URL
   - If it fails, show last server logs and common hints (ex: ensure Postgres is running)

Notes:

- Assume a fresh clone; only skip when the conditional says so.
- Note compilation warnings but do not treat them as errors unless server fails.
