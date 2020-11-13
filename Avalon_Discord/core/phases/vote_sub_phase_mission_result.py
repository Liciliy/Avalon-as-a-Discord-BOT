import logging

from .abstract_vote_sub_phase import \
    AbsVoteSubPhase, \
    VoteSubPhaseHandledActions

from .abstract_sub_phase import ResDictKWords, InterPhaseCrucialActions

from ..content_handlers.vote_content_handler import VoteType, VoteOptions

from .phase_handler import PhaseHandler

class MissionResultVoteSubPhase(AbsVoteSubPhase):

    MISSION_RESULT_K_WORD = ResDictKWords.MISSION_RESULT

    _selected_party_emojies = None
    _mission_result = None

    def __init__(self, 
                 phase_handler : PhaseHandler,
                 game,
                 party_leader,
                 selected_party_emojies):

        super().__init__(phase_handler, 
                         VoteSubPhaseHandledActions.MISSION_RESULT,
                         game,
                         None,
                         party_leader)

        self._selected_party_emojies = selected_party_emojies

        logging.info('Mission result sub phase created.')

    def get_next_sub_phase(self):
        result = None    

        logging.info('In function get_next_sub_phase')    

        mi_res = self._mission_result

        if   mi_res == True :
            logging.info('Registering successful mission.')
            self._phase_handler.game_info.register_succeeded_mission()
        elif mi_res == False:
            logging.info('Registering failed mission.')
            self._phase_handler.game_info.register_failed_mission()

        else:
            logging.error(
                f'Unxepected mission result value received {str(mi_res)}')

        self._game.update_game_table()
        
        if self._phase_handler.game_info.blue_won_queston():
            logging.info('Blue team won')
        elif self._phase_handler.game_info.red_won_queston():
            logging.info('Red team won')
        elif self._phase_handler.game_info.start_merlin_hunt_queston():
            logging.info('Starting merlin hunt')
            self._phase_handler.message_other_sub_phase(                  
                  self._sub_phase_type, 
                  {InterPhaseCrucialActions.MERLIN_HUNT_IS_STARTED : None}
            )
        else:
            logging.info('Notifying talk sub phase about another round start.')
            self._phase_handler.message_other_sub_phase(                  
                  self._sub_phase_type, 
                  {InterPhaseCrucialActions.VOTE_SUB_PHASES_CHAIN_ENDED : None}
            )

            from .vote_sub_phase_party_select import PartySelectVoteSubPhase

            result = PartySelectVoteSubPhase(                                  
                                 self._phase_handler, 
                                 self._game, 
                                 self.get_next_party_leader())
        
        # TODO :
        # if blue won
        #     display results and end game
        # elif red won :
        #     display result and eng game
        # elif start merlin hunt:
        #     notify talk sub phase about merlin hunt start
        #     return merlin hunt sub phase
        # else
        #     notify talk phase about round end - it should start player talk
        #     return party selection sub phase

        logging.info('Going to next Vote Sub Phase.')
        return result

    def start(self):
        logging.info('Starting phase.')
        self._sub_phase_ended = False

        self.vote_content_handler.\
                set_coordinating_sub_phase_and_expected_end(
                    self, 
                    None,
                    MissionResultVoteSubPhase.MISSION_RESULT_K_WORD)

        num_of_fails = \
            self._phase_handler.get_num_of_fails_to_fail_the_mission()
      
        vpids_to_vote_opts = dict()

        # === Getting vote options for selected players ===================== #

        from ..game import AvaGame

        game : AvaGame = self._game

        for voter_emoji_str in self._selected_party_emojies:
            voter_pid = None
            
            for pid, emoji in game.player_id_to_emoji_dict.items():
                if str(emoji) == voter_emoji_str:
                    voter_pid = pid
                    break
            
            from ..mechanics.roles import AbstractRole, Team

            voter_role : AbstractRole = game.player_id_to_role_dict[voter_pid]

            if voter_role.team == Team.BLUE:
                vpids_to_vote_opts[voter_pid] = VoteOptions.ONLY_YES
            else:
                vpids_to_vote_opts[voter_pid] = VoteOptions.YES_AND_NO
        
        # === End of getting vote options =================================== #


        self.vote_content_handler.initiate_vote(
            None,
            vpids_to_vote_opts,
            VoteType.MISSION_RESULT,
            party_players_emojies = self._selected_party_emojies,
            number_of_votes_to_fail = num_of_fails)

    def _stop(self):
        logging.info('Stopping phase.')
        
        self._sub_phase_ended = True
        self._notify_phase_handler_about_this_phase_end()

    def react_or_content_handler_action(self, content_dict):
        logging.error('Received action content dict: ' + str(content_dict)) 

        if not self._sub_phase_ended:            
           
            if MissionResultVoteSubPhase.MISSION_RESULT_K_WORD in content_dict:
                self._mission_result = \
                  content_dict[MissionResultVoteSubPhase.MISSION_RESULT_K_WORD]
        
                self._stop()

            else:
                logging.error('Unexpected action key word received.')
        
        else:
            logging.error('Received content action for a stoped sub phase.')
