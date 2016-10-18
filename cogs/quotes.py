from discord.ext import commands
from random import randint
from settings import admins
import json


class Quotes:
    """Quote commands"""

    def __init__(self, bot):
        self.bot = bot

    def ReadQuotes(self):
        with open("cogs/json/quotes.json") as file:
            data = json.load(file)
            return data

    @commands.group(pass_context=True)
    async def quote(self, ctx):
        if ctx.subcommand_passed != "add":
            try:
                print("try")
                quotes = self.ReadQuotes()
                index = int(ctx.subcommand_passed) - 1

                quote = quotes[index]
                await self.bot.say("(#{}) {}".format(index+1, quote))
            except:
                quotes = self.ReadQuotes()
                index = randint(0,len(quotes)-1)

                quote = quotes[index]
                await self.bot.say("(#{}) {}".format(index+1, quote))

    @quote.command(pass_context=True)
    async def add(self, ctx, *, quote : str):
        if ctx.message.author.id in admins:
            with open("cogs/json/quotes.json", "r") as file:
                quotes = json.load(file)

            quotes.append(quote)

            with open("cogs/json/quotes.json", "w+") as file:
                json.dump(quotes, file)

            await self.bot.say(":envelope_with_arrow: Quote added!")

def setup(bot):
    bot.add_cog(Quotes(bot))
