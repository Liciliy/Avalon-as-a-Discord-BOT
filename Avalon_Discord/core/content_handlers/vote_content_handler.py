import os
import asyncio
import logging


import languages.ukrainian_lang as lang

from .abstract_content_handler import AbsContentHandler

from ..panels.abstract_panel_handler import PanelContent

from ..panels.vote_panel_handler import MessageType


class VoteType:
    PARTY_FORMING   = 0
    PARTY_APPROVING = 1
    MISSION_RESULT  = 2
    MERLIN_HUNT     = 3


class VoteOptions:
    ONLY_YES   = 0
    YES_AND_NO = 1


class VoteContentHandler(AbsContentHandler):
    NO_VOTE     = '❌'
    YES_VOTE    = '✅'
    EMPTY_VOTE  = '▪️*******' 
    RESULTS_DISPLAY_TIME = 7
    MISSION_FAILURE_EMOJI = '❌'
    MISSION_SUCCESS_EMOJI = '✅'

    OPTIONS = {
        VoteOptions.YES_AND_NO : [YES_VOTE, NO_VOTE],
        VoteOptions.ONLY_YES   : [YES_VOTE]
    }

    _vote = None
    _ch_id_to_player_emoji = None    

    def __init__(self, game, channels_handlers, master_channel_id):
        super().__init__(game, master_channel_id)
        self._game = game

        for game_ch in channels_handlers:
            self._panels_handlers.append(game_ch.vote_panel)

        # === Here relation between CH ID and emoji is set. =================== 
        self._ch_id_to_player_emoji = dict()
        for pid, ch_handler in game.player_id_to_txt_ch_handler_dict.items():

            player_emoji = game.player_id_to_emoji_dict[pid]
            
            self._ch_id_to_player_emoji[ch_handler.id] = str(player_emoji)
        # =====================================================================
        
    # TODO think about move this one into init()
    # Probably impossible, because init cant be async. And here 
    # an awaited publish must be used.
    async def initial_render(self):

        content = {
                MessageType.TEXT_MSG  : VoteContentHandler.EMPTY_VOTE,
                MessageType.EMOJI_MSG : 
                  PanelContent(VoteContentHandler.EMPTY_VOTE, None)
            }
        for pannel_hdlr in self._panels_handlers:
            pannel_hdlr.set_content_handler(self)            
            await pannel_hdlr.publish(content)

    def initiate_vote(self, 
                      players_to_select_num, 
                      voting_players_ids_to_vote_options,
                      vote_type,
                      party_players_emojies = None,
                      number_of_votes_to_fail = 0):
        """Initiates a game vote.

        Args:
            players_to_select_num (int): Number of players to select.
                                         Applicable only to party gathering and
                                         Merlin hunt.

            voting_players_ids_to_vote_options (dict(int, list)):
                Defines who can vote and what vote options do they have.
                Example #1: on the mission success vote blue players can have 
                only Yes vote. 
                Example #2: on party players selection only party leader can 
                vote (when he selects players_to_select_num number of players).

                NOTE!!! SHOULD CONTAIN ONLY THOSE PLAYERS WHO CAN VOTE!!!  

            vote_type (VoteType): there are few vote types. For details please 
                see VoteType class.

            party_players_emojies (list(str)): list of emojies as strings.
                Should be used in cases when the list wont change through vote.

            number_of_votes_to_fail (int): number of votes needed to fail the 
                vote. Is applicable only in case of mission result vote.
        """        
        voters_chs_ids_to_vote_opts = dict()

        for pid, vote_option in voting_players_ids_to_vote_options.items():
            voters_chs_ids_to_vote_opts[self.pid_to_ch_hd[pid].id] = vote_option
        
        self._vote = Vote(vote_type, 
                          players_to_select_num,
                          voters_chs_ids_to_vote_opts,
                          number_of_votes_to_fail)

        if party_players_emojies != None:
            self._vote.set_party_players_emojies(party_players_emojies)

        self.update_vote_pannels()
            
    def start_vote(self):
        """Starts vote. The main consequence is that vote reactions are added 
        (in case of party forming vote).
        """
        self._vote.set_vote_started()
        self.update_vote_pannels()

    def _party_forming_vote_panels_update(self):
        # In party forming vote there is only one person who can vote - party 
        # leader.
        leader_ch_id = self._vote.all_voters_chs_ids[0]
        
        non_leaders_header = lang.VOTE_PLAYERS_SELECTED.format(
                    sel  = str(self._vote.selected_players_num),
                    need = str(self._vote.num_of_players_to_select))
        
        party_emoji_str = self._vote.party_str
        if party_emoji_str == '' or party_emoji_str == None:            
            party_emoji_str = VoteContentHandler.EMPTY_VOTE

        for p_hdlr in self._panels_handlers:

            content = {
                MessageType.TEXT_MSG  : None,
                MessageType.EMOJI_MSG : None
            }

            ch_id = p_hdlr.channel_id

            if ch_id == leader_ch_id:
                reaction = None

                sel_players  = self._vote.selected_players_num
                need_players = self._vote.num_of_players_to_select

                # Below 'if' handles case when needed number of players were
                # added to the party. 
                if sel_players == need_players: 
                    logging.info(
                        f'Number of needed players equeal {need_players} ' + 
                        f'to number of selected players {sel_players}.')                   

                    if self._vote.vote_started:
                        
                        content[MessageType.TEXT_MSG] =\
                            lang.VOTE_LEADER_SELECT_PLAYERS_RDY.format(
                               sel  = str(self._vote.selected_players_num),
                               need = str(self._vote.num_of_players_to_select))

                        # TODO below check doesnt work. There was a situation 
                        # when sel_players == need_players but no reaction was 
                        # added. NOTE: INVESTIGATE AND FIX!!!
                        if not self._vote.reactions_added:
                            logging.info(
                                'Vote reaction was NOT added before. Adding...')
                            reaction = [VoteContentHandler.YES_VOTE]
                            self._vote.reactions_added = True
                        else:
                            logging.info(
                                'Vote reaction was added before. Quiting...')
                    
                    else:
                        content[MessageType.TEXT_MSG] =\
                            lang.VOTE_LEADER_SELECT_PLAYERS_TALKS.format(
                               sel  = str(self._vote.selected_players_num),
                               need = str(self._vote.num_of_players_to_select))
                    
                # Below else handles case when leader hasn't selected needed 
                # number of players to the party. 
                else:
                    if self._vote.reactions_added: 
                        p_hdlr.clear_reactions()
                        self._vote.reactions_added = False

                    if sel_players > need_players:
                        content[MessageType.TEXT_MSG] =\
                             lang.VOTE_LEADER_TOO_MANY_PLAYERS_SELECTED.format(
                               sel  = str(self._vote.selected_players_num),
                               need = str(self._vote.num_of_players_to_select))

                    else: # number of selected players is lesser than needed.
                        content[MessageType.TEXT_MSG] =\
                             lang.VOTE_LEADER_TOO_FEW_PLAYERS_SELECTED.format(
                               sel  = str(self._vote.selected_players_num),
                               need = str(self._vote.num_of_players_to_select))                

                content[MessageType.EMOJI_MSG] = PanelContent(party_emoji_str, 
                                                              reaction)
            # Below else handles render for non-leaders.
            else:
                content[MessageType.TEXT_MSG]  = non_leaders_header
                content[MessageType.EMOJI_MSG] = PanelContent(party_emoji_str, 
                                                              None)
        
            p_hdlr.update_and_publish(content)
            
    def _party_approval_vote_panels_update(self):
        # === Getting string with emojies of yet not voted players. ===========
        players_to_vote_emojies = list()
        for ch_id in self._vote.players_left_to_vote_chs_ids:
            players_to_vote_emojies.append(
                str(self._ch_id_to_player_emoji[ch_id]))

        players_to_vote_str = ''.join(players_to_vote_emojies)
        # =====================================================================

        party_emoji_str     = self._vote.party_str

        for p_hdlr in self._panels_handlers:
            ch_id = p_hdlr.channel_id

            content = {
                MessageType.TEXT_MSG  : None,
                MessageType.EMOJI_MSG : None
            }

            if    ch_id not in self._vote.yes_voters_chs_ids \
              and ch_id not in self._vote.no_voters_chs_ids:
                
                content[MessageType.TEXT_MSG] = lang.VOTE_VOTE_FOR_PARTY_Q
                text      = None
                reactions = None

                text = party_emoji_str

                if not self._vote.reactions_added:
                    reactions = [VoteContentHandler.YES_VOTE,
                                 VoteContentHandler.NO_VOTE]

                content[MessageType.EMOJI_MSG] = PanelContent(text, reactions)

            else:
                content[MessageType.TEXT_MSG] = lang.VOTE_WAINTING_FOR_OTHERS
                content[MessageType.EMOJI_MSG] =\
                     PanelContent(players_to_vote_str, None)

            p_hdlr.update_and_publish(content)

        
        if not self._vote.reactions_added:
            self._vote.reactions_added = True
    
    async def _display_approval_results(self):  
        # === Filling yes voters str =================
        yes_votesrs_list = list()
        for ch_id in self._vote.yes_voters_chs_ids:
            yes_votesrs_list.append(self._ch_id_to_player_emoji[ch_id])

        yes_voters_str = ' '.join(yes_votesrs_list)
        # ============================================

        # === Filling no voters str ==================
        no_votesrs_list = list()
        for ch_id in self._vote.no_voters_chs_ids:
            no_votesrs_list.append(self._ch_id_to_player_emoji[ch_id])

        no_voters_str = ' '.join(no_votesrs_list)
        # ============================================

        emoji_msg_str = VoteContentHandler.YES_VOTE\
                      + '    '\
                      + yes_voters_str\
                      + '\n'\
                      + VoteContentHandler.NO_VOTE\
                      + '    '\
                      + no_voters_str

        content = {
                MessageType.TEXT_MSG  : lang.VOTE_APPROVAL_RESULT,
                MessageType.EMOJI_MSG : PanelContent(emoji_msg_str, None)
            }

        for p_hdlr in self._panels_handlers:
            p_hdlr.update_and_publish(content)

        await asyncio.sleep(VoteContentHandler.RESULTS_DISPLAY_TIME)

        self.notify_game_vote_is_done()

    def _mission_result_vote_panels_update(self):    

        for p_hdlr in self._panels_handlers:
            ch_id = p_hdlr.channel_id

            content = {
                MessageType.TEXT_MSG  : lang.VOTE_MISSION_HAS_STARTED,
                MessageType.EMOJI_MSG : None
            }
            
            # Handling not voting at all player.
            if ch_id not in self._vote.all_voters_chs_ids:
                content[MessageType.EMOJI_MSG] =\
                     PanelContent(lang.VOTE_MISSION_NON_PARTY, None)
            
            # Handling not yet voted played.
            elif  ch_id not in self._vote.yes_voters_chs_ids \
              and ch_id not in self._vote.no_voters_chs_ids:  
                
                reactions = None
                if not self._vote.reactions_added:
                    vote_options = self._vote.voter_ch_id_to_vote_options[ch_id]
                    
                    reactions = VoteContentHandler.OPTIONS[vote_options]

                content[MessageType.EMOJI_MSG] =\
                    PanelContent(lang.VOTE_CHOOSE_MISSION_RESULT, reactions)
            
            # Handling already voted player.
            else:
                content[MessageType.EMOJI_MSG] =\
                        PanelContent(lang.VOTE_WAITING_4_OTHERS, None)

            p_hdlr.update_and_publish(content)
        
        if not self._vote.reactions_added:
            self._vote.reactions_added = True

    async def _display_mission_results(self):

        emoji_msg_str = ((VoteContentHandler.MISSION_SUCCESS_EMOJI 
                          * len(self._vote.yes_voters_chs_ids))
                         +
                         (VoteContentHandler.MISSION_FAILURE_EMOJI
                          * len(self._vote.no_voters_chs_ids))
                        )

        header = ''
        if not self._vote.is_failed_mission_vote:
            header = lang.VOTE_SUCCESS_MISSION
        else:
            header = lang.VOTE_FAILED_MISSION

        content = {
                MessageType.TEXT_MSG  : header,
                MessageType.EMOJI_MSG : PanelContent(emoji_msg_str, None)
            }

        for p_hdlr in self._panels_handlers:
            p_hdlr.update_and_publish(content)

        await asyncio.sleep(VoteContentHandler.RESULTS_DISPLAY_TIME)

        self.notify_game_vote_is_done()

    def _merlin_hunt_vote_panels_update(self):
        # In party forming vote there is only one person who can vote - party 
        # leader.
        hunter_ch_id = self._vote.all_voters_chs_ids[0]
        
        non_hunters_header = ''
        hunters_header     = ''
        merlin_emoji_str   = ''

        # Merlin not selected 
        if self._vote.party_str == '':
            merlin_emoji_str = lang.VOTE_NO_ONE_SELECTED_AS_MERLIN

            hunters_header     = lang.VOTE_HUNTER_SELECTS_MERLIN
            non_hunters_header = lang.VOTE_RED_SEEK_MERLIN 
        # Merlin selected
        else:
            merlin_emoji_str   = self._vote.party_str

            hunters_header     = lang.VOTE_HUNTER_MERLIN_SELECTED
            non_hunters_header = lang.VOTE_MERLIN_SELECTED


        for p_hdlr in self._panels_handlers:

            content = {
                MessageType.TEXT_MSG  : None,
                MessageType.EMOJI_MSG : None
            }

            if p_hdlr.channel_id == hunter_ch_id:
                reacts = None  

                # It makes sense to add YES reaction only when Merlin is 
                # selected and the reactiun was not added previously.
                if not self._vote.reactions_added \
                  and self._vote.party_str != '': 
                    reacts = [VoteContentHandler.YES_VOTE]
                    self._vote.reactions_added = True

                content[MessageType.TEXT_MSG]  = hunters_header
                content[MessageType.EMOJI_MSG] = PanelContent(merlin_emoji_str, 
                                                              reacts)

            else:
                content[MessageType.TEXT_MSG]  = non_hunters_header
                content[MessageType.EMOJI_MSG] = PanelContent(merlin_emoji_str, 
                                                              None)
        
            p_hdlr.update_and_publish(content)

    async def _display_merlin_hunt_results(self):
       
        content = {
                MessageType.TEXT_MSG  : lang.VOTE_RED_SHOT_A_PLAYER,
                MessageType.EMOJI_MSG : PanelContent(self._vote.party_str, None)
            }

        for p_hdlr in self._panels_handlers:
            p_hdlr.update_and_publish(content)

        await asyncio.sleep(VoteContentHandler.RESULTS_DISPLAY_TIME)

        self.notify_game_vote_is_done()

    def update_vote_pannels(self, party_emojies_list = None):
        """Leads to vote panels re-render attempt.

        Args:
            party_emojies_list (list(str), optional): list of players emojies. 
                The list represents a game party. 
                Should be used only and Party fomrming and merlin hunt votes.
                Defaults to None.
                NOTE in case of Merlin hunt the list should contain only one
                emoji.
        """
        UPDATE_FUNC = {
            VoteType.PARTY_FORMING   : self._party_forming_vote_panels_update, 
            VoteType.PARTY_APPROVING : self._party_approval_vote_panels_update,
            VoteType.MISSION_RESULT  : self._mission_result_vote_panels_update,
            VoteType.MERLIN_HUNT     : self._merlin_hunt_vote_panels_update 
        }

        # TODO check if vote type is Party_forming or merlin_hunt, 
        # otherwise - dont change party str.
        if party_emojies_list != None:
            self._vote.set_party_players_emojies(party_emojies_list)

        UPDATE_FUNC[self._vote.type]()
    
    async def player_voted(self, emoji_str, player_ch_id):
        # TODO here react on a player vote - update his vote panel
        # with results (only party approve vote)or other stuff
        if   emoji_str == VoteContentHandler.YES_VOTE:            
            self._vote.yes_voters_chs_ids.append(player_ch_id)
        elif emoji_str == VoteContentHandler.NO_VOTE:
            self._vote.no_voters_chs_ids.append(player_ch_id)
        
        if self._vote.all_voters_voted:

            vote_type = self._vote.type

            if   vote_type == VoteType.PARTY_APPROVING:
                await self._display_approval_results()
            
            elif vote_type == VoteType.PARTY_FORMING:
                # TODO Here check if number of selected players is equal to 
                # number of needed players. If not - dont end vote. 
                self.notify_game_vote_is_done()
            
            elif vote_type == VoteType.MISSION_RESULT:
                await self._display_mission_results()

            elif vote_type ==VoteType.MERLIN_HUNT:
                await self._display_merlin_hunt_results()

        else:
            self.update_vote_pannels()

    def notify_game_vote_is_done(self):
        res_dict = dict()
        if self._vote._vote_type == VoteType.PARTY_APPROVING:
            res_dict = \
              {self._end_type_k_word : self._vote.is_successful_party_approval}

        elif self._vote._vote_type == VoteType.MISSION_RESULT:
            res_dict = \
              {self._end_type_k_word : not(self._vote.is_failed_mission_vote)}        

        else:
            res_dict = self.get_base_action_end_dict() 

        self._coordinating_sub_phase.\
            react_or_content_handler_action(res_dict)


    # TODO Find a way to make this function be executed immediately. 
    async def handle_reaction(self, reaction_payload):
        await self.player_voted(str(reaction_payload.emoji), 
                                reaction_payload.channel_id)

    @property
    def player_id_to_emoji(self):
        return self._game.player_id_to_emoji_dict

    @property
    def pid_to_ch_hd(self):
        return self._game.player_id_to_txt_ch_handler_dict

    @property
    def is_vote_done(self):
        return self._vote.all_voters_voted


class Vote:
    # === Data constant per vote ===============
    _vote_type                  = None
    party_players_emojies       = None
    all_voters_chs_ids          = None
    num_of_players_to_select    = None
    voter_ch_id_to_vote_options = None
    _votes_to_fail              = None
    #===========================================


    # === Data changed during vote =============
    voted_chs_ids        = None    
    yes_voters_chs_ids   = None
    no_voters_chs_ids    = None
    vote_started         = None
    reactions_added      = None
    _party_emojies_str   = None
    selected_players_num = None
    #===========================================    

    def __init__(self,
                 vote_type, 
                 players_to_select_number,
                 voters_chs_ids_to_vote_options,
                 votes_to_fail = 0):

        self._vote_type = vote_type
        self.party_players_emojies  = list()
        self.all_voters_chs_ids = [*voters_chs_ids_to_vote_options.keys()]
        self.voter_ch_id_to_vote_options = voters_chs_ids_to_vote_options
        self.num_of_players_to_select = players_to_select_number
        self._votes_to_fail = votes_to_fail
                 
        self.vote_started          = False
        self.reactions_added       = False
        self.voted_chs_ids         = list()
        self.yes_voters_chs_ids    = list()
        self.no_voters_chs_ids     = list()
        self.selected_players_num  = 0

    @property
    def all_voters_voted(self):
        voted_number = len(self.no_voters_chs_ids) + len(self.yes_voters_chs_ids)
        return (len(self.all_voters_chs_ids) == voted_number)

    def set_party_players_emojies(self, ems):
        self.selected_players_num = len(ems) 
        for em in ems:
            em = em.replace('<', '').replace('>', '')

        self._party_emojies_str = ' '.join(ems)

    def set_vote_started(self):
        self.vote_started = True

    @property
    def party_str(self):
        return self._party_emojies_str

    @property
    def players_left_to_vote_chs_ids(self):
        result = list()
    
        for ch_id in self.all_voters_chs_ids:
            if    ch_id not in self.yes_voters_chs_ids\
              and ch_id not in self.no_voters_chs_ids:
                result.append(ch_id)
        
        return result

    @property
    def type(self):
        return self._vote_type
    
    @property
    def is_failed_mission_vote(self):
        """Should be used only at mission result vote.

        Returns:
            Bool: True if mission was failed. False if it was successful.
        """
        return len(self.no_voters_chs_ids) >= self._votes_to_fail

    
    @property
    def is_successful_party_approval(self):
        """Should be used only at mission approval vote.

        Returns:
            Bool: True if vote was successful. False if it was failed.
        """
        return len(self.no_voters_chs_ids) < len(self.yes_voters_chs_ids) 