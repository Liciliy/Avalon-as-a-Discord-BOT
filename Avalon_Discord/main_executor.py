import discord
import logging
import asyncio


import core.utils as utils

from core.games_manager import GameManager
from core.messages_dispatching.messages_dispatcher import MessagesDispatcher

client_token = 'NzA2ODYwNDQ1MTU1NDU5MDgz.XrAajQ.M19zJPXV-DhdObx7MgWaSw-zdL4'

#logging.basicConfig(level=logging.INFO)

root_logger = logging.getLogger()
root_logger.setLevel(20)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(levelname)s:[%(filename)s:%(lineno)d][%(threadName)s][%(asctime)s] - %(message)s')
stream_handler.setFormatter(formatter)

root_logger.addHandler(stream_handler)

READY = False   

client = discord.Client()

message_dispatcher = MessagesDispatcher(client_token)

GameManager.set_client_object(client)

utils.set_messages_dispatcher(message_dispatcher)
GameManager.set_messages_dispatcher_object(message_dispatcher)

async def test_command(message):
    result = False
    if message.content == 'clear':
        result = True
        guild = client.get_guild(715959072532201492)

        for channel in guild.text_channels:
            await channel.delete()
            
        for channel in guild.voice_channels:
            await channel.delete()

        for role in guild.roles:
            try:
                await role.delete()
            except:
                pass
    if message.content == 'cl_users':
        result = True
        guild = client.get_guild(715959072532201492)

        for member in guild.members:
            try:
                await guild.kick(member)   
            except:
                pass            
    
    return result


async def clear_test_guild():
    guild = client.get_guild(715959072532201492)

    for channel in guild.text_channels:
        await channel.delete()
        
    for channel in guild.voice_channels:
        await channel.delete()

    for role in guild.roles:
        try:
            await role.delete()
        except:
            pass
    
    guild = client.get_guild(715959072532201492)

    for member in guild.members:
        try:
            await guild.kick(member)   
        except:
            pass

    for em in guild.emojis:
        await em.delete()

@client.event
async def on_ready():
    # TODO remove below clear in later releases
    await clear_test_guild()
    global READY
    READY = True
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    global READY
    
    if not READY:                     return
    if message.author == client.user: return
    
    # TODO delete this test comamnd at commercial release
    if await test_command(message):
        pass

    else: await GameManager.handle_message(message)

@client.event
async def on_member_join(member):

    global READY

    if not READY:                     return
    logging.info('Got join event')

    # TODO ignore if the bot triggers this event.

    await GameManager.handle_join_event(member)

@client.event
async def on_voice_state_update(member, before, after):
    global READY

    if not READY:                     return
    logging.info('Got voice state change event')

    # TODO ignore if the bot triggers this event.

    await GameManager.handle_voice_change_event(member, before, after)

@client.event
async def on_raw_reaction_add(payload):
    global READY

    if not READY:                         return
    if payload.user_id == client.user.id: return

    logging.info('Got reaction added event')
    await GameManager.handle_user_reaction_event(payload)

@client.event
async def on_raw_reaction_remove(payload):
    global READY

    if not READY:                         return
    if payload.user_id == client.user.id: return

    logging.info('Got reaction removed event')
    await GameManager.handle_user_reaction_event(payload)

client.run(client_token)
