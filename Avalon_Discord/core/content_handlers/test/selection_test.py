import os
import asyncio

from ..selection_content_handler import SelectionContentHandler,\
                                   SelectionType, REACTION_ADD, REACTION_REM

from .common import TestReactionPayload, TestGame, TestChannelHandler



SEL_PANEL = """
# === Channel ID: {ch_id}============================================
   # === Header message =============================================
         {header}
   # === Reactions message ==========================================
         {reacts}
#====================================================================
"""


class TestSelectionPanelHandler:
    name = None
    _msg_content = None
    channel_id = None
    content_handler = None
    
    def __init__(self, name, ch_id):
        self.name = name
        self.channel_id = ch_id

    def set_content_handler(self, cth):
        self.content_handler = cth

    async def publish(self, content):
        print(SEL_PANEL.format(
            ch_id   = self.channel_id,
            header  = content.text,
            reacts  = str(content.reactions)))
 
        self._msg_content = content

    def update_and_publish(self, content):
        prev_header = self._msg_content.text
        prev_reacts = self._msg_content.reactions

        if    content.text != None \
          and content.text != prev_header:
            pass
        
        else:
            content.text = prev_header

        reacts = list()
        if content.reactions != None:
            for reaction in content.reactions:
                reacts.append(reaction)
        elif prev_reacts != None:
            content.reactions = prev_reacts
            for reaction in prev_reacts:
                reacts.append(reaction)
         
        print(SEL_PANEL.format(
            ch_id   = self.channel_id,
            header  = content.text,
            reacts  = ''.join(str(reacts))))
            
        self._msg_content = content

    def clear_reactions(self):
        self._msg_content.reactions = None

    def order_del_reaction(self, emoji, pnl_hndl):
        print('+++++++++++++++ Removing reaction', str(emoji))

def init_sch_with_mock_data():
    
    sph_s = [None]

    for id in range(0,8):
       sph_s.append(TestSelectionPanelHandler('SPH#_' + str(id), id))

    ch_h_1 = TestChannelHandler(id = 1, sph = sph_s[1])
    ch_h_2 = TestChannelHandler(id = 2, sph = sph_s[2])
    ch_h_3 = TestChannelHandler(id = 3, sph = sph_s[3])
    ch_h_4 = TestChannelHandler(id = 4, sph = sph_s[4])
    ch_h_5 = TestChannelHandler(id = 5, sph = sph_s[5])
    ch_h_6 = TestChannelHandler(id = 6, sph = sph_s[6])
    ch_h_7 = TestChannelHandler(id = 7, sph = sph_s[7])
    ch_h_8 = TestChannelHandler(id = 8, sph = sph_s[8])

    os.environ['TEST'] = 'YES'

    pid_to_txt_ch_hd_dict ={
        11 : ch_h_1,
        12 : ch_h_2,
        13 : ch_h_3,
        14 : ch_h_4,
        15 : ch_h_5,
        16 : ch_h_6,
        17 : ch_h_7,
        18 : ch_h_8        
    }
    
    pid_to_emoji = {
        11 : ':one:',
        12 : ':two:',
        13 : ':three:',
        14 : ':four:',
        15 : ':five:',
        16 : ':six:',
        17 : ':seven:',
        18 : ':eight:'    
    }

    t_game = TestGame(pid_to_txt_ch_hd_dict, pid_to_emoji)
    ch_hndlrs = [ch_h_1,
                 ch_h_2,
                 ch_h_3,
                 ch_h_4,
                 ch_h_5,
                 ch_h_6,
                 ch_h_7,
                 ch_h_8
                 ] 

    sch = SelectionContentHandler(t_game, ch_hndlrs, 3)

    return sch, sph_s

async def tc1():
    
    sch, sph_s = init_sch_with_mock_data()

    await sch.initial_render() 

    sch.initiate_selection(SelectionType.PARTY, 14, 'Roflen')
    print('Selection', str(sch._selection.selection_list))
    
    rpl = TestReactionPayload(':four:', 4, REACTION_ADD)
    sch.handle_reaction(rpl, sph_s[4])
    print('Selection', str(sch._selection.selection_list))

    rpl = TestReactionPayload(':two:', 4, REACTION_ADD)
    sch.handle_reaction(rpl, sph_s[4])
    print('Selection', str(sch._selection.selection_list))

    rpl = TestReactionPayload(':one:', 4, REACTION_ADD)
    sch.handle_reaction(rpl, sph_s[4])
    print('Selection', str(sch._selection.selection_list))

    rpl = TestReactionPayload(':five:', 4, REACTION_ADD)
    sch.handle_reaction(rpl, sph_s[4])
    print('Selection', str(sch._selection.selection_list))

    rpl = TestReactionPayload(':one:', 4, REACTION_REM)
    sch.handle_reaction(rpl, sph_s[4])
    print('Selection', str(sch._selection.selection_list))


    sch.stop_selection()


async def tc2():
    
    sch, sph_s = init_sch_with_mock_data()

    await sch.initial_render() 

    sch.initiate_selection(SelectionType.MERLIN, 14, 'Roflun')
    print('Selection', str(sch._selection.selection_list))
    
    rpl = TestReactionPayload(':four:', 4, REACTION_ADD)
    sch.handle_reaction(rpl, sph_s[4])
    print('Selection', str(sch._selection.selection_list))

    rpl = TestReactionPayload(':two:', 4, REACTION_ADD)
    sch.handle_reaction(rpl, sph_s[4])
    print('Selection', str(sch._selection.selection_list))

    rpl = TestReactionPayload(':one:', 4, REACTION_ADD)
    sch.handle_reaction(rpl, sph_s[4])
    print('Selection', str(sch._selection.selection_list))

    rpl = TestReactionPayload(':five:', 4, REACTION_ADD)
    sch.handle_reaction(rpl, sph_s[4])
    print('Selection', str(sch._selection.selection_list))

    rpl = TestReactionPayload(':one:', 4, REACTION_REM)
    sch.handle_reaction(rpl, sph_s[4])
    print('Selection', str(sch._selection.selection_list))


    sch.stop_selection()

def run_test():
    loop = asyncio.new_event_loop()
    # TODO below tests are not working
    #asyncio.set_event_loop(loop)
    #loop.run_until_complete(tc1())    
    #loop.run_until_complete(tc2())