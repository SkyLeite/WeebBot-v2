defmodule Admin.Alerts.PSO2NAEvent do
  use Ecto.Schema
  import Ecto.Changeset

  schema "pso2_na_events" do
    field(:category_description, :string)
    field(:category_title, :string)
    field(:end_date, :naive_datetime)
    field(:start_date, :naive_datetime)
    field(:title, :string)
    field(:url, :string)

    timestamps()
  end

  @doc false
  def changeset(pso2_na_event, attrs) do
    pso2_na_event
    |> cast(attrs, [:title, :start_date, :end_date, :url, :category_title, :category_description])
    |> validate_required([
      :title,
      :start_date,
      :end_date,
      :url,
      :category_title,
      :category_description
    ])
  end
end
