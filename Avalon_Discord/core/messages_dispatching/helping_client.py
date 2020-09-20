import sys
import discord
import asyncio
import logging
import traceback


from .task import MsgActType, ContentType

from .edit_task import EditMsgTask

class HelpingClient(discord.Client):   

    _task_queue   = None
    _bg_task      = None
    _client_ready = None
    _helper_id    = None
    _edit_tasks_queue = None

    def __init__(self, 
                 tasks_queue, 
                 client_id, 
                 loop_to_run, 
                 edit_tasks_queue,
                 *args, 
                 **kwargs):
        
        super().__init__(loop = loop_to_run, *args, **kwargs)

        self._task_queue = tasks_queue
        self._helper_id = client_id
        self._edit_tasks_queue = edit_tasks_queue

        self._bg_task =\
            loop_to_run.create_task(self.check_queue_and_execute_tasks())

        self._client_ready = False

    async def on_ready(self):
        print('Helping client logged in as:',
              str(self.user.name),
              str(self.user.id))
        self._client_ready = True

    async def check_queue_and_execute_tasks(self):
        logging.info(
            'In task polling function. Waiting until client is ready...')

        while not self._client_ready:
            await asyncio.sleep(0.05)

        logging.info('Start polling for tasks...')

        while not self.is_closed():

            if not self._task_queue.is_empty:
                tasks = self._task_queue.get_tasks()

                logging.debug('Got {num} new task(s)'.format(num = len(tasks)))

                for task in tasks:
                    try:

                        logging.debug(task)
    
                        if task.type == MsgActType.DEL:
                            logging.debug('Removing message.')
                            await self.http.delete_message(
                                task.channel_id, 
                                task.message_id)

                        elif task.type == MsgActType.ADD_REACT:
                            logging.debug('Adding reaction: ' 
                                         + str(task.content))

                            await self.http.add_reaction(
                                channel_id = task.channel_id,
                                message_id = task.message_id,
                                emoji      = task.content)  

                        elif task.type == MsgActType.DEL_REACT:
                            logging.debug('Removing reaction: ' 
                                         + str(task.content))

                            await self.http.remove_reaction(
                                channel_id = task.channel_id, 
                                message_id = task.message_id,
                                emoji      = task.content,
                                member_id  = task.member_id)     

                        elif task.type == MsgActType.DEL_OWN_REACT:
                            logging.debug('Removing bot reaction: ' 
                                         + str(task.content))

                            await self.http.remove_own_reaction(
                                channel_id = task.channel_id, 
                                message_id = task.message_id, 
                                emoji      = task.content)                                                            
          
                        elif task.type == MsgActType.DEL_ALL_REACT:
                            logging.debug('Removing all reactions: ' 
                                         + str(task.content))

                            await self.http.clear_reactions(
                                channel_id = task.channel_id, 
                                message_id = task.message_id)   

                        elif task.type == MsgActType.SEND \
                          or task.type == MsgActType.EDIT:
                            text  = None
                            embed = None
    
                            if task.content_type == ContentType.FILE:
                                logging.info('Message type is File.')
                                # TODO implement file sending
                                # TODO need separate test for this type of msg content.
                                text = ' File send NOT implemented yet'
                            elif task.content_type == ContentType.EMBED:
                                logging.debug('Message type is Embed.')
                                embed = task.content
    
                            elif task.content_type == ContentType.TEXT:
                                logging.debug('Message type is Text.')
                                text = task.content
                            else:
                                # TODO think about processing an error somehow
                                # here.
                                logging.error('Wrong content type received: ' 
                                               + str(task.content_type))
    
                            if task.type == MsgActType.SEND:
                                logging.debug('Sending a message.')
    
                                if text  != None: text  = str(text)
                                if embed != None: embed = embed.to_dict()
   
                                await self.http.send_message(
                                    task.channel_id, 
                                    content = text, 
                                    embed = embed)
                                
                                logging.debug('Msg sent.')
    
                            else:
                                logging.debug('Editing a message.')
                                fields = dict()
                                if text  != None: 
                                    fields['content'] = str(text)
                                if embed != None: 
                                    fields['embed'] = embed.to_dict()

                                if task.edit_in_queue == False:

                                    await self.http.edit_message(
                                        task.channel_id, 
                                        task.message_id, 
                                        **fields)                                    

                                elif task.edit_in_queue == True:  

                                    edit_task = EditMsgTask(task.channel_id, 
                                                            task.message_id, 
                                                            fields)
    
                                    self._edit_tasks_queue.add_task(edit_task)                                  
                    
                        else:
                            # TODO think about processing an error somehow here.
                            logging.error('Wrong task type received: ' 
                                           + str(task.type))                        

                    except Exception as ex:
                        logging.error('Exception as string: ' 
                                      + str(ex))
                        logging.error('Sys exec info: '       
                                      + str(sys.exc_info()[0]))
                        logging.error('Traceback: '           
                                      + str(traceback.format_exc()))

                        logging.error('Executed task:\n' + str(task))           
                        
                        # TODO here thing if it is needed to re-raise 
                        # the exception or react on it somehow.

            try:
                self._edit_tasks_queue.process_edit_task_queue(
                        self._helper_id,
                        asyncio.get_running_loop(),
                        self
                    )

            except Exception as ex:
                    logging.error('Exception as string: ' 
                                  + str(ex))
                    logging.error('Sys exec info: '       
                                  + str(sys.exc_info()[0]))
                    logging.error('Traceback: '           
                                  + str(traceback.format_exc()))

                    logging.error('Executed task:\n' + str(task))           
                    
                    # TODO here thing if it is needed to re-raise 
                    # the exception or react on it somehow.

            await asyncio.sleep(0.01)

    # TODO Consider to add stop functionality?
                    

