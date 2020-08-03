import asyncio

from collections import deque

from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType,\
    PanelContent
   
class TimerPanelHandler(AbsGamePanelHandler):

    TIME_KEY      = 'time'
    TEXT_KEY      = 'text'
    REACTIONS_KEY = 'reactions'

    _content_handler = None

    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.TEXT)

    def set_content_handler(self, content_handler):
        self._content_handler = content_handler                

    async def _create_and_publish(self, content):
        self._message = await self._channel.send(content = content)
        self._msg_content = content
        
    # Interface version of update and publish.
    def _update_and_publish(self, content):
        self.order_edit_task(content, self._message.id)
        self._msg_content = content
    
    # Below is this-class-unique and public version of update and publish.
    def update_and_publish(self, content):
        """Request other thread to change contents of 
        this panel handler timer message.

        Args:
            content (string or PanelContent): If content type is string
                                              then only msg text is updated.
                                              If PanelContent - both text and
                                              reactions are requested to 
                                              be updated if  they are not None.
        """
        if type(content) == PanelContent:
            if content.text != None:
                self.order_edit_task(content.text, self._message.id)
            if content.reactions != None:
                for reaction in content.reactions:
                    self.order_add_reaction(reaction, self._message.id)
        else:
            self.order_edit_task(content, self._message.id)

        self._msg_content = content

    async def delete(self):
        if self._message != None:
            await self._message.delete()
            self._message = None

    async def publish(self, content = None):
        if self._message == None:
            await self._create_and_publish(content)
        else: self._update_and_publish(content)    