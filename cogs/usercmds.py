import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import time
import datetime

class UserCmds(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[LOGS] Canary Bot is Logged In')
        await self.client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="GVRSP Hosting Staff"))
        global startTime
        startTime = time.time()
    
    @nextcord.slash_command(guild_ids=[846646873251250246], description='Gives info about the bot!')
    async def about(self, interaction : Interaction):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))

        sendEmbed = nextcord.Embed(title="**About**", description="Coded with :heart: by <@806826503013924875>!")
        sendEmbed.add_field(name='Uptime', value=uptime, inline=True)
        sendEmbed.add_field(name='Database', value='Status: :green_circle: **Online**', inline=True)
        sendEmbed.add_field(name='Last Update', value='27/03/2022', inline=False)
        sendEmbed.add_field(name='Created By', value='https://www.savagedevelopment.tk/', inline=False)
        sendEmbed.set_footer(text='API & Database V1.0')

        await interaction.response.send_message(embed=sendEmbed)
    

def setup(client):
    client.add_cog(UserCmds(client))
