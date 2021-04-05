defmodule Admin.CommonTest do
  use Admin.DataCase

  alias Admin.Common

  describe "caches" do
    alias Admin.Common.Cache

    test "set/2 correctly sets a key" do
      key = "somekey"
      value = "somevalue"

      assert {:ok, response} = Admin.Cache.set(key, value)
      assert response.key == key
      assert response.value == value
    end

    test "set/2 updates an existing value" do
      key = "somekey"
      value = "somevalue"
      value_two = "somevalue2"

      assert {:ok, response} = Admin.Cache.set(key, value)
      assert response.key == key
      assert response.value == value

      assert {:ok, response_two} = Admin.Cache.set(key, value_two)
      assert response_two.value == value_two
    end

    test "get/1 correctly gets a key" do
      key = "somekey"
      value = "somevalue"

      Admin.Cache.set(key, value)

      assert Admin.Cache.get(key) == value
    end

    test "get/1 returns nil if key doesn't exist" do
      assert Admin.Cache.get("askjsahdfkajshdkjfh") == nil
    end
  end
end
