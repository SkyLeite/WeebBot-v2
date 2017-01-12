from discord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
import discord
import pytz
import aiohttp


class GDQ:
    """Games Done Quick commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def gdq(self, ctx):
        """Displays Games Done Quick information."""

        if ctx.invoked_subcommand is None:
            print('hi')
            #GDQ information

    async def getSoup(self):
        async with aiohttp.ClientSession() as session:
            try:
                r = await session.get("https://gamesdonequick.com/tracker/runs/agdq2017")
                if r.status == 200:
                    js = await r.text()
                    soup = BeautifulSoup(js, 'html.parser')

                    return soup

            except:
                print('noo')

    @gdq.command()
    async def games(self):
        """Previous, current and next games to be played on stream."""

        html = await self.getSoup()

        games = html.find_all("tr", class_="small")

        for game in games:
            info = game.find_all("td")

            name = info[0].a.text
            runner = info[1].text.replace("\n", "")
            start = datetime.strptime(info[3].span.text, "%m/%d/%Y %H:%M:%S %z").replace(tzinfo=pytz.timezone('US/Eastern'))
            finish = datetime.strptime(info[4].span.text, "%m/%d/%Y %H:%M:%S %z").replace(tzinfo=pytz.timezone('US/Eastern'))
            now = datetime.utcnow().replace(tzinfo=pytz.timezone('US/Eastern'))

            if start <= now <= finish:
                nextGame = games[games.index(game) + 1]
                nextInfo = nextGame.find_all("td")
                nextName = nextInfo[0].a.text
                nextRunner = nextInfo[1].text.replace("\n", "")

                data = discord.Embed(colour=discord.Colour.red())
                data.set_author(name="Games Done Quick", icon_url="http://lh3.googleusercontent.com/9KEhjD4aNfUYiAbwNcyWooXRjus_O_z1x9cItGEIIlommTRAgxHXfG1pSuJdIsMltDg=w300")

                data.add_field(name="Current Game", value="{}\nRunner(s): {}".format(name, runner))
                data.add_field(name="Next Game", value="{}\nRunner(s): {}".format(nextName, nextRunner))

                await self.bot.say(embed=data)

                #await self.bot.say("Current game: {} by {}\nNext game: {} by {}".format(name, runner, nextName, nextRunner))

def setup(bot):
    bot.add_cog(GDQ(bot))
