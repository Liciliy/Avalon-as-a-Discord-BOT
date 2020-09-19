import asyncio
import logging

from .abstract_vote_sub_phase import \
    AbsVoteSubPhase, \
    VoteSubPhaseHandledActions, \
    VoteExecutionEndType

from .abstract_sub_phase import ResDictKWords, InterPhaseCrucialActions

from ..content_handlers.vote_content_handler import VoteType, VoteOptions

from ..common import NotImplementedMethodUsage

from .phase_handler import PhaseHandler

class PartyApproveVoteSubPhase(AbsVoteSubPhase):

    VOTE_RESULT_K_WORD = ResDictKWords.PARTY_APPR_RES

    _selected_party_emojies = None
    _vote_result = None

    def __init__(self, 
                 phase_handler : PhaseHandler,
                 game,
                 party_leader,
                 selected_party_emojies):

        super().__init__(phase_handler, 
                         VoteSubPhaseHandledActions.PARTY_APPROVAL,
                         game,
                         None,
                         party_leader)

        self._selected_party_emojies = selected_party_emojies

        logging.info('Party apprroval sub phase created.')

    def get_next_sub_phase(self):
        logging.info('Going to next Vote Sub Phase.')

        result = None

        if self._vote_result == True:
            logging.info('The vote was successful.')
            from .vote_sub_phase_mission_result import MissionResultVoteSubPhase
            
            result =  MissionResultVoteSubPhase(
                self._phase_handler, 
                self._game,
                self._party_leader,
                self._selected_party_emojies)
        else:
            logging.info('The vote was failed...')
            self._phase_handler.game_info.register_failed_vote()
            self._phase_handler.message_other_sub_phase(                  
                  self._sub_phase_type, 
                  {InterPhaseCrucialActions.VOTE_SUB_PHASES_CHAIN_ENDED : None}
            )            

            self._game.update_game_table()

            from .vote_sub_phase_party_select import PartySelectVoteSubPhase

            result = PartySelectVoteSubPhase(                                  
                                 self._phase_handler, 
                                 self._game, 
                                 self.get_next_party_leader())

        return result

    def start(self):
        logging.info('Starting phase.')
        self._sub_phase_ended = False

        self.vote_content_handler.\
                set_coordinating_sub_phase_and_expected_end(
                    self, 
                    None,
                    PartyApproveVoteSubPhase.VOTE_RESULT_K_WORD)

        num_of_players_on_mission = \
            self._phase_handler.get_current_mission_players_num()  

        vpids_to_vote_opts = dict()

        for pid in self._game.players_ids_list:
            vpids_to_vote_opts[pid] = VoteOptions.YES_AND_NO

        self.vote_content_handler.initiate_vote(
            num_of_players_on_mission,
            vpids_to_vote_opts,
            VoteType.PARTY_APPROVING,
            party_players_emojies = self._selected_party_emojies)

    def _stop(self):
        logging.info('Stopping phase.')

        self._sub_phase_ended = True
        self._notify_phase_handler_about_this_phase_end()

    def react_or_content_handler_action(self, content_dict):
        logging.error('Received action content dict: ' + str(content_dict)) 

        if not self._sub_phase_ended:            
           
            if PartyApproveVoteSubPhase.VOTE_RESULT_K_WORD in content_dict:
                self._vote_result = \
                    content_dict[PartyApproveVoteSubPhase.VOTE_RESULT_K_WORD]

        
                self._stop()

            else:
                logging.error('Unexpected action key word received.')
        
        else:
            logging.error('Received content action for a stoped sub phase.')
