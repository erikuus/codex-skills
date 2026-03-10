defmodule {{web_module}}.UserLive.Confirmation do
  use {{web_module}}, :live_view

  alias {{app_module}}.Accounts

  @impl true
  def render(assigns) do
    ~H"""
    <Layouts.app flash={@flash} current_scope={assigns[:current_scope]}>
      <div class="bg-zinc-100 min-h-screen flex flex-col justify-center sm:px-6 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-md">
          <h2 class="text-center text-2xl font-bold text-zinc-900">
            Confirm your account
          </h2>
          <p class="mt-2 text-center text-sm text-zinc-600">
            Already confirmed?
            <.link navigate={~p"/users/log-in"} class="font-semibold">
              Sign in
            </.link>
          </p>
        </div>

        <div class="mt-10 mb-20 sm:mx-auto sm:w-full sm:max-w-[480px]">
          <div class="bg-white px-6 py-6 shadow-sm sm:rounded-lg">
            <.form
              :if={!@user.confirmed_at}
              for={@form}
              id="confirmation_form"
              phx-submit="submit"
              phx-mounted={JS.focus_first()}
              action={~p"/users/log-in?_action=confirmed"}
              phx-trigger-action={@trigger_submit}
            >
              <div class="space-y-6 bg-white">
                <input type="hidden" name={@form[:token].name} value={@form[:token].value} />
                <div class="mt-2 flex items-center justify-between gap-6">
                  <.button
                    name={@form[:remember_me].name}
                    value="true"
                    phx-disable-with="Confirming..."
                    class="w-full"
                  >
                    Confirm and stay logged in
                  </.button>
                </div>
                <div class="mt-2 flex items-center justify-between gap-6">
                  <.button phx-disable-with="Confirming..." class="w-full">
                    Confirm and log in only this time
                  </.button>
                </div>
              </div>
            </.form>

            <.form
              :if={@user.confirmed_at}
              for={@form}
              id="login_form"
              phx-submit="submit"
              phx-mounted={JS.focus_first()}
              action={~p"/users/log-in"}
              phx-trigger-action={@trigger_submit}
            >
              <div class="space-y-6 bg-white">
                <input type="hidden" name={@form[:token].name} value={@form[:token].value} />
                <div class="mt-2 flex items-center justify-between gap-6">
                  <.button
                    name={@form[:remember_me].name}
                    value="true"
                    phx-disable-with="Logging in..."
                    class="w-full"
                  >
                    Log me in
                  </.button>
                </div>
              </div>
            </.form>

            <p :if={!@user.confirmed_at} class="mt-4 text-center text-sm text-zinc-600">
              Tip: If you prefer passwords, you can enable them in the user settings.
            </p>
          </div>
        </div>
      </div>
    </Layouts.app>
    """
  end

  @impl true
  def mount(%{"token" => token}, _session, socket) do
    if user = Accounts.get_user_by_magic_link_token(token) do
      form = to_form(%{"token" => token}, as: "user")

      {:ok, assign(socket, user: user, form: form, trigger_submit: false),
       [layout: false, temporary_assigns: [form: nil]]}
    else
      {:ok,
       socket
       |> put_flash(:error, "Magic link is invalid or it has expired.")
       |> push_navigate(to: ~p"/users/log-in")}
    end
  end

  @impl true
  def handle_event("submit", %{"user" => params}, socket) do
    {:noreply, assign(socket, form: to_form(params, as: "user"), trigger_submit: true)}
  end
end
