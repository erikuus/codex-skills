defmodule {{web_module}}.Menus.SidebarWithAuth do
  use Phoenix.Component

  use Phoenix.VerifiedRoutes,
    endpoint: {{web_module}}.Endpoint,
    router: {{web_module}}.Router,
    statics: {{web_module}}.static_paths()

  import {{web_module}}.BaseComponents

  attr(:current_layout, :atom)
  attr(:current_scope, :map, default: %{user: nil})

  def menu(assigns) do
    ~H"""
    <div class="flex h-full w-full flex-col items-center">
      <div class="w-full flex-1 overflow-y-auto">
        <.narrow_sidebar items={get_items(@current_layout)} />
      </div>
      <div :if={@current_scope && @current_scope.user} class="pb-2">
        <.auth_menu
          id="auth-menu-sidebar"
          class="flex justify-center"
          avatar_only={true}
          avatar_class="w-10 h-10 md:w-12 md:h-12 border-2 border-zinc-600 hover:border-zinc-400"
          avatar_color="text-zinc-100 hover:bg-zinc-600/50 hover:text-white"
          dropdown_position="top-left"
          current_scope={@current_scope}
        >
          <:user_content>
            <p class="rounded-xl px-4 py-2 text-sm font-medium text-zinc-400">
              {@current_scope.user.email}
            </p>
          </:user_content>
        </.auth_menu>
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
      %{icon: "hero-user-group", label: "Clients", path: ~p"/clients", layout: :clients},
      %{icon: "hero-clipboard-document-list", label: "Orders", path: ~p"/orders", layout: :orders}
    ]
  end
end
