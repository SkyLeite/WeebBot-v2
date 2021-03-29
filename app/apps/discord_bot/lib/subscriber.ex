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

  def handle_info({:pso2_eq, eq}, state) do
    IO.inspect("#######################")
    IO.inspect("New EQ - Received EQ:")
    IO.inspect(eq)
    IO.inspect("#######################")

    DiscordBot.Consumer.handle_eq(eq)

    {:noreply, state}
  end
end
