defmodule Mix.Tasks.MultiColumn.Generate do
  use Mix.Task

  @shortdoc "Generates a multi-column navigation shell from a DSL spec"

  @moduledoc """
  Usage:

      mix multi_column.generate --spec priv/navigation.dsl --auth with_auth --dry-run
      mix multi_column.generate --spec priv/navigation.dsl --auth with_auth --apply
  """

  @switches [
    spec: :string,
    auth: :string,
    dry_run: :boolean,
    apply: :boolean
  ]

  @impl Mix.Task
  def run(args) do
    Mix.Task.run("app.start")

    {opts, _argv, invalid} = OptionParser.parse(args, strict: @switches)

    if invalid != [] do
      Mix.raise("unsupported arguments: #{inspect(invalid)}")
    end

    spec_path =
      case opts[:spec] do
        nil -> Mix.raise("--spec is required")
        path -> path
      end

    auth_mode =
      case opts[:auth] do
        "with_auth" -> :with_auth
        "without_auth" -> :without_auth
        nil -> Mix.raise("--auth is required and must be with_auth or without_auth")
        other -> Mix.raise("--auth must be with_auth or without_auth, got: #{other}")
      end

    mode =
      cond do
        opts[:dry_run] && opts[:apply] -> Mix.raise("choose either --dry-run or --apply")
        opts[:apply] -> :apply
        true -> :dry_run
      end

    {{app_module}}.MultiColumn.Generator.run!(
      spec_path: spec_path,
      auth_mode: auth_mode,
      mode: mode
    )
  end
end
