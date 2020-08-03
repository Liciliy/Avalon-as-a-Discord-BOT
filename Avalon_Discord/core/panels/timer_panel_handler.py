import asyncio
import logging 
import core.panels.constants_game_panel_handler as const

from collections import deque

from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType,\
    PanelContent

from ..content_handlers.timer_content_handler import\
    TimerContentHandler
   
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

    async def on_reaction(self, payload):
        str_to_log = 'Got reaction act: '

        if   payload.event_type == const.REACTION_ADD:
            str_to_log = str_to_log + const.REACTION_ADD + '. '\
                       + 'Added by: '   + payload.member.name + '. '\
                       + 'Message ID: ' + str(payload.message_id) + '. '\
                       + 'User ID: '    + str(payload.user_id) + '. '\
                       + 'Channel ID: ' + str(payload.channel_id) + '. '\
                       + 'Guild ID: '   + str(payload.guild_id) + '. '\
                       + 'Emoji: '      + str(payload.emoji) + '. '  
            
        elif payload.event_type == const.REACTION_REM:
            str_to_log += const.REACTION_REM + '. '\
                       + 'Message ID: ' + str(payload.message_id) + '. '\
                       + 'User ID: '    + str(payload.user_id) + '. '\
                       + 'Channel ID: ' + str(payload.channel_id) + '. '\
                       + 'Guild ID: '   + str(payload.guild_id) + '. '\
                       + 'Emoji: '      + str(payload.emoji) + '. '

        logging.info(str_to_log)

        self._content_handler.handle_reaction(str(payload.emoji))