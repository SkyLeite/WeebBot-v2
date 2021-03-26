defmodule AdminWeb.PageLive do
  use AdminWeb, :live_view

  @impl true
  def mount(_params, %{"user_token" => user_token, "guilds" => guilds}, socket) do
    user = Admin.Accounts.get_user_by_session_token(user_token)

    admin_guilds =
      guilds
      |> Enum.filter(fn x ->
        x
        |> Map.fetch!(:permissions)
        |> Nostrum.Permission.from_bitset()
        |> Enum.member?(:manage_guild)
      end)

    {:ok,
     assign(socket,
       query: "",
       results: %{},
       current_user: user,
       guilds: admin_guilds,
       current_guild: guilds |> List.first() |> Map.fetch!(:id)
     )}
  end

  @impl true
  def handle_event("select_guild", values, socket) do
    guild =
      socket.assigns.guilds
      |> Enum.find(fn guild -> guild.id == values["guild"] end)

    {:noreply, socket |> assign(current_guild: guild.id)}
  end

  defp search(query) do
    if not AdminWeb.Endpoint.config(:code_reloader) do
      raise "action disabled when not in development"
    end

    for {app, desc, vsn} <- Application.started_applications(),
        app = to_string(app),
        String.starts_with?(app, query) and not List.starts_with?(desc, ~c"ERTS"),
        into: %{},
        do: {app, vsn}
  end
end
