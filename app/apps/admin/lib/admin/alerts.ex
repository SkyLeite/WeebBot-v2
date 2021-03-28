defmodule Admin.Alerts do
  @moduledoc """
  The Alerts context.
  """

  import Ecto.Query, warn: false
  alias Admin.Repo

  alias Admin.Alerts.Alert
  alias Admin.Guilds.Setting

  @doc """
  Returns the list of alerts.

  ## Examples

      iex> list_alerts()
      [%Alert{}, ...]

  """
  def list_alerts do
    Repo.all(Alert)
  end

  @doc """
  Creates a alert.

  ## Examples

      iex> create_alert(%{field: value})
      {:ok, %Alert{}}

      iex> create_alert(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_alert(attrs \\ %{}) do
    %Alert{}
    |> Alert.changeset(attrs)
    |> Repo.insert()
  end

  def get_alert_guilds() do
    Setting
    |> select([s], %{channel_id: s.value, guild_id: s.guild_id})
    |> join(:left, [s], a in Admin.Guilds.AvailableSetting, on: s.available_setting_id == a.id)
    |> where([s, a], a.key == "alert_channel_id")
    |> where([s], not is_nil(s.value))
    |> where([s], s.value != "")
    |> Admin.Repo.all()
  end
end
