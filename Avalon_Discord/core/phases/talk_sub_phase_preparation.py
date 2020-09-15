import asyncio
import logging

from .abstract_talk_sub_phase import \
    AbsTalkSubPhase, \
    TalkSubPhaseHandledActions, \
    ExecutionEndType

from .abstract_sub_phase import ResDictKWords

from ..content_handlers.timer_content_handler import TimerType

from ..common import NotImplementedMethodUsage

class TalkPrepSubPhase(AbsTalkSubPhase):

    DEF_PREPARATION_TIME_S = 3
    PREP_END_TYPE = ExecutionEndType.PREP_ENDED

    PREP_END_K_WORD = ResDictKWords.ENDED_ACTION_TYPE

    _prep_time = None

    def __init__(self, 
                 phase_handler,
                 game,
                 talking_player_id,
                 party_leader,
                 prep_time = DEF_PREPARATION_TIME_S):

        super().__init__(phase_handler, 
                         TalkSubPhaseHandledActions.TALK_PREPARATION_PHASE,
                         game,
                         talking_player_id,
                         party_leader)
        
        self._prep_time = prep_time

    def react_on_other_sub_phase_end(self):
        """Check type of other sub phase handled action.
        If the action end requires any reactions from this phase - the response
        actions are executed.

        Raises:
            NotImplementedMethodUsage: [description]
        """
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage(\
            'Method name: react_on_other_sub_phase_end')

    def get_next_sub_phase(self):

        from . talk_sub_phase_one_player import OnePlayerTalkSubPhase
        logging.info(
            f'Retruning next phase - {OnePlayerTalkSubPhase.__name__}.')
        return OnePlayerTalkSubPhase(self._phase_handler, 
                                     self._game,
                                     self._talking_player_id,
                                     self._party_leader)

    def start(self):
        logging.info('Starting phase.')
        self._sub_phase_ended = False
        self.timer_content_handler.\
                set_coordinating_sub_phase_and_expected_end(self, 
                                           TalkPrepSubPhase.PREP_END_TYPE,
                                           TalkPrepSubPhase.PREP_END_K_WORD)

        player_name = self._game.player_id_to_name_dict[self._talking_player_id]
        
        ch_id = self._game.\
            player_id_to_txt_ch_handler_dict[self._talking_player_id].id

        event_loop = asyncio.get_running_loop()

        event_loop.create_task(
            self.timer_content_handler.start_timer(
                TimerType.TALK_PREPARATION_TIMER,
                self._prep_time,
                player_name,
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
                                        TalkPrepSubPhase.PREP_END_K_WORD,
                                        TalkPrepSubPhase.PREP_END_TYPE)

        if not res_type_is_correct:
            # TODO think if it is really needed to make any actions here.
            return
        
        if not self._sub_phase_ended:
            self._stop()