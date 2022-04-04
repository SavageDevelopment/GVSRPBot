import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle
from nextcord.ui import Button, View
import airtablesavage as atb

global reactions
reactions = 0

class HostCmds(commands.Cog):
    def __init__(self,client):
        self.client = client


    global start
    async def start(interaction):
        if interaction.user.id == hostid:
            reactionsList = []
            await interaction.response.send_message('Your session has been published!', ephemeral=True)
            atb.newsession(interaction.user.name, interaction.user.id)
            global host
            host = interaction.user.mention
            reactions = 0

            await interaction.user.send(f'**Link set as**: {initLink} !   \n Use **/setlink** to change it...')
            id = atb.getsessioninfo(hostid)
            atb.addlink(id, initLink)

            sendEmbed = nextcord.Embed(title="**Session Host**", description=f'{interaction.user.mention}')
            sendEmbed.add_field(name='Total Reactions', value=f'{str(reactions)}', inline=False)
            sendEmbed.add_field(name='Release Status', value='Awaiting Reactions', inline=False)
            sendEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/957635340577955882/957635414439628901/GV_LOGO.PNG')

            async def react_callback(interaction):
                if interaction.user.id in reactionsList:
                    await interaction.response.send_message('You already reacted. Nice try...', ephemeral=True)
                else:
                    reactionsList.append(interaction.user.id)
                    await interaction.response.send_message('Your reaction has been added! Please wait for the session to start.', ephemeral=True)
                    global reactions
                    reactions = reactions + 1
                    
                    newSendEmbed = nextcord.Embed(title="**Session Host**", description=f'{host}')
                    newSendEmbed.add_field(name='Total Reactions', value=f'{str(reactions)}', inline=False)
                    newSendEmbed.add_field(name='Release Status', value='Awaiting Reactions', inline=False)
                    newSendEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/957635340577955882/957635414439628901/GV_LOGO.PNG')
                    await mainembed.edit(embed=newSendEmbed)

            global reactButton
            reactButton = Button(label="React", style=ButtonStyle.blurple)
            reactButton.callback = react_callback
            global mainview
            mainview = View()
            mainview.add_item(reactButton)

            global mainembed
            mainembed = await hostingChannel.send("@here", embed=sendEmbed, view=mainview)
        else:
            await interaction.response.send_message('You are not the session host. Please dont touch this panel!', ephemeral=True)

    @nextcord.slash_command(guild_ids=[846646873251250246], description='Set the Private Server Link for Your Session!')
    async def setlink(self, interaction : Interaction, *, input):
        await interaction.response.send_message(f'**Link set as**: {input}', ephemeral=True)
        id = atb.getsessioninfo(interaction.user.id)
        atb.addlink(id, input)

    @nextcord.slash_command(guild_ids=[846646873251250246], description='Co-Host a session!')
    async def cohost(self, interaction : Interaction, host : nextcord.Member):
        await interaction.response.send_message(f'You are now Co-Hosting on {host.mention}s Session!', ephemeral=True)
        hostingChannel = self.client.get_channel(847882628744478730)
        sendEmbed = nextcord.Embed(title="**Co-Host**", description=f'{interaction.user.mention} is now Co-Hosting on {host.mention}s Session!')
        await hostingChannel.send(embed=sendEmbed)

    global earlyaccess
    async def earlyaccess(interaction):
        if interaction.user.id == hostid:
            await interaction.response.send_message('Early Access has been Opened!', ephemeral=True)

            id = atb.getsessioninfo(interaction.user.id)
            atb.setstatus(id, 1)

            mainview.remove_item(reactButton)
            sendEmbed = nextcord.Embed(title="**Session Host**", description=f'{interaction.user.mention}')
            sendEmbed.add_field(name='Release Status', value='Early Access', inline=False)
            sendEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/957635340577955882/957635414439628901/GV_LOGO.PNG')
            await mainembed.edit(embed=sendEmbed, view=mainview)

            async def join_callback(interaction):
                await interaction.response.send_message(f'Join the Session Here: {atb.getlink(hostid)}', ephemeral=True)
            global joinButton
            joinButton = Button(label="Join Session", style=ButtonStyle.blurple)
            joinButton.callback = join_callback
            global eaview
            eaview = View()
            eaview.add_item(joinButton)
            eaEmbed = nextcord.Embed(title="**Early Access**", description=f'Session Host: {interaction.user.mention}')
            eaEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/957635340577955882/957635414439628901/GV_LOGO.PNG')
            global eamessage
            eamessage = await eaChannel.send("@here", embed=eaEmbed, view=eaview)
        else:
            await interaction.response.send_message('You are not the session host. Please dont touch this panel!', ephemeral=True)
    
    global releasesession
    async def releasesession(interaction):
        if interaction.user.id == hostid:
            await interaction.response.send_message('Session has been released!', ephemeral=True)

            id = atb.getsessioninfo(interaction.user.id)
            atb.setstatus(id, 2)

            async def join_callback2(interaction):
                await interaction.response.send_message(f'Join the Session Here: {atb.getlink(hostid)}', ephemeral=True)
            global joinButton2
            joinButton2 = Button(label="Join Session", style=ButtonStyle.green)
            joinButton2.callback = join_callback2
            global eaview2
            eaview2 = View()
            eaview2.add_item(joinButton2)

            sendEmbed = nextcord.Embed(title="**Session Host**", description=f'{interaction.user.mention}')
            sendEmbed.add_field(name='Release Status', value='The SESSION has been RELEASED!', inline=False)
            sendEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/957635340577955882/957635414439628901/GV_LOGO.PNG')
            await mainembed.edit(embed=sendEmbed, view=eaview2)

            eaview.remove_item(joinButton)
            eaEmbed = nextcord.Embed(title="**Early Access**", description='Early Access is now CLOSED!')
            eaEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/957635340577955882/957635414439628901/GV_LOGO.PNG')
            await eamessage.edit(embed=eaEmbed, view=eaview)
        else:
            await interaction.response.send_message('You are not the session host. Please dont touch this panel!', ephemeral=True)

    global endsession
    async def endsession(interaction):
        if interaction.user.id == hostid:
            await interaction.response.send_message('Your session has been ended!', ephemeral=True)
            id = atb.getsessioninfo(interaction.user.id)
            atb.deletesession(id)

            eaview2.remove_item(joinButton2)
            sendEmbed = nextcord.Embed(title="**Session Ended**", description=f'Thanks for attending {interaction.user.mention}s Session! See you next time...')
            sendEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/957635340577955882/957635414439628901/GV_LOGO.PNG')
            await mainembed.edit(embed=sendEmbed, view=eaview2)
        else:
            await interaction.response.send_message('You are not the session host. Please dont touch this panel!', ephemeral=True)
    

    @nextcord.slash_command(guild_ids=[846646873251250246], description='Opens the Hosting Panel!')
    async def host(self, interaction : Interaction, *, link):
        role = nextcord.utils.get(interaction.guild.roles, name="GVRSP │ Staff Team")
        devrole = nextcord.utils.get(interaction.guild.roles, name="GVSRP | Bot Developer")
        activeSession = atb.checkSession(interaction.user.id)
        global hostid
        hostid = interaction.user.id
        global hostingChannel
        hostingChannel = self.client.get_channel(847882628744478730)
        global eaChannel
        eaChannel = self.client.get_channel(878628825741807656)
        global initLink
        initLink = link
        if role in interaction.user.roles or devrole in interaction.user.roles:
            if activeSession == False:
                StartSessionB = Button(label="Start Session", style=ButtonStyle.blurple)
                EASessionB = Button(label="Open Early Access", style=ButtonStyle.gray)
                ReleaseSessionB = Button(label="Release Session", style=ButtonStyle.green)
                EndSessionB = Button(label="End Session", style=ButtonStyle.red)

                StartSessionB.callback = start
                EASessionB.callback = earlyaccess
                ReleaseSessionB.callback = releasesession  
                EndSessionB.callback = endsession      

                panelView = View()
                panelView.add_item(StartSessionB)
                panelView.add_item(EASessionB)
                panelView.add_item(ReleaseSessionB)
                panelView.add_item(EndSessionB)

                sendEmbed = nextcord.Embed(title="**Hosting Panel**", description=f'Hello {interaction.user.mention}...')
                sendEmbed.add_field(name='Welcome to the Hosting Panel!', value='Please select an option below!', inline=False)
                sendEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/957635340577955882/957635414439628901/GV_LOGO.PNG')

                await interaction.response.send_message('The panel has been sent to your DMs!', ephemeral=True)
                await interaction.user.send(embed=sendEmbed, view=panelView)
            elif activeSession == True:
                EASessionB = Button(label="Open Early Access", style=ButtonStyle.gray)
                ReleaseSessionB = Button(label="Release Session", style=ButtonStyle.green)
                EndSessionB = Button(label="End Session", style=ButtonStyle.red)

                EASessionB.callback = earlyaccess
                ReleaseSessionB.callback = releasesession  
                EndSessionB.callback = endsession      

                panelView = View()
                panelView.add_item(EASessionB)
                panelView.add_item(ReleaseSessionB)
                panelView.add_item(EndSessionB)

                sendEmbed = nextcord.Embed(title="**Hosting Panel**", description=f'Hello {interaction.user.mention}...')
                sendEmbed.add_field(name='Welcome to the Hosting Panel!', value='Please select an option below!', inline=False)
                sendEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/957635340577955882/957635414439628901/GV_LOGO.PNG')

                await interaction.response.send_message('The panel has been sent to your DMs!', ephemeral=True)
                await interaction.user.send(embed=sendEmbed, view=panelView)

        else:
            await interaction.response.send_message('You do not have the permissions to do this.', ephemeral=True)

def setup(client):
    client.add_cog(HostCmds(client))
