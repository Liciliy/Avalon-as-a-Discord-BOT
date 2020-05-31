import logging
import asyncio
import discord.guild


import core.constants_game as const
import languages.ukrainian_lang as lang

class AvaGame:
    # Unique per guild
    game_id                      = None    
    guild_id                     = None
    
    # discord_user ID
    game_master_id               = None
    
    # list of discord userds IDs
    players_ids_list             = None
    
    # list of channels IDs
    private_txt_channels_list    = None
    
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

    game_voice_ch = None
    
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

        self.private_txt_channels_list      = list()
        self.player_id_to_channel_dict      = dict()
        self.roles_list                     = list()
        self.player_id_to_role_dict         = dict()
        self.player_id_to_guild_member_dict = dict()

        self.bot_client_link = bot_client_link        

    def add_player(self, player_id, player_name):
        self.players_ids_list.append(player_id)
        self.player_id_to_name_dict[player_id] = player_name

    async def lock_game(self, msg):
        self.__fill_players_list()

        game_guild = self.__game_hosting_guild
        self.lobby_channel = await game_guild.create_text_channel(
                msg.author.name + '\'s Avalon waiting room')

        await self.lobby_channel.send(lang.GAME_MSG_WAITING_ALL)

        waiting_room_invite = \
            await self.lobby_channel.create_invite()

        for user in self.players_list:
            dmc = None

            if user.dm_channel == None:
                await user.create_dm()

            dmc = user.dm_channel

            logging.debug('Sending lobby text invite to: ' + user.name)
            await dmc.send(waiting_room_invite)

        self.game_state = const.GAME_LOCKED_STATE

    async def start_game(self, msg):
        
        game_guild = self.__game_hosting_guild

        self.game_state = const.GAME_STARTED_STATE

        for player_id in self.players_ids_list:
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
            
            # Assigning role to the player
            member = game_guild.get_member(player_id)
            self.player_id_to_guild_member_dict[player_id] = member            
            await member.add_roles(new_role)  

            # Creating a channel accessible only to the role
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
        
        await self.lobby_channel.delete()     

        await asyncio.sleep(1)  

        overwrites = dict()
        for role in self.player_id_to_role_dict.values():
            overwrites[role] = discord.PermissionOverwrite(
                                            connect              = True, 
                                            speak                = True,
                                            use_voice_activation = True)
                                                           
        logging.debug('Game master name: ' + str(self.game_master_name))

        self.game_voice_ch = \
            await game_guild.create_voice_channel(
                name       = self.game_master_name + ' game voice', 
                overwrites = overwrites)

        voice_ch_invite = \
            await self.game_voice_ch.create_invite()

        for ch in self.player_id_to_channel_dict.values():
            await ch.send(lang.GAME_MSG_STARTING)           
            await ch.send(voice_ch_invite)

    def all_players_connected(self):
        game_guild = self.__game_hosting_guild

        result = True
        
        for player in self.players_list:
            if player not in game_guild.members:
                result = False
                break

        return result
 
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

    def __fill_players_list(self):
        self.players_list = list() 
        for player_id in self.players_ids_list:
            self.players_list.append(self.bot_client_link.get_user(player_id))

    @property
    def __game_hosting_guild(self):
        return self.bot_client_link.get_guild(715959072532201492)