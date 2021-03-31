defmodule Admin.Repo.Migrations.CreateAlerts do
  use Ecto.Migration

  def change do
    create table(:alerts) do
      add :content, :string
      add :type, :string

      timestamps()
    end

  end
end
