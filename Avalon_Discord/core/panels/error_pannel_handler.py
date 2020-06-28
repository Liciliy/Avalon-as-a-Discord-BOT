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

    async def __create_and_publish(self, content):
        self._message = await self._channel.send(embed = content)
        self._msg_content = self._message.content

    async def __update_and_publish(self, content):
        await self._message.edit(embed = content)
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
            await self.__create_and_publish(error_embed)
        else: await self.__update_and_publish(error_embed)
    
        await self._message.add_reaction(const.RED_CROSS)

    async def on_reaction(self, payload):
        str_to_log = 'Got reaction for an error message. Reaction was: '
        
        if payload.event_type == const.REACTION_ADD\
          and str(payload.emoji) == const.RED_CROSS:

            str_to_log = str_to_log + const.REACTION_ADD + '. '\
                       + 'Added by: '   + payload.member.name + '. '\
                       + 'Message ID: ' + str(payload.message_id) + '. '\
                       + 'User ID: '    + str(payload.user_id) + '. '\
                       + 'Channel ID: ' + str(payload.channel_id) + '. '\
                       + 'Guild ID: '   + str(payload.guild_id) + '. '\
                       + 'Emoji: '      + str(payload.emoji) + '. '  

            logging.debug(str_to_log)

            await self.delete()

        elif payload.event_type == const.REACTION_REM:
            str_to_log += const.REACTION_REM + '. '\
                       + 'Message ID: ' + str(payload.message_id) + '. '\
                       + 'User ID: '    + str(payload.user_id) + '. '\
                       + 'Channel ID: ' + str(payload.channel_id) + '. '\
                       + 'Guild ID: '   + str(payload.guild_id) + '. '\
                       + 'Emoji: '      + str(payload.emoji) + '. '

            logging.debug(str_to_log)