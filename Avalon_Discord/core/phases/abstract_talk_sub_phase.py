from .abstract_sub_phase import AbsSubPhase, SubPhaseType

class ExecutionEndType:
    PREP_ENDED      = 111
    PLAYER_TALK_END = 112
    DISCUSSION_END  = 113
    NO_TALK_END     = 114
    # TODO Add merlin Hunt end type

class TalkSubPhaseHandledActions:
    TALK_PREPARATION_PHASE = 120
    ONE_PLAYER_TALK        = 121
    ALL_DISCUSSION_TALK    = 122
    NO_TALK                = 123
    # TODO Add Merlin hunt talk phase(s)


class AbsTalkSubPhase(AbsSubPhase):

    _talking_player_id = None
    _sub_phase_ended   = None

    def __init__(self, 
                 parent_phase,  
                 sub_phase_action,
                 game,
                 talking_player_id,
                 party_leader):

        super().__init__(parent_phase,                          
                         SubPhaseType.TALK, 
                         sub_phase_action,
                         game,
                         party_leader)

        self._talking_player_id = talking_player_id
        self._sub_phase_ended   = False

    def _implemented_get_avatar(self):
        AVATAR_SIZE_TO_USE = 64 # NOTE MUST BE POWER OF TWO
        guild_member = \
            self._game.player_id_to_guild_member_dict[self._talking_player_id]

        return guild_member.avatar_url_as(size = AVATAR_SIZE_TO_USE)   

    @property
    def timer_content_handler(self):
        return self._game.timer_content_handler