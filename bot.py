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
  if message.content.startswith('!greet'):
    await client.send_message(message.channel, 'Ohayo!')
  
  elif message.content.startswith('!cat'):
    await showCat(message, client)
   
  elif message.content.startswith('!ping'):
    await ping(message, client)
    
  elif message.content.startswith('!msg'):
    if message.author.id == ownerid:
      message = message.content.split(' ',1)[1]
      
      for item in client.servers:
        channel = discord.Object(item.id)
        await client.send_message(channel, message)
  
  elif message.content.startswith('!join'):
    await client.send_message(message.channel, 'To get Weeb Bot in your server, simply click the following link: http://bit.ly/1X4p8U3')

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

  elif message.content.startswith('!pso2'):
    type = message.content.split(' ', 1)
    weapon = type[1].split(' ', 1)
    name = weapon[1]
    
    weaponType = ''.join((weapon[0],'s'))
    
    query = requests.get('http://pso2.arks-visiphone.com/api.php?action=query&titles=Simple_%s_List&prop=revisions&rvprop=content&format=json' % weaponType)
    parsed = json.loads(query.text)
    
    if weaponType == 'Swords':
      pageID = '138'
    
    elif weaponType == 'Wired_Lances':
      pageID = '686'
    
    elif weaponType == 'Partizans':
      pageID = '694'
    
    elif weaponType == 'Twin_Daggers':
      pageID = '729'
    
    elif weaponType == 'Double_Sabers':
      pageID = '730'
    
    elif weaponType == 'Knucles':
      pageID = '737'
    
    elif weaponType == 'Katanas':
      pageID = '738'
    
    elif weaponType == 'Dual_Blades':
      pageID = '739'
    
    elif weaponType == 'Gunslashes':
      pageID = '740'
    
    elif weaponType == 'Assault_Rifles':
      pageID = '731'
    
    elif weaponType == 'Launchers':
      pageID = '734'
    
    elif weaponType == 'Twin_Machine_Guns':
      pageID = '733'
    
    elif weaponType == 'Bullet_Bows':
      pageID = '736'

    elif weaponType == 'Rods':
      pageID = '735'
    
    elif weaponType == 'Talises':
      pageID = '732'
    
    elif weaponType == 'Wands':
      pageID = '741'
    
    elif weaponType == 'Jet_Boots':
      pageID = '742'
    
    str = parsed['query']['pages'][pageID]['revisions'][0]['*']
    
    match = re.search(r'\[\[%s\]\]' % name, str)
    if match:
      str1 = str.split('-\n')

    for i in range(0, len(str1)):
      if name in str1[i]:
        stats = str1[i].split('\n')
    
    stats2 = fixFormat(stats, name)
    if stats2:
      await client.send_message(message.channel, '**Weapon Name:** %s\n**Rarity:** %s\n**Base Stat:** %s ATK\n**+10 Stat:** %s ATK\n**Potential:** %s' % (stats2[1], stats2[0], stats2[2], stats2[3], stats2[4]))

  
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
