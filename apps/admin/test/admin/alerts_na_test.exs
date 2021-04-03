defmodule Admin.AlertsNATest do
  use Admin.DataCase

  alias Admin.AlertsNA

  alias Admin.Alerts.Alert

  setup do
    :dets.delete_all_objects(:alerts_cache)

    {:ok, %{}}
  end

  def create_quest(title) do
    %{
      "title" => title,
      "route" => "/myurl",
      "category" => %{
        "title" => "Some test category",
        "description" => "Some test category description"
      }
    }
  end

  def create_event(time) do
    %{
      "startDate" => time |> Admin.AlertsNA.to_utc() |> to_api_format(),
      "endDate" =>
        time
        |> Admin.AlertsNA.to_utc()
        |> Timex.add(Timex.Duration.from_hours(1))
        |> to_api_format()
    }
  end

  def to_api_format(time) do
    time |> Timex.Timezone.convert("America/Phoenix") |> Timex.format!("%FT%T", :strftime)
  end

  describe "EQ processing" do
    test "to_utc/1 correctly parses a date" do
      result = "2021-04-27T10:30:00" |> Admin.AlertsNA.to_utc()

      expected =
        Timex.now()
        |> Timex.set(
          year: 2021,
          month: 4,
          day: 27,
          hour: 17,
          minute: 30,
          second: 00
        )

      assert result |> Timex.diff(expected, :second) == 0
    end

    test "insert_event/2 correctly inserts an event" do
      now = Timex.now()
      eq_start_date = now |> Timex.add(Timex.Duration.from_hours(1))

      quest = create_quest("Some quest xdakjsdhakjsh")
      event = create_event("2021-04-27T10:30:00")

      assert {:ok, result} = Admin.AlertsNA.insert_event(event, quest)
      assert result.title == quest["title"]
    end

    test "should_alert/1 returns true for a list with an event happening now" do
      quest = create_quest("Some quest xdakjsdhakjsh")
      event = create_event(Timex.now() |> to_api_format)

      {:ok, eq} = Admin.AlertsNA.insert_event(event, quest)

      assert Admin.AlertsNA.should_alert([eq]) == true
    end

    test "should_alert/1 returns true for a list with an event happening in an hour" do
      quest = create_quest("Some quest xdakjsdhakjsh")

      event =
        create_event(Timex.now() |> Timex.add(Timex.Duration.from_hours(1)) |> to_api_format)

      {:ok, eq} = Admin.AlertsNA.insert_event(event, quest)

      assert Admin.AlertsNA.should_alert([eq]) == true
    end

    test "should_alert/1 returns false for a list with an event happening in 2 hours" do
      quest = create_quest("Some quest xdakjsdhakjsh")

      event =
        create_event(Timex.now() |> Timex.add(Timex.Duration.from_hours(2)) |> to_api_format)

      {:ok, eq} = Admin.AlertsNA.insert_event(event, quest)

      assert Admin.AlertsNA.should_alert([eq]) == false
    end

    test "should_alert/1 returns false for a list with an event happening in 1 hour and 30 minutes" do
      quest = create_quest("Some quest xdakjsdhakjsh")

      event =
        create_event(
          Timex.now()
          |> Timex.add(Timex.Duration.from_hours(1))
          |> Timex.add(Timex.Duration.from_minutes(30))
          |> to_api_format
        )

      {:ok, eq} = Admin.AlertsNA.insert_event(event, quest)

      assert Admin.AlertsNA.should_alert([eq]) == false
    end

    test "should_alert/1 returns true for a list with an event happening in less than 1 hour" do
      quest = create_quest("Some quest xdakjsdhakjsh")

      event =
        create_event(
          Timex.now()
          |> Timex.add(Timex.Duration.from_minutes(30))
          |> to_api_format
        )

      {:ok, eq} = Admin.AlertsNA.insert_event(event, quest)

      assert Admin.AlertsNA.should_alert([eq]) == true
    end

    test "should_alert/1 returns false for a list with a past event" do
      quest = create_quest("Some quest xdakjsdhakjsh")

      event =
        create_event(
          Timex.now()
          |> Timex.subtract(Timex.Duration.from_minutes(30))
          |> to_api_format
        )

      {:ok, eq} = Admin.AlertsNA.insert_event(event, quest)

      assert Admin.AlertsNA.should_alert([eq]) == true
    end

    test "is_already_alerted/1 returns false for an empty :dets table" do
      quest = create_quest("Some quest xdakjsdhakjsh")

      event =
        create_event(
          Timex.now()
          |> to_api_format
        )

      {:ok, eq} = Admin.AlertsNA.insert_event(event, quest)

      assert Admin.AlertsNA.is_already_alerted(eq) == false
    end

    @tag :wip
    test "is_already_alerted/1 returns false for event that's not been alerted" do
      quest = create_quest("Some quest xdakjsdhakjsh")

      event =
        create_event(
          Timex.now()
          |> to_api_format
        )

      {:ok, eq} = Admin.AlertsNA.insert_event(event, quest)

      :dets.insert(:alerts_cache, {"pso2_eq_alert_na", eq.id + 1})
      assert Admin.AlertsNA.is_already_alerted(eq) == false
    end

    test "is_already_alerted/1 returns true for an event that's already been alerted" do
      quest = create_quest("Some quest xdakjsdhakjsh")

      event =
        create_event(
          Timex.now()
          |> to_api_format
        )

      {:ok, eq} = Admin.AlertsNA.insert_event(event, quest)

      :dets.insert(:alerts_cache, {"pso2_eq_alert_na", eq.id})
      assert Admin.AlertsNA.is_already_alerted(eq) == true
    end
  end
end
