# WeebBot-v2
Discord bot used for alerting on Emergency Quests on Phantasy Star Online 2

Hey there, this is Weeb Bot, a Discord bot who's main functionality is to alert for Emergency Quests that happen on Phantasy Star Online 2. Previously on Python, it was rewritten on Javascript (using Discord.JS) for better performance.

## How to use

If you simply wish to have the bot on your server, just [click here](https://discordapp.com/oauth2/authorize?client_id=180088767669993474&scope=bot&permissions=0) and use the `+alerts` command to enable the EQ alerts.

## Dependencies

If you want to re-host the bot, you'll need to edit the `config.json` file with your bot's token, and install the following dependencies:

- (npm install) `request`
- (npm install) `discord.js`
- (npm install) `discord.js-commando`

Alternatively, you can `cd` to the bot's directory and run `npm install` to let npm take care of that for you.

## Commands

#### General

- `ping`: Pong!
- `cat`: Displays a random cat gif.

#### Phantasy Star Online 2

- `pso2`: General information regarding the game.
- `item <itemname>`: Looks up the japanese name of `<itemname>`.
- `alerts`: Enables EQ alerts.
- `dalerts`: Disables EQ alerts.
- `builds`: Displays current meta builds.

#### Shadowverse

- `card <cardname>`: Returns information about `<cardname>`

#### Settings 

All the following commands can be run by mentioning the bot and only work for server admins.

- `groups`: Lists all command groups.
- `prefix <prefix>`: Changes the bot's prefix to `<prefix>`. (Example: `@Weeb Bot prefix -` changes the prefix to `-`)
- `enable <group or command>`: Enables `<group or command>` to be used in this server.
- `disable <group or command>`: Disables `<group or command>` to be used in this server.

## Support

If you have any questions or something went wrong, please contact me at `Kaze ⚥#2125` or on [the bot's server](https://discord.gg/0xMXCNAFbH032Ig1).

## Donations

If you wish to support the creation of this bot, just say thanks :p
