defmodule {{web_module}}.UserLive.Settings do
  use {{web_module}}, :live_view

  on_mount { {{web_module}}.UserAuth, :require_sudo_mode}

  alias {{app_module}}.Accounts

  @impl true
  def render(assigns) do
    ~H"""
    <Layouts.app flash={@flash} current_scope={assigns[:current_scope]}>
      <div class="bg-zinc-100 min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-4xl">
          <div class="md:grid md:grid-cols-3 md:gap-6">
            <div class="mx-6 sm:mx-0 md:col-span-1">
              <h2 class="text-2xl font-bold text-zinc-900">
                Account Settings
              </h2>
              <p class="mt-2 text-sm text-zinc-600">
                Update your email address and password
              </p>
            </div>

            <div class="mt-5 md:mt-0 md:col-span-2 space-y-6">
              <div class="bg-white px-6 py-6 shadow-sm sm:rounded-lg">
                <.form
                  for={@email_form}
                  id="email_form"
                  phx-submit="update_email"
                  phx-change="validate_email"
                >
                  <div class="space-y-6 bg-white">
                    <.input
                      field={@email_form[:email]}
                      type="email"
                      label="Email"
                      autocomplete="username"
                      required
                    />
                    <div class="mt-2 flex items-center justify-between gap-6">
                      <.button phx-disable-with="Changing...">Change Email</.button>
                    </div>
                  </div>
                </.form>
              </div>

              <div class="bg-white px-6 py-6 shadow-sm sm:rounded-lg">
                <.form
                  for={@password_form}
                  id="password_form"
                  action={~p"/users/update-password"}
                  method="post"
                  phx-change="validate_password"
                  phx-submit="update_password"
                  phx-trigger-action={@trigger_submit}
                >
                  <div class="space-y-6 bg-white">
                    <input
                      name={@password_form[:email].name}
                      type="hidden"
                      id="hidden_user_email"
                      autocomplete="username"
                      value={@current_email}
                    />
                    <.input
                      field={@password_form[:password]}
                      type="password"
                      label="New password"
                      autocomplete="new-password"
                      required
                    />
                    <.input
                      field={@password_form[:password_confirmation]}
                      type="password"
                      label="Confirm new password"
                      autocomplete="new-password"
                    />
                    <div class="mt-2 flex items-center justify-between gap-6">
                      <.button phx-disable-with="Changing...">Change Password</.button>
                    </div>
                  </div>
                </.form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layouts.app>
    """
  end

  @impl true
  def mount(%{"token" => token}, _session, socket) do
    socket =
      case Accounts.update_user_email(socket.assigns.current_scope.user, token) do
        {:ok, _user} ->
          put_flash(socket, :info, "Email changed successfully.")

        {:error, _} ->
          put_flash(socket, :error, "Email change link is invalid or it has expired.")
      end

    {:ok, push_navigate(socket, to: ~p"/users/settings")}
  end

  def mount(_params, _session, socket) do
    user = socket.assigns.current_scope.user
    email_changeset = Accounts.change_user_email(user, %{}, validate_unique: false)
    password_changeset = Accounts.change_user_password(user, %{}, hash_password: false)

    socket =
      socket
      |> assign(:current_email, user.email)
      |> assign(:email_form, to_form(email_changeset))
      |> assign(:password_form, to_form(password_changeset))
      |> assign(:trigger_submit, false)

    {:ok, socket, layout: false}
  end

  @impl true
  def handle_event("validate_email", params, socket) do
    %{"user" => user_params} = params

    email_form =
      socket.assigns.current_scope.user
      |> Accounts.change_user_email(user_params, validate_unique: false)
      |> Map.put(:action, :validate)
      |> to_form()

    {:noreply, assign(socket, email_form: email_form)}
  end

  def handle_event("update_email", params, socket) do
    %{"user" => user_params} = params
    user = socket.assigns.current_scope.user
    true = Accounts.sudo_mode?(user)

    case Accounts.change_user_email(user, user_params) do
      %{valid?: true} = changeset ->
        Accounts.deliver_user_update_email_instructions(
          Ecto.Changeset.apply_action!(changeset, :insert),
          user.email,
          &url(~p"/users/settings/confirm-email/#{&1}")
        )

        info = "A link to confirm your email change has been sent to the new address."
        {:noreply, socket |> put_flash(:info, info)}

      changeset ->
        {:noreply, assign(socket, :email_form, to_form(changeset, action: :insert))}
    end
  end

  def handle_event("validate_password", params, socket) do
    %{"user" => user_params} = params

    password_form =
      socket.assigns.current_scope.user
      |> Accounts.change_user_password(user_params, hash_password: false)
      |> Map.put(:action, :validate)
      |> to_form()

    {:noreply, assign(socket, password_form: password_form)}
  end

  def handle_event("update_password", params, socket) do
    %{"user" => user_params} = params
    user = socket.assigns.current_scope.user
    true = Accounts.sudo_mode?(user)

    case Accounts.change_user_password(user, user_params) do
      %{valid?: true} = changeset ->
        {:noreply, assign(socket, trigger_submit: true, password_form: to_form(changeset))}

      changeset ->
        {:noreply, assign(socket, password_form: to_form(changeset, action: :insert))}
    end
  end
end
