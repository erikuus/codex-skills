defmodule {{web_module}}.Menus.GroupWithoutAuth do
  use Phoenix.Component

  use Phoenix.VerifiedRoutes,
    endpoint: {{web_module}}.Endpoint,
    router: {{web_module}}.Router,
    statics: {{web_module}}.static_paths()

  import {{web_module}}.MoreComponents

  attr(:id, :string, required: true)
  attr(:current_path, :string)

  def menu(assigns) do
    ~H"""
    <.vertical_navigation class="px-3" id={@id} items={get_items(@current_path)} />
    """
  end

  defp get_items(current_path) do
    [
      %{
        icon: "hero-home",
        label: "Overview",
        path: ~p"/overview",
        active: active_path?(current_path, ["/overview"])
      },
      %{
        section: %{label: "SECTIONS"},
        section_items: [
          %{
            icon: "hero-document-text",
            label: "Catalog",
            path: ~p"/catalog",
            active: active_path?(current_path, ["/catalog"])
          },
          %{
            icon: "hero-chart-bar",
            label: "Reports",
            path: ~p"/reports",
            active: active_path?(current_path, ["/reports"])
          }
        ]
      }
    ]
  end

  defp active_path?(current_path, paths) do
    current_path in paths
  end
end
