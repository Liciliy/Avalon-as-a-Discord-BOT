import discord
import logging
import asyncio
#import uvloop

from collections import deque

from core.panels.vote_panel_handler import VotePanelHandler
from core.utils import form_embed

from core.panels.timer_panel_handler import Timer

from test_client import HelpingClient 

from threading import Thread


def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def get_threads_with_loops(num_of_loops):
    threads_list = list()
    loops_deque  = deque()
    delay = 0
    for _ in range (0, num_of_loops):



        new_helper = HelpingClient(delay)
         
        new_helper.start('NzA2ODYwNDQ1MTU1NDU5MDgz.XrAajQ.M19zJPXV-DhdObx7MgWaSw-zdL4')
    
        loops_deque.append(new_helper.loop)
        threads_list.append(new_helper.thread)

        delay = delay + 0.2


    return threads_list, loops_deque



class PanelContentHdlrTester:
    messages = None

    _timer = None

    _threads_list  = None
    _loops_deque   = None

    def __init__(self):
        self._timer = Timer(60, self)
        self.messages = list()
        self._threads_list , self._loops_deque = get_threads_with_loops(8)
    
    async def update_panels(self):
        tasks = list()
        for msg in self.messages:
           #======================================================================================
           #loop_to_use = self._loops_deque[0]
           #self._loops_deque.rotate()
           #coro = msg.edit(content = self._timer.get_segments_string)
           #asyncio.run_coroutine_threadsafe(coro, loop_to_use)     
           #tasks.append(msg.edit(content = self._timer.get_segments_string))

           
      

           #======================================================================================
           fields = dict()
           fields['content'] = self._timer.get_segments_string
           tasks.append(msg._state.http.edit_message(msg.channel.id, msg.id, **fields))

           #======================================================================================


        await asyncio.gather(*tasks)       

    async def timer_expired(self):
        pass

    async def start_timer(self):
        await self._timer.start()
    

tester = PanelContentHdlrTester()


logging.basicConfig(level=logging.INFO)

#uvloop.install()

client = discord.Client()

vote_pan = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    global tester


    if message.author == client.user:
        return

    if message.content.startswith('ttest'):

        for _ in range (0, 8):

            tester.messages.append(await message.channel.send('lal'))
        st_t = asyncio.get_running_loop().time()
        print ('Start time: '  + str(st_t))

        await tester.start_timer()
        en_t = asyncio.get_running_loop().time()
        print ('End time: '  + str(en_t) )

        print('Took ' + str(en_t -st_t))

    
    


client.run('NzA2ODYwNDQ1MTU1NDU5MDgz.XrAajQ.M19zJPXV-DhdObx7MgWaSw-zdL4')