from nextcord.ext import commands
import nextcord
import os

TOKEN = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix='#')
client.remove_command('help')

for fn in os.listdir('./cogs'):
    if fn.endswith('.py'):
        client.load_extension(f'cogs.{fn[:-3]}')

client.run(TOKEN)
