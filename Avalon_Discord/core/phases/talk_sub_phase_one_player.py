import asyncio
import logging

from .abstract_talk_sub_phase import \
    AbsTalkSubPhase, \
    TalkSubPhaseHandledActions, \
    ExecutionEndType

from .abstract_sub_phase import ResDictKWords

from ..content_handlers.timer_content_handler import TimerType

from ..common import NotImplementedMethodUsage

class OnePlayerTalkSubPhase(AbsTalkSubPhase):

    DEF_TALK_TIME_S = 60
    PLAYER_TALK_END_TYPE = ExecutionEndType.PLAYER_TALK_END

    TALK_END_K_WORD = ResDictKWords.ENDED_ACTION_TYPE

    _talk_time = None

    def __init__(self, 
                 phase_handler,
                 game,
                 talking_player_id,
                 party_leader,
                 talk_time = DEF_TALK_TIME_S):

        super().__init__(phase_handler, 
                         TalkSubPhaseHandledActions.ONE_PLAYER_TALK,
                         game,
                         talking_player_id,
                         party_leader)
        
        self._talk_time = talk_time

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
        from .talk_sub_phase_preparation    import TalkPrepSubPhase
        from .talk_sub_phase_all_discussion import AllDiscussionTalkSubPhase

        LIST_START_POS = 0
        ONE_MORE_POS   = 1

        
        pids = self._game.players_ids_list

        curr_talker_pos = pids.index(self._talking_player_id)

        next_talker_pos = curr_talker_pos + ONE_MORE_POS

        if self._party_leader == self._talking_player_id:
            logging.info('Retruning next phase - All-Discussion.')
            return AllDiscussionTalkSubPhase(
                                self._phase_handler, 
                                self._game,
                                self._party_leader,
                                self._party_leader)

        elif (next_talker_pos) == len(pids):
            next_talker_pos = LIST_START_POS

        logging.info(f'Retruning next phase - {TalkPrepSubPhase.__name__}.')
        return TalkPrepSubPhase(self._phase_handler, 
                                self._game,
                                pids[next_talker_pos],
                                self._party_leader)

    def start(self):
        logging.info('Starting phase.')
        self._sub_phase_ended = False
        self.timer_content_handler.\
                set_coordinating_sub_phase_and_expected_end(
                    self, 
                    OnePlayerTalkSubPhase.PLAYER_TALK_END_TYPE,
                    OnePlayerTalkSubPhase.TALK_END_K_WORD)

        player_name = self._game.player_id_to_name_dict[self._talking_player_id]
        
        ch_id = self._game.\
            player_id_to_txt_ch_handler_dict[self._talking_player_id].id

        event_loop = asyncio.get_running_loop()

        event_loop.create_task(
            self.timer_content_handler.start_timer(
                TimerType.TALKING_TIMER,
                self._talk_time,
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
                                    OnePlayerTalkSubPhase.TALK_END_K_WORD,
                                    OnePlayerTalkSubPhase.PLAYER_TALK_END_TYPE)

        if not res_type_is_correct:
            # TODO think if it is really needed to make any actions here.
            return
        
        if not self._sub_phase_ended:
            self._stop()

    def get_talker_avatar_url(self):
        return self._implemented_get_avatar() 