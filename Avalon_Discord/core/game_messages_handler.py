import logging

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
    content_type = None

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
        await self._message.delete()

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
        await self._message.delete()

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
        await self._message.delete()
    
    async def publish(self, content = None):
        if self._message == None:
            await self.__create_and_publish(content)
        else: await self.__update_and_publish(content)


