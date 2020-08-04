import logging

from ..common import NotImplementedMethodUsage


class AbsContentHandler:
    # One time initiated variables
    _master_channel_id     = None    
    _panels_handlers = None
    _game = None


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