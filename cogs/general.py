from discord.ext import commands
import discord
import aiohttp


class General:
    """General commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def add(self, left: int, right: int):
        """Adds two numbers together"""

        await self.bot.say(left + right)

    @commands.group()
    async def cat(self):
        """Shows random cat gif"""

        async with aiohttp.ClientSession() as session:
            r = await session.get("http://edgecats.net/random")
            if r.status == 200:
                js = await r.text()
                await self.bot.say(js)

    @commands.group()
    async def donate(self):
        """Server costs are a thing. Help me out fam!"""

        await self.bot.say('Thanks for considering contributing to my project! If you wish to proceed with the donation,'
                           'go to http://kazesenoue.moe/donate.html .')

    @commands.group(pass_context=True)
    async def ping(self, ctx):
        """Pong!"""

        await self.bot.say('Pong! Channel ID: {}'.format(ctx.message.channel.id))

    @commands.group()
    async def join(self):
        """Returns information on how to add the bot to your server."""

        botInfo = await self.bot.application_info()
        oauthlink = discord.utils.oauth_url(botInfo.id)
        await self.bot.say('To invite Weeb Bot to your server, simply click the following link: {}'.format(oauthlink))


def setup(bot):
    bot.add_cog(General(bot))
