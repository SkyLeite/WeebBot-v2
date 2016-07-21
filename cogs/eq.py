from discord.ext import commands
import json


class EmergencyQuest:
    """Commands related to Emergency Quest Alerts"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def eq(self, ctx):
        """Does EQ-related things"""

        if ctx.invoked_subcommand is None:
            await self.bot.say('Incorrect subcommand passed.')

    @eq.command(pass_context=True)
    async def enable(self, ctx):
        """Enables Emergency Quest Alerts on this channel."""

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


def setup(bot):
    bot.add_cog(EmergencyQuest(bot))
