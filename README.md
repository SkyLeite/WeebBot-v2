# WeebBot-v2

Hey there. This is Weeb Bot. Currently it's core functionality is alerting for Emergency Quests on Phantasy Star Online 2. Pretty useful for end game grinding.

## How to install

Just clone this repo, edit the settings.py with your API Token and Owner ID, run the bot.py file, and you should be good to go. Requirements are discord.py, ffmpeg and requests.

## Commands

- `!cat`: Replies with a random cat gif and a random cat-related fact..
- `!pokemon name`: Retrives info about the pokemon named `name`.
- `!number`: Cool little fact about a random number. I was bored.
- `!msg message`: (Owner only) Sends `message` to every server your bot is in.
- `!game`: Changes game status to the same game as the owner's.
- `!servers`: Prints every server your bot is in.
- `!eq enable`: Enables EQ Alerts for the channel the message is sent to.
- `!eq disable`: Disables EQ Alerts for the channel the message is sent to.
- `!meme list`: Lists every meme in the ``audio`` folder.
- `!meme play name`: Joins sender's voice channel and plays ``name``.
