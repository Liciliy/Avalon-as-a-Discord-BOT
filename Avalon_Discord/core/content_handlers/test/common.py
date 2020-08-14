class TestReactionPayload:
    emoji      = None
    channel_id = None
    event_type = None

    def __init__(self, em, chid, event_type = None):
        self.emoji = em
        self.channel_id = chid
        self.event_type = event_type

class TestGame:
    player_id_to_txt_ch_handler_dict = None
    player_id_to_emoji_dict          = None
    
    def __init__(self, pid_to_txt_ch_hd_dict, pid_to_emoji):
        self.player_id_to_txt_ch_handler_dict = pid_to_txt_ch_hd_dict
        self.player_id_to_emoji_dict          = pid_to_emoji


class TestChannelHandler:
    vote_panel      = None
    selection_panel = None
    id = None

    def __init__(self, id, vph = None, sph = None):
        self.vote_panel = vph
        self.selection_panel = sph

        self.id = id
