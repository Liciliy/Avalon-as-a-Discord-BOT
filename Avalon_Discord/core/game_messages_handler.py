import discord
import logging

from .utils import form_embed

import core.constants_game_message_handler as const


class NotImplementedMethodUsage(Exception):
    pass 


class ContentType:
    FILE  = 0
    EMBED = 1
    TEXT  = 2


class AbsGameMessageHandler:
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


class ChatMessageHandler(AbsGameMessageHandler):

    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.TEXT)
        
    async def __create_and_publish(self, content):
        self._message = await self._channel.send(content = content)
        self._msg_content = self._message.content

    async def __update_and_publish(self, content):
        await self._message.edit(content = content)
        self._msg_content = self._message.content

    async def delete(self):
        if self._message != None:
            await self._message.delete()
            self._message = None

    async def publish(self, content = None):
        if self._message == None:
            await self.__create_and_publish(content)
        else: await self.__update_and_publish(content)


class ConnectionStatusMsgHandler(AbsGameMessageHandler):
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
        if self._message == None:
            await self.__create_and_publish(content)
        else: await self.__update_and_publish(content)


class ErrorMsgHandler(AbsGameMessageHandler):
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