import discord
import logging
import asyncio

from core.panels.vote_panel_handler import VotePanelHandler
from core.utils import form_embed

def get_emoji_name_from_author(author):

    name = ''
    name = author.nick if author.nick != None else author.name
    
    name = name.upper()
    name = '**`' + name + '`**'         
    return name


logging.basicConfig(level=logging.INFO)


CHAT_ON = False
CHAT_START_CONTENT = ':loudspeaker: **CHAT**\n'

chat_message = None
last_user_id = ''
chat_channel = None

client = discord.Client()

vote_pan = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
count = 0
#@client.event
#async def on_reaction_add(reaction, user):
#    global count
#    if count > 0:
#        await reaction.message.delete()
#        #await reaction.remove(user)
#    else: count =+ 1

@client.event
async def on_message(message):
    global chat_message
    global CHAT_ON
    global last_user_id
    global chat_channel

    global vote_pan

    if message.author == client.user:
        return
    elif CHAT_ON and message.channel.id == chat_channel: 
        content = ''
        if chat_message == None:
            content = CHAT_START_CONTENT
            
            emoji_nick = get_emoji_name_from_author(message.author)
            content += emoji_nick + '\n'

            content += message.content.replace('`', '')
            last_user_id = str(message.author)    
            chat_message = await message.channel.send(content)

            await message.delete()
        else:
            content = chat_message.content + '\n'
            if str(message.author) != last_user_id:                
                content += get_emoji_name_from_author(message.author) + '\n'
                last_user_id = str(message.author)
            
            content += message.content.replace('`', '') + '\n'            
            await message.delete()
            await chat_message.edit(content = content)

    if message.content.startswith('crv'):
        vote_pan = VotePanelHandler(None, message.channel)

    if message.content.startswith('vote1'):
        header_embed = form_embed(descr = 'Test vote:',
                                  colour = discord.Color.dark_blue())
        emoji_embed  = form_embed(title = 'Test vote:',
                                  descr = ':rage::kiss:<:P1:720339313824628818>',
                                  colour = discord.Color.dark_blue())
        content = {
            VotePanelHandler.HEADER_KEY    : 'Test vote:',
            VotePanelHandler.EMOJIES_KEY   : ':rage::kiss:<:P1:720339313824628818>',
            VotePanelHandler.REACTIONS_KEY : ['✅', '🚫']            
        }
        await vote_pan.publish(content)

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$chat_on'):        
        print("Chat on")
        CHAT_ON = True
        chat_channel = message.channel.id

    if message.content.startswith('$chat_off'):
        print("Chat off")
        CHAT_ON = False
        chat_channel = None

    if message.content.startswith('$mute_me'):        
        print("mute")
        await message.author.edit(mute = True)

    if message.content.startswith('$unmute_me'):
        print("unmute")
        await message.author.edit(mute = False)

    if message.content.startswith('$timer'):
        time = 20
        timer_message = await message.channel.send('Time left:' + str(time))
        while time != 0:
            await asyncio.sleep(1)
            time = time - 1
            message_str = 'Time left: ' + str(time)
            await timer_message.edit(content = message_str)
        await message.channel.send('Time ended.')
    
    if message.content == 'invite':

        guild = client.get_guild(715959072532201492)

        channel = await guild.create_text_channel(
                'Avalon test channel1')
        
        invite = await channel.create_invite()

        await message.channel.send(invite)


client.run('NzA2ODYwNDQ1MTU1NDU5MDgz.XrAajQ.M19zJPXV-DhdObx7MgWaSw-zdL4')