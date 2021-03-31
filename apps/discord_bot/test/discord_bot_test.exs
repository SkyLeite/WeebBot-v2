defmodule DiscordBotTest do
  use ExUnit.Case
  doctest DiscordBot

  test "greets the world" do
    assert DiscordBot.hello() == :world
  end
end
