defmodule AdminWeb.UserOauthController do
  use AdminWeb, :controller

  alias Admin.Accounts
  alias AdminWeb.UserAuth

  plug Ueberauth

  def callback(%{assigns: %{ueberauth_auth: %{info: user_info}}} = conn, %{
        "provider" => "discord"
      }) do
    user_params = %{email: user_info.email}

    IO.inspect(user_info)

    case Accounts.fetch_or_create_user(user_params) do
      {:ok, user} ->
        UserAuth.log_in_user(conn, user)

      _ ->
        conn
        |> put_flash(:error, "Authentication failed")
        |> redirect(to: "/")
    end
  end

  def callback(conn, _params) do
    conn
    |> put_flash(:error, "Authentication failed")
    |> redirect(to: "/")
  end
end
