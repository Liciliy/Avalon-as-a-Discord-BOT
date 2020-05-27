import core.constants_game as const

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
    
    player_id_to_channel_id_dict = None
    roles_list                   = None
    player_id_to_role_dict       = None
    
    # INITIATED -> LOCKED -> STARTED -> PAUSED -> ENDED
    game_state                   = None

    # ID of the channel were game was initiated.
    # Should be used for joining the game.
    initial_text_channel_id      = None

    player_id_to_name_dict       = None
    
    def __init__(self, 
                 game_id, 
                 guild_id, 
                 game_master_id,
                 game_master_name, 
                 init_channel_id):
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

        self.private_txt_channels_list    = list()
        self.player_id_to_channel_id_dict = dict()
        self.roles_list                   = list()
        self.player_id_to_role_dict       = dict()
        

    def add_player(self, player_id, player_name):
        self.players_ids_list.append(player_id)
        self.player_id_to_name_dict[player_id] = player_name

    @property
    def num_of_players_str(self):
        return str(self.num_of_players)

    @property
    def num_of_players(self):
        return len(self.players_ids_list)
        
    @property
    def players_names_list(self):
        result = list()
        for id in self.player_id_to_name_dict:
            if id == self.game_master_id: continue
            result.append(self.player_id_to_name_dict[id])

        return result
