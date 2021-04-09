defmodule Admin.Cache do
  require Logger
  import Ecto.Query

  def get(key) do
    Admin.Common.Cache
    |> where([c], c.key == ^key)
    |> Admin.Repo.one()
    |> case do
      nil -> nil
      c -> c.value
    end
  end

  def set(key, value) when is_binary(key) and is_binary(value) do
    Logger.info("Setting cache: #{key}: #{value}")

    %Admin.Common.Cache{}
    |> Admin.Common.Cache.changeset(%{key: key, value: value})
    |> Admin.Repo.insert(
      on_conflict: {:replace, [:value]},
      conflict_target: :key
    )
  end
end
