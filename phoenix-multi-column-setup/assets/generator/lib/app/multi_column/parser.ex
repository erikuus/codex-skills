defmodule {{app_module}}.MultiColumn.Parser do
  @moduledoc false

  def parse_file!(path) do
    path
    |> File.read!()
    |> String.split("\n")
    |> Enum.with_index(1)
    |> Enum.reduce(initial_state(), &parse_line/2)
    |> finish!()
  end

  defp initial_state do
    %{
      groups: [],
      current_group: nil,
      current_section: nil,
      current_expandable: nil
    }
  end

  defp parse_line({raw_line, line_no}, state) do
    line = String.trim_trailing(raw_line)
    trimmed = String.trim(line)

    cond do
      trimmed == "" ->
        state

      trimmed == "}" ->
        close_expandable!(state, line_no)

      state.current_expandable && Regex.match?(~r/^\[.+\]$/, trimmed) ->
        raise_parse!(line_no, "cannot start a new group inside an expandable block")

      state.current_expandable && Regex.match?(~r/^##\s+.+$/, trimmed) ->
        raise_parse!(line_no, "cannot start a new section inside an expandable block")

      Regex.match?(~r/^\[(.+)\]$/, trimmed) ->
        start_group!(state, line_no, trimmed)

      Regex.match?(~r/^##\s+(.+)$/, trimmed) ->
        start_section!(state, line_no, trimmed)

      String.ends_with?(trimmed, "{") ->
        start_expandable!(state, line_no, trimmed)

      state.current_expandable ->
        append_expandable_child!(state, line_no, trimmed)

      true ->
        append_group_item!(state, line_no, trimmed)
    end
  end

  defp finish!(%{current_expandable: %{label: label}}) do
    raise ArgumentError,
          "navigation spec ended before expandable block #{inspect(label)} was closed"
  end

  defp finish!(%{current_group: nil}) do
    raise ArgumentError, "navigation spec must contain at least one [Group]"
  end

  defp finish!(state) do
    groups =
      state.groups ++
        [
          %{
            label: state.current_group.label,
            items: state.current_group.items
          }
        ]

    groups
  end

  defp start_group!(%{current_expandable: current_expandable}, line_no, _trimmed)
       when not is_nil(current_expandable) do
    raise_parse!(line_no, "cannot start a new group inside an expandable block")
  end

  defp start_group!(state, line_no, trimmed) do
    [_match, label] = Regex.run(~r/^\[(.+)\]$/, trimmed)
    label = String.trim(label)

    if label == "" do
      raise_parse!(line_no, "group label cannot be empty")
    end

    committed_groups =
      case state.current_group do
        nil -> state.groups
        group -> state.groups ++ [%{label: group.label, items: group.items}]
      end

    %{
      groups: committed_groups,
      current_group: %{label: label, items: []},
      current_section: nil,
      current_expandable: nil
    }
  end

  defp start_section!(%{current_group: nil}, line_no, _trimmed) do
    raise_parse!(line_no, "section declared before any [Group]")
  end

  defp start_section!(state, line_no, trimmed) do
    [_match, label] = Regex.run(~r/^##\s+(.+)$/, trimmed)
    label = String.trim(label)

    if label == "" do
      raise_parse!(line_no, "section label cannot be empty")
    end

    %{state | current_section: label}
  end

  defp start_expandable!(%{current_group: nil}, line_no, _trimmed) do
    raise_parse!(line_no, "expandable block declared before any [Group]")
  end

  defp start_expandable!(%{current_expandable: current_expandable}, line_no, _trimmed)
       when not is_nil(current_expandable) do
    raise_parse!(line_no, "nested expandable blocks are not supported")
  end

  defp start_expandable!(state, line_no, trimmed) do
    label =
      trimmed
      |> String.trim_trailing("{")
      |> String.trim()

    item = parse_item_line!(label, line_no, child?: false)

    if item.path do
      raise_parse!(line_no, "expandable parents cannot declare a direct route in v1")
    end

    %{
      state
      | current_expandable: %{label: item.label, section: state.current_section, children: []}
    }
  end

  defp close_expandable!(%{current_expandable: nil}, line_no) do
    raise_parse!(line_no, "unexpected closing brace")
  end

  defp close_expandable!(state, _line_no) do
    expandable = %{
      kind: :expandable,
      label: state.current_expandable.label,
      section: state.current_expandable.section,
      children: state.current_expandable.children
    }

    group = %{state.current_group | items: state.current_group.items ++ [expandable]}

    %{state | current_group: group, current_expandable: nil}
  end

  defp append_expandable_child!(state, line_no, trimmed) do
    item = parse_item_line!(trimmed, line_no, child?: true)

    child =
      Map.merge(item, %{
        kind: :item,
        section: nil
      })

    expandable = %{
      state.current_expandable
      | children: state.current_expandable.children ++ [child]
    }

    %{state | current_expandable: expandable}
  end

  defp append_group_item!(%{current_group: nil}, line_no, _trimmed) do
    raise_parse!(line_no, "menu item declared before any [Group]")
  end

  defp append_group_item!(state, line_no, trimmed) do
    item = parse_item_line!(trimmed, line_no, child?: false)

    group =
      %{
        state.current_group
        | items:
            state.current_group.items ++
              [
                Map.merge(item, %{
                  kind: :item,
                  section: state.current_section
                })
              ]
      }

    %{state | current_group: group}
  end

  defp parse_item_line!(line, line_no, opts) do
    case String.split(line, "->", parts: 2) do
      [label] ->
        label = String.trim(label)

        if label == "" do
          raise_parse!(line_no, "menu item label cannot be empty")
        end

        if opts[:child?] do
          raise_parse!(line_no, "expandable children must declare an explicit route")
        end

        %{label: label, path: nil, aliases: []}

      [label, path_spec] ->
        label = String.trim(label)

        paths =
          path_spec |> String.split("|") |> Enum.map(&String.trim/1) |> Enum.reject(&(&1 == ""))

        cond do
          label == "" ->
            raise_parse!(line_no, "menu item label cannot be empty")

          paths == [] ->
            raise_parse!(line_no, "menu item route cannot be empty")

          Enum.any?(paths, &(not String.starts_with?(&1, "/"))) ->
            raise_parse!(line_no, "routes must start with /")

          true ->
            [path | aliases] = paths
            %{label: label, path: path, aliases: aliases}
        end
    end
  end

  defp raise_parse!(line_no, message) do
    raise ArgumentError, "navigation spec line #{line_no}: #{message}"
  end
end
