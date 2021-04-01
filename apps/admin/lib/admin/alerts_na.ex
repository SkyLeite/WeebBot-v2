defmodule Admin.AlertsNA do
  def update_na_schedule do
    fetch_na_schedule()
    |> Enum.each(&process_schedule_quest/1)
  end

  defp fetch_na_schedule do
    with {:ok, %HTTPoison.Response{status_code: 302, body: body}} <-
           HTTPoison.get("https://pso2.com/news/LoadScheduleCampaigns", []),
         schedule when is_list(schedule) <- Poison.decode!(body) do
      schedule
    else
      {:ok, %HTTPoison.Response{}} -> nil
    end
  end

  defp process_schedule_quest(quest) do
    quest
    |> Map.get("events")
    |> Enum.each(fn event -> insert_event(event, quest) end)
  end

  defp insert_event(event, quest) do
    %Admin.Alerts.PSO2NAEvent{}
    |> Admin.Alerts.PSO2NAEvent.changeset(%{
      title: quest["title"],
      url: quest["route"],
      start_date: event["startDate"],
      end_date: event["endDate"],
      category_title: quest["category"]["title"],
      category_description: quest["category"]["description"]
    })
    |> Admin.Repo.insert(
      on_conflict: {:replace_all_except, [:title]},
      conflict_target: [:title, :start_date, :end_date]
    )
  end
end
