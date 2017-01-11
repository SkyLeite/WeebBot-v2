from functions import *
from settings import *
from discord.ext import commands

description = '''A bot focused on alerting for Emergency Quests on PSO2.\nSupport: https://discord.gg/0xMXCNAFbH032Ig1'''

bot = commands.Bot(command_prefix=['+'], description=description)

extensions = [
    'cogs.general',
    'cogs.pso2',
    'cogs.macro',
    'cogs.quotes',
    'cogs.gdq'
]


@bot.event
async def on_ready():
    botInfo = await bot.application_info()
    oauthlink = discord.utils.oauth_url(botInfo.id)

    print('---------')
    print('Username: {}'.format(bot.user.name))
    print('ID: {}'.format(bot.user.id))
    print('Server count: {}'.format(str(len(bot.servers))))
    print('Member count: {}'.format(str(len(set(bot.get_all_members())))))
    print('OAuth URL: {}'.format(oauthlink))
    print('Cogs: {}'.format(bot.cogs))
    print('---------')
    #app.run('localhost', port=5001)


@bot.event
async def on_member_join(member):
    if member.server.id == '80900839538962432':
        role = discord.utils.get(member.server.roles, name='Members')
        await bot.add_roles(member, role)
        await bot.send_message(discord.Object("80900839538962432"), '{}, welcome to the PSO2 Discord. Type `+pso2` if you need information regarding the game, and read the #rules.'.format(member.mention))


if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    loop = asyncio.get_event_loop()

    bot.loop.create_task(checkPSO2EQ(bot))
    bot.loop.create_task(changeGame(bot))
    bot.loop.create_task(gdqTopic(bot))
    bot.run(token)
