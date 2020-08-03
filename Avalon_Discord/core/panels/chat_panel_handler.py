from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType

class ChatPanelHandler(AbsGamePanelHandler):

    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.TEXT)
        
    async def _create_and_publish(self, content):
        self._message = await self._channel.send(content = content)
        self._msg_content = self._message.content
    
    def _update_and_publish(self, content):
        self.order_edit_task(content, self._message.id)
        #await self._message.edit(content = content)
        self._msg_content = self._message.content

    async def delete(self):
        if self._message != None:
            await self._message.delete()
            self._message = None

    async def publish(self, content = None):
        if self._message == None:
            await self._create_and_publish(content)
        else: self._update_and_publish(content)