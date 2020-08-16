import logging

import languages.ukrainian_lang as lang

from .abstract_content_handler import AbsContentHandler

class SecretInfoContentHandler(AbsContentHandler):


    def __init__(self, game, channels_handlers, master_channel_id):
        super().__init__(game, master_channel_id)
        self._game = game
    
        for game_ch in channels_handlers:
            self._panels_handlers.append(game_ch.secret_info_panel)

    async def initial_render(self):

        pids_to_channels = self._game.player_id_to_txt_ch_handler_dict 

        ch_ids_to_pids =\
            dict((ch.id, pid) for pid, ch in pids_to_channels.items())
        
        for panel_hdlr in self._panels_handlers:
            pid = ch_ids_to_pids[panel_hdlr.channel_id]
            panel_hdlr.set_content_handler(self)   
            
            role = self._game.player_id_to_role_dict[pid]
            
            secret_info = role.get_secret_info_embed(pid)

            await panel_hdlr.publish(secret_info)