defmodule Admin.Guilds.AvailableSetting do
  use Ecto.Schema
  import Ecto.Changeset

  schema "available_settings" do
    field(:key, :string)
    field(:type, :string)

    has_many(:guild_setting, Admin.Guilds.Setting)

    timestamps()
  end

  @doc false
  def changeset(available_setting, attrs) do
    available_setting
    |> cast(attrs, [:key, :type])
    |> unique_constraint(:key)
    |> validate_required([:key, :type])
  end
end
