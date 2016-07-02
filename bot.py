from functions import *
from settings import *

client = discord.Client()

print("Starting bot...\n")


@client.event
async def on_ready():
    print("## BOT IS RUNNING ##")
    print('Username: %s' % client.user.name)
    print('ID: %s' % client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!cat'):
        await showCat(message, client)

    elif message.content.startswith('!help'):
        await showHelp(client, message)

    elif message.content.startswith('!ping'):
        await ping(message, client)

    elif message.content.startswith('!id'):
        await client.send_message(message.channel, message.channel.id)

    elif message.content.startswith('!send'):
        print(message.attachments)

    elif message.content.startswith('!meme'):
        msg = message.content.split(' ')

        try:
            if msg[1] == "play":
                meme = msg[2] + '.mp3'
                await playMeme(message, client, meme)

            elif msg[1] == "bye":
                meme = 'bye'
                await playMeme(message, client, meme)

            elif msg[1] == "list":
                await memeList(message, client)

            elif msg[1] == "add":
                if message.author.id == ownerid:
                    await addMeme(message, client)
        except:
            string = ":mega: **Welcome!**\n Type ``!meme list`` to receive a list with every available meme, and ``!meme play memename`` to play the one you want!"
            await client.send_message(message.channel, string)

    elif 'ayy' in message.content and 'lmao' not in message.content:
        await client.send_message(message.channel, 'lmao')

    elif message.content.startswith('!recommend'):
        query = message.content.split(' ', 1)[1]
        await showRecommendation(message, client, query)

    elif message.content.startswith('!pokemon'):
        pokemon = message.content.split(' ', 1)[1]
        await showPokemon(message, client, pokemon)

    elif message.content.startswith('!lasteq'):
        await showLastEQ(client, message)

    elif message.content.startswith('!msg'):
        if message.author.id == ownerid:
            message = message.content.split(' ', 1)[1]

            try:
                for item in client.servers:
                    await client.send_message(client.servers.default_channel, message)
            except:
                pass

    elif message.content.startswith('!join'):
        await client.send_message(message.channel,
                                  'To get Weeb Bot in your server, simply click the following link: http://bit.ly/1X4p8U3')

    elif message.content.startswith('!servers'):
        servers = []

        for item in client.servers:
            servers.append('%s(%d)' % (item.name, item.member_count))

        string = ', '.join(servers)
        await client.send_message(message.channel, 'Servers: %s' % string)

    elif message.content.lower() == 'i see what you did there':
        await client.send_file(message.channel, 'img/isee.jpg')

    elif message.content.startswith('!game'):
        if message.author.id == ownerid:
            gamename = message.content.split(' ', 1)[1]

            game = discord.Game(name=gamename)
            await client.change_status(game, idle=False)
        else:
            await client.send_message(message.channel, 'Your ID:%s \nOwner ID:%s' % (message.author.id, ownerid))

    elif message.content.startswith('!eq'):
      admin = 'False'
      
      if message.content == '!eq enable':
        for item in message.author.roles:
          if item.name == "Administrator":
            await addEQChannel(message, client)
            admin = 'True'
        if admin == 'False':
          await client.send_message(message.channel, "You need the 'Administrator' role to do that.")
      
      elif message.content == '!eq disable':
        for item in message.author.roles:
          if item.name == "Administrator":
            await removeEQChannel(message, client)
            admin = 'True'
        if admin == 'False':
          await client.send_message(message.channel, "You need the 'Administrator' role to do that.")
      
      else:
        await client.send_message(message.channel, "Welcome to Weeb Bot's Emergency Quest Alert! To get started, please type !eq enable on the channel you want EQs to appear. Please keep in mind you need the 'Administrator' role to do that.")

@client.event
async def on_server_join(server):
    channel = discord.Object(test_channel)
    await client.send_message(channel, u':mega: **Joined:** {0:s}\n``Member Count:`` {1:s}\n``Icon URL:`` {2:s}'.format(
      server.name, server.member_count, server.icon_url))


loop = asyncio.get_event_loop()

try:
    loop.create_task(showPSO2EQ(client))
    loop.run_until_complete(client.login(token))
    loop.run_until_complete(client.connect())
except Exception:
    loop.run_until_complete(client.close())
finally:
    loop.close()
