import logging

from ..common import NotImplementedMethodUsage

from ..game import AvaGame

from.phase_handler import PhaseHandler

class SubPhaseType:
    TALK = 0
    VOTE = 1

class VoteSubPhaseHandledActions:
    PLAYERS_SELECTION_VOTE = 0
    PARTY_APPROVAL_VOTE    = 1
    MISSION_RESULT_VOTE    = 2
    # TODO Add Merlin hunt phase(s) (if needed)

class ResDictKWords:
    ENDED_ACTION_TYPE = 'ended_action_type'
    SELECTION_CHANGED = 'selection_changed'
    PARTY_APPR_RES    = 'party_appr_vote_results'
    MISSION_RESULT    = 'mission_results'

class InterPhaseCrucialActions:
    PLAYERS_SPEACHES_ROUND_ENDED = 301
    VOTE_SUB_PHASES_CHAIN_ENDED  = 302
    MERLIN_HUNT_IS_STARTED       = 303

class AbsSubPhase:
    

    _sub_phase_type   = None
    _phase_handler : PhaseHandler    = None
    _sub_phase_action = None
    _game_instance    = None
    _party_leader     = None

    def __init__(self, 
                phase_handler  : PhaseHandler, 
                this_sub_phase_type, 
                sub_phase_action,
                game: AvaGame,
                party_leader):
        self._sub_phase_type   = this_sub_phase_type
        self._phase_handler    = phase_handler
        self._sub_phase_action = sub_phase_action
        self._game_instance    = game
        self._party_leader     = party_leader

    def _notify_phase_handler_about_this_phase_end(self):
        self._phase_handler.sub_phase_ended(self)

    def react_on_other_sub_phase_action(self, content : dict):
        """Check type of other sub phase handled action.
        If the action end requires any reactions from this phase - the response
        actions are executed.

        Raises:
            NotImplementedMethodUsage: [description]
        """
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage(\
            'Method name: react_on_other_sub_phase_action')

    def get_next_sub_phase(self):
        """Constructs a next-to-be-executed sub phase of this type and
        return result object.

        Raises:
            NotImplementedMethodUsage: [description]
        """
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage(\
            'Method name: get_next_sub_phase')

    def start(self):
        """Contact all needed content handlers and initiates their actions with
        certain information.

        Raises:
            NotImplementedMethodUsage: [description]
        """
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: start')

    def _stop(self):
        """Notifies parent Phase and (if needed) other sub phase about this 
        phase end.

        Raises:
            NotImplementedMethodUsage: [description]
        """
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: start')

    def react_or_content_handler_action(self, content): 
        """Should be used by content handlers to notify the phase about 
        the content handler action (most ofter - some action execution end).
        
        Args:
            content_dict (dict): dict of parameters. Most ofter only contains 
                                 ended action type.
        """       
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage(
          'Method name: react_or_content_handler_action')

    def get_talker_avatar_url(self):
        logging.warn('Unimplemented method get_talker_avatar_url usage!')

        return None
    
    def check_if_action_end_type_is_correct(self, 
                                            res_dict, 
                                            res_type_k_word,
                                            expected_res_type):

        result = True
        
        if not res_type_k_word in res_dict:
            result = False 
            logging.error(
              f'Result type key word "{res_type_k_word}"' + 
               ' not found in res dict!')

        elif res_dict[res_type_k_word] != expected_res_type:
            result = False 
            logging.error(
              f'Recieved result type "{str(res_dict[res_type_k_word])}"' + 
              f' desnt mach expected reult type "{str(expected_res_type)}" !')

        return result
    
    @property
    def type(self):
        return self._sub_phase_type

    @property
    def _game(self) -> AvaGame:
        return self._game_instance

    def get_next_party_leader(self):
        LIST_START_POS = 0
        pids = self._game.players_ids_list


        curr_leader_pos = pids.index(self._party_leader)

        next_leader_pos = curr_leader_pos + 1

        if next_leader_pos == len(pids):
            next_leader_pos = LIST_START_POS

        return pids[next_leader_pos]

    def get_round_starting_talker(self, party_leader_id):   
        LIST_START_POS = 0
        pids = self._game.players_ids_list

        curr_leader_pos = pids.index(party_leader_id)

        starting_talker_pos = curr_leader_pos + 1

        if starting_talker_pos == len(pids):
            starting_talker_pos = LIST_START_POS

        return pids[starting_talker_pos]
        