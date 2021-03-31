defmodule Admin.Repo.Migrations.AvailableSettingLabel do
  use Ecto.Migration

  def change do
    alter table(:available_settings) do
      add :label, :string
    end
  end
end
