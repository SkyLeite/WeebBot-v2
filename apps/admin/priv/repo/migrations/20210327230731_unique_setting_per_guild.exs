defmodule Admin.Repo.Migrations.UniqueSettingPerGuild do
  use Ecto.Migration

  def change do
    create(unique_index(:guild_settings, [:guild_id, :available_setting_id]))
  end
end
