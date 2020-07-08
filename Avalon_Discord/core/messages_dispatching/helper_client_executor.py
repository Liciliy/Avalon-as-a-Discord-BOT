import discord
import logging
import asyncio


from threading import Thread

from .helping_client import HelpingClient

class HelperClientExecutor:
    _thread = None
    _loop   = None
    _client = None
    _client_token = None

    def __init__(self, tasks_queue, client_token):
        self._client_token = client_token
        self._loop         = asyncio.new_event_loop()
        self._client       = HelpingClient(tasks_queue, 
                                           loop_to_run = self._loop)
          
    @property
    def loop(self):
        return self._loop

    @property
    def thread (self):
        return self._thread
    
    def start(self, thread_name):
        logging.info('Creating a new thread...')
        self._thread = Thread(target = self._run, 
                              args   = (self._client_token,), 
                              daemon = True)
        
        self._thread.name = thread_name
        logging.info('Thread is created. Starting the thread...')
        self._thread.start()

    def _run(self, token):
        logging.info('Attaching event loop to a current thread...')
        asyncio.set_event_loop(self._loop)
        logging.info('Starting client in a blocking manner....')
        self._client.run(token)
    
    # TODO Consider to add stop functionality?