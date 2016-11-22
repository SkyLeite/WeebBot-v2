from discord.ext import commands
import json, aiohttp, discord


class PSO2:
    """Commands related to the Emergency Quest alerts"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pso2(self):
        data = discord.Embed(colour=discord.Colour.red())
        data.set_author(name="Phantasy Star Online 2", icon_url="http://img.informer.com/icons/png/48/3365/3365560.png")

        info = "[News](http://bumped.org/psublog)\n[Reddit](http://reddit.com/r/pso2)\n[Guides](http://fulldive.nu)\n[Forums](http://pso-world.com)\n[Wiki](https://pso2.arks-visiphone.com)"
        data.add_field(name="Information", value=info)

        downloads = "[Launcher](http://arks-layer.com)\n[Mods](https://goo.gl/M8PpWh)"
        data.add_field(name="Downloads", value=downloads)

        translations = "English Patch: :ballot_box_with_check:\nStory Patch: :ballot_box_with_check:\nItem Patch: :ballot_box_with_check:"
        data.add_field(name="Translations", value=translations)

        data.set_footer(text="Those are hyperlinks. Give them a click.")

        await self.bot.say(embed=data)

    @commands.command()
    async def builds(self):
        data = discord.Embed(colour=discord.Colour.red())
        data.set_author(name="Meta Builds", icon_url="http://img.informer.com/icons/png/48/3365/3365560.png")

        hunter = "[Hu/Fi](https://goo.gl/CA7Eos)\n[Hu/Br (Dragonslayer)](https://goo.gl/3SkU17)"
        data.add_field(name="Hunter", value=hunter)

        ranger = "[Ra/Hu](https://goo.gl/86sIbw)\n[Ra/Br](https://goo.gl/6vgczQ)"
        data.add_field(name="Ranger", value=ranger)

        force = "[Fo/Te (Fire/Dark)](https://goo.gl/98Sed0)\n[Fo/Te (Ice/Light)](https://goo.gl/VLz3nA)"
        data.add_field(name="Force", value=force)

        fighter = "[Fi/Hu](https://goo.gl/7sdiyQ)"
        data.add_field(name="Fighter", value=fighter)

        gunner = "[Gu/Hu](https://goo.gl/TZf5Hk)\n[Gu/Ra](https://goo.gl/JNz9tM)"
        data.add_field(name="Gunner", value=gunner)

        techer = "[Te/Br](https://goo.gl/miAabv)\n[Te/Hu](https://goo.gl/ggHROJ)"
        data.add_field(name="Techer", value=techer)

        bouncer = "[Bo/Hu (Dual Blades)](https://goo.gl/pexGnC)\n[Bo/Hu (Jet Boots)](https://goo.gl/b3lmg6)\n[Bo/Hu (Hybrid)](https://goo.gl/IcWGLM)"
        data.add_field(name="Bouncer", value=bouncer)

        await self.bot.say(embed=data)

    @commands.group(pass_context=True)
    async def eq(self, ctx):
        """EQ-related commands"""

        if ctx.invoked_subcommand is None:
            await self.bot.say('Incorrect subcommand passed. Do ``+help eq`` for the available subcommands.')

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

    @commands.command(pass_context=True)
    async def item(self, ctx, *, itemname : str):
        """Looks up JP name of an item."""

        async with aiohttp.ClientSession() as session:
            url = "http://db.kakia.org/item/search?name={0}".format(itemname.replace(" ", "%20"))
            r = await session.get(url)
            if r.status == 200:
                js = await r.json()
                iteminfo = []

                if js:
                    if len(js) > 1 and len(js) <= 11:
                        for result in js:
                            if result["EnName"]:
                                iteminfo.append("``EN Name:`` {}".format(result["EnName"]))

                        string = "\n".join(iteminfo)
                        message = "{} Found multiple items matching ``{}``. Try again with one of these names:\n{}".format(ctx.message.author.mention, itemname, string)
                        await self.bot.say(message)

                    elif len(js) > 11:
                        i = 0
                        for result in js:
                            i+= 1
                            if result["EnName"] and i < 11:
                                iteminfo.append("``EN Name:`` {}".format(result["EnName"]))

                        string = "\n".join(iteminfo)
                        message = "{} Too many items matching ``{}``. Here are the first 11 results:\n{}".format(
                            ctx.message.author.mention, itemname, string)
                        await self.bot.say(message)

                    else:
                        if js[0]["Img"]:
                            iteminfo.append({"``IMG:`` http://db.kakia.org/{}".format(js[0]["Img"])})
                        if js[0]["JpName"]:
                            iteminfo.append("``JP Name:`` {}".format(js[0]["JpName"]))
                        if js[0]["EnName"]:
                            iteminfo.append("``EN Name:`` {}".format(js[0]["EnName"]))
                        if js[0]["EnDesc"]:
                            iteminfo.append("``EN Description:`` {}".format(js[0]["EnDesc"].replace("\\n", " ")))

                        string = "\n".join(iteminfo)
                        await self.bot.say("{}\n{}".format(ctx.message.author.mention, string))

                else:
                    await self.bot.say("{} Could not find that item :(".format(ctx.message.author.mention))

def setup(bot):
    bot.add_cog(PSO2(bot))
