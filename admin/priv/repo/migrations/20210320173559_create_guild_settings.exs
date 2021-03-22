defmodule Admin.Repo.Migrations.CreateGuildSettings do
  use Ecto.Migration

  def change do
    create table(:guild_settings) do
      add :guild_id, :string
      add :value, :string

      timestamps()
    end

  end
end
