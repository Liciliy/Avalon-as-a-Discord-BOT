import logging

import languages.ukrainian_lang as lang

import core.panels.constants_game_panel_handler as const

from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType

from ..messages_dispatching.task import ContentType

from ..utils import form_embed


class SecretInfoPanelHandler(AbsGamePanelHandler):  
    VISIBILITY_REACTION = '👁️'

    _secret_info  = None
    _info_is_hidden = None
    
    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.TEXT)

    async def publish(self, content = None): 
        if self._message == None:
            await self._create_and_publish(content)
        else: self._update_and_publish(content)   

    async def _create_and_publish(self, content):
        self._message = await self._channel.send(embed = content)
        self._msg_content = content
        self.order_add_reaction(SecretInfoPanelHandler.VISIBILITY_REACTION,
                                self._message.id)
        
    def update_and_publish(self, content, initial_update = False): 
        if initial_update:
            self._secret_info    = content
            self._info_is_hidden = False

        if type(content) == str:
            self.order_edit_task(content, self._message.id, ContentType.TEXT)
        else:
            self.order_edit_task(content, self._message.id, ContentType.EMBED)
            
    async def delete(self):
        if self._message != None:
            await self._message.delete()
            self._message = None

    async def on_reaction(self, payload):
        str_to_log = 'Got reaction act: ' \
                   + self._get_react_payload_info_as_string(payload) 

        logging.info(str_to_log)

        self.order_del_reaction(payload.emoji, self.id)

        if   payload.event_type == const.REACTION_REM\
          or self._secret_info == None:
            return        

        # TODO bool variable self._info_is_hidden might not always be in sync 
        # with actual state of panel. Think about better solution.
        if self._info_is_hidden:
            self.update_and_publish(self._secret_info)
            self._info_is_hidden = False
        else:
            
            self.update_and_publish(
                form_embed(author = lang.PUCH_EYE_TO_SEE_INFO))
            self._info_is_hidden = True

