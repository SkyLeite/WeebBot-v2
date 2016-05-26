import discord, asyncio, random, requests, json, re

client = discord.Client()

print("Starting bot...\n")
token = 'x'

async def showPSO2EQ():
  await client.wait_until_ready()
  while not client.is_closed:
    #Async shit to use requests
    future1 = loop.run_in_executor(None, requests.get, 'http://pso2emq.flyergo.eu/api/v2/')
    r = await future1
    
    #Loads EQ data
    eq = json.loads(r.text)
    
    #Loads last_eq.json
    with open('last_eq.json', encoding="utf8") as in_f:
      last_eq = json.load(in_f)
    
    #If current EQ is different than last EQ recorded, send alert and update last_eq file
    if last_eq['jst'] != eq[0]['jst']:
      with open('eq_channels.json', encoding="utf8") as eq_channels:
        eq_channels = json.load(eq_channels)
      
      for item in eq_channels['channels']:
        channel = discord.Object(item)
        await client.send_message(channel, eq[0]['text'])
      print('#EQ ALERT!')
    
      with open('last_eq.json', 'w') as out_f:
        json.dump(eq[0], out_f)
      
    await asyncio.sleep(600) #Task runs every 60 seconds
  
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
    await showCat(message)
  
  elif message.content.startswith('!join'):
    await client.send_message(message.channel, 'To get Weeb Bot in your server, simply click the following link: http://bit.ly/1X4p8U3')

  elif message.content.startswith('!eq'):
    message2 = message.content.split(" ")
    command = message2[1]
    admin = 'False'
    if command == 'enable':
      for item in message.author.roles:
        if item.name == "Administrator":
          await addEQChannel(message)
          admin = 'True'
      if admin == 'False':
        await client.send_message(message.channel, "You need the 'Administrator' role to do that.")
    elif command == 'disable':
      for item in message.author.roles:
        if item.name == "Administrator":
          await removeEQChannel(message)
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
    
async def addEQChannel(message):
  #Loads eq_channels.json file
  with open('eq_channels.json', encoding="utf8") as eq_channels:
    eq_channels = json.load(eq_channels)
    
  if message.channel.id not in eq_channels['channels']:
    #Writes channel ID to file
    with open('eq_channels.json', 'w') as outfile:
      eq_channels['channels'].append(message.channel.id)
      json.dump(eq_channels, outfile)
      
    await client.send_message(message.channel, "EQ Alerts successfully enabled on this channel.")
  else:
    await client.send_message(message.channel, 'EQ Alerts are already enabled on this channel.')

async def removeEQChannel(message):
    #Loads eq_channels.json file
    with open('eq_channels.json', encoding="utf8") as eq_channels:
      eq_channels = json.load(eq_channels)
      eq_channels['channels'].remove(message.channel.id)
      
    #Writes channel ID to file
    with open('eq_channels.json', 'w') as outfile:
      json.dump(eq_channels, outfile)
    await client.send_message(message.channel, 'EQ Alerts successfully disabled on this channel.')

def fixFormat(stats, name):
  #Returns rarity
  m = re.search('\d\d', stats[0])
  print(stats[0])
  if m:
    rarity = m.group(0)
  
  #Returns name
  m = re.search('\[\[%s\]\]' % name, stats[2])
  if m:
    weapon = m.group(0)
    weapon = weapon.replace('[', '')
    weapon = weapon.replace(']', '')
  
    #Returns requirement
    #m = re.search('\d\d\d\s\w\-ATK', stats[3])
    #if m:
    #  req = m.group(0)

    #Returns base
    m = stats[5].split('|')
    m = m[1].split('<')
    base = m[0]
  
    #Returns +10
    m = stats[6].split('|')
    m = m[1].split('<')
    grinded = m[0]
  
    #Returns pot
    m = re.search('\{\{pots\|.*\}\}', stats[7])
    if m:
      pot = m.group(0).split('|')
      pot = pot[1].split('}')

  return(rarity, weapon, base, grinded, pot[0])
  
@client.event
async def on_server_join(server):
  await client.send_message(server, 'Ohayo!')
  
loop = asyncio.get_event_loop()
  
try:
  loop.create_task(showPSO2EQ())
  loop.run_until_complete(client.login(token))
  loop.run_until_complete(client.connect())
except Exception:
  loop.run_until_complete(client.close())
finally:
  loop.close()
