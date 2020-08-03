from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType
    
class ConnectionStatusPanelHandler(AbsGamePanelHandler):
    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.EMBED)

    async def _create_and_publish(self, content):
        self._message = await self._channel.send(embed = content)
        self._msg_content = self._message.content

    # TODO use task orrder/message dispatcher here
    def _update_and_publish(self, content):
    #    await self._message.edit(embed = content)
        self._msg_content = self._message.content

    async def delete(self):
        if self._message != None:
            await self._message.delete()
            self._message = None

    async def publish(self, content = None):
        if self._message == None:
            await self._create_and_publish(content)
        else: self._update_and_publish(content)