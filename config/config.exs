# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
use Mix.Config

config :admin,
  ecto_repos: [Admin.Repo]

# Configures the endpoint
config :admin, AdminWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "KvYuCCn1VdKyiIkUCIDEKV3yt35OWGEn4RjmZgDeeBdDjM5rpebMMWMQPKEodzwC",
  render_errors: [view: AdminWeb.ErrorView, accepts: ~w(html json), layout: false],
  pubsub_server: Admin.PubSub,
  live_view: [signing_salt: "jRmuPRdM"]

config :ueberauth, Ueberauth,
  providers: [
    discord: {Ueberauth.Strategy.Discord, [default_scope: "identify email guilds"]}
  ]

config :admin, AdminWeb.Endpoint,
  http: [
    protocol_options: [
      max_header_value_length: 8192
    ]
  ]

config :admin, Admin.Scheduler,
  jobs: [
    {"*/5 * * * *"}, {Admin.Alerts, :check_twitter, []}},
    {"0 */12 * * *"}, {Admin.AlertsNA, :update_na_schedule, []}},
    {"*/5 * * * *"}, {Admin.AlertsNA, :alert_channels, []}}
  ]

config :extwitter, :oauth,
  consumer_key: "K9m4Cjhzd3r0kpx25RHUo5J6r",
  consumer_secret: "BWLGW4hD219uBchshogvnMEhfXp5zKvmLyj9fEupXzIOzpNkOu",
  access_token: "1251460537998852097-Q2JHXSwtGNfNSXyWloOUcsuzq9CtBm",
  access_token_secret: "LPJ2OzdubN3lE4VPHmGQocHbbZkSq8HTPILYy2teShxGE"

config :nostrum,
  # The number of shards you want to run your bot under, or :auto.
  num_shards: :auto

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
