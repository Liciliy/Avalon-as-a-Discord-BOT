import discord
import logging
import asyncio
from core.games_manager import GameManager

logging.basicConfig(level=logging.INFO)

READY = False

client = discord.Client()

@staticmethod

@client.event
async def on_ready():
    global READY
    READY = True
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    global READY
    
    if not READY:                     return
    if message.author == client.user: return
        
    await GameManager.handle_message(message)

client.run('NzA2ODYwNDQ1MTU1NDU5MDgz.XrAajQ.M19zJPXV-DhdObx7MgWaSw-zdL4')