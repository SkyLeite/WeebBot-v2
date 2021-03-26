defmodule Admin.GuildTest do
  use Admin.DataCase

  alias Admin.Guild

  describe "available_settings" do
    alias Admin.Guild.AvailableSetting

    @valid_attrs %{key: "some key", type: "some type"}
    @update_attrs %{key: "some updated key", type: "some updated type"}
    @invalid_attrs %{key: nil, type: nil}

    def available_setting_fixture(attrs \\ %{}) do
      {:ok, available_setting} =
        attrs
        |> Enum.into(@valid_attrs)
        |> Guild.create_available_setting()

      available_setting
    end

    test "list_available_settings/0 returns all available_settings" do
      available_setting = available_setting_fixture()
      assert Guild.list_available_settings() == [available_setting]
    end

    test "get_available_setting!/1 returns the available_setting with given id" do
      available_setting = available_setting_fixture()
      assert Guild.get_available_setting!(available_setting.id) == available_setting
    end

    test "create_available_setting/1 with valid data creates a available_setting" do
      assert {:ok, %AvailableSetting{} = available_setting} = Guild.create_available_setting(@valid_attrs)
      assert available_setting.key == "some key"
      assert available_setting.type == "some type"
    end

    test "create_available_setting/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Guild.create_available_setting(@invalid_attrs)
    end

    test "update_available_setting/2 with valid data updates the available_setting" do
      available_setting = available_setting_fixture()
      assert {:ok, %AvailableSetting{} = available_setting} = Guild.update_available_setting(available_setting, @update_attrs)
      assert available_setting.key == "some updated key"
      assert available_setting.type == "some updated type"
    end

    test "update_available_setting/2 with invalid data returns error changeset" do
      available_setting = available_setting_fixture()
      assert {:error, %Ecto.Changeset{}} = Guild.update_available_setting(available_setting, @invalid_attrs)
      assert available_setting == Guild.get_available_setting!(available_setting.id)
    end

    test "delete_available_setting/1 deletes the available_setting" do
      available_setting = available_setting_fixture()
      assert {:ok, %AvailableSetting{}} = Guild.delete_available_setting(available_setting)
      assert_raise Ecto.NoResultsError, fn -> Guild.get_available_setting!(available_setting.id) end
    end

    test "change_available_setting/1 returns a available_setting changeset" do
      available_setting = available_setting_fixture()
      assert %Ecto.Changeset{} = Guild.change_available_setting(available_setting)
    end
  end
end
