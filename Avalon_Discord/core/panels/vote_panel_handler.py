import logging

from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType

class VotePanelHandler(AbsGamePanelHandler):

    HEADER_KEY    = 'header'
    EMOJIES_KEY   = 'emojies'
    REACTIONS_KEY = 'reactions'

    _header_message = None
    _emoji_message  = None

    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.EMBED)
        
    async def _create_and_publish(self, content):
        self._header_message = await self._channel.send(
            content = content[VotePanelHandler.HEADER_KEY])
        
        self._emoji_message = await self._channel.send(
            content = content[VotePanelHandler.EMOJIES_KEY])

        for reac in content[VotePanelHandler.REACTIONS_KEY]:
            await self._emoji_message.add_reaction(reac)
        
        self._msg_content = content

    # TODO use task orrder/message dispatcher here
    def _update_and_publish(self, content):
        await self._header_message.edit(
            content = content[VotePanelHandler.HEADER_KEY])

        await self._emoji_message.edit(
            content = content[VotePanelHandler.EMOJIES_KEY])

        await self._emoji_message.clear_reactions()   

        for reac in content[VotePanelHandler.REACTIONS_KEY]:
            await self._emoji_message.add_reaction(reac)

        self._msg_content = content

    async def delete(self):
        old_header = self._header_message
        old_emoji  = self._emoji_message

        self._header_message = None
        self._emoji_message  = None

        if old_header != None:
            await old_header.delete()
        
        if old_emoji != None:
            await old_emoji.delete()

    # TODO use task orrder/message dispatcher here
    async def publish(self, content = None):
        if self._header_message == None and self._emoji_message == None:
            logging.info('Creating vote messages')
            await self._create_and_publish(content)

        elif self._header_message != None and self._emoji_message != None:
            logging.info('Editing vote messages')
            self._update_and_publish(content)

        else:
            logging.critical(
                'One message is None; other is not. ' 
                + 'Header msg: ' + str(self._header_message) 
                + ' Emoji msg: ' + str(self._emoji_message))
            
            logging.info('Recreating vote panel.')
            self.delete()
            self.publish(content)