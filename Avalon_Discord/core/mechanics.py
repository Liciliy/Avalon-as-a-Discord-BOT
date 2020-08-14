import random

import languages.ukrainian_lang as lang

class Team:
    RED  = 0
    BLUE = 1

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


class AbstractRole:
    _game = None
    
    # List of roles that this role knows
    sees          = None
    
    # Role string name.
    real_name     = None

    # Role string name to show for Red players (if needed)
    name_for_red  = None

    # Role string name to show for Blue players (if needed)
    name_for_blue = None

    # Role string name for Merlin
    name_for_merlin = None

    name_for_persival = None

    name_for_persival_no_oponent = None

    team          = None

    def __init__(self, 
                 game):
        self._game = game

    def get_info_for_this_player(self):
        pass

    def get_info_string_for_other_player(self, pid):
        pass

    def knows_player_role(self, role):
        pass


class BluePlayer(AbstractRole):
    team = Team.BLUE
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name     = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_blue = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red  = lang.SIMPLE_BLUE_ROLE_NAME

        self.sees = []

        #self.team = Team.BLUE


class RedPlayer(AbstractRole):
    team = Team.RED
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name       = lang.SIMPLE_RED_ROLE_NAME
        self.name_for_blue   = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red    = lang.SIMPLE_RED_ROLE_NAME
        self.name_for_merlin = lang.SIMPLE_RED_ROLE_NAME

        self.sees = []

        #self.team = Team.RED


class Merlin(AbstractRole):
    team = Team.BLUE
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name         = lang.MERLIN_ROLE_NAME
        self.name_for_persival = lang.MORGANA_OR_MERLIN_ROLE_NAME
        self.name_for_red      = lang.SIMPLE_BLUE_ROLE_NAME

        self.name_for_persival_no_oponent = lang.MERLIN_ROLE_NAME

        self.sees = [Morgana, Assassin, Oberon, RedPlayer]

        #self.team = Team.BLUE


class Morgana(AbstractRole):
    team = Team.RED
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name         = lang.MORGANA_ROLE_NAME
        self.name_for_persival = lang.MORGANA_OR_MERLIN_ROLE_NAME
        self.name_for_red      = lang.MORGANA_ROLE_NAME
        self.name_for_merlin   = lang.SIMPLE_RED_ROLE_NAME

        self.name_for_persival_no_oponent = lang.MORGANA_ROLE_NAME

        self.sees = [Assassin, Mordred, RedPlayer]

        #self.team = Team.RED


class Persival(AbstractRole):    
    team = Team.BLUE
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name     = lang.PERSIVAL_ROLE_NAME
        self.name_for_blue = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red  = lang.SIMPLE_BLUE_ROLE_NAME

        self.sees = [Morgana, Merlin]

        #self.team = Team.BLUE


class Mordred(AbstractRole):
    team = Team.RED
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name     = lang.MORDRED_ROLE_NAME
        self.name_for_blue = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red  = lang.MORDRED_ROLE_NAME

        self.sees = [Assassin, Morgana, RedPlayer]

        #self.team = Team.RED


class Oberon(AbstractRole):
    team = Team.RED
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name     = lang.OBERON_ROLE_NAME
        self.name_for_blue = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red  = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_merlin = lang.SIMPLE_RED_ROLE_NAME

        self.sees = []

        #self.team = Team.RED


class Assassin(AbstractRole):
    team = Team.RED
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name     = lang.ASSASSIN_ROLE_NAME
        self.name_for_blue = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red  = lang.ASSASSIN_ROLE_NAME
        self.name_for_merlin = lang.SIMPLE_RED_ROLE_NAME

        self.sees = [Mordred, Morgana, RedPlayer]

        #self.team = Team.RED


class NumbersAndRolesHandler:
    _game         = None
    _game_stats   = None
    pids_to_roles = None

    def __init__(self, game, game_roles = [Merlin, Morgana, Mordred, Persival]):
        # TODO Initialyze game_roles here.
        
        pid_to_role = dict()

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
        #print (game_roles)
        # ==== Here roles classes are destributed between players =========== # 

        print(roles)
        print(pids)

        print('==============')

        random.shuffle(roles)
        random.shuffle(pids)

        print(roles)
        print(pids)
        # =================================================================== #


        
            


    def distribute_roles(self):
        # TODO distribute roles here. 
        pass

    def has_merlin(self):
        # TODO use this method to let the game understand if merlin hunt needed.
        pass

    def get_merlin_hunter_pid(self):
        # NOTE should return either Morgana or assassin.
        pass

    def get_number_of_player_for_mission(self, mission_number):
        return self.\
            _game_stats.get_number_of_player_for_mission(mission_number)

    def get_number_of_fails_to_fail_mission(self, mission_number):
        return self.\
            _game_stats.get_number_of_fails_to_fail_mission(mission_number)