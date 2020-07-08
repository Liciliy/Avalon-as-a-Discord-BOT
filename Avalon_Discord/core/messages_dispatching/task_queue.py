import sys
import time
import logging
import traceback

from threading import Lock
from collections import deque


def thread_safe(func):

    def call_in_thread_safe_manner(self, *args, **kwargs):
        ## TODO Here add some kind of an timeout.
        ## If execution takes too much time - return error.        

        try:
            self.mutex.acquire()
            
            result = func(self, *args, **kwargs)

        except Exception as ex:
            logging.error('Exception as string: ' 
                          + str(ex))
            logging.error('Sys exec info: '       
                          + str(sys.exc_info()[0]))
            logging.error('Traceback: '           
                          + str(traceback.format_exc()))

        finally: 
            self.mutex.release()

        return result
    
    return call_in_thread_safe_manner


class TaskQueue:
    _is_used = None
    _queue   = None
    mutex   = None

    def __init__(self):
        self._is_used = False
        self._queue   = deque()
        self.mutex    = Lock()

    @property
    @thread_safe
    def is_empty(self): 

        result = True       

        if len(self._queue) > 0:
            result = False
            
        return result

    @thread_safe
    def add_task(self, task):  

        logging.info('A task received. Adding to a task list.')

        self._queue.append(task)

    @thread_safe
    def get_tasks(self):
        result = list()

        while len(self._queue) > 0:
            logging.info('A task(s) to execute found. Moving to an executor.')
            result.append(self._queue.popleft())

        return result