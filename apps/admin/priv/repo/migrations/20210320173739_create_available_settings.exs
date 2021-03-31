defmodule Admin.Repo.Migrations.CreateAvailableSettings do
  use Ecto.Migration

  def change do
    create table(:available_settings) do
      add :key, :string
      add :type, :string

      timestamps()
    end

    create unique_index(:available_settings, [:key])
  end
end
