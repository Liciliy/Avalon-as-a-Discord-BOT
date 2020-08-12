import sys
import discord
import asyncio
import logging
import traceback


from .task import MsgActType, ContentType

class HelpingClient(discord.Client):   

    _task_queue   = None
    _bg_task      = None
    _client_ready = None

    def __init__(self, queue_with_taks, loop_to_run, *args, **kwargs):
        
        super().__init__(loop = loop_to_run, *args, **kwargs)

        self._task_queue = queue_with_taks

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

                logging.info('Got {num} new task(s)'.format(num = len(tasks)))

                for task in tasks:
                    try:

                        logging.info(task)
    
                        if task.type == MsgActType.DEL:
                            logging.info('Removing message.')
                            await self.http.delete_message(
                                task.channel_id, 
                                task.message_id)

                        elif task.type == MsgActType.ADD_REACT:
                            logging.info('Adding reaction: ' 
                                         + str(task.content))

                            await self.http.add_reaction(
                                channel_id = task.channel_id,
                                message_id = task.message_id,
                                emoji      = task.content)  

                        elif task.type == MsgActType.DEL_REACT:
                            logging.info('Removing reaction: ' 
                                         + str(task.content))

                            await self.http.remove_reaction(
                                channel_id = task.channel_id, 
                                message_id = task.message_id,
                                emoji      = task.content,
                                member_id  = task.member_id)     

                        elif task.type == MsgActType.DEL_OWN_REACT:
                            logging.info('Removing bot reaction: ' 
                                         + str(task.content))

                            await self.http.remove_own_reaction(
                                channel_id = task.channel_id, 
                                message_id = task.message_id, 
                                emoji      = task.content)                                                            
          
                        elif task.type == MsgActType.DEL_ALL_REACT:
                            logging.info('Removing all reactions: ' 
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
                                logging.info('Message type is Embed.')
                                embed = task.content
    
                            elif task.content_type == ContentType.TEXT:
                                logging.info('Message type is Text.')
                                text = task.content
                            else:
                                # TODO think about processing an error somehow
                                # here.
                                logging.error('Wrong content type received: ' 
                                               + str(task.content_type))
    
                            if task.type == MsgActType.SEND:
                                logging.info('Sending a message.')
    
                                if text  != None: text  = str(text)
                                if embed != None: embed = embed.to_dict()
   
                                await self.http.send_message(
                                    task.channel_id, 
                                    content = text, 
                                    embed = embed)
                                
                                logging.info('Msg sent.')
    
                            else:
                                logging.info('Editing a message.')
                                fields = dict()
                                if text  != None: 
                                    fields['content'] = str(text)
                                if embed != None: 
                                    fields['embed'] = embed.to_dict()
    
                                await self.http.edit_message(task.channel_id, 
                                                             task.message_id, 
                                                             **fields)
                    
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
            
            await asyncio.sleep(0.01)

    # TODO Consider to add stop functionality?
                    

