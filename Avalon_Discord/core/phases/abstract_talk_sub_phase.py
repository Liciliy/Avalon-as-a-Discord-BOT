from .abstract_sub_phase import AbsSubPhase, SubPhaseType

class ExecutionEndType:
    PREP_ENDED      = 11
    PLAYER_TALK_END = 12
    DISCUSSION_END  = 13
    NO_TALK_END     = 14
    # TODO Add merlin Hunt end type

class TalkSubPhaseHandledActions:
    TALK_PREPARATION_PHASE = 0
    ONE_PLAYER_TALK        = 1
    ALL_DISCUSSION_TALK    = 2
    NO_TALK                = 3
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

    @property
    def timer_content_handler(self):
        return self._game.timer_content_handler