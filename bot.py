import discord, asyncio, random, requests, json, re, random
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
   
  elif message.content.startswith('!ping'):
    await ping(message, client)
    
  elif message.content.startswith('!number'):
    await showNumberTrivia(message, client)
    
  elif message.content.startswith('!pokemon'):
    pokemon = message.content.split(' ',1)[1]
    await showPokemon(message, client, pokemon)
    
  elif message.content.startswith('!msg'):
    if message.author.id == ownerid:
      message = message.content.split(' ',1)[1]
      
      for item in client.servers:
        channel = discord.Object(item.id)
        await client.send_message(channel, message)
  
  elif message.content.startswith('!join'):
    await client.send_message(message.channel, 'To get Weeb Bot in your server, simply click the following link: http://bit.ly/1X4p8U3')
    
  elif message.content.startswith('!servers'):
    for item in client.servers:
      print(item)
      
  elif message.content.startswith('!game'):
    if message.author.id == ownerid:
      game = message.content.split(' ',1)[1]
      await client.change_status(message.author.game, idle=False)
    else:
      await client.send_message(message.channel, 'Your ID:%s \nOwner ID:%s' % (message.author.id, ownerid))

  elif message.content.startswith('!eq'):
    message2 = message.content.split(" ")
    command = message2[1]
    admin = 'False'
    if command == 'enable':
      for item in message.author.roles:
        if item.name == "Administrator":
          await addEQChannel(message, client)
          admin = 'True'
      if admin == 'False':
        await client.send_message(message.channel, "You need the 'Administrator' role to do that.")
    elif command == 'disable':
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
  await client.send_message(server, 'Ohayo!')
  
loop = asyncio.get_event_loop()
  
try:
  loop.create_task(showPSO2EQ(client))
  loop.run_until_complete(client.login(token))
  loop.run_until_complete(client.connect())
except Exception:
  loop.run_until_complete(client.close())
finally:
  loop.close()
