import discord
import logging
import asyncio

import core.constants_games_manager as const

class GameManager:

    __active_games_list = None
    
    @staticmethod
    async def handle_message(msg):
        if msg.content in const.AVALON_COMMANDS:
            await msg.channel.send('I know this command.')
        else: await msg.channel.send('I DONT know this command.')
