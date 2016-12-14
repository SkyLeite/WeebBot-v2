import asyncio
import json
import re
import pytz
from datetime import datetime, timedelta

# External modules
import aiohttp
import discord
import feedparser


async def checkPSO2EQ(bot):
    while not bot.is_closed:
        await bot.wait_until_ready()

        async with aiohttp.ClientSession() as session:
            try:
                r = await session.get("http://pso2emq.flyergo.eu/api/v2/")
                if r.status == 200:
                    js = await r.json()

                    eqtime = js[0]['jst']
                    equtc = (eqtime - 9) % 24
                    eqpst = (eqtime - 16) % 24
                    eqest = (eqtime - 13) % 24
                    eqgmt = (eqtime - 6) % 24
                    eqs = []
                    rodos = []

                    # Adds EQ data to eqs and formats them properly
                    shipEQ = re.compile(r'(\d*:[^0-9-]+)')
                    announcement = re.compile(r'(\[\D*\].*)')
                    allShipsEQ = re.compile(r'(^\d+:\d+.*)')

                    for line in js[0]['text'].splitlines():
                        try:
                            if shipEQ.match(line):
                                string = shipEQ.match(line).group(0)
                                eqs.append('``SHIP ' + string.replace(':', ':`` '))
                            elif announcement.match(line):
                                string = announcement.match(line).group(0)
                                eqs.append(string.replace("[", "``").replace("]", "``"))
                            elif allShipsEQ.match(line):
                                string = allShipsEQ.match(line).group(0)
                                eqs.append("``ALL SHIPS:`` " + string)
                        except Exception as e:
                            print(e)
                            pass

                    #Checks if there's a rodos daily going on
                    order = ["Defeat: Bal Rodos(VH)", "2016-08-03", [3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]]
                    orderDate = datetime.strptime(order[1], "%Y-%m-%d")
                    jstNow = datetime.utcnow().replace(tzinfo=pytz.timezone('Asia/Tokyo')).date()

                    for i in range(0, 50):
                        for interval in order[2]:
                            orderDate = orderDate + timedelta(days=interval)
                            if orderDate.date() == jstNow:
                                rodos.append(":fishing_pole_and_fish: Today is VH Bal Rodos day!")
                            else:
                                if (orderDate.date() > jstNow):
                                    rodos.append(":fishing_pole_and_fish: ``Next VH Rodos:`` {}".format(orderDate.date()))
                                    break
                        break

                    # Loads last_eq.json
                    with open('cogs/json/last_eq.json', encoding="utf8") as in_f:
                        last_eq = json.load(in_f)

                    #Builds string
                    string = '\n'.join(eqs)
                    rodos2 = '\n'.join(rodos)

                    donation = ':love_letter: Support me on Patreon! <http://patreon.kazesenoue.moe>'

                    message = (':arrow_right: **Emergency Quest '
                               'Notice\n:watch:{:02d} JST / {:02d} UTC /'
                               ' {:02d} PST / {:02d} EST / {:02d} GMT +3**\n\n{}\n\n{}\n\n{}'.format(eqtime, equtc, eqpst, eqest, eqgmt, string, rodos2, donation))

                    # Checks if current EQ is different from the last one
                    # recorded AND if there is an EQ
                    if last_eq['jst'] != eqtime:
                        if not eqs:
                            pass
                        else:
                            await sendAlert(message, bot)

                        # Updates last_eq file
                        with open('cogs/json/last_eq.json', 'w') as file:
                            json.dump(js[0], file)

            except Exception as e:
                await bot.send_message(discord.Object("198483667289374720"), repr(e))
                continue

        await asyncio.sleep(5)

async def checkBumpedArticle(bot):
    while not bot.is_closed:
        await bot.wait_until_ready()
        async with aiohttp.get('http://bumped.org/psublog/feed/atom') as r:
            if r.status == 200:
                feed = await r.text()
                d = feedparser.parse(feed)

                articleTitle = d['entries'][0]['title']
                articleLink = d['entries'][0]['links'][0]['href']
                articleSummary = d['entries'][0]['summary']
                articleId = d['entries'][0]['id']

                message = ':mega: **New Bumped article!** \n``TITLE:`` {} \n``LINK:`` {}'.format(
                    articleTitle, articleLink)

                # Loads last_article.json
                with open('cogs/json/last_article.json', encoding="utf8") as file:
                    last_article = json.load(file)

                if articleId != last_article['id']:
                    await sendAlert(message, bot)

                    with open('cogs/json/last_article.json', 'w') as file:
                        last_article = {"id": articleId}
                        json.dump(last_article, file)

                else:
                    pass

        await asyncio.sleep(5)


async def sendAlert(message, bot):
    # Loads eq_channels.json
    with open('cogs/json/eq_channels.json', encoding="utf8") as file:
        eq_channels = json.load(file)

    for item in eq_channels['channels']:
        if bot.get_channel(item):
            try:
                await bot.send_message(discord.Object(item), message)
            except:
                pass


async def removeEQChannel(chID):
    # Loads eq_channels.json file
    with open('cogs/json/eq_channels.json', encoding="utf8") as eq_channels:
        eq_channels = json.load(eq_channels)

    if chID in eq_channels['channels']:
        eq_channels['channels'].remove(chID)

    # Writes channel ID to file
    with open('cogs/json/eq_channels.json', 'w') as outfile:
        json.dump(eq_channels, outfile)


async def changeGame(bot):
    while not bot.is_closed:
        await bot.wait_until_ready()
        games = ['+help', '+donate', 'Prefix is +']
        for gamename in games:
            await bot.change_presence(game=discord.Game(name=gamename))

            await asyncio.sleep(120)


async def monitorEQs(bot):
    while not bot.is_closed:
        await bot.wait_until_ready()

        async with aiohttp.ClientSession() as session:
            r = await session.get("http://pso2.kazesenoue.moe/eq/")
            if r.status == 200:
                js = await r.json()

                with open('cogs/json/last_eq_lfp.json', 'r') as file:
                    last_eq = json.load(file)

                if last_eq != js[0]:
                    with open('cogs/json/groups.json', 'r') as file:
                        groups = json.load(file)

                    for eq in js[0]['eqs']:
                        groups.append({"eq" : eq['name'], "group" : [], "ship" : int(eq['ship'])})

                    with open('cogs/json/groups.json', 'w+') as file:
                        json.dump(groups, file, sort_keys=True, indent=4)

                    with open('cogs/json/last_eq_lfp.json', 'w+') as file:
                        json.dump(js[0], file, sort_keys=True, indent=4)

                    await asyncio.sleep(30)

                    #Terminates every group
                    server = bot.get_server("171412745302835201")
                    for i in range(1, 4):
                        #Deletes channels and roles
                        role = discord.utils.get(server.roles, name='Ship {}'.format(i))
                        await bot.delete_role(server, role)

                        channel = discord.utils.get(server.channels, name='ship-{}'.format(i))
                        await bot.delete_channel(channel)

                        #Creates them back
                        role = await bot.create_role(server, name='Ship {}'.format(i))

                        everyone = discord.PermissionOverwrite(read_messages=False)
                        rolePerms = discord.PermissionOverwrite(read_messages=True)
                        await bot.create_channel(server, 'ship-{}'.format(i), (server.default_role, everyone), (role, rolePerms))

                    #Wipes groups.json
                    with open('cogs/json/groups.json', 'w+') as file:
                        json.dump([], file)

        await asyncio.sleep(10)