import discord
import logging

from ..utils import form_embed

import core.panels.constants_game_panel_handler as const

from ..common import NotImplementedMethodUsage

from ..messages_dispatching.task import ContentType, Task, MsgActType

class PanelContent:
    text      = None
    reactions = None

    def __init__(self, text = None, reactions = None):
        """Creates object to be used for updating/creating game messages.

        Args:
            text (string, optional): message text. Defaults to None.
            reactions (list[string], optional): emoji to add. Defaults to None.
        """
        self.text = text
        self.reactions = reactions

class AbsGamePanelHandler:
    _game             = None
    _channel          = None
    _message          = None
    _list_of_messages = None
    _msg_content      = None
    _content_type     = None
    _content_handler  = None
    
    def __init__(self, game, channel, content_type):
        self._game         = game
        self._channel      = channel
        self._content_type = content_type
        self._list_of_messages = list()

    def set_content_handler(self, content_handler):
        self._content_handler = content_handler  

    def is_pnl_hndlr_msg(self, message_to_check_id):
        result = False

        if self._message != None and self.id == message_to_check_id:
            result = True
        elif self._list_of_messages != None:
            for msg in self._list_of_messages:
                if msg.id == message_to_check_id:
                    result = True
                    break

        return result
            
    async def publish(self, content = None):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: publish')

    # TODO this must not be async since the operation will be sent to other thread.
    def _update_and_publish(self, content = None):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: _update_and_publish')

    async def _create_and_publish(self, content = None): 
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: _create_and_publish')

    async def delete(self):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: delete')

    def _get_react_payload_info_as_string(self, payload):
        result = ''

        if   payload.event_type == const.REACTION_ADD:
            result += const.REACTION_ADD + '. '\
                       + 'Added by: '   + payload.member.name + '. '\
                       + 'Message ID: ' + str(payload.message_id) + '. '\
                       + 'User ID: '    + str(payload.user_id) + '. '\
                       + 'Channel ID: ' + str(payload.channel_id) + '. '\
                       + 'Guild ID: '   + str(payload.guild_id) + '. '\
                       + 'Emoji: '      + str(payload.emoji) + '. '  
            
        elif payload.event_type == const.REACTION_REM:
            result += const.REACTION_REM + '. '\
                       + 'Message ID: ' + str(payload.message_id) + '. '\
                       + 'User ID: '    + str(payload.user_id) + '. '\
                       + 'Channel ID: ' + str(payload.channel_id) + '. '\
                       + 'Guild ID: '   + str(payload.guild_id) + '. '\
                       + 'Emoji: '      + str(payload.emoji) + '. '

        return result
        
    # TODO make on_reaction not async: here and in children
    async def on_reaction(self, payload):
        str_to_log = 'Got un-handled reaction act: ' \
                   + self._get_react_payload_info_as_string(payload)        

        logging.error(str_to_log)

    def order_edit_task(self, 
                        new_content, 
                        message_id,
                        content_type = None):

        type_to_use = None
        if content_type == None:
            type_to_use = self._content_type
        else:
            type_to_use = content_type

        edit_task = Task(type = MsgActType.EDIT,
                         content = new_content,
                         content_type = type_to_use,
                         channel_id = self._channel.id,
                         message_id = message_id)

        self._game.order_task_to_msg_dispatcher(edit_task)

    def order_add_reaction(self,
                           reaction,
                           message_id):
        add_reactions_task = Task(type = MsgActType.ADD_REACT,
                                  content = reaction,
                                  content_type = ContentType.REACTIONS,
                                  channel_id = self._channel.id,
                                  message_id = message_id)

        self._game.order_task_to_msg_dispatcher(add_reactions_task)

    def order_del_reaction(self,
                           reaction,
                           message_id):

        del_reactions_task = Task(type = MsgActType.DEL_REACT,
                                  content = reaction,
                                  content_type = ContentType.REACTIONS,
                                  channel_id = self._channel.id,
                                  message_id = message_id,
                                  member_id = self._channel.user_id)

        self._game.order_task_to_msg_dispatcher(del_reactions_task)

    def order_del_own_reaction(self,
                               reaction,
                               message_id):

        del_own_react_task = Task(type = MsgActType.DEL_OWN_REACT,
                                  content = reaction,
                                  content_type = ContentType.REACTIONS,
                                  channel_id = self._channel.id,
                                  message_id = message_id)

        self._game.order_task_to_msg_dispatcher(del_own_react_task)

    def order_remove_all_reactions(self, msg_id):
        del_all_react_task = Task(type = MsgActType.DEL_ALL_REACT,
                                  content_type = ContentType.REACTIONS,     
                                  channel_id = self._channel.id,
                                  message_id = msg_id)

        self._game.order_task_to_msg_dispatcher(del_all_react_task)

    @property
    def id(self):
        result = None
        if self._message != None:
            result = self._message.id
        return result

    @property
    def channel_id(self):
        result = None
        if self._channel != None:
            result = self._channel.id
        return result