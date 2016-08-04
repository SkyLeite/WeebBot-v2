import asyncio
import json
import feedparser

# External modules
import aiohttp
import discord


async def checkPSO2EQ(bot):
    while not bot.is_closed:
        await bot.wait_until_ready()

        async with aiohttp.get('http://pso2emq.flyergo.eu/api/v2/') as r:
            if r.status == 200:
                js = await r.json()

                eq = js[0]['text'].splitlines()
                eqtime = js[0]['jst']
                eqs = []
                i = 0

                # Adds EQ data to eqs and formats them properly
                eqatthishour = True
                for line in eq:
                    if 'Emergency Quest' not in line and \
                            line != 'Ship%02d: -' % i and \
                            line.startswith('Ship'):
                        line = '``' + line.replace(':', ':``')
                        line = line.replace('Ship', 'SHIP ')
                        eqs.append(line)

                    if line == 'All ships are in event preparation.':
                        eqs.append('``' + line + '``')

                    if 'no emergency quest' in line:
                        eqatthishour = False

                    if line.startswith('[In Progress]'):
                        line = line.replace('[In Progress]',
                                                           '``IN PROGRESS:``')
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

                    if 'is maintenance' in line:
                        line = line.replace(line,
                                            '``Later: M A I N T E N A N C E``')
                        eqs.append(line)

                    i += 1

                # Loads last_eq.json
                with open('cogs/json/last_eq.json', encoding="utf8") as in_f:
                    last_eq = json.load(in_f)

                # If current EQ is different than last EQ recorded,
                # send alert and update last_eq file
                with open('cogs/json/eq_channels.json',
                                        encoding="utf8") as eq_channels:
                    eq_channels = json.load(eq_channels)

                string = '\n'.join(eqs)
                message = (':mega: **{} JST Emergency Quest '
                           'Notice**\n\n{}'.format(eqtime, string))

                # Checks if current EQ is different from the last one 
                # recorded AND if there is an EQ
                if last_eq['jst'] != eqtime:
                    if not eqatthishour:
                        pass
                    else:

                        # Checks if channel exists, and if it does, 
                        # sends an alert to it
                        await sendAlert(message, bot)

                        # Updates last_eq file
                        with open('cogs/json/last_eq.json', 'w') as file:
                            json.dump(js[0], file)

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
            await bot.send_message(discord.Object(item), message)

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
        games = ['!help', '!donate']
        for gamename in games:
            await bot.change_status(game=discord.Game(name=gamename))

            await asyncio.sleep(120)