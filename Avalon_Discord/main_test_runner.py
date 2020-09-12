from core.content_handlers.test.selection_test \
    import run_test as selection_test

from core.content_handlers.test.vote_test \
    import run_test as vote_test

from core.mechanics.test.numbers_roles_test \
    import run_test as roles_test

from core.mechanics.test.game_info_test \
    import run_test as game_info_test


if __name__ == "__main__":
    vote_test()
    selection_test()
    roles_test()
    game_info_test()