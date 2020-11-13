import os
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

    if message.content.startswith('not_akajabi_test'):
        user = client.get_user(743480034383102013)
        await user.send('Hello') 


    if message.content.startswith('kajabi_test'):
        user = client.get_user(757563852043845653)


        await user.send('Hello')

        #if user.dm_channel == None:
        #    await user.create_dm()

        #dmc = user.send

    if message.content.startswith('soundon'):

        user = message.author

        print(user)

        voice_state   = user.voice
        print(voice_state)
        voice_channel = voice_state.channel
        # only play music if user is in a voice channel
        if voice_channel != None:
            vc = await voice_channel.connect()

            #player = vc.create_ffmpeg_player('hearbeat.wav', after = lambda: print('done'))
            #player.start()
            #while not player.is_done():
            #    await asyncio.sleep(1)

            #await vc.disconnect()

            sounds_dir_name = 'sounds'

            this_dir = os.path.dirname(os.path.realpath(__file__))

            sounds_dir = os.path.join(str(this_dir), sounds_dir_name)

            first_sound = os.path.join(sounds_dir, "analog-alarm-clock_quiter_2_sec.wav")
            third_sound = os.path.join(sounds_dir, "hearbeat_quiet_14_5_sec.wav")
         
            

            

            hb = discord.FFmpegPCMAudio(third_sound)

            if not vc.is_playing():
                vc.play(hb, after=None)

            while vc.is_playing():
                await asyncio.sleep(0.2)                

            clock = discord.FFmpegPCMAudio(first_sound)

            if not vc.is_playing():
                vc.play(clock, after=None)


            while vc.is_playing():
                await asyncio.sleep(0.2)    



            await vc.disconnect()

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
    
    if message.content.startswith('emt'):
        msg = await message.channel.send('Lol a message')

        MISSION_SUCCESS_EMOJI = '✅'
        await message.channel.send(MISSION_SUCCESS_EMOJI)
        await asyncio.sleep(3)

        await msg.edit(content = '')


client.run('NzA2ODYwNDQ1MTU1NDU5MDgz.XrAajQ.M19zJPXV-DhdObx7MgWaSw-zdL4')