import discord
import logging
import asyncio


LETTER_TO_EMOJI = {
    'a' : ':regional_indicator_a:',
    'b' : ':regional_indicator_b:',
    'c' : ':regional_indicator_c:',
    'd' : ':regional_indicator_d:',
    'e' : ':regional_indicator_e:',
    'f' : ':regional_indicator_f:',
    'g' : ':regional_indicator_g:',
    'h' : ':regional_indicator_h:',
    'i' : ':regional_indicator_i:',
    'j' : ':regional_indicator_j:',
    'k' : ':regional_indicator_k:',
    'l' : ':regional_indicator_l:',
    'm' : ':regional_indicator_m:',
    'n' : ':regional_indicator_n:',
    'o' : ':regional_indicator_o:',
    'p' : ':regional_indicator_p:',
    'q' : ':regional_indicator_q:',
    'r' : ':regional_indicator_r:',
    's' : ':regional_indicator_s:',
    't' : ':regional_indicator_t:',
    'u' : ':regional_indicator_u:',
    'v' : ':regional_indicator_v:',
    'w' : ':regional_indicator_w:',
    'x' : ':regional_indicator_x:',
    'y' : ':regional_indicator_y:',
    'z' : ':regional_indicator_z:'
}

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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):
    global chat_message
    global CHAT_ON
    global last_user_id
    global chat_channel
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
            


client.run('NzA2ODYwNDQ1MTU1NDU5MDgz.XrAajQ.M19zJPXV-DhdObx7MgWaSw-zdL4')