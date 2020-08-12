import os
import asyncio

from ..vote_content_handler import VoteContentHandler,\
                                   Vote,\
                                   VoteType,\
                                   VoteOptions,\
                                   MessageType

#from content_handlers.vote_content_handler import\
#    VoteContentHandler,\
#    Vote,\
#    VoteType,\
#    VoteOptions,\
#    MessageType

VOTE_PANEL = """
# === Channel ID: {ch_id}============================================
   # === Header message =============================================
         {header}
   # === Emoji message ==============================================
         {emojies}
   # === Reactions message ==========================================
         {reacts}
#====================================================================
"""

class TestReactionPayload:
    emoji      = None
    channel_id = None

    def __init__(self, em, chid):
        self.emoji = em
        self.channel_id = chid

class TestGame:
    player_id_to_txt_ch_handler_dict = None
    player_id_to_emoji_dict          = None
    
    def __init__(self, pid_to_txt_ch_hd_dict, pid_to_emoji):
        self.player_id_to_txt_ch_handler_dict = pid_to_txt_ch_hd_dict
        self.player_id_to_emoji_dict          = pid_to_emoji


class TestChannelHandler:
    vote_panel = None
    id = None

    def __init__(self, vph, id):
        self.vote_panel = vph
        self.id = id


class TestPanelHandler:
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
        print(VOTE_PANEL.format(
            ch_id   = self.channel_id,
            header  = content[MessageType.TEXT_MSG],
            emojies = content[MessageType.EMOJI_MSG].text,
            reacts  = ''))
 
        self._msg_content = content

    def update_and_publish(self, content):
        prev_header = self._msg_content[MessageType.TEXT_MSG]
        prev_emoji  = self._msg_content[MessageType.EMOJI_MSG].text
        prev_reacts = self._msg_content[MessageType.EMOJI_MSG].reactions

        reacts = list()
        
        if    content[MessageType.TEXT_MSG] != None \
          and content[MessageType.TEXT_MSG] != prev_header:
            pass
        
        else:
            content[MessageType.TEXT_MSG] = prev_header

        emoji_content = content[MessageType.EMOJI_MSG]
        if emoji_content != None:
            if emoji_content.text != None and emoji_content.text != prev_emoji:
                pass
            else:
                content[MessageType.EMOJI_MSG].text = prev_emoji
            
            if emoji_content.reactions != None:
                for reaction in emoji_content.reactions:
                    reacts.append(reaction)
            elif prev_reacts != None:
                content[MessageType.EMOJI_MSG].reactions = prev_reacts
                for reaction in prev_reacts:
                    reacts.append(reaction)

         
        print(VOTE_PANEL.format(
            ch_id   = self.channel_id,
            header  = content[MessageType.TEXT_MSG],
            emojies = content[MessageType.EMOJI_MSG].text,
            reacts  = ''.join(reacts)))
            
        self._msg_content = content

    def clear_reactions(self):
        self._msg_content[MessageType.EMOJI_MSG].reactions = None

def init_vch_with_mock_data():

    ch_h_1 = TestChannelHandler(TestPanelHandler('VPH#_1', 1), id = 1)
    ch_h_2 = TestChannelHandler(TestPanelHandler('VPH#_2', 2), id = 2)
    ch_h_3 = TestChannelHandler(TestPanelHandler('VPH#_3', 3), id = 3)
    ch_h_4 = TestChannelHandler(TestPanelHandler('VPH#_4', 4), id = 4)
    ch_h_5 = TestChannelHandler(TestPanelHandler('VPH#_5', 5), id = 5)
    ch_h_6 = TestChannelHandler(TestPanelHandler('VPH#_6', 6), id = 6)
    ch_h_7 = TestChannelHandler(TestPanelHandler('VPH#_7', 7), id = 7)
    ch_h_8 = TestChannelHandler(TestPanelHandler('VPH#_8', 8), id = 8)

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

    vch = VoteContentHandler(t_game, ch_hndlrs, 3)

    return vch

async def tc1():

    vch = init_vch_with_mock_data()

    vpids_to_vote_opts ={
        11 : VoteOptions.YES_AND_NO,
        12 : VoteOptions.YES_AND_NO,
        13 : VoteOptions.YES_AND_NO,
        14 : VoteOptions.YES_AND_NO,
        15 : VoteOptions.YES_AND_NO,
        16 : VoteOptions.YES_AND_NO,
        17 : VoteOptions.YES_AND_NO,
        18 : VoteOptions.YES_AND_NO
    }

    await vch.initial_render()    

    party_emojies = ['⭕', '⛔', '🅰️', 'Ⓜ️']

    vch.initiate_vote(5, 
                      vpids_to_vote_opts, 
                      VoteType.PARTY_APPROVING,
                      party_emojies)

    await asyncio.sleep(0.05)
    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.NO_VOTE, 1))

    await asyncio.sleep(0.05)
    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.YES_VOTE, 2))

    await asyncio.sleep(0.05)
    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.NO_VOTE, 3))

    await asyncio.sleep(0.05)
    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.NO_VOTE, 4))

    await asyncio.sleep(0.05)
    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.NO_VOTE, 5))
    
    await asyncio.sleep(0.05)
    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.YES_VOTE, 6))
    
    await asyncio.sleep(0.05)
    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.NO_VOTE, 7))
    
    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.YES_VOTE, 8))


async def tc2():
    vch = init_vch_with_mock_data()

    await vch.initial_render() 

    vpids_to_vote_opts ={
        17 : VoteOptions.ONLY_YES,
    }

    vch.initiate_vote(3, 
                      vpids_to_vote_opts, 
                      VoteType.PARTY_FORMING,
                      [])


    vch.update_vote_pannels(['⭕'])
    vch.update_vote_pannels(['⭕', '⛔'])
    vch.update_vote_pannels(['⭕', '⛔', '🅰️'])
    vch.update_vote_pannels(['⭕', '⛔', '🅰️', 'Ⓜ️'])

    vch.start_vote()

    vch.update_vote_pannels(['⭕', 'Ⓜ️', '🅰️'])

    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.YES_VOTE, 7))
    
async def tc3():
    vch = init_vch_with_mock_data()

    await vch.initial_render() 

    vpids_to_vote_opts ={
        17 : VoteOptions.ONLY_YES,
        13 : VoteOptions.YES_AND_NO,
        14 : VoteOptions.ONLY_YES,
    }

    vch.initiate_vote(3, 
                      vpids_to_vote_opts, 
                      VoteType.MISSION_RESULT,
                      [],
                      2)


    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.YES_VOTE, 7))
    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.NO_VOTE, 3))
    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.YES_VOTE, 4))
    

async def tc4():
    vch = init_vch_with_mock_data()

    await vch.initial_render() 

    vpids_to_vote_opts ={
        17 : VoteOptions.ONLY_YES,
    }

    vch.initiate_vote(1, 
                      vpids_to_vote_opts, 
                      VoteType.MERLIN_HUNT,
                      [])

    vch.update_vote_pannels(['⭕'])
    vch.update_vote_pannels(['⛔'])
    vch.update_vote_pannels(['🅰️'])
    vch.update_vote_pannels(['Ⓜ️'])

    await vch.handle_reaction(TestReactionPayload(VoteContentHandler.YES_VOTE, 7))


def run_test():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(tc1())
    loop.run_until_complete(tc2())
    loop.run_until_complete(tc3())
    loop.run_until_complete(tc4())
    