defmodule Admin.Repo do
  use Ecto.Repo,
    otp_app: :admin,
    adapter: Ecto.Adapters.Postgres
end
