defmodule DiscordBot.Consumer do
  use Nostrum.Consumer

  alias Nostrum.Api

  import Ecto.Query, warn: false
  import Nostrum.Struct.Embed

  def start_link do
    Consumer.start_link(__MODULE__)
  end

  def handle_event({:MESSAGE_CREATE, msg, _ws_state}) do
    case msg.content do
      "!sleep" ->
        Api.create_message(msg.channel_id, "Going to sleep...")
        # This won't stop other events from being handled.
        Process.sleep(3000)

      "!ping" ->
        Api.create_message(msg.channel_id, "pyongyang!")

      "!raise" ->
        # This won't crash the entire Consumer.
        raise "No problems here!"

      _ ->
        :ignore
    end
  end

  # Default event handler, if you don't include this, your consumer WILL crash if
  # you don't have a method definition for each event type.
  def handle_event(_event) do
    :noop
  end

  def handle_eq(eqs) do
    base_embed =
      %Nostrum.Struct.Embed{}
      |> put_author(
        "Emergency Quest Notice",
        "https://leite.dev",
        "https://images.emojiterra.com/mozilla/512px/231a.png"
      )
      |> put_footer("https://weebbot.com")
      |> put_timestamp(Timex.now())

    embed =
      Enum.reduce(eqs, base_embed, fn eq, embed ->
        put_field(
          embed,
          if eq.date.difference > 0 do
            "In about #{eq.date.difference} hours"
          else
            "In progress"
          end,
          eq.name,
          eq.date.difference > 0
        )
      end)

    get_alert_guilds("jp_alert_channel_id")
    |> Enum.map(fn alert_guild ->
      embed = Api.create_message(alert_guild.channel_id |> String.to_integer(), embed: embed)
    end)
  end

  def handle_na_eq(eqs) do
    now = Timex.now()

    base_embed =
      %Nostrum.Struct.Embed{}
      |> put_author(
        "Emergency Quest Notice (NA)",
        "https://leite.dev",
        "https://images.emojiterra.com/mozilla/512px/231a.png"
      )
      |> put_footer("https://weebbot.com")
      |> put_timestamp(now)

    embed =
      Enum.reduce(eqs, base_embed, fn eq, embed ->
        difference_in_hours = eq.start_date |> Timex.diff(Timex.now(), :hours)
        in_progress? = eq.start_date |> Timex.diff(Timex.now(), :minutes) > 10

        put_field(
          embed,
          if in_progress? do
            "In about #{difference_in_hours} hours"
          else
            "In progress"
          end,
          eq.title
        )
      end)

    get_alert_guilds("na_alert_channel_id")
    |> Enum.map(fn alert_guild ->
      embed = Api.create_message(alert_guild.channel_id |> String.to_integer(), embed: embed)
    end)
  end

  defp get_alert_guilds(key) do
    Admin.Guilds.Setting
    |> select([s], %{channel_id: s.value, guild_id: s.guild_id})
    |> join(:left, [s], a in Admin.Guilds.AvailableSetting, on: s.available_setting_id == a.id)
    |> where([s, a], a.key == ^key)
    |> where([s], not is_nil(s.value))
    |> where([s], s.value != "")
    |> Admin.Repo.all()
  end
end
