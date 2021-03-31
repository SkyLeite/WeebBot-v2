defmodule AdminWeb.HomeLive do
  use AdminWeb, :live_view

  @impl true
  def mount(_params, _values, socket) do
    {:ok, socket}
  end
end
