import asyncio
import discord
import json
import os
import random
import re
import requests
import urllib.request
from settings import *

global loop

loop = asyncio.get_event_loop()


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


async def showNumberTrivia(message, client):
    r = requests.get("https://numbersapi.p.mashape.com/random/trivia?json=true",
                     headers={
                         "X-Mashape-Key": "Q7n8VApOzPmshmeZQNtthye630hmp1LDw0HjsnZIoR8eOu4JX6",
                         "Accept": "text/plain"
                     }
                     )

    response = json.loads(r.text)
    await client.send_message(message.channel, response['text'])


async def ping(message, client):
    await client.send_message(message.channel, 'Pong!')
      

async def showPSO2EQ(client):
    while not client.is_closed:
        # Async shit to use requests
        future1 = loop.run_in_executor(None, requests.get, 'http://pso2emq.flyergo.eu/api/v2/')
        r = await future1

        # Loads EQ data
        r2 = json.loads(r.text)
        eq = r2[0]['text'].splitlines()
        eqtime = r2[0]['jst']
        eqs = []
        i = 0

        # Adds EQ data to eqs and formats them properly
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

            i = i + 1

        # Loads last_eq.json
        with open('last_eq.json', encoding="utf8") as in_f:
            last_eq = json.load(in_f)

        # If current EQ is different than last EQ recorded, send alert and update last_eq file
        if last_eq['jst'] != eqtime:
            with open('eq_channels.json', encoding="utf8") as eq_channels:
                eq_channels = json.load(eq_channels)

            try:
                string = '\n'.join(eqs)
                message = ':mega: **%s JST Emergency Quest Notice**\n\n%s' % (eqtime, string)
                for item in eq_channels['channels']:
                    try:
                        channel = client.get_channel(item)
                        
                        await client.send_message(discord.Object(item), message)
                        await client.send_message(discord.Object(test_channel), 'EQ Alert sent to: ``%s`` (%s)' % (channel.server.name, channel.server.id))
                    except:
                        try:
                            await client.send_message(discord.Object(test_channel), ':mega: **Alert!**\n Channel %s does not exist.' % (item))
                await client.send_message(discord.Object(test_channel), '-------------------')
            except Exception as exception:
                print(exception)
                pass

            with open('last_eq.json', 'w') as out_f:
                json.dump(r2[0], out_f)

        await asyncio.sleep(3)  # Task runs every 300 seconds


async def showLastEQ(client, message):
    eqs = []

    with open('last_eq.json', 'r') as file:
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

        i = i + 1

    try:
        string = '\n'.join(eqs)
        lasteq = ':mega: **%02d JST Emergency Quest Notice**\n\n%s' % (eqtime, string)
        await client.send_message(message.channel, lasteq)
    except:
        pass


async def addEQChannel(message, client):
    # Loads eq_channels.json file
    with open('eq_channels.json', encoding="utf8") as eq_channels:
        eq_channels = json.load(eq_channels)

    if message.channel.id not in eq_channels['channels']:
        # Writes channel ID to file
        with open('eq_channels.json', 'w') as outfile:
            eq_channels['channels'].append(message.channel.id)
            json.dump(eq_channels, outfile)

        await client.send_message(message.channel, "EQ Alerts successfully enabled on this channel.")
    else:
        await client.send_message(message.channel, 'EQ Alerts are already enabled on this channel.')


async def removeEQChannel(message, client):
    # Loads eq_channels.json file
    with open('eq_channels.json', encoding="utf8") as eq_channels:
        eq_channels = json.load(eq_channels)
        eq_channels['channels'].remove(message.channel.id)

    # Writes channel ID to file
    with open('eq_channels.json', 'w') as outfile:
        json.dump(eq_channels, outfile)
    await client.send_message(message.channel, 'EQ Alerts successfully disabled on this channel.')

async def showHelp(client, message):
    with open('help.json') as file:
        help = json.load(file)

    commands = []

    for item in help['commands']:
        commands.append(item + ": " + help['commands'][item])

    commands = "\n".join(commands)
    string = ":mega: **These are the current available commands:**\n{}".format(commands)

    await client.send_message(message.channel, string)
