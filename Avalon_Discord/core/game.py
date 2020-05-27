GAME_INITIATED_

class Game:
    # Uniqe per guild
    game_id                      = None    
    guild_id                     = None
    players_ids_list             = None
    private_txt_channels_list    = None
    player_id_to_channel_id_dict = None
    roles_list                   = None
    player_id_to_role_dict       = None
    game_state                   = None