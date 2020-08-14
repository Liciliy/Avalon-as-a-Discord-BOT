import logging

from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType
    
class SelectionPanelHandler(AbsGamePanelHandler):  

    _message = None  

    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.TEXT)   

    async def publish(self, content = None): 
        if self._message == None:
            await self._create_and_publish(content)
        else: self._update_and_publish(content)      
        
    async def _create_and_publish(self, content):
        self._message = await self._channel.send(content = content)
        self._msg_content = content

    async def delete(self):
        if self._message != None:
            await self._message.delete()
            self._message = None

    def update_and_publish(self, content): 
        if content.text != None:
            self.order_edit_task(content.text, self._message.id)
        if content.reactions != None:
            for reaction in content.reactions:
                self.order_add_reaction(reaction, self._message.id)
            
        self._msg_content = content

    async def on_reaction(self, payload):
        str_to_log = 'Got reaction act: ' \
                   + self._get_react_payload_info_as_string(payload) 

        logging.info(str_to_log)
        self._content_handler.handle_reaction(payload, self)

    def clear_reactions(self):
        logging.info('Clearing reactions')
        self.order_remove_all_reactions(self._message.id)