defmodule Admin.Guilds.Setting do
  use Ecto.Schema
  import Ecto.Changeset

  schema "guild_settings" do
    field(:guild_id, :string)
    field(:value, :string)

    belongs_to(:available_setting, Admin.Guilds.AvailableSetting)

    timestamps()
  end

  @doc false
  def changeset(setting, attrs) do
    setting
    |> cast(attrs, [:guild_id, :value])
    |> validate_required([:guild_id, :value])
  end
end
