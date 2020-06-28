import asyncio

from .abstract_phase import\
    MissionType,\
    AbstractPhase,\
    PhaseType,\
    TalkType

from .constants_phases import\
    ONE_PLAYER_TALK_TIME_S,\
    PREPARATION_TIME_S

from ..constants_game import NUM_OF_PLAYERS_TO_GAME_STATS

class TalkPreparationPhase(AbstractPhase):
    _time_left_seconds = None
    _sub_phase         = None
    _talkers           = None
    _talk_type         = None

    def __init__(self, mission_type, leader, game, talking_players):
        super().__init__(mission_type, leader, game)
        self._phase_type = PhaseType.TALK_PREPARATION
        self._talkers = talking_players

        talkers_num = len(talking_players)

        if talkers_num == 1:
            self._talk_type = TalkType.ONE_PLAYER_SPEACH

        elif talkers_num == game.number_of_players:
            self._talk_type = TalkType.ALL_TALK

        else:
            self._talk_type = TalkType.RED_PLAYERS_TALK

        self._time_left_seconds = PREPARATION_TIME_S

    async def start(self): 
        await asyncio.sleep(self._time_left_seconds)

    




        
