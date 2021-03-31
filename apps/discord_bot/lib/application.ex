defmodule DiscordBot.Application do
  use Application

  def start(_type, _args) do
    children = [
      DiscordBot.Consumer,
      DiscordBot.Subscriber
    ]

    opts = [strategy: :one_for_one]
    Supervisor.start_link(children, opts)
  end

  # def start_link(args) do
  #   IO.puts("(!@*&#(*(@*#&(*!@#))))")
  #   Supervisor.start_link(__MODULE__, args, name: __MODULE__)
  # end

  # @impl true
  # def init(_init_arg) do
  #   IO.puts("QOIWEUOIQUWEIOUQWOIE")
  #   children = [DiscordBot.Consumer]

  #   Supervisor.init(children, strategy: :one_for_one)
  # end
end
