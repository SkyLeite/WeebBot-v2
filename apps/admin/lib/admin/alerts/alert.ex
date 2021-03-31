defmodule Admin.Alerts.Alert do
  use Ecto.Schema
  import Ecto.Changeset

  schema "alerts" do
    field :content, :string
    field :type, :string

    timestamps()
  end

  @doc false
  def changeset(alert, attrs) do
    alert
    |> cast(attrs, [:content, :type])
    |> validate_required([:content, :type])
  end
end
