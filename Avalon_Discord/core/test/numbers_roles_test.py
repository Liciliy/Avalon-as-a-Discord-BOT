from ..mechanics import NumbersAndRolesHandler

class TestGame:
    players_ids_list = None

    def __init__(self, pids):
        self.players_ids_list = pids

def tc1():
    game = TestGame([1,2,3,4,5,6,7])

    NumbersAndRolesHandler(game)
    


def run_test():
    tc1()