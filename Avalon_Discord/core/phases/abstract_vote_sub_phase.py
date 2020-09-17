from .abstract_sub_phase import AbsSubPhase, SubPhaseType

class VoteExecutionEndType:
    PARTY_SELECTION_END = 211
    PARTY_APPROVAL_END  = 212
    MISSION_RESULT_END  = 213
    # TODO Add merlin Hunt end type

class VoteSubPhaseHandledActions:
    PARTY_SELECTION = 220
    PARTY_APPROVAL  = 221
    MISSION_RESULT  = 222
    # TODO Add Merlin hunt vote phase(s)


class AbsVoteSubPhase(AbsSubPhase):

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

        self._sub_phase_ended   = False

    @property
    def vote_content_handler(self):
        return self._game.vote_content_handler

    @property
    def selection_content_handler(self):
        return self._game.selection_content_handler

