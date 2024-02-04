import discord
from discord.ext import commands, tasks
import os
import asyncio
import random
import time
import wikipedia


"""
==================================================
SETUP
==================================================
"""

client = commands.Bot(command_prefix=commands.when_mentioned_or("-"),case_insensitive=True, intents = discord.Intents.all())
client.remove_command('help')

report_channel = client.get_channel(1071601656267022336)

colors = [
        0xE1A852,
        0x33A852,
        0xB4A852,
        0x00C252,
        0x7BC2AC,
        0x7B4FA5,
        0x7BABFB,
        0x1B009F,
        0x1B8C9F,
        0xD18C9F
        ]

@client.event
async def on_ready():
    change_status.start()
    print('Bot online!')

#Status
@tasks.loop(seconds=5)
async def change_status():
    statuses = ['the servers','YOU','BellHacks 24']
    status = random.choice(statuses)
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type = discord.ActivityType.watching, name=status))



    
#Errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        embed1 = discord.Embed(
            title='Sorry, not enough perms!',
            description='Sorry, you need more permissions to use this command!',
            color=random.choice(colors))
        await ctx.send(embed=embed1)
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('I don\'t have enough permissions to do that!')
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='Missing Required Argument', description='Please pass in the correct arguments for this command!',color=discord.Colour.red())
    
    else:
        embed = discord.Embed(title='Error executing command!',
                              color=random.choice(colors))
        embed.add_field(name=f'Error', value=f"```{error}```", inline=False)
        embed.add_field(name='Command', value=ctx.command, inline=False)
        embed.add_field(name='Server', value=ctx.guild.name, inline=False)
        embed.add_field(name='Author', value=ctx.author.display_name+'\n'+ctx.author.mention, inline=False)
        embed.add_field(name='Channel', value=ctx.message.channel.name+'\n'+ctx.message.channel.mention, inline=False)
        await ctx.send(embed=embed)
        raise error


#Snipe Command Setup
snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

@client.event
async def on_message_delete(message):
    global snipe_message_content
    global snipe_message_author
    global snipe_message_id

    snipe_message_content = message.content
    snipe_message_author = message.author.id
    snipe_message_id = message.id
    await asyncio.sleep(60)

    if message.id == snipe_message_id:
        snipe_message_author = None
        snipe_message_content = None
        snipe_message_id = None

    



"""
===============================================
HELP COMMAND
===============================================

"""

#Main
main = discord.Embed(
    title='VECTOR HELP',
    description='Type `-help <category>` for a specific category\n\n**Categories:** \nUtility\nModeration\nFun\nAI',
    color = random.choice(colors)
)
main.add_field(name = 'Navigation Help',
              value=':rewind:  go to home\n:arrow_left:  go to previous\n:arrow_right:  go to next\n:fast_forward:  go to end',
               inline=False)
main.add_field(name='Command Format', 
              value = 'The command will start with "-", and parameters will be enclosed with <> if requried and () if optional')
main.set_footer(text='Home Page')

page1 = discord.Embed(title='Utility Commands',description='> `-help (category)`\n> shows this page\n\n> `-send <message>`\n> sends whatever message you want\n\n> `-serverinfo`\n> gets a server\'s information\n\n> `-remind <time> <todo>`\n> sets a reminder\n\n> `-whois (user)`\n> shows a member\'s info\n\n> `-createchannel <channel name>`\n> creates a new text channel\n\n> `-deletechannel <channel name>`\n> deletes a text channel\n\n> `-lock <channel> (reason)`\n> locks a channel\n\n> `-unlock <channel>`\n> unlocks a channel\n\n> `-lockdown`\n> locks all channels in the server\n\n> `-unlockdown`\n> unlocks all channels in the server', color=0x32CD32)
page1.set_footer(text='Help Page 1/4')
page2 = discord.Embed(title='Moderation Commands',
           description='> `-kick <user> (reason)`\n> kicks a user\n\n> `-ban <user> (reason)`\n> bans a user\n\n> `-warn <user> <reason>`\n> warns a user\n\n> `-mute <user> (reason)`\n> mutes a person\n\n> `-unmute <user>`\n> unmutes a user\n\n> `-tempmute <user> <mins> <reason>`\n> tempmutes a user for an amount of MINUTES\n\n> `-slowmode <seconds>`\n> sets a slowmode for the current channel\n\n> `-nuke <channel>`\n> nukes a channel\n\n> `-purge <amount>`\n> purges an amount of messages',
            color=0xFF8C00)
page2.set_footer(text='Help Page 2/4')
page3 = discord.Embed(title='Fun Commands', 
            description='> `-guilds`\n> shows how many servers the bot is in\n\n> `-rps <choice>`\n> rock paper scissors\n\n> `-pfp (user)`\n> gets a pfp of a user\n\n> `-hack <user>`\n> hacks a person :smiling_imp:\n\n> `-search <word/thing>`\n> searches wikipedia for something\n\n> `-8ball <question>`\n> ask the 8ball a question\n\n> `-shoot <user>`\n> "shoots" another person\n\n> `-ping`\n> gets the bot\'s latency\n\n> `-snipe`\n> gets recently deleted messages',
            color=0x9B26B6)
page3.set_footer(text='Help Page 3/4')
page4 = discord.Embed(title='AI Commands',
            description="> `-chat <message>`\n> chat with the bot\n\n> `-generate <image_description>`\n> generates an image",
            color=0x1E90FF)
page4.set_footer(text='Help Page 4/4')



@client.command(aliases=['h'])
async def help(ctx, *, category = None):
    if category == None:
        pages = [main, page1, page2, page3, page4]
        current = 0
        msg = await ctx.send(embed=pages[current])
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout = 60.0)
            except asyncio.TimeoutError:
                pass
            else:
                previous_page = current

                if reaction.emoji == u"\u23EA":
                    current = 0
                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1
                elif reaction.emoji == u"\u27A1":
                    if current < len(pages)-1:
                        current += 1
                elif reaction.emoji == u"\u23E9":
                    current = len(pages)-1
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)


                    if current != previous_page:
                        await msg.edit(embed=pages[current])

    elif 'util' in category.lower():
        await ctx.send(embed=page1)
    elif 'mod' in category.lower():
        await ctx.send(embed=page2)
    elif 'fun' in category.lower():
        await ctx.send(embed=page3)
    elif 'ai' in category.lower():
        await ctx.send(embed=page4)
    else:
        await ctx.send('That\'s not a category! Type `-help` for all help pages!')
              
    
        


"""

======================================
UTILITY COMMANDS
======================================

"""

#Send Command
@client.command(aliases=['say'])
async def send(ctx, *, message=None):
    if message == None:
        await ctx.send('What do you want me to send?')
    else:
        await ctx.send(message)


#Serverinfo Command
@client.command(aliases=['guildinfo'])
async def serverinfo(ctx):
    role_count = len(ctx.guild.roles)
    embed = discord.Embed(title='Server Info for '+ctx.guild.name, timestamp = ctx.message.created_at, color=ctx.author.color)
    embed.add_field(name='Server Name', value=ctx.guild.name, inline=False)
    embed.add_field(name='Server ID', value=ctx.guild.id)
    embed.add_field(name='Verification Level', value=str(ctx.guild.verification_level), inline=False)
    embed.add_field(name='Highest Role', value=ctx.guild.roles[-1], inline=False)
    embed.add_field(name='Number of roles', value=str(role_count), inline=False)
    embed.add_field(name='Number of members', value=ctx.guild.member_count, inline=False)
    embed.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %B %d, %Y at %H:%M:%S'), inline=False)
    embed.add_field(name='Text Channels', value=len(ctx.guild.text_channels), inline=False)
    embed.add_field(name='Voice Channels', value=len(ctx.guild.voice_channels), inline=False)
    channels = len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)
    embed.add_field(name='Total Channels', value=str(channels), inline=False)
    embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

#Remind Command
def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2
    return val * time_dict[unit]
    
@client.command()
async def remind(ctx, time, *, todo):
    retime = convert(time)
    if int(retime) == -1:
        await ctx.send('Please use a correct time unit: s, m, d, or h!')
    elif int(retime) == -2:
        await ctx.send('Please enter a number and then a time unit (s, m, h, or d)!')
    else:
        embed = discord.Embed(title='Reminder Set!', description='You will be reminded to `'+todo+'` in '+time+'!', color = random.choice(colors))
        await ctx.send('Reminder set, check your DMs')
        try:
            await ctx.author.send(embed=embed)
        except:
            await ctx.send('I need to be able to DM you for that command!')
            return
        await asyncio.sleep(int(retime))
        embed2 = discord.Embed(title='Reminder', description='`'+todo+'`', color=random.choice(colors))
        await ctx.author.send(embed=embed2)



#Whois Command
@client.command()
async def whois(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
        roles = [role for role in ctx.author.roles]

    else:
        roles = [role for role in member.roles]

    embed = discord.Embed(title=f"{member}",
                          colour=member.colour,
                          timestamp=ctx.message.created_at)
    embed.set_footer(text=f"Requested by: {ctx.author}",
                     icon_url=ctx.author.avatar.url)
    embed.set_author(name="User Info: ")
    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(name="User Name:", value=member.display_name, inline=False)
    embed.add_field(name="Discriminator:",
                    value=member.discriminator,
                    inline=False)
    embed.add_field(name="Current Status:",
                    value=str(member.status).title(),
                    inline=False)
    embed.add_field(
        name="Current Activity:",
        value=
        f"{str(member.activity.type).title().split('.')[1]}: {member.activity.name}"
        if member.activity is not None else "None",
        inline=False)
    embed.add_field(
        name="Created At:",
        value=member.created_at.strftime("%a, %d, %B, %Y, %I:%M %p UTC"),
        inline=False)
    embed.add_field(
        name="Joined At:",
        value=member.joined_at.strftime("%a, %d, %B, %Y, %I:%M %p UTC"),
        inline=False)
    embed.add_field(name=f"Roles [{len(roles)}]",
                    value=" **|** ".join([role.mention for role in roles]),
                    inline=False)
    embed.add_field(name="Top Role:", value=member.top_role, inline=False)
    embed.add_field(name="Bot?:", value=member.bot, inline=False)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)


#Createchannel Command
@client.command(aliases=['cc','create_channel'])
@commands.has_permissions(manage_channels=True)
async def createchannel(ctx, channelname=None):
    if channelname == None:
        await ctx.send('What is the name is the new channel?')
        return
    guild = ctx.message.guild
    await guild.create_text_channel(channelname)
    embed = discord.Embed(title='Channel Created!',
                          description='Created the channel ' +
                          str(channelname) + '!',
                          color=random.choice(colors))
    await ctx.send(embed=embed)

#Deletechannel Command
@client.command(aliases=['dc', 'delete_channel'])
@commands.has_permissions(manage_channels=True)
async def deletechannel(ctx, channel: discord.TextChannel=None):
    if channel == None:
        await ctx.send('What channel are you going to delete? (Mention it)')
    await channel.delete()
    embed = discord.Embed(title='Channel deleted!',
                          color=random.choice(colors))
    await ctx.send(embed=embed)

#Lock Command
@client.command(pass_context=True)
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None, *, reason=None):
    if channel == None:
        channel = ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send('Channel Locked!')
    embed = discord.Embed(title='Channel Locked', description=reason, color=random.choice(colors))
    await channel.send(embed=embed)

#Unlock Command
@client.command(pass_context=True)
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
    if channel == None:
        channel = ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=None)
    await ctx.send('Channel Unlocked!')
    embed = discord.Embed(title='Channel Unlocked!', description='You may chat here now!', color=random.choice(colors))
    await channel.send(embed=embed)

#Lockdown Command
@client.command()
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):
    for channel in ctx.guild.channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send('The server is now on lockdown!')


#Unlockdown Command
@client.command()
@commands.has_permissions(manage_channels=True)
async def unlockdown(ctx):
    for channel in ctx.guild.channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=None)
    await ctx.send('Server is now unlocked')



"""
===========================
MODERATION COMMANDS
===========================
"""

#Kick Command
@client.command(aliases=['boot'], pass_content=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member=None, *, reason=None):
    if member == None:
        await ctx.send('Who are you going to kick?')
    else:
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(title='User Kicked!',
                                  description='User ' + member.display_name +' has been kicked', color=random.choice(colors))
            if reason:
                embed.add_field(name='Reason', value=str(reason), inline=False)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed1 = discord.Embed(
                title='Cannot Kick!',
                description='I don\'t have enough permissions to kick ' +
                member.mention + '!',
                color=random.choice(colors))
            await ctx.send(embed=embed1)

#Ban Command
@client.command(aliases=['hammer'], pass_content=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None, *, reason=None):
    if member == None:
        await ctx.send('Who are you going to ban?')
    else:
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(title='User Banned!',
                                  description='User ' + member.display_name +
                                  ' has been banned!',
                                  color=random.choice(colors))
            if reason:
                embed.add_field(name='Reason', value=str(reason), inline=False)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed1 = discord.Embed(
                title='Cannot Ban!',
                description='I don\'t have enough permissions to ban ' +
                member.mention + '!',
                color=random.choice(colors))
            await ctx.send(embed=embed1)

#Warn Command
@client.command(name='warn', pass_content=True)
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member=None, *, reason=None):
    if member == None:
        await ctx.send('Who are you going to warn?')
    if reason == None:
        await ctx.send('Why are they being warned?')
    else:
        wEmbed = discord.Embed(
                title='Warning!',
                description=f'This is a one time warning, {member.mention}.',
                color=0xFF0000)
        wEmbed.add_field(name='Reason', value=reason)
        embed0 = discord.Embed(
                title='Warning Stats',
                description=f'Username: {member.mention}',
        color=0xFF0000)
        embed0.add_field(name='Reason for Warn', value=str(reason))
        
        await ctx.send(embed=embed0)
        try:
            await member.send(embed=wEmbed)
        except:
            embed = discord.Embed(title=':x: Couldn\'t DM User',
                                  description='I couldn\'t DM ' + member.mention + ', they probably blocked me.',
                                  color=random.choice(colors))
            await ctx.send(embed=embed)


#Mute Command
@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        await ctx.send('Who are you going to mute?')
        return
    if reason == None:
        await ctx.send('Why are they being muted?')
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name='muted')

    if not mutedRole:
        mutedRole = await guild.create_role(name="muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages = False, read_message_history = True, add_reactions=False)

    embed = discord.Embed(title='Member Muted!', description=f"{member.mention} was muted", color=random.choice(colors))
    embed.add_field(name='Reason', value=reason, inline = False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    try:
        await member.send(f"You have been muted in {guild.name}!")
        await member.send('Reason: '+reason)
    except:
        pass


#Unmute Command
@client.command()
@commands.has_permissions(manage_messages = True)
async def unmute(ctx, member: discord.Member = None):
    if member == None:
        await ctx.send('Who are you going to unmute?')
        return
    mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
    try:
        await member.remove_roles(mutedRole)
    except:
        await ctx.send('That member isn\'t muted!')
    try:
        await member.send(f"You have been unmtued in {ctx.guild.name}")
    except:
        pass
    embed = discord.Embed(title='Unmuted!', description=f"{member.mention} has been unmuted!", color=random.choice(colors))
    await ctx.send(embed=embed)


#Tempmute Command
@client.command()
@commands.has_permissions(manage_messages = True)
async def tempmute(ctx, member: discord.Member = None, time = None, *, reason = None):
    if member == None:
        await ctx.send('Who are you going to tempmute?')
        return
    if time == None:
        await ctx.send('How many minutes are they going to be muted?')
        return
    if reason == None:
        await ctx.send('Why are they being tempmuted?')
    try:
        int(time)
    except:
        await ctx.send('Please input a number of minutes for the time!')
        return
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name='muted')

    if not mutedRole:
        mutedRole = await guild.create_role(name="muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages = False, read_message_history = True, add_reactions=False)

    embed = discord.Embed(title='Member Muted!', description=f"{member.mention} was tempmuted for "+str(time)+" minutes for ", color=random.choice(colors))
    embed.add_field(name='Reason', value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    try:
        await member.send(f"You have been muted in {guild.name} for {str(time)} minutes!")
    except:
        pass
    await asyncio.sleep(int(time) * 60)
    await member.remove_roles(mutedRole)
    try:
        await member.send(f"You have been unmuted in {ctx.guild.name}")
    except:
        pass
    embed = discord.Embed(title='Unmuted!', description=f"{member.mention} has been unmuted!", color=random.choice(colors))
    await ctx.send(embed=embed)

#Slowmode Command
@client.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds=None):
    if seconds == None:
        await ctx.send('How many seconds do you want the slowmode to be?')
    try:
        int(seconds)
    except:
        await ctx.send('Please enter a number of seconds the slowmode should be!')
    else:
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(title='Slowmode Set!',
                                  description='Set this channel\'s slowmode to ' +
                                  str(seconds) + ' seconds!',
                                  color=random.choice(colors))
            await ctx.send(embed=embed)
        except:
            await ctx.send('Please enter a valid number between 0 and 100!')

#Nuke Command
@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx, channel: discord.TextChannel = None):
    if channel == None:
        channel = ctx.channel

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel == None:
        await ctx.send(f'{channel.name} is not a valid channel')
    else:
        pos = channel.position
        new_channel = await nuke_channel.clone()
        await new_channel.edit(position=pos)
        await nuke_channel.delete()
        msg = await new_channel.send('THIS CHANNEL HAS BEEN NUKED BY '+ctx.author.mention+'\n\nhttps://tenor.com/view/saussi%c3%a7on-explode-boom-gif-16089684')
        await asyncio.sleep(5)
        await msg.delete()

#Purge Command
@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit=10):
    await ctx.channel.purge(limit = limit+1)
    embed = discord.Embed(title='Deleted '+str(limit)+' messages!', description='Messages purged by '+ctx.author.mention, color=random.choice(colors))
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await msg.delete()

#Snipe Command
@client.command()
@commands.has_permissions(manage_messages=True)
async def snipe(ctx):
    if snipe_message_content is None:
        await ctx.send("There's nothing to snipe.")
    else:
        msgauthor = client.get_user(snipe_message_author)
        if msgauthor is None:
            await ctx.send("User not found.")
        else:
            embed = discord.Embed(title="Message Deleted", description=f"{snipe_message_content}")
            embed.set_author(name=msgauthor.name, icon_url=msgauthor.avatar)
            embed.set_footer(text=f"Channel: #{ctx.channel.name}", icon_url=ctx.guild.icon)
            await ctx.send(embed=embed)


"""
=================================
FUN COMMANDS
=================================
"""


#Guilds Command
@client.command(name='guilds')
async def servers(ctx):
    embed = discord.Embed(
        title='Vector\'s Server Stats',
        description=f"This bot is in {len(client.guilds)} servers!",
        color=random.choice(colors))
    await ctx.send(embed=embed)


#RPS Command
@client.command(name='rps')
async def rps(ctx, choice):
    choices = ['rock', 'paper', 'scissors']
    if choice.lower() not in choices:
        embed = discord.Embed(
            title='Not a choice!',
            description='You can only enter "rock", "paper", or "scissors"!',
            color=random.choice(colors))
        await ctx.send(embed=embed)
    else:
        bot_choice = random.choice(choices)
        if choice == bot_choice:
            tie = discord.Embed(title='Tie Game!',
                                description='You chose: ' + choice +
                                '\nBot chose: ' + bot_choice,
                                color=random.choice(colors))
            await ctx.send(embed=tie)
        elif choice == 'rock' and bot_choice == 'paper' or choice == 'scissors' and bot_choice == 'rock' or choice == 'paper' and bot_choice == 'scissors':
            lose = discord.Embed(title='You Lose!',
                                 description='You chose: ' + choice +
                                 '\nBot chose: ' + bot_choice,
                                 color=random.choice(colors))
            await ctx.send(embed=lose)
        else:
            win = discord.Embed(title='You Win!',
                                description='You chose: ' + choice +
                                '\nBot chose: ' + bot_choice,
                                color=random.choice(colors))
            await ctx.send(embed=win)

#PFP command
@client.command(name='pfp')
async def pfp(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    await ctx.send(member.avatar.url)

#Hack Command
@client.command()
async def hack(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    msg = await ctx.send(f"Hacking {member.mention}...")
    await asyncio.sleep(2)
    embed1 = discord.Embed(title='Bad Records:', description='1/22/2023: stole red pockets from grandma on Chinese New Year\n\n5/9/2022: didn\'t give his mom a mother\'s day card\n\n4/22/2022: dumped the neighborhood trash cans onto the street after Earth Day cleanup', color=random.choice(colors))
    await msg.edit(embed=embed1)
    await asyncio.sleep(3)
    embed2 = discord.Embed(title='Last Messages Sent', description='1 min ago: "wtf stfu u idiot"\n\n5 min ago: "he\'s a dumb idiot"\n\n', color=random.choice(colors))
    await msg.edit(embed=embed2)
    await asyncio.sleep(2)
    passwords = ['meedummy123', '12345678',f'{member.display_name}-dapog', 'superman']
    password = random.choice(passwords)
    embed3=discord.Embed(title='Discord Account Login', description=f'Email: {member.display_name}@gmail.com\nPassword: '+password+'\n2FA: On, but bypassed', color=random.choice(colors))
    ip = random.randint(10000000,99999999)
    embedi = discord.Embed(title='IP Address', description=str(ip), color=random.choice(colors))
    await msg.edit(embed=embedi)
    await asyncio.sleep(5)
    await msg.edit(embed=embed3)
    await asyncio.sleep(5)
    embed4 = discord.Embed(title='Hacking For Nitro', description='Getting credit card from local browser "Chrome"...', color=random.choice(colors))
    await msg.edit(embed=embed4)
    await asyncio.sleep(3)
    embed5 = discord.Embed(title='Code Failed, Retrying Backup...', description='Looking in file directories for browsers...', color=random.choice(colors))
    await msg.edit(embed=embed5)
    embed6 = discord.Embed(title='Nitro Classic Has Been Purchased', description='Nitro Classic Retrieved, but link corrupted (still works): https://dis.cord.gifts/c/XAoXrdBRiaG96VDr', color=random.choice(colors))
    await asyncio.sleep(5)
    await msg.edit(embed=embed6)
    embed7 = discord.Embed(title='Hack Complete!', description=f'FInished hacking {member.mention}!', color=random.choice(colors))
    await asyncio.sleep(5)
    await msg.edit(embed=embed7)
    await asyncio.sleep(5)
    await msg.delete()




#Search Command
def wiki_summary(arg):
    try:
        definition = wikipedia.summary(arg, sentences=3,auto_suggest=True, redirect=True)
    
        return definition
    except:
        return 'No results for that word!'
    
@client.command(aliases=['define','lookup','whatis'])
async def search(ctx, *, word):
    search = discord.Embed(title=f'Search Result for {word}', description=wiki_summary(word), color=random.choice(colors))
    await ctx.send(embed=search)


#8Ball Command
@client.command(name='8ball', aliases=['ask'])
async def _8ball(ctx, *, question = None):
    if question == None:
        await ctx.send('What do you want to ask the 8ball?')
        return
    responses = [
    discord.Embed(title='It is certain.'),
    discord.Embed(title='It is decidedly so.'),
    discord.Embed(title='Without a doubt.'),
    discord.Embed(title='Yes - definitely.'),
    discord.Embed(title='You may rely on it.'),
    discord.Embed(title='Most likely.'),
    discord.Embed(title='Outlook good.'),
    discord.Embed(title='Yes.'),
    discord.Embed(title='Signs point to yes.'),
    discord.Embed(title='Reply hazy, try again.'),
    discord.Embed(title='Ask again later.'),
    discord.Embed(title='Better not tell you now.'),
    discord.Embed(title='Cannot predict now.'),
    discord.Embed(title='Concentrate and ask again.'),
    discord.Embed(title="Don't count on it."),
    discord.Embed(title='My reply is no.'),
    discord.Embed(title='My sources say no.'),
    discord.Embed(title='Outlook not very good.'),
    discord.Embed(title='Very doubtful.')
    ]
    responses = random.choice(responses)
    await ctx.send(content=f'Question: {question}\nAnswer:', embed=responses)

#Shoot Command
@client.command()
async def shoot(ctx, member: discord.Member = None):
    if not member:
        await ctx.send('Who are you going to shoot?')
    else:
        user = ctx.message.author.mention
        sembed = discord.Embed(title='WOAH THERE\'S A SHOOTING!', description=str(user)+' SHOT '+member.mention, color=random.choice(colors))
        await ctx.send(embed=sembed)

#Ping Command
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency*1000)}ms")
    
"""
#Image Generator Command
@client.command()
async def image(ctx, *, image = None):
    if image == None:
        await ctx.send('What image do you want to generate?')
    else:
        embed = discord.Embed(title='Image Generated!', description='Generated the image '+image+'!', color=random.choice(colors))
        await ctx.send(embed=embed)
"""   


# Chat Command
        
client.run("MTA3MTU4OTc0OTI4Mzg4OTIyMw.GqCUEa.5WzLzCmbOQTFJ3dtzGVIGKUKZRJUgYbt0pKkP4")