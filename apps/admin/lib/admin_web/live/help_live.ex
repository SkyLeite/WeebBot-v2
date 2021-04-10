defmodule AdminWeb.HelpLive do
  use AdminWeb, :live_view

  @impl true
  def mount(_params, _values, socket) do
    questions = [
      %{
        prompt: "How do I configure Weeb Bot on my server?",
        answer: """
        <p>The first step is to add Weeb Bot to your server by <a href="https://discord.com/oauth2/authorize?client_id=198479757900251136&scope=bot&permissions=412736">clicking here.</a></p>

        <p>After that's done, head to <a href="/settings">Weeb Bot's Settings page</a> and select your guild on the left.
        If you see a button telling you to login with Discord, please do so.</p>

        <p>Once you're logged in, select your guild on the left and use the dropdown menus to select the channel each alert should go to.</p>
        """
      },
      %{
        prompt: "Why doesn't my server show up on the server list?",
        answer: """
        <p>
          When you log in, Weeb Bot takes your guild list and only shows the ones you have Administrator rights. Please make sure you have Administrator rights in the server that's missing, log out and log back in.
        </p>
        """
      },
      %{
        prompt: "My server doesn't receive alerts!",
        answer: """
        <p>
          Please make sure Weeb Bot has the appropriate permissions (Send Message and Embed Links) in the channel you selected.
        </p>
        """
      },
      %{
        prompt: "How do I request a new feature for Weeb Bot?",
        answer: """
        <p>
          Post your suggestion on Discord or open an Issue on <a class="text-blue-700 underline" href="https://github.com/RodrigoLeiteF/WeebBot-v2">Weeb Bot's Github repository</a>.
        </p>
        """
      },
      %{
        prompt: "Quest X is not translated!",
        answer: """
        <p>
          The list of quest translations needs to be written manually. This means whenever there's a new quest, it'll show up wth the original Japanese name for a while.
          If you notice an untranslated quest, please open a pull request or send me a message on Discord (preferably with the quest name in English).
        </p>
        """
      }
    ]

    {:ok, socket |> assign(questions: questions)}
  end
end
