import logging
import asyncio
import discord.guild


import core.constants_game as const
import languages.ukrainian_lang as lang

from core.utils import form_embed,\
    EmbedField,\
    InfoToDisplay

from core.game_voice_handler import\
    VoiceHandler

class AvaGame:
    # Unique per guild
    game_id                      = None    
    guild_id                     = None
    
    # discord_user ID
    game_master_id               = None
    
    # list of discord userds IDs
    players_ids_list             = None
    
    player_id_to_channel_dict    = None
    roles_list                   = None
    player_id_to_role_dict       = None
    
    # INITIATED -> LOCKED -> STARTED -> PAUSED -> ENDED
    game_state                   = None

    # ID of the channel were game was initiated.
    # Should be used for joining the game.
    initial_text_channel_id      = None

    player_id_to_name_dict       = None

    player_id_to_guild_member_dict = None

    bot_client_link = None

    lobby_channel = None
    
    # Contains members of the guild taking part in the game.
    players_list = None

    __voice_handler = None
    
    def __init__(self, 
                 game_id, 
                 guild_id, 
                 game_master_id,
                 game_master_name, 
                 init_channel_id,
                 bot_client_link):
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

        self.player_id_to_channel_dict      = dict()
        self.roles_list                     = list()
        self.player_id_to_role_dict         = dict()
        self.player_id_to_guild_member_dict = dict()

        self.bot_client_link = bot_client_link   

        self.__voice_handler = VoiceHandler(self)     

    def add_player(self, player_id, player_name):
        self.players_ids_list.append(player_id)
        self.player_id_to_name_dict[player_id] = player_name

    async def lock_game(self, msg):
        self.game_state = const.GAME_LOCKED_STATE

        self.__fill_players_list()

        game_guild = self.game_hosting_guild       

        # Creating voice channel. Invite to channel will b send to each player
        # upon connection to ones private game channel (created later).
        await self.__voice_handler.create_channel_and_invite()

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

            # Creating a private text channel accessible only to the role
            overwrites = {
                game_guild.default_role : 
                    discord.PermissionOverwrite(read_messages = False, 
                                                send_messages = False),
                new_role : 
                    discord.PermissionOverwrite(read_messages = True, 
                                                send_messages = True),
                game_guild.me : 
                    discord.PermissionOverwrite(read_messages   = True, 
                                                send_messages   = True,
                                                manage_messages = True)
            }
            
            channel = await game_guild.create_text_channel(
                'Avalon: ' + self.player_id_to_name_dict[player_id], 
                overwrites=overwrites)
            self.player_id_to_channel_dict[player_id] = channel 
            
            # Sending the channel invite to player who will use it to play.
            invite = \
                await channel.create_invite()

            dmc = None

            if user.dm_channel == None:
                await user.create_dm()

            dmc = user.dm_channel

            logging.debug('Sending game txt channel invite to: ' + user.name)
            await dmc.send(invite)
              
    async def start_game(self, msg):
        """Does:
        1) Changes game state
        2) Creates voice channel
        3) Gives all players server roles access to the channel
        4) Sends the channel invite to the players.

        Arguments:
            msg {[type]} -- [description]
        """
        self.game_state = const.GAME_STARTED_STATE 

        for ch in self.player_id_to_channel_dict.values():
            await ch.send(lang.GAME_MSG_STARTING)           
            

    def all_players_connected(self):
        game_guild = self.game_hosting_guild

        result = True
        
        for player in self.players_list:
            if player not in game_guild.members:
                result = False
                break

        return result
 
    def __fill_players_list(self):
        """
        Using previously stored players IDs fetches corresponding 
        user discord objects and save them to game list.
        """
        self.players_list = list() 
        for player_id in self.players_ids_list:
            self.players_list.append(self.bot_client_link.get_user(player_id))

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

        if self.game_state == const.GAME_LOCKED_STATE\
          and member.guild.id == self.game_hosting_guild.id\
          and member.id in self.players_ids_list:
            result = True
            logging.debug('Giving role to user ' + str(member))
            # Assigning role to the player                
            self.player_id_to_guild_member_dict[member.id] = member            
            await member.add_roles(self.player_id_to_role_dict[member.id])
            await self.player_id_to_channel_dict[member.id].\
                        send(lang.GAME_MSG_WAITING_ALL)
            await self.player_id_to_channel_dict[member.id].\
                send(self.__voice_handler.get_voice_ch_invite)
        return result              

    @property
    def game_hosting_guild(self):
        return self.bot_client_link.get_guild(715959072532201492)

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