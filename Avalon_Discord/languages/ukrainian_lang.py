from core.constants_games_manager import\
    HELP_CMD,\
    GAME_JOIN_CMD,\
    GAME_INITIATE_CMD
    
from core.constants_game import MAX_PLAYERS, MIN_PLAYERS

ERR_MSG_WRONG_CMD_CHANNEL_COMB_TITTLE =\
'Не в цьому чаті!'

ERR_MSG_WRONG_CMD_CHANNEL_COMB_TEXT =\
'Ця команда не може бути виконано у цьому каналі.\n\
Щоб роздрукувати інструкцію використання Авалон бота,\
 будь ласка, використайте команду ' + HELP_CMD


ERR_MSG_GAME_ALREADY_INITIATED_HERE_TITLE =\
'Набір гравців вже розпочато!'

ERR_MSG_GAME_ALREADY_INITIATED_HERE_TEXT =\
'На цьому сервері вже розпочатий набір гравців до гри!\n\
Щоб приєднатися до гри використайте команду ' + GAME_JOIN_CMD

ERR_MSG_GAME_NOT_INITIATED_HERE_TITLE =\
'Немає куди приєднуватися :( !'

ERR_MSG_GAME_NOT_INITIATED_HERE_TEXT =\
'На цьому сервері немає набору на гру!\n\
Щоб створити гру використайте команду ' + GAME_INITIATE_CMD

ERR_MSG_USER_ALREADY_IN_A_GAME_TITLE =\
'Ви вже берете участь у грі!'

ERR_MSG_USER_ALREADY_IN_A_GAME_TEXT =\
'Ви вже берете участь у одній з ігор.\n\
Одночасна участь одного гравця в декількох\
 іграх не підтримується.'


INFO_MSG_GAME_INITIATED_TITLE =\
'Набір у гру розпочато!'

INFO_MSG_GAME_INITIATED_TEXT =\
'Щоб доєднатись до гри використайте команду ' + GAME_JOIN_CMD

INFO_MSG_PARTY_LEADER_FIELD_NAME =\
'\nМайстер гри: '

INFO_MSG_OTHER_PALYERS_FIELD_NAME =\
'\nГравці, що доєдналися: '

INFO_MSG_FOOTER =\
('Мінімум гравців : ' 
+ str(MIN_PLAYERS) 
+ '. Максимум гравців:'
+ str(MAX_PLAYERS)
+ '. Набрано гравців: {number}')