import asyncio
import logging

from .abstract_vote_sub_phase import \
    AbsVoteSubPhase, \
    VoteSubPhaseHandledActions, \
    VoteExecutionEndType

from .abstract_sub_phase import ResDictKWords, InterPhaseCrucialActions

from ..content_handlers.selection_content_handler import SelectionType
from ..content_handlers.vote_content_handler import VoteType, VoteOptions

from ..common import NotImplementedMethodUsage

from .phase_handler import PhaseHandler

class PartySelectVoteSubPhase(AbsVoteSubPhase):

    PARTY_SELECT_END_TYPE = VoteExecutionEndType.PARTY_SELECTION_END

    VOTE_END_K_WORD = ResDictKWords.ENDED_ACTION_TYPE

    _selected_party_emojies = None

    def __init__(self, 
                 phase_handler : PhaseHandler,
                 game,
                 party_leader):

        super().__init__(phase_handler, 
                         VoteSubPhaseHandledActions.PARTY_SELECTION,
                         game,
                         None,
                         party_leader)
        logging.info('Party selection sub phase created.')
        
    def react_on_other_sub_phase_action(self, content : dict):
        if InterPhaseCrucialActions.PLAYERS_SPEACHES_ROUND_ENDED \
              in \
           content:

            self.vote_content_handler.start_vote()

    def get_next_sub_phase(self):
        #from .talk_sub_phase_no_talks import NoTalkTalkSubPhase
#
        #logging.info(f'Retruning next phase - {NoTalkTalkSubPhase.__name__}.')
        #return NoTalkTalkSubPhase(self._phase_handler, 
        #                          self._game,
        #                          self._party_leader,
        #                          self._party_leader)
        pass

    def start(self):
        logging.info('Starting phase.')
        self._sub_phase_ended = False

        self.vote_content_handler.\
                set_coordinating_sub_phase_and_expected_end(
                    self, 
                    PartySelectVoteSubPhase.PARTY_SELECT_END_TYPE,
                    PartySelectVoteSubPhase.VOTE_END_K_WORD)

        self.selection_content_handler.\
                set_coordinating_sub_phase_and_expected_end(
                    self, 
                    None,
                    ResDictKWords.SELECTION_CHANGED)


        num_of_players_on_mission = \
            self._phase_handler.get_current_mission_players_num()        

        vpids_to_vote_opts = {self._party_leader : VoteOptions.ONLY_YES}

        selector_name = self._game.player_id_to_name_dict[self._party_leader]
        
        # Launching vote panels.
        self.selection_content_handler.initiate_selection(
            SelectionType.PARTY,
            self._party_leader,
            selector_name)

        self.vote_content_handler.initiate_vote(
            num_of_players_on_mission,
            vpids_to_vote_opts,
            VoteType.PARTY_FORMING)
        # Launch done.

    def _stop(self):
        logging.info('Stopping phase.')
        logging.info('Received selection: '
                     + str (self._selected_party_emojies))
        self._sub_phase_ended = True
        #self._notify_phase_handler_about_this_phase_end()

    def react_or_content_handler_action(self, content_dict): 

        if not self._sub_phase_ended \
              and\
           ResDictKWords.SELECTION_CHANGED in content_dict:
            self._selected_party_emojies = \
                content_dict[ResDictKWords.SELECTION_CHANGED]

            self.vote_content_handler.\
                update_vote_pannels(self._selected_party_emojies)

        else:
            res_type_is_correct =\
                 self.check_if_action_end_type_is_correct(
                     content_dict,
                     PartySelectVoteSubPhase.VOTE_END_K_WORD,
                     PartySelectVoteSubPhase.PARTY_SELECT_END_TYPE)

            if not res_type_is_correct:
                # TODO think if it is really needed to make any actions here.
                return
            
            if not self._sub_phase_ended:
                self._stop()