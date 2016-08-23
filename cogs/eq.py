from discord.ext import commands
import json
import pytz
import datetime


class EmergencyQuest:
    """Commands related to the Emergency Quest alerts"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def eq(self, ctx):
        """EQ-related commands"""

        if ctx.invoked_subcommand is None:
            await self.bot.say('Incorrect subcommand passed. Do ``!help eq`` for the available subcommands.')

    @eq.command()
    async def last(self):
        """Returns last EQ recorded by the bot"""

        eqs = []
        i = 0

        with open('cogs/json/last_eq.json', 'r') as file:
            file = json.load(file)
            eq = file['text'].splitlines()
            eqtime = file['jst']

            for line in eq:
                if 'Emergency Quest' not in line and line != 'Ship%02d: -' % i and line.startswith('Ship'):
                    line = '``' + line.replace(':', ':``')
                    line = line.replace('Ship', 'SHIP ')
                    eqs.append(line)

                if line == 'All ships are in event preparation.':
                    eqs.append('``' + line + '``')

                if line.startswith('[In Progress]'):
                    line = line.replace('[In Progress]', '``IN PROGRESS:``')
                    eqs.append(line)

                if line.startswith('[In Preparation]'):
                    line = line.replace('[In Preparation]', '``IN 1 HOUR:``')
                    eqs.append(line)

                if line.startswith('[1 hour later]'):
                    line = line.replace('[1 hour later]', '``IN 2 HOURS:``')
                    eqs.append(line)

                if line.startswith('[2 hours later]'):
                    line = line.replace('[2 hours later]', '``IN 3 HOURS:``')
                    eqs.append(line)

                i += 1

            string = '\n'.join(eqs)
            message = ':mega: **%s JST Emergency Quest Notice**\n\n%s' % (eqtime, string)

            await self.bot.say(message)

    @eq.command(pass_context=True)
    async def enable(self, ctx):
        """Enables Emergency Quest alerts on this channel."""

        # Loads eq_channels.json file
        with open('cogs/json/eq_channels.json', encoding="utf8") as eq_channels:
            eq_channels = json.load(eq_channels)

        if ctx.message.channel.id not in eq_channels['channels']:
            # Writes channel ID to file
            with open('cogs/json/eq_channels.json', 'w') as outfile:
                eq_channels['channels'].append(ctx.message.channel.id)
                json.dump(eq_channels, outfile)

            await self.bot.say("EQ alerts successfully enabled on this channel.")
        else:
            await self.bot.say('EQ alerts are already enabled on this channel.')

    @eq.command(pass_context=True)
    async def disable(self, ctx):
        """Disables Emergency Quest alerts on this channel."""

        # Loads eq_channels.json file
        with open('cogs/json/eq_channels.json', encoding="utf8") as eq_channels:
            eq_channels = json.load(eq_channels)

        if ctx.message.channel.id in eq_channels['channels']:
            eq_channels['channels'].remove(ctx.message.channel.id)

            # Writes channel ID to file
            with open('cogs/json/eq_channels.json', 'w') as outfile:
                json.dump(eq_channels, outfile)

            await self.bot.say("EQ alerts successfully disabled on this channel.")

        else:
            await self.bot.say("EQ alerts are not enabled on this channel.")


    async def addLFP(self, shipnumber, user):
        with open('cogs/json/lfp.json') as file:
            lfp = json.load(file)

def setup(bot):
    bot.add_cog(EmergencyQuest(bot))
