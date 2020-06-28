import discord
import logging

from ..utils import form_embed

import core.panels.constants_game_panel_handler as const

from ..common import NotImplementedMethodUsage

class ContentType:
    FILE  = 0
    EMBED = 1
    TEXT  = 2    

class AbsGamePanelHandler:
    _game         = None
    _channel      = None
    _message      = None
    _msg_content  = None
    content_type  = None
    
    def __init__(self, game, channel, content_type):
        self._game         = game
        self._channel      = channel
        self._content_type = content_type

    async def publish(self, content = None):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: publish')

    async def __update_and_publish(self, content = None):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: __update_and_publish')

    async def __create_and_publish(self, content = None): 
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: __create_and_publish')

    async def delete(self):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: delete')

    async def on_reaction(self, payload):
        str_to_log = 'Got un-handled reaction act: '

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

        logging.error(str_to_log)

    @property
    def id(self):
        result = None
        if self._message != None:
            result = self._message.id
        return result