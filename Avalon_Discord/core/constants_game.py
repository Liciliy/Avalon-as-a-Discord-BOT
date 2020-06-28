GAME_INITIATED_STATE = 0
GAME_LOCKED_STATE    = 1
GAME_STARTED_STATE   = 2
GAME_PAUSED_STATE    = 3
GAME_ENDED_STATE     = 4

MAX_PLAYERS          =  16
MIN_PLAYERS          =  1 

ROLE_CREATION_REASON = 'This role is used by avalon bot and should \
be automatically removed after the game.'

ROLE_NAME_SUFFIX     = '_avalon_player'

class GameStats:
    blue_p = None
    red_p  = None

    q1_players_num  = None
    q1_fails_needed = None
    
    q2_players_num  = None
    q2_fails_needed = None
    
    q3_players_num  = None
    q3_fails_needed = None
    
    q4_players_num  = None
    q4_fails_needed = None
    
    q5_players_num  = None
    q5_fails_needed = None

    def __init__(self, 
                 blue, 
                 red, 
                 q1p, q1f,
                 q2p, q2f,
                 q3p, q3f,
                 q4p, q4f,
                 q5p, q5f):

        self.blue_p = blue
        self.red_p  = red
    
        self.q1_players_num  = q1p
        self.q1_fails_needed = q1f
    
        self.q2_players_num  = q2p
        self.q2_fails_needed = q2f
    
        self.q3_players_num  = q3p
        self.q3_fails_needed = q3f
    
        self.q4_players_num  = q4p
        self.q4_fails_needed = q4f
    
        self.q5_players_num  = q5p
        self.q5_fails_needed = q5f

    
NUM_OF_PLAYERS_TO_GAME_STATS = {
    #              B  R     Q1 F   Q2 F   Q3 F   Q4 F   Q5 F 
    5  : GameStats(3, 2,    2, 1,  3, 1,  2, 1,  3, 1,  3, 1),
    6  : GameStats(4, 2,    2, 1,  3, 1,  4, 1,  3, 1,  4, 1),
    7  : GameStats(4, 3,    2, 1,  3, 1,  3, 1,  4, 2,  4, 1),
    8  : GameStats(5, 3,    3, 1,  4, 1,  4, 1,  5, 2,  5, 1),
    9  : GameStats(6, 3,    3, 1,  4, 1,  4, 1,  5, 2,  5, 1),
    10 : GameStats(6, 4,    3, 1,  4, 1,  4, 1,  5, 2,  5, 1)
}