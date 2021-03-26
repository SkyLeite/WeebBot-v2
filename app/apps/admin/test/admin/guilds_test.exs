defmodule Admin.GuildsTest do
  use Admin.DataCase

  alias Admin.Guilds

  describe "guild_settings" do
    alias Admin.Guilds.Setting

    @valid_attrs %{guild_id: "some guild_id", value: "some value"}
    @update_attrs %{guild_id: "some updated guild_id", value: "some updated value"}
    @invalid_attrs %{guild_id: nil, value: nil}

    def setting_fixture(attrs \\ %{}) do
      {:ok, setting} =
        attrs
        |> Enum.into(@valid_attrs)
        |> Guilds.create_setting()

      setting
    end

    test "list_guild_settings/0 returns all guild_settings" do
      setting = setting_fixture()
      assert Guilds.list_guild_settings() == [setting]
    end

    test "get_setting!/1 returns the setting with given id" do
      setting = setting_fixture()
      assert Guilds.get_setting!(setting.id) == setting
    end

    test "create_setting/1 with valid data creates a setting" do
      assert {:ok, %Setting{} = setting} = Guilds.create_setting(@valid_attrs)
      assert setting.guild_id == "some guild_id"
      assert setting.value == "some value"
    end

    test "create_setting/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Guilds.create_setting(@invalid_attrs)
    end

    test "update_setting/2 with valid data updates the setting" do
      setting = setting_fixture()
      assert {:ok, %Setting{} = setting} = Guilds.update_setting(setting, @update_attrs)
      assert setting.guild_id == "some updated guild_id"
      assert setting.value == "some updated value"
    end

    test "update_setting/2 with invalid data returns error changeset" do
      setting = setting_fixture()
      assert {:error, %Ecto.Changeset{}} = Guilds.update_setting(setting, @invalid_attrs)
      assert setting == Guilds.get_setting!(setting.id)
    end

    test "delete_setting/1 deletes the setting" do
      setting = setting_fixture()
      assert {:ok, %Setting{}} = Guilds.delete_setting(setting)
      assert_raise Ecto.NoResultsError, fn -> Guilds.get_setting!(setting.id) end
    end

    test "change_setting/1 returns a setting changeset" do
      setting = setting_fixture()
      assert %Ecto.Changeset{} = Guilds.change_setting(setting)
    end
  end
end
