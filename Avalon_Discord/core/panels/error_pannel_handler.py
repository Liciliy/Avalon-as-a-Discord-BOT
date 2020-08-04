from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType

import discord
import logging

from ..utils import form_embed

import core.panels.constants_game_panel_handler as const

class ErrorPanelHandler(AbsGamePanelHandler):
    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.EMBED)

    async def _create_and_publish(self, content):
        self._message = await self._channel.send(embed = content)
        self._msg_content = self._message.content
    
    # TODO use task orrder/message dispatcher here
    def _update_and_publish(self, content):
        # await self._message.edit(embed = content)
        self._msg_content = self._message.content

    async def delete(self):
        if self._message != None:
            await self._message.delete()
            self._message = None
    
    async def publish(self, content = None):
        error_embed = form_embed(
            title  = content.title,
            descr  = content.text,
            footer = content.footer,
            colour = discord.Colour.red())
        
        if self._message == None:
            await self._create_and_publish(error_embed)
        else: self._update_and_publish(error_embed)
    
        await self._message.add_reaction(const.RED_CROSS)

    # TODO delete message using task ordering
    async def on_reaction(self, payload):
        str_to_log = 'Got reaction for an error message. Reaction was: ' \
                   + self._get_react_payload_info_as_string(payload) 
        
        if payload.event_type == const.REACTION_ADD\
          and str(payload.emoji) == const.RED_CROSS:
            await self.delete()

        logging.debug(str_to_log)