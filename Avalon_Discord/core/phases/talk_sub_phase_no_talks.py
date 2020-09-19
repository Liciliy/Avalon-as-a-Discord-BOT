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
        if    InterPhaseCrucialActions.VOTE_SUB_PHASES_CHAIN_ENDED \
                in \
              content:
            logging.info('Going to initiate next talking round.')
            
            self.initiate_new_talk_round()
        elif  InterPhaseCrucialActions.MERLIN_HUNT_IS_STARTED \
                in \
              content:
            logging.info('Going to initiate Merlin Hunt talking round.')
            # TODO add merlin hunt actions here
            pass
        logging.info('Leaving function: react_on_other_sub_phase_action.')
        

    def get_next_sub_phase(self):
        result = None

        if self._next_talk_phase != None:
            result = self._next_talk_phase
            self._next_talk_phase = None
        
        else:
            logging.error('Next talk sub phase object is None.')
        
        return result

    def start(self):
        logging.info('Starting no talk phase.')        

    def _stop(self):
        logging.info('Stopping phase.')
        self._sub_phase_ended = True
        self._notify_phase_handler_about_this_phase_end()