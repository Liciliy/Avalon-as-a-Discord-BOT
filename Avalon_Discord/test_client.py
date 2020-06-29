import discord
import logging
import asyncio

from collections import deque

from core.panels.vote_panel_handler import VotePanelHandler
from core.utils import form_embed

from core.panels.timer_panel_handler import Timer

from threading import Thread

class HelpingClient:
    _thread = None
    _loop   = None
    _client = None
    _delay  = None

    def __init__(self, exec_delay):
        self._loop = asyncio.new_event_loop()
        self._delay = exec_delay
        client = discord.Client(loop = self._loop)
        
        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            if  message.content.startswith('roflan'):
                print ('Sleeping for: ', self._delay)
                await asyncio.sleep(self._delay)
                await message.channel.send('kekan!')

        self._client = client


    
    @property
    def loop(self):
        return self._loop

    @property
    def thread (self):
        return self._thread
    
    def start(self, token):
        self._thread = Thread(target = self._run, 
                              args   = (token,), 
                              daemon = True)
        self._thread.start()

    def _run(self, token):
        asyncio.set_event_loop(self._loop)
        self._client.run(token)