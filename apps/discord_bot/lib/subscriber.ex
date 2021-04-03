defmodule DiscordBot.Subscriber do
  require Logger

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
    Logger.info("PSO2 JP alert received")
    DiscordBot.Consumer.handle_eq(eq)

    {:noreply, state}
  end

  def handle_info({"pso2_eq_alert_na", eq}, state) do
    Logger.info("PSO2 NA alert received")
    DiscordBot.Consumer.handle_na_eq(eq)

    {:noreply, state}
  end

  def handle_info({"bumped_alert", entry}, state) do
    Logger.info("Bumped alert received")
    DiscordBot.Consumer.handle_bumped_entry(entry)

    {:noreply, state}
  end
end
