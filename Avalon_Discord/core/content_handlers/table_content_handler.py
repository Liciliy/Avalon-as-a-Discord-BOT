import copy
import logging

import languages.ukrainian_lang as lang

from .abstract_content_handler import AbsContentHandler

from core.mechanics.game_info import GameInfo

class TConst:
    F_MISSION = '🔴'
    S_MISSION = '🔵'
    N_MISSION = '⚪' 
    CURR_VOTE = '🛡️'
    VOTES_NUMS_LIST = [':one:', ':two:', ':three:', ':four:', ':five:']

class TableContentHandler(AbsContentHandler):     

    _players_ems_in_talk_order_str = None

    def __init__(self, game, channels_handlers, master_channel_id):
        super().__init__(game, master_channel_id)
        self._game = game

        for game_ch in channels_handlers:
            self._panels_handlers.append(game_ch.table_panel)

        players_emojies = list()

        for pid in game.players_ids_list:
            emoji_as_str = str(game.player_id_to_emoji_dict[pid])
            players_emojies.append(emoji_as_str)

        #for _, em in game.player_id_to_emoji_dict.items():
        #    emoji_as_str = str(em)
        #    players_emojies.append(emoji_as_str)

        self._players_ems_in_talk_order_str = ' '.join(players_emojies)

    def _form_table_msg(self, missions_results_list, num_of_failed_votes):
        result_str = lang.PLAYERS_ORDER + self._players_ems_in_talk_order_str \
                   + '\n'

        missions_ems = list()

        for res in missions_results_list:
            if   res == GameInfo.NOT_FINISHED_MISSION:
                missions_ems.append(TConst.N_MISSION)
                
            elif res == GameInfo.SUCCEEDED_MISSION:
                missions_ems.append(TConst.S_MISSION)

            elif res == GameInfo.FAILED_MISSION:
                missions_ems.append(TConst.F_MISSION)
        
        result_str += lang.MISSIONS_STATUSES  + ' '.join(missions_ems) + '\n'
        
        curr_vote_st = copy.deepcopy(TConst.VOTES_NUMS_LIST)

        curr_vote_st[num_of_failed_votes] = TConst.CURR_VOTE

        result_str += lang.VOTING_NUMBER  + ' '.join(curr_vote_st)

        return result_str

    async def initial_render(self):

        # TODO make [2,2,2,2,2] list be fetched from the gameInfo, isntead 
        # of filling it in manually.
        content = self._form_table_msg([2, 2, 2, 2, 2], 0)

        for panel_hdlr in self._panels_handlers:
            panel_hdlr.set_content_handler(self)            
            await panel_hdlr.publish(content)


    def update_table_pannels(self, missions_ress_list, failed_votes_num):
        
        content = self._form_table_msg(missions_ress_list, failed_votes_num)

        for panel_hdlr in self._panels_handlers:
            panel_hdlr.update_and_publish(content)
