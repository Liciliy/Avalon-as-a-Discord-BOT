import logging

from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType
    
class TablePanelHandler(AbsGamePanelHandler):  

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
        self.order_edit_task(content, self._message.id)
            
        self._msg_content = content