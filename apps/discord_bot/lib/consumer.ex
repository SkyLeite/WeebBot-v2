defmodule DiscordBot.Consumer do
  require Logger

  use Nostrum.Consumer

  alias Nostrum.Api

  import Ecto.Query, warn: false
  import Nostrum.Struct.Embed

  def start_link do
    Consumer.start_link(__MODULE__)
  end

  def handle_event({:MESSAGE_CREATE, msg, _ws_state}) do
    case msg.content do
      ";help" ->
        Api.create_message(msg.channel_id, embed: help_embed)

      ";ping" ->
        Api.create_message(msg.channel_id, "Pong")

      _ ->
        :ignore
    end
  end

  def help_embed do
    %Nostrum.Struct.Embed{}
    |> put_author("Weeb Bot", "https://weebbot.com", "")
    |> put_thumbnail(
      "https://cdn.discordapp.com/avatars/198480001480392704/71fc96884bb642a74be0f4c0fd1ed226.png"
    )
    |> put_field("Settings", "[Click here](https://weebbot.com/user/settings)", true)
    |> put_field("Github", "[Click here](https://github.com/RodrigoLeiteF/WeebBot-v2)", true)
    |> put_field(
      "Discord / Support",
      "[Click here](https://discord.com/invite/0xMXCNAFbH032Ig1)",
      true
    )
    |> put_field("Alive since", "May 26th, 2016", true)
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
      Logger.info("Sending JP alert to channel #{alert_guild.channel_id}")
      Api.create_message(alert_guild.channel_id |> String.to_integer(), embed: embed)
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
      Logger.info("Sending NA alert to channel #{alert_guild.channel_id}")
      Api.create_message(alert_guild.channel_id |> String.to_integer(), embed: embed)
    end)
  end

  def handle_bumped_entry(entry) do
    get_alert_guilds("bumped_alert_channel_id")
    |> Enum.map(fn alert_guild ->
      Logger.info("Sending Bumped alert to channel #{alert_guild.channel_id}")

      Api.create_message(
        alert_guild.channel_id |> String.to_integer(),
        "New Bumped article! #{entry.id}"
      )
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
