import random

from .roles import Team, \
                   BluePlayer, \
                   RedPlayer, \
                   Mordred, \
                   Merlin, \
                   Morgana, \
                   Assassin, \
                   Oberon, \
                   Persival

class GameStats:
    _blue_p = None
    _red_p  = None

    _mission_to_num_of_players = None
    _mission_to_num_of_fails   = None

    def __init__(self, 
                 blue, 
                 red, 
                 q1p, q1f,
                 q2p, q2f,
                 q3p, q3f,
                 q4p, q4f,
                 q5p, q5f):
 
        self._mission_to_num_of_players = {
            1 : q1p,
            2 : q2p,
            3 : q3p,
            4 : q4p,
            5 : q5p
        }

        self._mission_to_num_of_fails   = {
            1 : q1f,
            2 : q2f,
            3 : q3f,
            4 : q4f,
            5 : q5f
        }

        self._blue_p = blue
        self._red_p  = red

    def get_number_of_player_for_mission(self, mission_number):
        return self._mission_to_num_of_players[mission_number]

    def get_number_of_fails_to_fail_mission(self, mission_number):
        return self._mission_to_num_of_fails[mission_number]

    def number_of_blue_players(self):
        return self._blue_p

    def number_of_red_players(self):
        return self._red_p

    
NUM_OF_PLAYERS_TO_GAME_STATS = {
    #              B  R     Q1 F   Q2 F   Q3 F   Q4 F   Q5 F 
    5  : GameStats(3, 2,    2, 1,  3, 1,  2, 1,  3, 1,  3, 1),
    6  : GameStats(4, 2,    2, 1,  3, 1,  4, 1,  3, 1,  4, 1),
    7  : GameStats(4, 3,    2, 1,  3, 1,  3, 1,  4, 2,  4, 1),
    8  : GameStats(5, 3,    3, 1,  4, 1,  4, 1,  5, 2,  5, 1),
    9  : GameStats(6, 3,    3, 1,  4, 1,  4, 1,  5, 2,  5, 1),
    10 : GameStats(6, 4,    3, 1,  4, 1,  4, 1,  5, 2,  5, 1)
}


class NumbersAndRolesHandler:
    _game         = None
    _game_stats   = None
    _pids_to_roles = None

    def __init__(self, game, game_roles = [Merlin, Morgana, Mordred, Persival]):
        # TODO Initialyze game_roles here.
        
        roles = list()
        
        self._game = game
 
        pids = game.players_ids_list
        number_of_players = len(pids)
        
        # ==== Here it is decided what role classes to use and those classes 
        # are instantiated. ==================================================#
        self._game_stats = NUM_OF_PLAYERS_TO_GAME_STATS[number_of_players]
 
        red_roles_needed  = self._game_stats.number_of_red_players()
        blue_roles_needed = self._game_stats.number_of_blue_players()
        
        for role in game_roles:
            if role.team == Team.BLUE:
                blue_roles_needed -= 1
            if role.team == Team.RED:
                red_roles_needed -= 1
        
        simple_blue_roles = list()
        simple_red_roles  = list()

        for _ in range(0, blue_roles_needed):
            simple_blue_roles.append(BluePlayer)

        for _ in range(0, red_roles_needed):
            simple_red_roles.append(RedPlayer)
   
        game_roles.extend(simple_blue_roles)
        game_roles.extend(simple_red_roles)


        for role_class in game_roles:
            roles.append(role_class(self._game))
        # =================================================================== #

        # ==== Here roles classes are destributed between players =========== # 
        random.shuffle(roles)
        random.shuffle(pids)
        
        self._pids_to_roles = dict()

        for id in range(0, len(pids)):
            self._pids_to_roles[pids[id]] = roles[id]
        # =================================================================== #

    def has_merlin(self):
        result = False

        for role in self._pids_to_roles.values():
            if role == Merlin:
                result = True
                break

        return result

    def get_merlin_hunter_pid(self):
        result = None
        
        assasin_pid     = None
        morgana_pid     = None
        red_players_pid = list()

        # This loop checks if there is assasin and morgana. 
        # Also gets other red players IDs
        for pid, role in self._pids_to_roles.values():
            
            if   role == Assassin:
                assasin_pid = pid
                break

            elif role == Morgana:
                morgana_pid = pid 

            elif role.team == Team.RED:
                red_players_pid.append(pid)

        # Here, choose who will hunt the Merlin.
        if   assasin_pid != None:
            result = assasin_pid

        elif morgana_pid != None:
            result = morgana_pid

        else:
            result = random.choice(red_players_pid)

        return result

    def get_number_of_player_for_mission(self, mission_number):
        return self.\
            _game_stats.get_number_of_player_for_mission(mission_number)

    def get_number_of_fails_to_fail_mission(self, mission_number):
        return self.\
            _game_stats.get_number_of_fails_to_fail_mission(mission_number)
    
    @property
    def player_ids_to_roles(self):
        return self._pids_to_roles
