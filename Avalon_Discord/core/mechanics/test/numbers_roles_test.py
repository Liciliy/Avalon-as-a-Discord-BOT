from ..mechanics import NumbersAndRolesHandler

class TestGame:
    players_ids_list = None
    player_id_to_role_dict = None
    player_id_to_emoji_dict = None
    player_id_to_name_dict = None

    def __init__(self, 
                 pids,
                 player_id_to_emoji_dict = None,
                 player_id_to_name_dict  = None):
        self.player_id_to_emoji_dict = player_id_to_emoji_dict
        self.player_id_to_name_dict  = player_id_to_name_dict
        self.players_ids_list = pids

class TestEmoji:
    id   = None
    name = None
    
    def __init__(self, id, name):
        self.id = id
        self.name = name


def tc1():
    game = TestGame([1,2,3,4,5,6,7])

    NumbersAndRolesHandler(game)
    
def tc2():
    pid_to_emoji = {
        1  : TestEmoji(11,  'p1'),
        2  : TestEmoji(12,  'p2'),
        3  : TestEmoji(13,  'p3'),
        4  : TestEmoji(14,  'p4'),
        5  : TestEmoji(15,  'p5'),
        6  : TestEmoji(16,  'p6'),
        7  : TestEmoji(17,  'p7'),
        8  : TestEmoji(18,  'p8'),
        9  : TestEmoji(19,  'p9'),
        10 : TestEmoji(110, 'p10'),
    }

    pid_to_pname = {
        1  : 'player #1',
        2  : 'player #2',
        3  : 'player #3',
        4  : 'player #4',
        5  : 'player #5',
        6  : 'player #6',
        7  : 'player #7',
        8  : 'player #8',
        9  : 'player #9',
        10 : 'player #10',
    }


    game = TestGame([1,2,3,4,5,6,7,8,9,10],
                    player_id_to_emoji_dict = pid_to_emoji,
                    player_id_to_name_dict  = pid_to_pname)

    nr_handler = NumbersAndRolesHandler(game)

    game.player_id_to_role_dict = nr_handler.player_ids_to_roles

    # === Test start =============== #

    for pid, role in game.player_id_to_role_dict.items():
        print (f'# === Player #{str(pid)} secret info ===================== #' )
        print(role.get_secret_info(pid))
        print ( '# ======================================================== #' )

def run_test():
    tc1()
    tc2()