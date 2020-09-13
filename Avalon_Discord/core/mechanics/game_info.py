import copy

class GameInfo:
    """Contains current game real time info, such as:
    1) List of missions results
    2) Number of failed (in a row) votes

    Returns:
        [type]: [description]
    """

    FAILED_MISSION       = 0
    SUCCEEDED_MISSION    = 1
    NOT_FINISHED_MISSION = 2

    DEFAULT_MAX_FAILED_VOTES_IN_A_ROW = 4
    INITiAL_FAILED_VOTES_NUM = 0
    
    DEFAULT_MISSIONS_TO_WIN = 3
    DEFAULT_MAX_MISSIONS_NUMBER = 5

    _max_game_missions      = None
    _num_of_missions_to_win = None
    _merlin_in_game         = None
    _num_of_failed_votes    = None
    _missions_results_list  = None

    def __init__(self, 
                 merlin_in_game, 
                 max_missions = None,
                 num_of_missions_to_win = None):
        if max_missions == None:
            max_missions = GameInfo.DEFAULT_MAX_MISSIONS_NUMBER 
        
        if num_of_missions_to_win == None:
            num_of_missions_to_win = GameInfo.DEFAULT_MISSIONS_TO_WIN

        self._max_game_missions      = max_missions
        self._num_of_missions_to_win = num_of_missions_to_win
        self._merlin_in_game         = merlin_in_game
        self._num_of_failed_votes    = GameInfo.INITiAL_FAILED_VOTES_NUM
        self._missions_results_list  = list()

    def register_failed_mission(self):
        self._missions_results_list.append(GameInfo.FAILED_MISSION)
        self._num_of_failed_votes    = GameInfo.INITiAL_FAILED_VOTES_NUM

    def register_succeeded_mission(self):
        self._missions_results_list.append(GameInfo.SUCCEEDED_MISSION)
        self._num_of_failed_votes    = GameInfo.INITiAL_FAILED_VOTES_NUM

    def register_failed_vote(self):
        self._num_of_failed_votes += 1

    def maximum_failed_votes_thr_reached(self):
        result = False

        if self._num_of_failed_votes \
              >= \
           GameInfo.DEFAULT_MAX_FAILED_VOTES_IN_A_ROW:
            result = True

        return result

    def red_won_queston(self):
        result = False

        red_missions  = \
            self._missions_results_list.count(GameInfo.FAILED_MISSION)

        if red_missions == GameInfo.DEFAULT_MISSIONS_TO_WIN:
            result = True

        return result

    def blue_won_queston(self):
        result = False
        
        blue_missions = \
            self._missions_results_list.count(GameInfo.SUCCEEDED_MISSION)

        if blue_missions == GameInfo.DEFAULT_MISSIONS_TO_WIN \
              and\
           not self._merlin_in_game:

            result = True

        return result

    def start_merlin_hunt_queston(self):
        result = False
        
        blue_missions = \
            self._missions_results_list.count(GameInfo.SUCCEEDED_MISSION)

        if blue_missions == GameInfo.DEFAULT_MISSIONS_TO_WIN \
              and\
           self._merlin_in_game:

            result = True

        return result
        
    def get_missions_results_list(self):
        result_list = list()

        finished_mission_num = len(self._missions_results_list)
        not_finished_missions = self._max_game_missions - finished_mission_num

        result_list = copy.deepcopy(self._missions_results_list)


        for _ in range(not_finished_missions):
            result_list.append(GameInfo.NOT_FINISHED_MISSION)

        return result_list    

    def get_num_of_failed_votes(self):
        return self._num_of_failed_votes