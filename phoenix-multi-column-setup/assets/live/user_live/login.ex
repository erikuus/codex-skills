defmodule {{web_module}}.UserLive.Login do
  use {{web_module}}, :live_view

  alias {{app_module}}.Accounts

  @impl true
  def render(assigns) do
    ~H"""
    <Layouts.app flash={@flash} current_scope={assigns[:current_scope]}>
      <div class="bg-zinc-100 min-h-screen flex flex-col justify-center sm:px-6 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-md">
          <h2 class="text-center text-2xl font-bold text-zinc-900">
            Sign in to your account
          </h2>
          <p class="mt-2 text-center text-sm text-zinc-600">
            Don't have an account?
            <.link navigate={~p"/users/register"} class="font-semibold">
              Sign up
            </.link>
          </p>
        </div>

        <div class="mt-10 mb-20 sm:mx-auto sm:w-full sm:max-w-[480px]">
          <div class="bg-white px-6 py-6 shadow-sm sm:rounded-lg space-y-6">
            <.form
              :let={f}
              for={@form}
              id="login_form_magic"
              action={~p"/users/log-in"}
              phx-submit="submit_magic"
              class="space-y-4"
            >
              <.input
                readonly={!!@current_scope}
                field={f[:email]}
                type="email"
                label="Email address"
                autocomplete="email"
                required
                phx-mounted={JS.focus()}
              />
              <.button class="w-full">
                Email me a magic link
              </.button>
            </.form>

            <div class="border-t border-zinc-200" />

            <.form
              :let={f}
              for={@form}
              id="login_form_password"
              action={~p"/users/log-in"}
              phx-submit="submit_password"
              phx-trigger-action={@trigger_submit}
              class="space-y-4"
            >
              <.input
                readonly={!!@current_scope}
                field={f[:email]}
                type="email"
                label="Email address"
                autocomplete="email"
                required
              />
              <.input
                field={@form[:password]}
                type="password"
                label="Password"
                autocomplete="current-password"
              />
              <div class="flex items-center justify-between">
                <.input field={@form[:remember_me]} type="checkbox" label="Remember me" />
              </div>
              <.button class="w-full" name={@form[:remember_me].name} value="true">
                Sign in
              </.button>
            </.form>
          </div>

          <div :if={local_mail_adapter?()} class="mt-6 text-center text-sm text-zinc-600">
            Using the local mail adapter. Visit
            <.link href="/dev/mailbox" class="font-semibold">the mailbox page</.link>
            to see sent emails.
          </div>
        </div>
      </div>
    </Layouts.app>
    """
  end

  @impl true
  def mount(_params, _session, socket) do
    email =
      Phoenix.Flash.get(socket.assigns.flash, :email) ||
        get_in(socket.assigns, [:current_scope, Access.key(:user), Access.key(:email)])

    form = to_form(%{"email" => email}, as: "user")

    {:ok, assign(socket, form: form, trigger_submit: false), layout: false}
  end

  @impl true
  def handle_event("submit_password", _params, socket) do
    {:noreply, assign(socket, :trigger_submit, true)}
  end

  def handle_event("submit_magic", %{"user" => %{"email" => email}}, socket) do
    if user = Accounts.get_user_by_email(email) do
      Accounts.deliver_login_instructions(
        user,
        &url(~p"/users/log-in/#{&1}")
      )
    end

    info =
      "If your email is in our system, you will receive instructions for logging in shortly."

    {:noreply,
     socket
     |> put_flash(:info, info)
     |> push_navigate(to: ~p"/users/log-in")}
  end

  defp local_mail_adapter? do
    Application.get_env(:{{otp_app}}, {{app_module}}.Mailer)[:adapter] ==
      Swoosh.Adapters.Local
  end
end
