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

from .emoji_handler import\
    EmojiHandler

class AvaGame:
    # Unique per guild
    game_id                      = None    
    guild_id                     = None
    
    # discord_user ID
    game_master_id               = None
    
    # list of discord userds IDs
    players_ids_list             = None
    
    player_id_to_txt_ch_handler_dict = None
    player_id_to_role_dict           = None
    
    # INITIATED -> LOCKED -> STARTED -> PAUSED -> ENDED
    game_state                   = None

    # ID of the channel were game was initiated.
    # Should be used for joining the game.
    initial_text_channel_id        = None

    player_id_to_name_dict         = None

    player_id_to_guild_member_dict = None

    player_id_to_emoji_dict   = None

    bot_client_link = None

    # Contains members of the guild taking part in the game.
    players_list = None

    _voice_handler = None
    _chat_handler  = None

    _phase = None

    _messages_dispatcher = None
    
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
        
        await self._publish_chat()
              
    async def start_game(self, msg):    

        self.player_id_to_emoji_dict = \
            await EmojiHandler.create_emojies_for_game(self) 
      
        self.game_state = const.GAME_STARTED_STATE 

        for ch in self.player_id_to_txt_ch_handler_dict.values():
            await ch.send(lang.GAME_MSG_STARTING)    

        await msg.delete()      
     
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

            await member_channel.send(lang.GAME_MSG_WAITING_ALL)

            await member_channel.send(self._voice_handler.get_voice_ch_invite)

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

    async def handle_player_add_reaction(self, player_id, payload):
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