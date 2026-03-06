defmodule {{web_module}}.Menus.GroupWithAuth do
  use Phoenix.Component

  use Phoenix.VerifiedRoutes,
    endpoint: {{web_module}}.Endpoint,
    router: {{web_module}}.Router,
    statics: {{web_module}}.static_paths()

  import {{web_module}}.BaseComponents

  attr(:id, :string, required: true)
  attr(:current_path, :string)
  attr(:current_scope, :map, default: %{user: nil})

  def menu(assigns) do
    ~H"""
    <.vertical_navigation
      class="px-3"
      id={@id}
      items={get_items(@current_path, @current_scope)}
    />
    """
  end

  defp get_items(current_path, current_scope) do
    public_items = [
      %{
        icon: "hero-home",
        label: "Overview",
        path: ~p"/overview",
        active: active_path?(current_path, ["/overview"])
      }
    ]

    auth_items =
      if current_scope && current_scope.user do
        [
          %{
            section: %{label: "MANAGE"},
            section_items: [
              %{
                icon: "hero-user-group",
                label: "Customers",
                path: ~p"/customers",
                active: active_path?(current_path, ["/customers"])
              },
              %{
                icon: "hero-clipboard-document-list",
                label: "Orders",
                path: ~p"/orders",
                active: active_path?(current_path, ["/orders"])
              }
            ]
          }
        ]
      else
        []
      end

    public_items ++ auth_items
  end

  defp active_path?(current_path, paths) do
    current_path in paths
  end
end
