# Script for populating the database. You can run it as:
#
#     mix run priv/repo/seeds.exs
#
# Inside the script, you can read and write to any of your
# repositories directly:
#
#     Admin.Repo.insert!(%Admin.SomeSchema{})
#
# We recommend using the bang functions (`insert!`, `update!`
# and so on) as they will fail if something goes wrong.

Admin.Repo.insert!(
  %Admin.Guilds.AvailableSetting{
    id: 1,
    key: "alert_channel_id",
    label: "Alert Channel ID",
    type: "string"
  },
  on_conflict: :nothing
)

# Admin.Repo.insert!(
#   %Admin.Guilds.AvailableSetting{
#     id: 2,
#     key: "role_mention_id",
#     label: "Role Mention ID",
#     type: "string"
#   },
#   on_conflict: :nothing
# )
