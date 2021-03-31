defmodule Admin.Repo.Migrations.GuildSettingBelongsToSetting do
  use Ecto.Migration

  def change do
    alter table(:guild_settings) do
      add(:available_setting_id, references(:available_settings))
    end
  end
end
