defmodule DiscordBot.Subscriber do
  use GenServer

  def start_link(channel) do
    GenServer.start_link(__MODULE__, channel)
  end

  def init(channel) do
    pid = self
    ref = Phoenix.PubSub.subscribe(Admin.PubSub, "alerts")

    {:ok, {pid, channel, ref}}
  end

  def handle_info({"pso2_eq_alert_jp", eq}, state) do
    DiscordBot.Consumer.handle_eq(eq)

    {:noreply, state}
  end

  def handle_info({"pso2_eq_alert_na", eq}, state) do
    DiscordBot.Consumer.handle_na_eq(eq)

    {:noreply, state}
  end

  def handle_info({"bumped_alert", entry}, state) do
    DiscordBot.Consumer.handle_bumped_entry(entry)

    {:noreply, state}
  end
end
