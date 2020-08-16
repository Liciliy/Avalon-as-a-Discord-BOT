import logging
import discord

import languages.ukrainian_lang as lang

from .utils import \
    form_embed,\
    EmbedField,\
    ErrorToDisplay,\
    InfoToDisplay

from .panels.chat_panel_handler import\
    ChatPanelHandler

from .panels.error_pannel_handler import\
    ErrorPanelHandler

from .panels.timer_panel_handler import\
    TimerPanelHandler

from .panels.vote_panel_handler import\
    VotePanelHandler

from .panels.conn_st_panel_handler import\
    ConnectionStatusPanelHandler

from .panels.selection_panel_handler import\
    SelectionPanelHandler

from .panels.secret_info_panel_handler import\
    SecretInfoPanelHandler

from .messages_dispatching.task import Task, ContentType, MsgActType

class TextChannelHandler:
    _game         = None
    _text_channel = None
    _user         = None
    _invite       = None
    _user_role    = None

    _error_pnl_handler = None
    _chat_pnl_handler  = None
    _timer_pnl_handler = None
    _vote_pnl_handler  = None
    _selection_pnl_handler = None
    _secret_info_pnl_handler = None
    
    _pre_game_messages = None      
   

    _panels_handlers_list = None
    def __init__(self, game, user, role):
        """[summary]

        Arguments:
            game {game}            -- the game instance to be played.
            user {discord.user}    -- the channel game user (player)
            role {discord.role}    -- role of the user on the server.
        """
        self._game         = game
        self._user         = user
        self._user_role    = role

        self._pre_game_messages = list()

    async def send_pregame_msg(self, content):
        self._pre_game_messages.append(
            await self.send(content)
        )
        
    async def clear_pre_game_messages(self):
        for msg in self._pre_game_messages:
            await msg.delete()
        
        self._pre_game_messages.clear()

    async def create_channel_and_invite_player(self):
        game_guild = self._game.game_hosting_guild
        
        # Creating a private text channel accessible only to the role
        overwrites = {
            game_guild.default_role : 
                discord.PermissionOverwrite(read_messages         = False, 
                                            send_messages         = False,
                                            embed_links           = False,
                                            attach_files          = False,
                                            mention_everyone      = False,
                                            view_guild_insights   = False,
                                            send_tts_messages     = False,
                                            add_reactions         = False,
                                            create_instant_invite = False),
            self._user_role : 
                discord.PermissionOverwrite(read_messages = True, 
                                            send_messages = True),
            game_guild.me : 
                discord.PermissionOverwrite(read_messages   = True, 
                                            send_messages   = True,
                                            manage_messages = True)
        }

        self._text_channel = await game_guild.create_text_channel(
                'Avalon: ' + self._user.name, 
                overwrites=overwrites)

        self._error_pnl_handler =\
             ErrorPanelHandler(self._game, self)
        self._chat_pnl_handler  =\
             ChatPanelHandler(self._game, self)
        self._timer_pnl_handler =\
             TimerPanelHandler(self._game, self)
        self._vote_pnl_handler =\
            VotePanelHandler(self._game, self)
        self._selection_pnl_handler =\
            SelectionPanelHandler(self._game, self)
        self._secret_info_pnl_handler =\
            SecretInfoPanelHandler(self._game, self)
       
        # TODO reorder pannels as they should be visioble to players.
        self._panels_handlers_list = [self._error_pnl_handler, 
                                      self._chat_pnl_handler,
                                      self._timer_pnl_handler,
                                      self._vote_pnl_handler,
                                      self._selection_pnl_handler,
                                      self._secret_info_pnl_handler]

        await self.invite_player()

    async def send(self, 
                   content          = None, 
                   *, 
                   tts              = False, 
                   embed            = None, 
                   file             = None, 
                   files            = None, 
                   delete_after     = None, 
                   nonce            = None):
        return await self._text_channel.send(
            content          = content          , 
            tts              = tts              , 
            embed            = embed            , 
            file             = file             , 
            files            = files            , 
            delete_after     = delete_after     , 
            nonce            = nonce            )

    async def invite_player(self):
        # Sending the channel invite to player who will use it to play.
        
        self._invite = \
            await self._text_channel.create_invite()

        dmc = None

        if self._user.dm_channel == None:
            await self._user.create_dm()

        dmc = self._user.dm_channel

        logging.debug('Sending game txt channel invite to: ' + self._user.name)

        self._game.order_task_to_msg_dispatcher(
            Task(
                type         = MsgActType.SEND,
                content_type = ContentType.TEXT,
                content      = self._invite,
                channel_id   = dmc.id))
        #await dmc.send(self._invite)
    
    async def display_error_msg(self, error_content):
        await self._error_pnl_handler.publish(error_content)

    async def update_chat(self, new_chat_str):
        await self._chat_pnl_handler.publish(new_chat_str)

    async def react_on_reaction(self, payload):
        for pannel_handler in self._panels_handlers_list:

            if pannel_handler != None \
              and pannel_handler.is_pnl_hndlr_msg(payload.message_id):

                await pannel_handler.on_reaction(payload)
                break

    def history(self, limit):
        return self._text_channel.history(limit = limit)
    
    @property
    def id(self):
        return self._text_channel.id

    @property
    def user_name(self):
        return self._user.name

    @property
    def user_id(self):
        return self._user.id

    @property
    def user_mention(self):
        return self._user.mention

    @property
    def timer_panel(self):
        return self._timer_pnl_handler

    @property
    def vote_panel(self):
        return self._vote_pnl_handler

    @property
    def selection_panel(self):
        return self._selection_pnl_handler

    @property
    def secret_info_panel(self):
        return self._secret_info_pnl_handler

class GameMasterTxtChHandler(TextChannelHandler):
    _connection_info_pnl_handler = None

    def __init__(self,  game, user, role):
        super().__init__( game, user, role)

    async def create_channel_and_invite_player(self):
        await super().create_channel_and_invite_player()
        self._connection_info_pnl_handler  =\
            ConnectionStatusPanelHandler(self._game, self._text_channel)

    async def refresh_connection_data(self):

        embed_fields = list()

        not_in_guild_list = self._game.get_players_not_in_guild

        not_in_voice_list = self._game.get_players_not_in_voice

        not_in_voice_list.extend(not_in_guild_list)
        
        if len(not_in_guild_list) > 0:  
            embed_fields.append(EmbedField(lang.INFO_MSG_NOT_IN_GUILD_FIELD_NAME,
                                           '\n'.join(not_in_guild_list) + '\n',
                                           True))

        if len(not_in_voice_list) > 0:      
            embed_fields.append(EmbedField(lang.INFO_MSG_NOT_IN_VOICE_FIELD_NAME,
                                           '\n'.join(not_in_voice_list) + '\n',
                                           True))
        if len(embed_fields) > 0:                 
            await self._connection_info_pnl_handler.publish(
                form_embed(colour = discord.Colour.green(),
                           descr  = lang.INFO_MSG_CONNECTNESS_STATUS_TEXT,
                           title  = lang.INFO_MSG_CONNECTNESS_STATUS_TITLE,
                           fields = embed_fields))

        else: await self._connection_info_pnl_handler.delete()