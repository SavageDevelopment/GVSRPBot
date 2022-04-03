from nextcord.ext import commands
import nextcord
import keep_alive
import os

client = commands.Bot(command_prefix='#')
client.remove_command('help')

for fn in os.listdir('./cogs'):
    if fn.endswith('.py'):
        client.load_extension(f'cogs.{fn[:-3]}')

keep_alive.keep_alive()
client.run('OTU3NTk3MTgxNzIyOTEwNzgx.YkBF3w._vuF0HIQYyV7Sj_8VbmrxY7r7rA')