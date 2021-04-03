defmodule Admin.Alerts.Bumped do
  require Logger

  @moduledoc """
  The context for Bumped.org Alerts
  """

  @feed_url "https://www.bumped.org/psublog/feed/"
  @alert_type "bumped_alert"

  def alert do
    feed = get_feed()

    if should_alert(feed.entries) do
      entry = feed |> Map.fetch!(:entries) |> List.first()

      Admin.Alerts.create_alert(entry, entry.id, @alert_type)
    end
  end

  def get_feed do
    with {:ok, %HTTPoison.Response{status_code: 200, body: body}} <- HTTPoison.get(@feed_url),
         feed <- ElixirFeedParser.parse(body) do
      feed
    end
  end

  def should_alert(entries) do
    entries
    |> List.first()
    |> Map.fetch!(:id)
    |> Kernel.!=(get_last_alerted_entry())
  end

  def get_last_alerted_entry do
    case :dets.lookup(:alerts_cache, @alert_type) do
      [{"bumped_alert", id}] -> id
      _ -> nil
    end
  end
end
