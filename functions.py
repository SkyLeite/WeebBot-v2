import asyncio
import json

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

                    eq = js[0]['text'].splitlines()
                    eqtime = js[0]['jst']
                    equtc = (eqtime - 9) % 24
                    eqpst = (eqtime - 16) % 24
                    eqest = (eqtime - 13) % 24
                    eqs = []
                    i = 0

                    # Adds EQ data to eqs and formats them properly
                    eqatthishour = True
                    for line in eq:
                        if line.startswith('{0:02d}:'.format(i)):
                            line = '``SHIP ' + line.replace(':', ':`` ')
                            eqs.append(line)

                        elif 'Emergency Quest' not in line and line != '%02d: -' % i:
                            eqs.append(line)

                        elif line == 'All ships are in event preparation.':
                            eqs.append('``' + line + '``')

                        elif 'no report at all ships' in line:
                            eqatthishour = False

                        elif '[In Preparation]' in line:
                            line = line.replace('[In Preparation]', '``IN PREPARATION:``')
                            eqs.append(line)

                        elif '[In Progress]' in line:
                            line = line.replace('[In Progress]', '``IN PROGRESS:``')
                            eqs.append(line)

                        i += 1

                    # Loads last_eq.json
                    with open('cogs/json/last_eq.json', encoding="utf8") as in_f:
                        last_eq = json.load(in_f)

                    #Builds string
                    string = '\n'.join(eqs)

                    donation = ':love_letter: Support me on Patreon! <http://patreon.kazesenoue.moe>'

                    message = (':arrow_right: **Emergency Quest '
                               'Notice\n:watch:{:02d} JST / {:02d} UTC /'
                               ' {:02d} PST / {:02d} EST**\n\n{}\n\n{}'.format(eqtime, equtc, eqpst, eqest, string, donation))

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
            await bot.change_status(game=discord.Game(name=gamename))

            await asyncio.sleep(120)
