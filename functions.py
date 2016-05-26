import discord, asyncio, random, requests, json, re, random
global loop

loop = asyncio.get_event_loop()

async def showCat(message, client):
  offset = random.randint(0,348)
  
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
  
  await client.send_message(message.channel, 'http://catoverflow.com/cats/%s.gif' % gif2)
    
async def ping(message, client):
  await client.send_message(message.channel, 'Pong!')
 
async def showPSO2EQ(client):
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
    
async def addEQChannel(message, client):
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
    
async def removeEQChannel(message, client):
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