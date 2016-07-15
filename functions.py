import asyncio
import discord
import json
import os
import random
import re
import requests
import urllib.request
import feedparser
from settings import *

global loop

loop = asyncio.get_event_loop()

async def backgroundTask(client):
    while not client.is_closed:
        await client.wait_until_ready()

        await showPSO2EQ(client)
        #await showBumpedArticle(client)
        await changeGame(client)

        await asyncio.sleep(30)  # Task runs every 30 seconds

async def changeGame(client):
    for game in games:
        await client.change_status(discord.Game(name=game), idle=False)

        await asyncio.sleep(30)

    changeGame(client)

async def playMeme(message, client, meme):
    if meme == 'bye':
        channel = message.author.voice_channel
        voice = discord.VoiceClient()
        await voice.disconnect()
    else:
        if message.author.voice_channel is not None:
            channel = message.author.voice_channel
            file = "audio/%s" % meme
            meme = re.sub('\.mp3$', '', meme)

            voice = await client.join_voice_channel(channel)
            player = voice.create_ffmpeg_player(file, after=lambda: disconnect(client, voice))

            player.start()

            await client.send_message(message.channel,
                                      'Playing ``%s`` in ``%s``' % (meme, message.author.voice_channel.name))
        else:
            await client.send_message(message.channel, 'You are not in a voice channel.')


def disconnect(client, voice):
    coro = voice.disconnect()
    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)

    fut.result()


async def addMeme(message, client):
    array = message.content.split(' ')

    try:
        name = array[2]
        url = array[3]

        urllib.request.urlretrieve(url, 'audio/%s.mp3' % name)
        await client.send_message(message.channel, '``%s`` successfully added.' % name)
    except:
        await client.send_message(message.channel, 'Something went wrong. Check your syntax, or try another filehost.')


async def memeList(message, client):
    indir = 'audio/'
    memes = []

    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            j = re.sub('\.mp3$', '', f)
            k = '``%s``' % j
            memes.append(k)

    string = ', '.join(memes)
    await client.send_message(message.channel, '**List of available dank maymays:** \n\n%s' % string)


async def showCat(message, client):
    offset = random.randint(0, 348)

    r = requests.get("https://montanaflynn-cat-overflow.p.mashape.com/?limit=1&offset=%i" % offset,
                     headers={
                         "X-Mashape-Key": "pzH8A2js8xmshCoMqkJkXSCGxzz9p1p1Ue9jsndowy6k3oVmhw",
                         "Accept": "text/plain"
                     }
                     )

    url = str(r.text)
    url2 = url.replace('\n', '')

    gif = url2.split('/')
    gifid = gif[3]
    gif2 = gifid.replace('c', '', 1)

    r = requests.get("http://catfacts-api.appspot.com/api/facts?number=1")
    response = json.loads(r.text)

    fact = response['facts'][0]

    await client.send_message(message.channel, 'http://catoverflow.com/cats/%s.gif \n\nRandom fact: %s' % (gif2, fact))


async def showPokemon(message, client, pokemon):
    try:
        api = "http://pokeapi.co/api/v2/pokemon/%s/" % pokemon.lower()

        future1 = loop.run_in_executor(None, requests.get, api)
        r = await future1

        response = json.loads(r.text)
        abilities = []
        types = []

        # Assings types and abilities to lists
        for i in response['abilities']:
            abilities.append(i['ability']['name'])

        for i in response['types']:
            types.append(i['type']['name'])

        # Converts lists to human readable strings
        ability = ', '.join(abilities)
        type = ', '.join(types)

        # Assigns data to variables for easier reading
        name = response['name']
        weight = response['weight']
        height = response['height']
        speed = response['stats'][0]['base_stat']
        spdef = response['stats'][1]['base_stat']
        spatk = response['stats'][2]['base_stat']
        defense = response['stats'][3]['base_stat']
        attack = response['stats'][4]['base_stat']
        hp = response['stats'][5]['base_stat']
        sprite = response['sprites']['front_default']
        shiny = response['sprites']['front_shiny']

        string = '**Name:** %s\n**Type:** %s\n**Weight:** %s\n**Height:** %s\n**Abilities:** %s\n**Stats:**\n  Speed: %s\n  Special Defense: %s\n  Special Attack: %s\n  Defense: %s\n  Attack: %s\n  HP: %s\n**Sprite (Normal):** %s\n**Sprite (Shiny):** %s' % (
            name, type, weight, height, ability, speed, spdef, spatk, defense, attack, hp, sprite, shiny)
        await client.send_message(message.channel, string)
    except:
        await client.send_message(message.channel, 'Could not find a Pokémon with the name ``%s``' % pokemon)


async def showPSO2EQ(client):
    # Async shit
    future1 = loop.run_in_executor(None, requests.get, 'http://pso2emq.flyergo.eu/api/v2/')
    r = await future1

    # Loads EQ data
    r2 = json.loads(r.text)
    eq = r2[0]['text'].splitlines()
    eqtime = r2[0]['jst']
    eqs = []
    i = 0

    # Adds EQ data to eqs and formats them properly
    EqAtThisHour = 'true'
    for line in eq:
        if 'Emergency Quest' not in line and line != 'Ship%02d: -' % i and line.startswith('Ship'):
            line = '``' + line.replace(':', ':``')
            line = line.replace('Ship', 'SHIP ')
            eqs.append(line)

        if line == 'All ships are in event preparation.':
            eqs.append('``' + line + '``')

        if 'no emergency quest' in line:
            EqAtThisHour = 'false'

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

        i = i + 1

    # Loads last_eq.json
    with open('json/last_eq.json', encoding="utf8") as in_f:
        last_eq = json.load(in_f)

    # If current EQ is different than last EQ recorded, send alert and update last_eq file
    with open('json/eq_channels.json', encoding="utf8") as eq_channels:
        eq_channels = json.load(eq_channels)

    string = '\n'.join(eqs)
    message = ':mega: **%s JST Emergency Quest Notice**\n\n%s' % (eqtime, string)
    if last_eq['jst'] != eqtime:
        if EqAtThisHour == 'false':
            pass
        else:
            for item in eq_channels['channels']:
                if client.get_channel(item):
                    channel = client.get_channel(item)

                    try:
                        await client.send_message(discord.Object(item), message)
                    except:
                        print('Something went wrong when sending a message to "{}"'.format(channel.server.name))
                    if client.get_channel(test_channel):
                        await client.send_message(discord.Object(test_channel), 'EQ Alert sent to: ``%s`` (%s)' % (
                        channel.server.name, channel.server.id))
                else:
                    msg = ':mega: **Alert!**\n Channel %s does not exist. Removing...' % item
                    if client.get_channel(test_channel):
                        await client.send_message(discord.Object(test_channel), msg)
                    await removeEQChannel(item)
            if client.get_channel(test_channel):
                await client.send_message(discord.Object(test_channel), '-------------------')

            with open('json/last_eq.json', 'w') as file:
                json.dump(r2[0], file)

async def showBumpedArticle(client):
    d = feedparser.parse('http://bumped.org/psublog/feed/atom')
    tags = []

    articleTitle = d['entries'][0]['title']
    articleLink = d['entries'][0]['links'][0]['href']
    articleSummary = d['entries'][0]['summary']
    articleId = d['entries'][0]['id']

    for item in d['entries'][0]['tags']:
        tags.append(item['term'])

    tags = ' ,'.join(tags)

    message = ':mega: **New Bumped article!** \n``TITLE:`` {} \n``TAGS:`` {} \n``SUMMARY:`` {} \n``LINK:`` {}'.format(articleTitle, tags, articleSummary, articleLink)

    # Loads last_article.json
    with open('json/last_article.json', encoding="utf8") as file:
        last_article = json.load(file)

    # Loads eq_channels.json
    with open('json/eq_channels.json', encoding="utf8") as file:
        eq_channels = json.load(file)

    # If last article is different than the one in last_article.json, send alert and update json file
    if last_article['id'] != articleId:
        for item in eq_channels['channels']:
            if client.get_channel(item):
                channel = client.get_channel(item)

                await client.send_message(discord.Object(item), message)
                if client.get_channel(test_channel):
                    await client.send_message(discord.Object(test_channel), 'EQ Alert sent to: ``%s`` (%s)' % (
                        channel.server.name, channel.server.id))
            else:
                msg = ':mega: **Alert!**\n Channel %s does not exist. Removing...' % item
                if client.get_channel(test_channel):
                    await client.send_message(discord.Object(test_channel), msg)
                await removeEQChannel(item)
        if client.get_channel(test_channel):
            await client.send_message(discord.Object(test_channel), '-------------------')

        with open('json/last_article.json', 'w') as file:
            last_article = {"id" : articleId}
            json.dump(last_article, file)


async def showLastEQ(client, message):
    eqs = []

    with open('json/last_eq.json', 'r') as file:
        eq = json.load(file)

    eqtime = eq['jst']
    i = 0

    # Adds EQ data to eqs and formats them properly
    for line in eq['text'].splitlines():
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

        if line == "1 hour later is maintenance.":
            line = line.replace('1 hour later is maintenance.', 'NotLikeThis ``M A I N T E N A N C E`` NotLikeThis')
            eqs.append(line)

        i = i + 1

    try:
        string = '\n'.join(eqs)
        lasteq = ':mega: **%02d JST Emergency Quest Notice**\n\n%s' % (eqtime, string)
        await client.send_message(message.channel, lasteq)
    except:
        pass


async def addEQChannel(message, client):
    # Loads eq_channels.json file
    with open('json/eq_channels.json', encoding="utf8") as eq_channels:
        eq_channels = json.load(eq_channels)

    if message.channel.id not in eq_channels['channels']:
        # Writes channel ID to file
        with open('json/eq_channels.json', 'w') as outfile:
            eq_channels['channels'].append(message.channel.id)
            json.dump(eq_channels, outfile)

        await client.send_message(message.channel, "EQ Alerts successfully enabled on this channel.")
    else:
        await client.send_message(message.channel, 'EQ Alerts are already enabled on this channel.')


async def removeEQChannel(id):
    # Loads eq_channels.json file
    with open('json/eq_channels.json', encoding="utf8") as eq_channels:
        eq_channels = json.load(eq_channels)

    if id in eq_channels['channels']:
        eq_channels['channels'].remove(id)

    # Writes channel ID to file
    with open('json/eq_channels.json', 'w') as outfile:
        json.dump(eq_channels, outfile)


async def showHelp(client, message):
    with open('json/help.json') as file:
        help = json.load(file)

    commands = []

    for item in help['commands']:
        commands.append(item + ": " + help['commands'][item])

    commands = "\n".join(commands)
    string = ":mega: **These are the current available commands:**\n{}".format(commands)

    await client.send_message(message.channel, string)

async def leafyTitle(message, client):
    with open('json/leafy.json') as file:
        leafy = json.loads(file)

    first = leafy['first'][random.randint(0, len(leafy['first'])-1)]
    middle = leafy['middle'][random.randint(0, len(leafy['middle'])-1)]
    last = leafy['last'][random.randint(0, len(leafy['last'])-1)]

    await client.send_message(message.channel, 'THE %s %s %s' % (first, middle, last))

#async def searchManga(message, client):
#    manga = message.content.split(' ', 1)[1]
#    r = requests.get("https://doodle-manga-scraper.p.mashape.com/mangareader.net/search?cover=0&info=0&l=3&q={}".format(manga),
#                    headers={
#                        "X-Mashape-Key": "pzH8A2js8xmshCoMqkJkXSCGxzz9p1p1Ue9jsndowy6k3oVmhw",
#                        "Accept": "text/plain"
#                        }
#                    )
#
#    result = json.loads(r.text)
#
#    return(result[0][name], result[0]['mangaId'])


#async def addManga(message, client):
#    manga = message.content.split(' ', 1)[1]
#    r = requests.get("https://doodle-manga-scraper.p.mashape.com/mangareader.net/search?cover=0&info=0&l=10&q={}".format(manga),
#                     headers={
#                         "X-Mashape-Key": "pzH8A2js8xmshCoMqkJkXSCGxzz9p1p1Ue9jsndowy6k3oVmhw",
#                         "Accept": "text/plain"
#                        }
#                     )
#
#    with open('json/manga.json', 'r') as file:
#        mangaList = json.load(file)
#
#    with open('json/manga.json', 'w') as file:
#        mangaList['user'].update({message.author.id : manga})
#        json.dump(mangaList, file, sort_keys=True, indent=4)
#
#    response = json.loads(r.text)
#
#    await client.send_message(message.channel, message.author.id)
#    await client.send_message(message.server.get_member(message.author.id), 'hi')

