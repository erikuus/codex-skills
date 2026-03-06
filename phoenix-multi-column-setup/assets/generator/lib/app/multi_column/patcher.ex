defmodule {{app_module}}.MultiColumn.Patcher do
  @moduledoc false

  @router_start "# multi-column:generated:start"
  @router_end "# multi-column:generated:end"
  @app_js_import_start "// multi-column:generated-imports:start"
  @app_js_import_end "// multi-column:generated-imports:end"
  @app_js_hook_start "  // multi-column:generated-hooks:start"
  @app_js_hook_end "  // multi-column:generated-hooks:end"
  @web_import_start "      # multi-column:generated-imports:start"
  @web_import_end "      # multi-column:generated-imports:end"

  def patch_router!(contents, generated_block) do
    managed_block = """
      #{@router_start}
    #{generated_block}
      #{@router_end}
    """

    marker = first_router_marker(contents)

    cond do
      String.contains?(contents, @router_start) && String.contains?(contents, @router_end) ->
        replace_between(contents, @router_start, @router_end, managed_block)

      marker ->
        String.replace(contents, marker, managed_block <> "\n\n" <> marker, global: false)

      true ->
        Mix.raise("router.ex has no supported insertion point for multi-column live_sessions")
    end
  end

  def patch_app_js!(contents) do
    contents
    |> ensure_js_imports!()
    |> ensure_js_hooks!()
  end

  def patch_web_module!(contents, web_module) do
    managed_block = """
#{@web_import_start}
      import #{web_module}.BaseComponents
#{@web_import_end}
"""

    cond do
      String.contains?(contents, @web_import_start) && String.contains?(contents, @web_import_end) ->
        replace_between(contents, @web_import_start, @web_import_end, managed_block)

      String.contains?(contents, "import #{web_module}.BaseComponents") ->
        contents

      String.contains?(contents, "import #{web_module}.CoreComponents") ->
        String.replace(
          contents,
          "      import #{web_module}.CoreComponents",
          "      import #{web_module}.CoreComponents\n" <> managed_block,
          global: false
        )

      true ->
        Mix.raise("#{web_module |> Macro.underscore()}.ex does not contain a recognizable html_helpers import block")
    end
  end

  defp ensure_js_imports!(contents) do
    managed_block = """
#{@app_js_import_start}
import PreserveScroll from "./hooks/preserve-scroll";
#{@app_js_import_end}
"""

    cond do
      String.contains?(contents, @app_js_import_start) && String.contains?(contents, @app_js_import_end) ->
        replace_between(contents, @app_js_import_start, @app_js_import_end, managed_block)

      String.contains?(contents, ~s(import PreserveScroll from "./hooks/preserve-scroll";)) ->
        contents

      String.contains?(contents, "import topbar from \"../vendor/topbar\";") ->
        String.replace(
          contents,
          "import topbar from \"../vendor/topbar\";",
          "import topbar from \"../vendor/topbar\";\n\n" <> managed_block,
          global: false
        )

      true ->
        Mix.raise("assets/js/app.js has no supported hook import insertion point")
    end
  end

  defp ensure_js_hooks!(contents) do
    managed_block = """
#{@app_js_hook_start}
  PreserveScroll: PreserveScroll,
#{@app_js_hook_end}
"""

    cond do
      String.contains?(contents, @app_js_hook_start) && String.contains?(contents, @app_js_hook_end) ->
        replace_between(contents, @app_js_hook_start, @app_js_hook_end, managed_block)

      String.contains?(contents, "PreserveScroll: PreserveScroll") ->
        contents

      String.contains?(contents, "let Hooks = {") ->
        String.replace(contents, "let Hooks = {\n", "let Hooks = {\n" <> managed_block, global: false)

      String.contains?(contents, "const Hooks = {") ->
        String.replace(
          contents,
          "const Hooks = {\n",
          "const Hooks = {\n" <> managed_block,
          global: false
        )

      true ->
        Mix.raise("assets/js/app.js has no supported Hooks registry")
    end
  end

  defp replace_between(contents, start_marker, end_marker, replacement) do
    [before, after_start] = String.split(contents, start_marker, parts: 2)
    [_existing, after_] = String.split(after_start, end_marker, parts: 2)
    before <> replacement <> after_
  end

  defp first_router_marker(contents) do
    Enum.find(
      [
        "  ## Authentication routes",
        "  # Enable LiveDashboard and Swoosh mailbox preview in development",
        "  if Application.compile_env("
      ],
      &String.contains?(contents, &1)
    )
  end
end
