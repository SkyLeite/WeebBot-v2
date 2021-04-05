defmodule Admin.Common.Cache do
  use Ecto.Schema
  import Ecto.Changeset

  schema "caches" do
    field(:key, :string)
    field(:value, :string)

    timestamps()
  end

  @doc false
  def changeset(cache, attrs) do
    cache
    |> cast(attrs, [:key, :value])
    |> validate_required([:key, :value])
    |> unique_constraint(:key)
  end
end
