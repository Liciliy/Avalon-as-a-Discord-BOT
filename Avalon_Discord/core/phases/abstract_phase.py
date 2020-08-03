import logging

from ..common import NotImplementedMethodUsage

class MissionType:
    JOURNEY     = 0
    MERLIN_HUNT = 1

class PhaseType:
    TALK_PREPARATION = 0
    TALK             = 1
    PLAYER_SELECTION = 2
    VOTE             = 3

class VoteType:
    PARTY_APPROVAL  = 0
    MISSION_SUCCESS = 1

class PlayerReactionType:
    TIMER_REACTION   = 0
    VOTE_REACTION    = 1
    PLAYER_SELECTION = 2

class TalkType:
    ONE_PLAYER_SPEACH = 0
    ALL_TALK          = 1
    RED_PLAYERS_TALK  = 2
    SERIOUS_TALK      = ALL_TALK


class AbstractPhase:
    _mission_type          = None
    _phase_type            = None
    _mission_leader_player = None
    _phase_is_active       = None
    _game                  = None
    
    def __init__(self,
                 mission_type,
                 leader,
                 game):

        self._mission_type          = mission_type
        self._mission_leader_player = leader
        self._phase_is_active       = True
        self._game                  = game        
        
    def start(self):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: start')

    def _notify_game_about_phase_end(self):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage(
                'Method name: _notify_game_about_phase_end')

    def get_next_phase(self):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: get_next_phase')

    def get_selected_players(self):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: get_selected_players')

    def end_phase(self):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: end_phase')

