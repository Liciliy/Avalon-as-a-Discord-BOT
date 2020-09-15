import logging

from ..common import NotImplementedMethodUsage


class AbsContentHandler:
    # One time initiated variables
    _master_channel_id     = None    
    _panels_handlers = None
    _game = None

    _coordinating_sub_phase = None
    _expected_execution_end = None
    _end_type_k_word        = None


    def __init__(self, game, master_channel_id):
        self._game = game
        self._master_channel_id = master_channel_id
        self._panels_handlers = list()


    async def initial_render(self):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: initial_render')

    def handle_reaction(self, emoji_str):
        logging.critical('Unimplemented method usage!')
        raise NotImplementedMethodUsage('Method name: handle_reaction')

    def set_coordinating_sub_phase_and_expected_end(self, 
                                                    sub_phase, 
                                                    end,
                                                    end_type_k_word):
        self._coordinating_sub_phase = sub_phase
        self._expected_execution_end = end
        self._end_type_k_word        = end_type_k_word

    def get_base_action_end_dict(self):
        return {self._end_type_k_word : self._expected_execution_end}