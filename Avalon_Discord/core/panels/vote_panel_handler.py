import logging

from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType,\
    PanelContent

class MessageType:
    TEXT_MSG  = 0
    EMOJI_MSG = 1

class VotePanelHandler(AbsGamePanelHandler):

    HEADER_KEY    = 'header'
    EMOJIES_KEY   = 'emojies'
    REACTIONS_KEY = 'reactions'

    _header_message  = None
    _emoji_message   = None

    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.TEXT)
        
    async def _create_and_publish(self, content):
        self._header_message = await self._channel.send(
            content = content[MessageType.TEXT_MSG])
        
        self._emoji_message = await self._channel.send(
            content = content[MessageType.EMOJI_MSG].text)

        self._list_of_messages = [self._header_message, self._emoji_message]
        
        self._msg_content = content

    # Below is this-class-unique and public version of update and publish.
    def update_and_publish(self, content):   
        prev_header = self._msg_content[MessageType.TEXT_MSG]
        prev_emoji  = self._msg_content[MessageType.EMOJI_MSG].text

        if    content[MessageType.TEXT_MSG] != None \
          and content[MessageType.TEXT_MSG] != prev_header:
            self.order_edit_task(content[MessageType.TEXT_MSG], 
                                 self._header_message.id)
        
        else:
            content[MessageType.TEXT_MSG] = prev_header

        emoji_content = content[MessageType.EMOJI_MSG]
        if emoji_content != None:
            if emoji_content.text != None and emoji_content.text != prev_emoji:
                self.order_edit_task(emoji_content.text, self._emoji_message.id)
            else:
                content[MessageType.EMOJI_MSG].text = prev_emoji
            
            if emoji_content.reactions != None:
                for reaction in emoji_content.reactions:
                    self.order_add_reaction(reaction, self._emoji_message.id)
         
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

    async def on_reaction(self, payload):
        str_to_log = 'Got reaction act: ' \
                   + self._get_react_payload_info_as_string(payload) 

        logging.info(str_to_log)
        self.order_remove_all_reactions(self._emoji_message.id)
        await self._content_handler.handle_reaction(payload)

    def clear_reactions(self):
        logging.info('Clearing reactions')
        self.order_remove_all_reactions(self._emoji_message.id)