from discord.ext import commands
import os
import re
import discord
import aiohttp


class Macro:
    """Image macros!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def macro(self, ctx):
        """Displays a macro."""

        if (ctx.subcommand_passed != 'add') and (ctx.subcommand_passed != 'remove') and (ctx.subcommand_passed != 'remove'):
            for root, dirs, filenames in os.walk('cogs/macro/'):
                for f in filenames:
                    filename = os.path.splitext(f)[0]
                    if ctx.subcommand_passed == filename:
                        await self.bot.send_file(ctx.message.channel, 'cogs/macro/{}'.format(f))

    @macro.command()
    async def list(self):
        """Lists every macro available."""

        macros = []

        for root, dirs, filenames in os.walk('cogs/macro/'):
            for f in filenames:
                filename = os.path.splitext(f)[0]
                macros.append('``' + filename + '``')

        string = ', '.join(macros)
        await self.bot.say(':mega: **List of available macros:** \n{}'.format(string))

def setup(bot):
    bot.add_cog(Macro(bot))