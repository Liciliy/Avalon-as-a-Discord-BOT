import logging

class VoteType:
    PARTY_FORMING   = 0
    PARTY_APPROVING = 1
    MISSION_RESULT  = 2
    MERLIN_HUNT     = 3

class VoteContentHandler:

    def __init__(self, game):
        self._game = game

    def start_vote(self, players_to_select_num, selecting_palyer_id):
        pass    

    def _party_forming_vote_panels_update(self):
        pass

    def _party_approval_vote_panels_update(self):
        pass

    def _merlin_hunt_vote_panels_update(self):
        pass

    def update_vote_pannels(self):
        pass

    def player_voted(self):
        # TODO here react on a player vote - update his vote panel
        # with results (only party approve vote)or other stuff
        pass

    def vote_is_done(self):
        # TODO here notify game phase about vote results.
        pass

    @property
    def player_id_to_emoji(self):
        return self._game.player_id_to_emoji_dict