defmodule Admin.Repo.Migrations.CreateCaches do
  use Ecto.Migration

  def change do
    create table(:caches) do
      add(:key, :string)
      add(:value, :string)

      timestamps()
    end

    create(unique_index(:caches, [:key]))
  end
end
