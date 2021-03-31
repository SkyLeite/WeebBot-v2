defmodule AdminWeb.UserOauthController do
  use AdminWeb, :controller

  alias Admin.Accounts
  alias AdminWeb.UserAuth

  plug Ueberauth

  def callback(%{assigns: %{ueberauth_auth: user}} = conn, %{
        "provider" => "discord"
      }) do
    guilds =
      user.extra.raw_info.guilds
      |> Enum.map(fn guild ->
        %{
          id: guild["id"],
          name: guild["name"],
          icon: guild["icon"],
          permissions: guild["permissions"]
        }
      end)

    user_params = %{email: user.info.email}

    case Accounts.fetch_or_create_user(user_params) do
      {:ok, user} ->
        UserAuth.log_in_user(conn, user, guilds)

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
