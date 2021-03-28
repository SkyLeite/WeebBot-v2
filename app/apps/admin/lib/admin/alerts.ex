defmodule Admin.Alerts do
  @moduledoc """
  The Alerts context.
  """

  import Ecto.Query, warn: false
  alias Admin.Repo

  alias Admin.Alerts.Alert
  alias Admin.Guilds.Setting

  @in_progress_pattern ~r/【開催中】(\d+)時\s(.+)/
  @upcoming_pattern ~r/^(\d+)時\s(.+)/

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

  def check_twitter() do
    case :ets.lookup(:alerts_cache, "eq_tweet_id") do
      [{"eq_tweet_id", id}] -> process_alert()
      [] -> process_alert()
      _ -> :noop
    end
  end

  defp process_alert do
    ExTwitter.user_timeline(screen_name: "pso2_emg_hour", count: 1)
    |> List.first()
    |> format_eq_data()
    |> IO.inspect()
  end

  defp format_eq_data(tweet) do
    tweet
    |> Map.fetch!(:text)
    |> String.split("\n")
    |> Enum.map(fn x ->
      x
      |> String.replace("#PSO2", "")
      |> String.trim()
      |> handle_eq_line(tweet)
    end)
    |> Enum.reject(&is_nil/1)
  end

  defp handle_eq_line(line, tweet) do
    cond do
      String.match?(line, @in_progress_pattern) -> process_in_progress_eq(line, tweet.created_at)
      String.match?(line, @upcoming_pattern) -> process_upcoming_eq(line, tweet.created_at)
      true -> nil
    end
  end

  defp process_upcoming_eq(line, date) do
    [full_line, hour, name] = @upcoming_pattern |> Regex.run(line)

    tweet_creation_time =
      date
      |> Timex.parse!("%a %b %d %T %z %Y", :strftime)

    jp_date =
      tweet_creation_time
      |> Timex.Timezone.convert("Asia/Tokyo")

    hours_to_add =
      jp_date
      |> Map.fetch!(:hour)
      |> Kernel.-(String.to_integer(hour))
      |> Timex.Duration.from_hours()

    eq_date =
      jp_date
      |> Timex.add(hours_to_add)

    %{
      # Remove [Notice]
      name: name |> String.replace("[予告\]", ""),
      inProgress: false,
      date: %{
        JP: eq_date |> Timex.to_unix(),
        UTC: eq_date |> Timex.Timezone.convert("Etc/UTC") |> Timex.to_unix(),
        difference: eq_date |> Timex.diff(jp_date, :hours) |> abs()
      }
    }
  end

  defp process_in_progress_eq(line, date) do
    [full_line, hour, name] = @in_progress_pattern |> Regex.run(line)

    tweet_creation_time =
      date
      |> Timex.parse!("%a %b %d %T %z %Y", :strftime)

    %{
      # Remove [Notice]
      name: name |> String.replace("[予告\]", ""),
      inProgress: true,
      date: %{
        JP:
          tweet_creation_time
          |> Timex.Timezone.convert("Asia/Tokyo")
          |> Timex.to_unix(),
        UTC: tweet_creation_time |> Timex.to_unix(),
        difference: 0
      }
    }
  end
end