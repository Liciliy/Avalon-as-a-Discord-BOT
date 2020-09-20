import asyncio
import logging

from threading import Lock
from .task_queue import thread_safe
from .edit_task import EditMsgTask
from .helping_client import HelpingClient

from asyncio.events import AbstractEventLoop

class EditTasksQueue:
    HANDLER_ID    = 'hndler_id'
    OREDERED_TASK = 'ordered_task' 
    ASYNC_TASK    = 'async_task' 


    mutex               = None
    _ch_id_to_task_data = None


    def __init__(self):
        self.mutex               = Lock()
        self._ch_id_to_task_data = dict()

    @thread_safe
    def add_task(self, edit_task : EditMsgTask):   
        task_ch_id  = edit_task.channel_id
        task_msg_id = edit_task.message_id 

        logging.info(f'Adding task to edit tasks queud for CH ID {task_ch_id} '
                     + f'and MSG ID {task_msg_id}')

        if not task_ch_id in self._ch_id_to_task_data:
            self._ch_id_to_task_data[task_ch_id] = dict()
        
        msg_id_to_task_data = self._ch_id_to_task_data[task_ch_id]

        if not task_msg_id in msg_id_to_task_data:
            msg_id_to_task_data[task_msg_id] = list()

        msg_id_to_task_data[task_msg_id].append(
            {
                EditTasksQueue.HANDLER_ID    : None,
                EditTasksQueue.OREDERED_TASK : edit_task,
                EditTasksQueue.ASYNC_TASK    : None
            }
        )  


    @thread_safe
    def process_edit_task_queue(self, 
                                this_handler_id, 
                                loop      : AbstractEventLoop,
                                ds_client : HelpingClient):
        
        FIRST_TASK_POS = 0

        for ch_id, msg_ids_to_task_data in self._ch_id_to_task_data.items():

            for msg_id, tasks_dicts_list in  msg_ids_to_task_data.items():
            
                if len(tasks_dicts_list) == 0:
                    continue
    
                first_task_dict = tasks_dicts_list[FIRST_TASK_POS]
    
                first_task : EditMsgTask = \
                    first_task_dict[EditTasksQueue.OREDERED_TASK]
    
                handler_id = first_task_dict[EditTasksQueue.HANDLER_ID]
               
                if handler_id == None:
                    logging.info(
                        f'Starting a new task to CH ID {ch_id} '
                        + f'and MSG ID {msg_id}')
                    
                    self._start_task(first_task_dict, 
                                     this_handler_id, 
                                     loop, 
                                     ds_client, 
                                     first_task)
    
                elif handler_id == this_handler_id\
                       and \
                     first_task_dict[EditTasksQueue.ASYNC_TASK].done():
    
                    logging.info(
                      'A task launched by this helping client is finished.')
                    
                    del tasks_dicts_list[FIRST_TASK_POS]
    
                    if len(tasks_dicts_list) != 0:
                        logging.info(
                            f'Starting next task for CH ID {ch_id} '+
                            f'and MSG ID {msg_id}')
                        next_task_dict = tasks_dicts_list[FIRST_TASK_POS]
    
                        next_task : EditMsgTask = \
                                  next_task_dict[EditTasksQueue.OREDERED_TASK]
    
                        self._start_task(next_task_dict, 
                                         this_handler_id, 
                                         loop, 
                                         ds_client, 
                                         next_task)

    def _start_task(self, 
                    task_dict, 
                    this_handler_id, 
                    loop, 
                    ds_client, 
                    task):

        task_dict[EditTasksQueue.HANDLER_ID] = this_handler_id
                
        async_task = loop.create_task(
            ds_client.http.edit_message(
                task.channel_id,
                task.message_id,
                **task.fields
            )
        )

        task_dict[EditTasksQueue.ASYNC_TASK] = async_task