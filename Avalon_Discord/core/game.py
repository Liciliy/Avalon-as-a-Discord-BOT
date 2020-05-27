import core.constants_game as const

class Game:
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
    
    def __init__(self, game_id, guild_id, game_master_id, init_channel_id):
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
