defmodule Admin.Repo.Migrations.CreatePso2NaEvents do
  use Ecto.Migration

  def change do
    create table(:pso2_na_events) do
      add(:title, :string)
      add(:start_date, :naive_datetime)
      add(:end_date, :naive_datetime)
      add(:url, :string)
      add(:category_title, :string)
      add(:category_description, :string)

      timestamps()
    end

    create(unique_index(:pso2_na_events, [:title, :start_date]))
  end
end
