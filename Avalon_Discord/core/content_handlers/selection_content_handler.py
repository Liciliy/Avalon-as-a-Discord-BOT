import logging

import languages.ukrainian_lang as lang

from .abstract_content_handler import AbsContentHandler
from ..panels.abstract_panel_handler import PanelContent
from ..panels.constants_game_panel_handler import REACTION_ADD, REACTION_REM

class SelectionType:
    PARTY  = 0
    MERLIN = 1


class SelectionContentHandler(AbsContentHandler):
    _selection       = None
    _players_emojies = None
    
    def __init__(self, game, channels_handlers, master_channel_id):
        super().__init__(game, master_channel_id)
        self._game = game

        for game_ch in channels_handlers:
            self._panels_handlers.append(game_ch.selection_panel)

        self._players_emojies = list()

        for _, em in game.player_id_to_emoji_dict.items():
            emoji_as_str = str(em)[1:-1]
            self._players_emojies.append(emoji_as_str)

    async def initial_render(self):
        content = PanelContent(
            text = lang.SEL_EMPTY_SELECTION, 
            reactions = None)

        for panel_hdlr in self._panels_handlers:
            panel_hdlr.set_content_handler(self)            
            await panel_hdlr.publish(content)

    def initiate_selection(self, type, selector_pid, selector_name):
        self._selection = Selection(self.pid_to_ch_hd[selector_pid].id,
                                    selector_name,
                                    type)

        self.update_selection_pannels()
    
    def handle_reaction(self, reaction_payload, pnl_hndl):
        
        emoji = reaction_payload.emoji
        logging.info(f'Got new reaction: {str(emoji)}.')
        logging.info(f'Type is: {reaction_payload.event_type}')

        logging.info(f'Prev selection: {str(self._selection.selection_list)}')

        emoji_str = f'<:{emoji.name}:{str(emoji.id)}>'
        if   self._selection.type == SelectionType.PARTY:
            
            if reaction_payload.event_type == REACTION_ADD:
                self._selection.selection_list.append(emoji_str)  
            
            else:
                self._selection.selection_list.remove(emoji_str)

        elif self._selection.type == SelectionType.MERLIN:
            if reaction_payload.event_type == REACTION_ADD:
                self._selection.selection_list.clear()
                self._selection.selection_list.append(emoji_str)
                pnl_hndl.order_del_reaction(reaction_payload.emoji, 
                                            pnl_hndl.channel_id)
            
            else: pass

        logging.info(f'New selection: {str(self._selection.selection_list)}')

        # NOTE Below panels update commented because it give no info to user and
        # just uses resources.
        # self.update_selection_pannels()

        self.notify_game_about_selection()

    def _merlin_selection_panels_update(self):
        for p_hdlr in self._panels_handlers:
            content = None

            if p_hdlr.channel_id == self._selection.selector_ch_id:
                if self._selection.is_selected:
                    content = PanelContent(lang.SEL_YOU_HAVE_CHOSEN_MERLIN, 
                                           None)

                else:
                    content =\
                        PanelContent(lang.SEL_YOU_GUESS_MERLIN, 
                                     self._players_emojies)
            else:
                if self._selection.is_selected:
                    content =\
                      PanelContent(
                        lang.SEL_PLAYER_HAVE_CHOSEN_MERLIN.\
                            format(self._selection.selector_name), 
                        None)
                else:
                    content =\
                      PanelContent(
                        lang.SEL_PLAYER_GUESSES_MERLIN.\
                            format(self._selection.selector_name), 
                        None)

            p_hdlr.update_and_publish(content)

    def _party_selection_panels_update(self):
        for p_hdlr in self._panels_handlers:
            content = None

            if p_hdlr.channel_id == self._selection.selector_ch_id:
                # NOTE Below 'if' wont be executed (unless uncomment panel update
                # in handle reaction function ).
                if self._selection.is_selected:
                    content = PanelContent(lang.SEL_YOU_HAVE_CHOSEN_PARTY, 
                                           None)

                else:
                    content =\
                        PanelContent(lang.SEL_YOU_CHOOSE_PARTY, 
                                     self._players_emojies)
            else:
                # NOTE Below 'if' wont be executed (unless uncomment panel update
                # in handle reaction function ).
                if self._selection.is_selected:
                    content =\
                      PanelContent(
                        lang.SEL_PLAYER_HAVE_CHOSEN_PARTY.\
                            format(self._selection.selector_name), 
                        None)
                else:
                    content =\
                      PanelContent(
                        lang.SEL_PLAYER_CHOOSES_PARTY.\
                            format(self._selection.selector_name), 
                        None)

            p_hdlr.update_and_publish(content)
    
    def update_selection_pannels(self):
        UPDATE_FUNC = {
            SelectionType.PARTY   : self._party_selection_panels_update, 
            SelectionType.MERLIN  : self._merlin_selection_panels_update
        }

        UPDATE_FUNC[self._selection.type]()

    def notify_game_about_selection(self):
        # TODO Notify game here
        #self._game.selection_happen(self._selection.selection_list)
        #print('Here game is notified about selection.')
        self._coordinating_sub_phase.\
            react_or_content_handler_action(
                {self._end_type_k_word : self._selection.selection_list})
        
    def stop_selection(self):
        # TODO think about checking if the selection actually happen.

        for p_hdlr in self._panels_handlers:
            content = None
            
            sel_type = self._selection.type
            s_name   = self._selection.selector_name 

            if p_hdlr.channel_id == self._selection.selector_ch_id:
                if   sel_type == SelectionType.PARTY:
                    content = PanelContent(lang.SEL_YOU_HAVE_CHOSEN_PARTY, 
                                           None)

                elif sel_type == SelectionType.MERLIN:
                    content = PanelContent(lang.SEL_YOU_HAVE_CHOSEN_MERLIN, 
                                           None)
                    
                # TODO add an 'else' with throwing of an exception telling that
                # unexpected type received.

                p_hdlr.clear_reactions()

            else:
                if   sel_type == SelectionType.PARTY:
                    content = PanelContent(
                      lang.SEL_PLAYER_HAVE_CHOSEN_PARTY.format(s_name), 
                      None)

                elif sel_type == SelectionType.MERLIN:
                    content = PanelContent(
                      lang.SEL_PLAYER_HAVE_CHOSEN_MERLIN.format(s_name), 
                      None)
        
            p_hdlr.update_and_publish(content)

    @property
    def pid_to_ch_hd(self):
        return self._game.player_id_to_txt_ch_handler_dict


class Selection:
    selector_ch_id = None
    selector_name  = None
    type           = None
    selection_list = None

    reactions_were_added = None

    def __init__(self, selector_ch_id, selector_name, type):
        self.type = type
        self.selector_ch_id = selector_ch_id
        self.selector_name  = selector_name
        self.selection_list = list()

        self.reactions_were_added = False

    @property
    def is_selected(self):
        return len(self.selection_list) > 0