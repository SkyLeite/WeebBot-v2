defmodule Admin.AlertsTest do
  use Admin.DataCase

  alias Admin.Alerts

  describe "alerts" do
    alias Admin.Alerts.Alert

    @valid_attrs %{content: "some content", type: "some type"}
    @update_attrs %{content: "some updated content", type: "some updated type"}
    @invalid_attrs %{content: nil, type: nil}

    def alert_fixture(attrs \\ %{}) do
      {:ok, alert} =
        attrs
        |> Enum.into(@valid_attrs)
        |> Alerts.create_alert()

      alert
    end
  end

  describe "EQ processing" do
    test "process_upcoming_eq/2 correctly translates an EQ" do
      result =
        Admin.Alerts.process_upcoming_eq("10時 [予告]アークスリーグ", "Sat Aug 04 11:48:27 +0000 2012")

      assert result.name == "ARKS League"
    end

    test "process_in_progress_eq/2 correctly reports an EQ as in progress" do
      result =
        Admin.Alerts.process_in_progress_eq(
          "【開催中】07時 [予告]闇のゆりかご",
          "Sat Aug 04 11:48:27 +0000 2012"
        )

      assert result.inProgress == true
    end

    @tag :wip
    test "process_upcoming_eq/2 correctly reports time differences" do
      data = [
        {"16時 [予告]アークスリーグ", "Sat Aug 04 05:00:00 +0000 2012", 2},
        {"00時 [予告]アークスリーグ", "Sat Aug 04 13:00:00 +0000 2012", 2},
        {"01時 [予告]アークスリーグ", "Sat Aug 04 13:00:00 +0000 2012", 3},
        {"03時 [予告]アークスリーグ", "Sat Aug 04 13:00:00 +0000 2012", 5}
      ]

      for {eq, date, expected} <- data do
        assert Admin.Alerts.process_upcoming_eq(eq, date).date.difference == expected
      end
    end
  end
end
