import asyncio
import logging

from .abstract_talk_sub_phase import \
    AbsTalkSubPhase, \
    TalkSubPhaseHandledActions, \
    ExecutionEndType

from .abstract_sub_phase import ResDictKWords

from ..content_handlers.timer_content_handler import TimerType

from ..common import NotImplementedMethodUsage

from .phase_handler import PhaseHandler

class NoTalkTalkSubPhase(AbsTalkSubPhase):

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
        # TODO to be implemented.
        pass

    def start(self):
        logging.info('Starting no talk phase.')        

    def _stop(self):
        logging.info('Stopping phase.')
        self._sub_phase_ended = True
        self._notify_phase_handler_about_this_phase_end()