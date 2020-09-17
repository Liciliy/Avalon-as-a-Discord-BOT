import asyncio
import logging

from .abstract_talk_sub_phase import \
    AbsTalkSubPhase, \
    TalkSubPhaseHandledActions, \
    ExecutionEndType

from .abstract_sub_phase import ResDictKWords, InterPhaseCrucialActions

from ..content_handlers.timer_content_handler import TimerType

from ..common import NotImplementedMethodUsage

from .phase_handler import PhaseHandler

class AllDiscussionTalkSubPhase(AbsTalkSubPhase):

    ONE_MINUTE_S = 60
    ALL_DISCUS_END_TYPE = ExecutionEndType.DISCUSSION_END

    TALK_END_K_WORD = ResDictKWords.ENDED_ACTION_TYPE

    _talk_time = None

    def __init__(self, 
                 phase_handler : PhaseHandler,
                 game,
                 talking_player_id,
                 party_leader):

        super().__init__(phase_handler, 
                         TalkSubPhaseHandledActions.ALL_DISCUSSION_TALK,
                         game,
                         talking_player_id,
                         party_leader)

        num_of_players_on_mission = \
            phase_handler.get_current_mission_players_num()

        logging.info(
            f'Number of mission needed players {num_of_players_on_mission}')

        
        self._talk_time = AllDiscussionTalkSubPhase.ONE_MINUTE_S \
                        * int(num_of_players_on_mission)

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
        from .talk_sub_phase_no_talks import NoTalkTalkSubPhase

        logging.info(f'Retruning next phase - {NoTalkTalkSubPhase.__name__}.')
        return NoTalkTalkSubPhase(self._phase_handler, 
                                  self._game,
                                  self._party_leader,
                                  self._party_leader)

    def start(self):
        logging.info('Starting phase.')
        self._sub_phase_ended = False

        self._phase_handler.message_other_sub_phase(
            self._sub_phase_type, 
            {InterPhaseCrucialActions.PLAYERS_SPEACHES_ROUND_ENDED : None}
        )

        self.timer_content_handler.\
                set_coordinating_sub_phase_and_expected_end(
                    self, 
                    AllDiscussionTalkSubPhase.ALL_DISCUS_END_TYPE,
                    AllDiscussionTalkSubPhase.TALK_END_K_WORD)

        ch_id = self._game.\
            player_id_to_txt_ch_handler_dict[self._talking_player_id].id

        event_loop = asyncio.get_running_loop()

        event_loop.create_task(
            self.timer_content_handler.start_timer(
                TimerType.BALAGAN_TIMER,
                self._talk_time,
                '',
                ch_id
            )
        )

    def _stop(self):
        logging.info('Stopping phase.')
        self._sub_phase_ended = True
        self._notify_phase_handler_about_this_phase_end()

    def react_or_content_handler_action(self, content_dict):   

        res_type_is_correct = self.check_if_action_end_type_is_correct(
                                content_dict,
                                AllDiscussionTalkSubPhase.TALK_END_K_WORD,
                                AllDiscussionTalkSubPhase.ALL_DISCUS_END_TYPE)

        if not res_type_is_correct:
            # TODO think if it is really needed to make any actions here.
            return
        
        if not self._sub_phase_ended:
            self._stop()