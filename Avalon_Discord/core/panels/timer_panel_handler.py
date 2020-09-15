import asyncio
import logging 
import discord
import core.panels.constants_game_panel_handler as const

from discord import Embed

from collections import deque

from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType,\
    PanelContent

from ..content_handlers.timer_content_handler import\
    TimerContentHandler

class TimerPanelHandler(AbsGamePanelHandler):    

    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.EMBED)                  

    async def _create_and_publish(self, content):
        self._message = await self._channel.send(embed = self.to_embed(content))
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
                self.order_edit_task(self.to_embed(content.text), 
                                     self._message.id)
            if content.reactions != None:
                for reaction in content.reactions:
                    self.order_add_reaction(reaction, self._message.id)
        else:
            self.order_edit_task(self.to_embed(content), self._message.id)

        self._msg_content = content

    async def delete(self):
        if self._message != None:
            await self._message.delete()
            self._message = None

    async def publish(self, content = None):
        if self._message == None:
            await self._create_and_publish(content)
        else: self._update_and_publish(content)    

    # TODO looks like below function has no need in being async.
    # Or, maybe, since it is an interface funct - it should be...
    # Need to investigate - check all on_reaction functions.
    async def on_reaction(self, payload):
        # TODO dont react on reaction removal.
        str_to_log = 'Got reaction act: ' \
                   + self._get_react_payload_info_as_string(payload) 

        logging.info(str_to_log)

        if payload.event_type == const.REACTION_REM:
            return

        self.order_del_reaction(payload.emoji, self.id)
        self._content_handler.handle_reaction(str(payload.emoji))
    
    def to_embed(self, text):
        embed = \
            Embed(
                colour      = discord.Colour(0x1fca2c), 
                description = text )

        picture_url = self._content_handler.get_talking_entity_picture_url()

        logging.info('Embed text is: ' + str(text))

        if picture_url != None:
            embed.set_thumbnail(url = picture_url)
            logging.warn('Avatar URL is: ' + str(picture_url))
        else:
            logging.warn('Could not fetch avatar.')

        return embed