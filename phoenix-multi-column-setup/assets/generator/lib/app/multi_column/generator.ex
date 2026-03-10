defmodule {{app_module}}.MultiColumn.Generator do
  @moduledoc false

  alias {{app_module}}.MultiColumn.Parser
  alias {{app_module}}.MultiColumn.Patcher
  alias {{app_module}}.MultiColumn.Spec
  alias {{app_module}}.MultiColumn.Spec.Group
  alias {{app_module}}.MultiColumn.Spec.Item

  def run!(opts) do
    spec =
      opts
      |> build_spec!()
      |> validate_spec!()

    plan = build_plan(spec)

    print_plan(spec, plan)

    if opts[:mode] == :apply do
      apply_plan!(plan)
      Mix.shell().info("\nApplied multi-column generation plan.")
    end
  end

  defp build_spec!(opts) do
    otp_app = Mix.Project.config()[:app] |> to_string()
    app_module = otp_app |> Macro.camelize()
    web_module = app_module <> "Web"

    groups =
      opts[:spec_path]
      |> Parser.parse_file!()
      |> Enum.map(&derive_group(&1, otp_app, web_module))

    %Spec{
      otp_app: otp_app,
      app_module: app_module,
      web_module: web_module,
      auth_mode: opts[:auth_mode],
      spec_path: opts[:spec_path],
      groups: groups
    }
  end

  defp derive_group(raw_group, otp_app, web_module) do
    key = slug(raw_group.label, "_")
    menu_module = Macro.camelize(key)
    group_dir = Path.join(["lib", "#{otp_app}_web", "live", "#{key}_live"])

    %Group{
      key: key,
      label: raw_group.label,
      icon: pick_icon(raw_group.label, :group),
      layout_name: key,
      session_name: key,
      menu_module: menu_module,
      layout_file: Path.join(["lib", "#{otp_app}_web", "components", "layouts", "#{key}.html.heex"]),
      menu_file: Path.join(["lib", "#{otp_app}_web", "components", "menus", "#{key}.ex"]),
      live_dir: group_dir,
      items: derive_items(raw_group.items, key, web_module, otp_app, [])
    }
  end

  defp derive_items(items, group_key, web_module, otp_app, parent_labels) do
    Enum.map(items, fn item ->
      case item.kind do
        :expandable ->
          expandable_key = slug(item.label, "_")

          %Item{
            kind: :expandable,
            key: expandable_key,
            label: item.label,
            icon: pick_icon(item.label, :item),
            section: item.section,
            expandable_id: slug(Enum.join(parent_labels ++ [item.label], "-"), "-"),
            parent_labels: parent_labels,
            children:
              derive_items(
                item.children,
                group_key,
                web_module,
                otp_app,
                parent_labels ++ [item.label]
              )
          }

        :item ->
          item_key = slug(item.label, "_")
          path = item.path || default_path(group_key, item_key)
          aliases = Enum.uniq([path | item.aliases])
          module_segments = Enum.map(parent_labels ++ [item.label], &Macro.camelize(slug(&1, "_")))
          relative_module = Enum.join([Macro.camelize(group_key) <> "Live" | module_segments], ".")
          full_module = web_module <> "." <> relative_module

          live_file =
            Path.join(
              [
                "lib",
                "#{otp_app}_web",
                "live",
                "#{group_key}_live"
                | Enum.map(parent_labels, &slug(&1, "_"))
              ] ++ ["#{slug(item.label, "_")}.ex"]
            )

          %Item{
            kind: :item,
            key: item_key,
            label: item.label,
            icon: pick_icon(item.label, :item),
            path: path,
            aliases: aliases,
            section: item.section,
            relative_module: relative_module,
            full_module: full_module,
            live_file: live_file,
            dom_id: slug(Enum.join([group_key | parent_labels] ++ [item.label], "-"), "-"),
            parent_labels: parent_labels
          }
      end
    end)
  end

  defp validate_spec!(%Spec{groups: groups} = spec) do
    assert_unique!(Enum.map(groups, & &1.key), "group keys")
    assert_unique!(Enum.map(groups, & &1.label), "group labels")

    leaf_items = leaf_items(groups)

    assert_unique!(Enum.map(leaf_items, & &1.path), "route paths")
    assert_unique!(Enum.map(leaf_items, & &1.full_module), "LiveView modules")

    router_contents = File.read!(Path.join(["lib", "#{spec.otp_app}_web", "router.ex"]))
    router_without_managed = remove_managed_router_block(router_contents)

    Enum.each(leaf_items, fn item ->
      route_line = ~s(live "#{item.path}")

      if String.contains?(router_without_managed, route_line) do
        Mix.raise("router.ex already defines #{item.path} outside the managed multi-column block")
      end
    end)

    spec
  end

  defp remove_managed_router_block(contents) do
    case {String.contains?(contents, "# multi-column:generated:start"),
          String.contains?(contents, "# multi-column:generated:end")} do
      {true, true} ->
        String.replace(
          contents,
          ~r/\s*# multi-column:generated:start.*?# multi-column:generated:end/s,
          ""
        )

      _ ->
        contents
    end
  end

  defp build_plan(spec) do
    generated_files =
      spec
      |> generated_file_entries()
      |> Map.new()

    router_path = Path.join(["lib", "#{spec.otp_app}_web", "router.ex"])
    app_js_path = Path.join(["assets", "js", "app.js"])
    web_module_path = Path.join(["lib", "#{spec.otp_app}_web.ex"])

    router_contents =
      router_path
      |> File.read!()
      |> Patcher.patch_router!(render_router_block(spec))

    app_js_contents =
      app_js_path
      |> File.read!()
      |> Patcher.patch_app_js!()

    web_module_contents =
      web_module_path
      |> File.read!()
      |> Patcher.patch_web_module!(spec.web_module)

    %{
      creates: generated_files,
      patches: %{
        router_path => router_contents,
        app_js_path => app_js_contents,
        web_module_path => web_module_contents
      }
    }
  end

  defp generated_file_entries(spec) do
    sidebar_template =
      case spec.auth_mode do
        :with_auth -> template_path("components/menus/sidebar_with_auth.ex.eex")
        :without_auth -> template_path("components/menus/sidebar_without_auth.ex.eex")
      end

    [
      {Path.join(["lib", "#{spec.otp_app}_web", "components", "menus", "sidebar.ex"]),
       EEx.eval_file(
         sidebar_template,
         [
           sidebar_items_literal: render_sidebar_items(spec.groups)
         ],
         trim: true
       )}
    ] ++ Enum.flat_map(spec.groups, &group_file_entries(spec, &1))
  end

  defp group_file_entries(spec, group) do
    menu_template =
      case spec.auth_mode do
        :with_auth -> template_path("components/menus/group_with_auth.ex.eex")
        :without_auth -> template_path("components/menus/group_without_auth.ex.eex")
      end

    layout_template =
      case spec.auth_mode do
        :with_auth -> template_path("components/layouts/group_with_auth.html.heex.eex")
        :without_auth -> template_path("components/layouts/group_without_auth.html.heex.eex")
      end

    live_template = template_path("live/page_live.ex.eex")

    [
      {group.menu_file,
       EEx.eval_file(
         menu_template,
         [
           group_module: group.menu_module,
           items_literal: render_group_items(group.items)
         ],
         trim: true
       )},
      {group.layout_file,
       EEx.eval_file(
         layout_template,
         [
           group_module: group.menu_module,
           group_key: group.key
         ],
         trim: true
       )}
    ] ++ Enum.map(leaf_items([group]), fn item ->
          breadcrumb =
            (item.parent_labels ++ [item.label])
            |> Enum.join(" / ")

          {item.live_file,
           EEx.eval_file(
             live_template,
             [
               live_module: item.relative_module,
               page_title: item.label,
               breadcrumb: breadcrumb,
               dom_id: item.dom_id,
               route_path: item.path
             ],
             trim: true
           )}
        end)
  end

  defp render_router_block(spec) do
    spec.groups
    |> Enum.map(&render_group_session(spec, &1))
    |> Enum.join("\n\n")
  end

  defp render_group_session(spec, group) do
    on_mount_lines =
      [
        "      #{spec.web_module}.InitLive"
        | case spec.auth_mode do
            :with_auth -> ["      {#{spec.web_module}.UserAuth, :mount_current_scope}"]
            :without_auth -> []
          end
      ]
      |> Enum.join(",\n")

    routes =
      group.items
      |> leaf_items()
      |> Enum.map(fn item -> "      live \"#{item.path}\", #{item.relative_module}" end)
      |> Enum.join("\n")

    """
      live_session :#{group.session_name},
        layout: {#{spec.web_module}.Layouts, :#{group.layout_name}},
        on_mount: [
#{on_mount_lines}
        ] do
        scope "/", #{spec.web_module} do
          pipe_through :browser

#{routes}
        end
      end
    """
  end

  defp render_sidebar_items(groups) do
    home_item = """
    %{
      icon: "hero-home",
      label: "Home",
      path: "/",
      layout: :home
    }
    """ |> String.trim_trailing()

    group_items =
      groups
      |> Enum.map(fn group ->
        first_path =
          group.items
          |> leaf_items()
          |> List.first()
          |> Map.fetch!(:path)

        """
        %{
          icon: "#{group.icon}",
          label: "#{group.label}",
          path: "#{first_path}",
          layout: :#{group.layout_name}
        }
        """
        |> String.trim_trailing()
      end)

    ([home_item] ++ group_items)
    |> Enum.join(",\n")
    |> indent(6)
  end

  defp render_group_items(items) do
    items
    |> group_entries()
    |> Enum.map(&render_entry(&1, 6))
    |> Enum.map(&String.trim_trailing/1)
    |> Enum.join(",\n")
    |> indent(0)
  end

  defp group_entries(items) do
    {entries, current_section, current_items} =
      Enum.reduce(items, {[], nil, []}, fn item, {entries, current_section, current_items} ->
        section = Map.get(item, :section)

        cond do
          is_binary(section) && current_section == section ->
            {entries, current_section, current_items ++ [item]}

          is_binary(section) ->
            flushed = flush_section(entries, current_section, current_items)
            {flushed, section, [item]}

          true ->
            flushed = flush_section(entries, current_section, current_items)
            {flushed ++ [item], nil, []}
        end
      end)

    flush_section(entries, current_section, current_items)
  end

  defp flush_section(entries, nil, []), do: entries

  defp flush_section(entries, section, items) do
    entries ++ [%{kind: :section, label: section, items: items}]
  end

  defp render_entry(%{kind: :section, label: label, items: items}, indent_level) do
    """
#{spaces(indent_level)}%{
#{spaces(indent_level + 2)}section: %{
#{spaces(indent_level + 4)}label: "#{label}"
#{spaces(indent_level + 2)}},
#{spaces(indent_level + 2)}section_items: [
#{Enum.map_join(items, ",\n", &(render_entry(&1, indent_level + 4) |> String.trim_trailing()))}
#{spaces(indent_level + 2)}]
#{spaces(indent_level)}}
"""
  end

  defp render_entry(%Item{kind: :expandable} = item, indent_level) do
    child_active_paths =
      item.children
      |> leaf_items()
      |> Enum.flat_map(& &1.aliases)
      |> Enum.uniq()
      |> render_string_list()

    """
#{spaces(indent_level)}%{
#{spaces(indent_level + 2)}expandable: %{
#{spaces(indent_level + 4)}id: "#{item.expandable_id}",
#{spaces(indent_level + 4)}icon: "#{item.icon}",
#{spaces(indent_level + 4)}label: "#{item.label}",
#{spaces(indent_level + 4)}open: active_path?(current_path, #{child_active_paths})
#{spaces(indent_level + 2)}},
#{spaces(indent_level + 2)}expandable_items: [
#{Enum.map_join(item.children, ",\n", &(render_entry(&1, indent_level + 4) |> String.trim_trailing()))}
#{spaces(indent_level + 2)}]
#{spaces(indent_level)}}
"""
  end

  defp render_entry(%Item{} = item, indent_level) do
    """
#{spaces(indent_level)}%{
#{spaces(indent_level + 2)}icon: "#{item.icon}",
#{spaces(indent_level + 2)}label: "#{item.label}",
#{spaces(indent_level + 2)}path: "#{item.path}",
#{spaces(indent_level + 2)}active: active_path?(current_path, #{render_string_list(item.aliases)})
#{spaces(indent_level)}}
"""
  end

  defp template_path(relative_path) do
    Path.join([File.cwd!(), "priv", "multi_column", "templates", relative_path])
  end

  defp apply_plan!(plan) do
    Enum.each(plan.creates, fn {path, contents} ->
      path |> Path.dirname() |> File.mkdir_p!()
      File.write!(path, contents <> "\n")
    end)

    Enum.each(plan.patches, fn {path, contents} ->
      File.write!(path, contents)
    end)
  end

  defp print_plan(spec, plan) do
    Mix.shell().info("Multi-column generation plan")
    Mix.shell().info("  spec: #{spec.spec_path}")
    Mix.shell().info("  auth: #{spec.auth_mode}")
    Mix.shell().info("")
    Mix.shell().info("Sessions")

    Enum.each(spec.groups, fn group ->
      Mix.shell().info("  - #{group.session_name} -> layout :#{group.layout_name}")
    end)

    Mix.shell().info("")
    Mix.shell().info("Routes")

    spec.groups
    |> leaf_items()
    |> Enum.each(fn item ->
      Mix.shell().info("  - #{item.path} -> #{item.relative_module}")
    end)

    Mix.shell().info("")
    Mix.shell().info("Files to create")
    Enum.each(Map.keys(plan.creates), &Mix.shell().info("  - #{&1}"))

    Mix.shell().info("")
    Mix.shell().info("Files to update")
    Enum.each(Map.keys(plan.patches), &Mix.shell().info("  - #{&1}"))
  end

  defp leaf_items(groups_or_items) when is_list(groups_or_items) do
    Enum.flat_map(groups_or_items, fn
      %Group{items: items} -> leaf_items(items)
      %Item{kind: :expandable, children: children} -> leaf_items(children)
      %Item{kind: :item} = item -> [item]
      %{kind: :expandable, children: children} -> leaf_items(children)
      %{kind: :item} = item -> [item]
    end)
  end

  defp assert_unique!(items, label) do
    dupes =
      items
      |> Enum.frequencies()
      |> Enum.filter(fn {_value, count} -> count > 1 end)
      |> Enum.map(&elem(&1, 0))

    if dupes != [] do
      Mix.raise("duplicate #{label}: #{Enum.join(Enum.map(dupes, &to_string/1), ", ")}")
    end
  end

  defp default_path(group_key, item_key), do: "/#{group_key}/#{String.replace(item_key, "_", "-")}"

  defp slug(label, separator) do
    label
    |> String.downcase()
    |> String.replace(~r/[^a-z0-9]+/u, separator)
    |> String.trim(separator)
  end

  defp pick_icon(label, kind) do
    value = String.downcase(label)

    cond do
      String.contains?(value, "overview") -> "hero-home"
      String.contains?(value, "activity") -> "hero-bolt"
      String.contains?(value, "resource") -> "hero-folder-open"
      String.contains?(value, "setting") -> "hero-cog-6-tooth"
      String.contains?(value, "guide") -> "hero-book-open"
      String.contains?(value, "reference") -> "hero-document-text"
      String.contains?(value, "workspace") -> "hero-squares-2x2"
      String.contains?(value, "management") -> "hero-briefcase"
      String.contains?(value, "update") -> "hero-arrow-path"
      kind == :group -> "hero-rectangle-group"
      true -> "hero-rectangle-stack"
    end
  end

  defp render_string_list(items) do
    "[" <>
      Enum.map_join(items, ", ", fn item -> ~s("#{item}") end) <>
      "]"
  end

  defp indent(text, 0), do: text

  defp indent(text, spaces_count) do
    prefix = spaces(spaces_count)

    text
    |> String.split("\n")
    |> Enum.map_join("\n", fn
      "" -> ""
      line -> prefix <> line
    end)
  end

  defp spaces(count), do: String.duplicate(" ", count)
end
