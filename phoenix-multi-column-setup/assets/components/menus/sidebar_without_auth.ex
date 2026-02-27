defmodule {{web_module}}.Menus.SidebarWithoutAuth do
  use Phoenix.Component

  use Phoenix.VerifiedRoutes,
    endpoint: {{web_module}}.Endpoint,
    router: {{web_module}}.Router,
    statics: {{web_module}}.static_paths()

  import {{web_module}}.MoreComponents

  attr(:current_layout, :atom)

  def menu(assigns) do
    ~H"""
    <div class="flex h-full w-full flex-col items-center">
      <div class="w-full flex-1 overflow-y-auto">
        <.narrow_sidebar items={get_items(@current_layout)} />
      </div>
    </div>
    """
  end

  defp get_items(current_layout) do
    get_items() |> Enum.map(&Map.put(&1, :active, current_layout == &1.layout))
  end

  defp get_items do
    [
      %{icon: "hero-home", label: "Home", path: ~p"/", layout: :home},
      %{icon: "hero-document-text", label: "Catalog", path: ~p"/catalog", layout: :catalog},
      %{icon: "hero-chart-bar", label: "Reports", path: ~p"/reports", layout: :reports}
    ]
  end
end
