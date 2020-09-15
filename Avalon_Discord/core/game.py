import random
import logging
import asyncio
import discord.guild

import core.constants_game as const
import languages.ukrainian_lang as lang

from .utils import\
    form_embed,\
    EmbedField,\
    InfoToDisplay,\
    ErrorToDisplay

from .voice_channel_handler import\
    VoiceChannelHandler

from .text_channel_handler import\
    TextChannelHandler,\
    GameMasterTxtChHandler

from .content_handlers.game_chat_handler import\
    ChatHandler

from .content_handlers.timer_content_handler import\
    TimerContentHandler

from .content_handlers.vote_content_handler import\
    VoteContentHandler,\
    VoteOptions,\
    VoteType

from .content_handlers.selection_content_handler import\
    SelectionContentHandler,\
    SelectionType

from .content_handlers.secret_info_content_handler import\
    SecretInfoContentHandler

from .content_handlers.table_content_handler import\
    TableContentHandler

from .emoji_handler import\
    EmojiHandler

from .mechanics.mechanics import NumbersAndRolesHandler

from .sound_manager import SoundManager

class AvaGame:

    # ==== Fields with simple data ========================================== #

    # Unique per guild
    game_id                      = None    
    guild_id                     = None
    
    # discord_user ID
    game_master_id               = None
    
    # list of discord userds IDs
    players_ids_list = None
    
    player_id_to_txt_ch_handler_dict = None
    player_id_to_role_dict           = None
    player_id_to_name_dict           = None
    player_id_to_guild_member_dict   = None
    player_id_to_emoji_dict          = None
    
    # INITIATED -> LOCKED -> STARTED -> PAUSED -> ENDED
    game_state                   = None

    # ID of the channel were game was initiated.
    # Should be used for joining the game.
    initial_text_channel_id        = None
  
    # ======================================================================= #
   
    # ==== Fields with helping classes ====================================== #

    bot_client_link = None

    # Contains members of the guild taking part in the game.
    players_list = None

    _voice_handler = None
    _chat_handler  = None

    # Game contents handlers
    _timer_content_handler       = None
    _vote_content_handler        = None
    _selection_content_handler   = None
    _secret_info_content_handler = None
    _table_content_handler       = None  

    _phase = None

    _messages_dispatcher = None
    _numbers_and_roles_handler = None
    _phases_handler = None

    # ======================================================================= #

    
    def __init__(self, 
                 game_id, 
                 guild_id, 
                 game_master_id,
                 game_master_name, 
                 init_channel_id,
                 bot_client_link,
                 messages_dispatcher):
        """Creates game object

        Arguments:
            game_id int -- game unique ID (within guild)
            guild_id int -- ID of duild/server on which game was initiated
            game_master_id int -- game initiated player ID.
            init_channel_id int -- id of the channel where game was initiated
        """
        self.game_id                 = game_id
        self.guild_id                = guild_id
        self.game_master_id          = game_master_id
        self.initial_text_channel_id = init_channel_id

        self.game_state = const.GAME_INITIATED_STATE

        self.players_ids_list = [game_master_id]

        self.player_id_to_name_dict = {game_master_id : game_master_name}

        self.player_id_to_txt_ch_handler_dict = dict()
        self.player_id_to_role_dict           = dict()
        self.player_id_to_guild_member_dict   = dict()
        self.player_id_to_emoji_dict          = dict()

        self.bot_client_link = bot_client_link   

        self._voice_handler = VoiceChannelHandler(self)   
        self._chat_handler  = ChatHandler(self)        

        self._messages_dispatcher = messages_dispatcher

    def add_player(self, player_id, player_name):
        self.players_ids_list.append(player_id)
        self.player_id_to_name_dict[player_id] = player_name

    async def lock_game(self, msg):
        self.game_state = const.GAME_LOCKED_STATE

        self.__fill_players_list()

        game_guild = self.game_hosting_guild 

        for user in self.players_list:
            player_id = user.id
            
            # TODO check if a role with the same name exists.
            # If yes - create a role with some index

            # Role creation 
            role_name = self.player_id_to_name_dict[player_id] \
                      + const.ROLE_NAME_SUFFIX

            new_role = await game_guild.create_role(
                reason = const.ROLE_CREATION_REASON,
                name   = role_name,
                color = discord.Color.dark_blue())            
             
            self.player_id_to_role_dict[player_id] = new_role
           
            # Create palyer game txt channel handler
            if player_id == self.game_master_id:
                self.player_id_to_txt_ch_handler_dict[player_id] =\
                    GameMasterTxtChHandler(self, user, new_role)
            else:
                self.player_id_to_txt_ch_handler_dict[player_id] =\
                    TextChannelHandler(self, user, new_role)

        # Creating voice channel. Invite to channel will be send to each player
        # upon connection to ones private game text channel (created later).
        await self._voice_handler.create_channel_with_invite()

        # Inviting players to their game txt channels. Appropriate roles 
        # will be assigned upon player guild join.
        for txt_ch_handler in self.player_id_to_txt_ch_handler_dict.values():
            await txt_ch_handler.create_channel_and_invite_player()
        
        # === Secret Info ===
        self._secret_info_content_handler = \
            SecretInfoContentHandler(
                self,
                self.player_id_to_txt_ch_handler_dict.values(),
                self.player_id_to_txt_ch_handler_dict[self.game_master_id].id)
        await self._secret_info_content_handler.initial_render()
        # =================  

        await self._publish_chat()

        # TODO timer test code below. Remove later:

        # self._timer_content_handler =\
        #     TimerContentHandler(
        #         self, 
        #         self.player_id_to_txt_ch_handler_dict.values(),
        #         self.player_id_to_txt_ch_handler_dict[self.game_master_id].id)
        # await self._timer_content_handler.initial_render()
 
        # master_ch_id = self.player_id_to_txt_ch_handler_dict[self.game_master_id].id
        # 
        # talker_id = None
        # for ch in self.player_id_to_txt_ch_handler_dict.values():
        #     if ch.id != master_ch_id:
        #         talker_id = ch.id
        #         break
 
        # await self._timer_content_handler.start_timer(0, 60, 'Алісія вікандер', talker_id)
  
        # ================ End test code ================ 
              
    async def start_game(self, msg):  
      
        self.game_state = const.GAME_STARTED_STATE 
        
        await msg.delete() 
        
        random.shuffle(self.players_ids_list)

        self.player_id_to_emoji_dict = \
            await EmojiHandler.create_emojies_for_game(self)  

        for _, txt_ch in self.player_id_to_txt_ch_handler_dict.items():
            await txt_ch.clear_pre_game_messages()

      # === Setup sound handling ========================================== #
        await self._voice_handler.connect_bot_to_voice_channel()
        SoundManager.setup_sound_manager(self._voice_handler)
      # =================================================================== #

      # === Setting up game roles ========================================= #
        self._numbers_and_roles_handler = NumbersAndRolesHandler(self)
        self.player_id_to_role_dict =\
            self._numbers_and_roles_handler.player_ids_to_roles
       
        self._secret_info_content_handler.update_with_info()
      # =================================================================== #

      # === Setting up timer content handler and render timer pannels. ==== #  
        self._timer_content_handler =\
            TimerContentHandler(
                self, 
                self.player_id_to_txt_ch_handler_dict.values(),
                self.player_id_to_txt_ch_handler_dict[self.game_master_id].id)
        await self._timer_content_handler.initial_render()
      # =================================================================== #

      # TODO test code below. Remove later:

       # === Selection panel ===
        self._selection_content_handler =\
            SelectionContentHandler(
                self,
                self.player_id_to_txt_ch_handler_dict.values(),
                self.player_id_to_txt_ch_handler_dict[self.game_master_id].id)
        await self._selection_content_handler.initial_render() 

        name = self.player_id_to_name_dict[self.players_ids_list[0]]

        self._selection_content_handler.initiate_selection(
                          SelectionType.PARTY, 
                          self.players_ids_list[0], 
                          name)
       # =================

       # === Vote panel ===
        self._vote_content_handler =\
            VoteContentHandler(
                self, 
                self.player_id_to_txt_ch_handler_dict.values(),
                self.player_id_to_txt_ch_handler_dict[self.game_master_id].id)
        await self._vote_content_handler.initial_render() 
       # =================

       # === Vote and selection setup panel ===
        vpids_to_vote_opts = dict()
        vpids_to_vote_opts[self.players_ids_list[0]] = VoteOptions.ONLY_YES


        party_emojies = list()
        for _, em in self.player_id_to_emoji_dict.items():
            party_emojies.append(str(em))
           

        self._vote_content_handler.initiate_vote(
                          2, 
                          vpids_to_vote_opts, 
                          VoteType.PARTY_FORMING)
        self._vote_content_handler.start_vote()
       # ================= 

       # === Temporary table panel ===
        self._table_content_handler =\
            TableContentHandler(
                self, 
                self.player_id_to_txt_ch_handler_dict.values(),
                self.player_id_to_txt_ch_handler_dict[self.game_master_id].id)
        await self._table_content_handler.initial_render()
       # =================                     
      # ================ End test code ================
        
      # === Setting up and starting game phases handler =================== #
        from .phases.phase_handler import PhaseHandler
        
        self._phases_handler = PhaseHandler.initiate_and_get_phase_handler(self)

        self._phases_handler.start_phases()
      # =================================================================== #

    # TODO check if below func is needed 
    def timer_expired(self):
        pass

    # TODO check if below func is needed 
    def vote_is_done(self, content):
        pass

    # TODO check if below func is needed 
    def selection_happen(self, content):
        self._vote_content_handler.update_vote_pannels(content)

    async def display_error_msg(self, msg, error_to_display):
        player_chanel = self.player_id_to_txt_ch_handler_dict[msg.author.id]
        await player_chanel.display_error_msg(error_to_display)
        await msg.delete()

    def __fill_players_list(self):
        """
        Using previously stored players IDs fetches corresponding 
        user discord objects and save them to game list.
        """
        self.players_list = list() 
        for player_id in self.players_ids_list:
            self.players_list.append(self.bot_client_link.get_user(player_id))

    async def __notify_game_master_about_join_status(self):
        if self.game_master_id in self.player_id_to_guild_member_dict:            
            master_channel_hdler =\
                self.player_id_to_txt_ch_handler_dict[self.game_master_id]

            logging.info('Game master in guild.')

            await master_channel_hdler.refresh_connection_data()

    async def check_if_joined_member_is_game_player(self, member):
        """Checks if waited player had joined to the game.
        If yes - 
         1) gives the player permissions to read ones game text 
            channel.
         2) send an invite to voice channel
        
        Arguments:
            member {[type]} -- [description]

        Returns:
            bool -- True if ember has joined to a guild which hosts
            game where member is a player.
            False otherwise.          
        """
        result = False

        logging.debug('New member guild id ' + str (member.guild.id) )
        logging.debug('Game guild id ' + str (self.game_hosting_guild.id) )

        if self.game_state    == const.GAME_LOCKED_STATE\
          and member.guild.id == self.game_hosting_guild.id\
          and member.id       in self.players_ids_list:
            result = True
            logging.debug('Giving role to user ' + str(member))
            
            self.player_id_to_guild_member_dict[member.id] = member

            member_channel = self.player_id_to_txt_ch_handler_dict[member.id]
            
            # Assigning role to the player
            await member.add_roles(self.player_id_to_role_dict[member.id])

            await member_channel.send_pregame_msg(lang.GAME_MSG_WAITING_ALL)

            await member_channel.send_pregame_msg(
                self._voice_handler.get_voice_ch_invite)

            await self.__notify_game_master_about_join_status()

        return result              

    async def check_if_player_joined_locked_game_voice(self, member, voice_ch):
        
        result = False

        if self.game_state    == const.GAME_LOCKED_STATE\
          and member.guild.id == self.game_hosting_guild.id\
          and voice_ch.id     == self._voice_handler.voice_ch_id:
          
            result = True            
            await self.__notify_game_master_about_join_status()

        return result              

    async def _publish_chat(self):
        for ch_hdlr in self.player_id_to_txt_ch_handler_dict.values():
            name = ch_hdlr.user_mention
            await ch_hdlr.update_chat(self._chat_handler.get_chat_str(name))

    async def handle_player_chat_message(self, msg):
        # TODO filter out style changing characters (at least  those,
        # thase that are used for highlighting nick in chat).
        
        # TODO Filter out images, auto embedded messages (links?) and other
        # stuff that can break chat.
        # Maybe do this on lower layers 

        await self._chat_handler.handle_new_player_message(msg)

        await self._publish_chat()

    async def handle_player_reaction(self, player_id, payload):
        await self.player_id_to_txt_ch_handler_dict[player_id].\
            react_on_reaction(payload)

    def order_task_to_msg_dispatcher(self, task):
        self._messages_dispatcher.order_task_to_execute(task)

    @property
    def game_hosting_guild(self):
        return self.bot_client_link.get_guild(715959072532201492)

    @property
    def game_hosting_guild_id(self):
        return self.game_hosting_guild.id

    @property
    def num_of_players_str(self):
        return str(self.num_of_players)

    @property
    def num_of_players(self):
        return len(self.players_ids_list)
        
    @property
    def non_master_players_names(self):
        result = list()
        for id in self.player_id_to_name_dict:
            if id == self.game_master_id: continue
            result.append(self.player_id_to_name_dict[id])

        return result

    @property
    def game_master_name(self):
        return self.player_id_to_name_dict[self.game_master_id]

    @property
    def txt_channels_handlers(self):
        return self.player_id_to_txt_ch_handler_dict.values()

    @property 
    def get_players_not_in_voice(self):
        """Used to understand who did not join game voice chat.

        Returns:
            list[String]: list of user names who has not joined the game voice 
                          chat.  
        """
        return self._voice_handler.get_players_not_in_voice()

    @property
    def get_players_not_in_guild(self):
        """Used to understand who did not join guild yet.

        Returns:
            list[String]: list of user names who has not joined the game guild.  
        """
        result = list()
        
        for player in self.players_list:
            if player.id not in self.player_id_to_guild_member_dict:
                result.append(player.name)
        
        return result
    
    @property
    def number_of_players(self):
        return len(self.players_ids_list) 

    @property
    def timer_content_handler(self):
        return self._timer_content_handler

    @property
    def vote_content_handler(self):
        return self._vote_content_handler 

    @property
    def selection_content_handler(self):
        return self._selection_content_handler

    @property
    def secret_info_content_handler(self):
        return self._secret_info_content_handler

    @property
    def table_content_handler(self):
        return self._table_content_handler