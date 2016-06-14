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
  
async def showPokemon(message, client, pokemon):
  api = "http://pokeapi.co/api/v2/pokemon/%s/" % pokemon.lower()
  
  future1 = loop.run_in_executor(None, requests.get, api)
  r = await future1
  
  response = json.loads(r.text)
  abilities = []
  types = []
  
  #Assings types and abilities to lists
  for i in response['abilities']:
    abilities.append(i['ability']['name'])
  
  for i in response['types']:
    types.append(i['type']['name'])
    
  #Converts lists to human readable strings
  ability = ', '.join(abilities)
  type = ', '.join(types)
  
  #Assigns data to variables for easier reading
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
  
  string = '**Name:** %s\n**Type:** %s\n**Weight:** %s\n**Height:** %s\n**Abilities:** %s\n**Stats:**\n  Speed: %s\n  Special Defense: %s\n  Special Attack: %s\n  Defense: %s\n  Attack: %s\n  HP: %s\n**Sprite (Normal):** %s\n**Sprite (Shiny):** %s' % (name, type, weight, height, ability, speed, spdef, spatk, defense, attack, hp, sprite, shiny)
  await client.send_message(message.channel, string)
  
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
      
      try:
        for item in eq_channels['channels']:
          channel = discord.Object(item)
          await client.send_message(channel, eq[0]['text'])
        print('#EQ ALERT!')
      except:
        pass
    
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