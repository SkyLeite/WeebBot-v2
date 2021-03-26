defmodule Admin.Repo.Migrations.GuildSettingBelongsToSetting do
  use Ecto.Migration

  def change do
    alter table(:guild_settings) do
      add :setting_id, references(:available_setting)
    end
  end
end
