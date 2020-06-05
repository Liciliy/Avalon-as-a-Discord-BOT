from core.constants_games_manager import\
    HELP_CMD,\
    GAME_JOIN_CMD,\
    GAME_INITIATE_CMD,\
    GAME_START_CMD,\
    GAME_LOCK_CMD
    
from core.constants_game import MAX_PLAYERS, MIN_PLAYERS

ERR_MSG_WRONG_CMD_CHANNEL_COMB_TITTLE =\
'Не в цьому чаті!'

ERR_MSG_WRONG_CMD_CHANNEL_COMB_TEXT =\
'Ця команда не може бути виконано у цьому каналі.\n\
Щоб роздрукувати інструкцію використання Авалон бота,\
 будь ласка, використайте команду `' + HELP_CMD  + '`'

ERR_MSG_GAME_ALREADY_INITIATED_HERE_TITLE =\
'Набір гравців вже розпочато!'

ERR_MSG_GAME_ALREADY_INITIATED_HERE_TEXT =\
'На цьому сервері вже розпочатий набір гравців до гри!\n\
Щоб приєднатися до гри використайте команду `' + GAME_JOIN_CMD  + '`'

ERR_MSG_GAME_NOT_INITIATED_HERE_TITLE =\
'Немає куди приєднуватися :( !'

ERR_MSG_GAME_NOT_INITIATED_HERE_TEXT =\
'На цьому сервері немає набору на гру!\n\
Щоб створити гру використайте команду `' + GAME_INITIATE_CMD  + '`'

ERR_MSG_NO_GAME_TO_LOCK_TITLE =\
'На цьому сервері немає гри :( !'

ERR_MSG_NO_GAME_TO_LOCK_TEXT =\
'На цьому сервері немає розпочатої гри!\n\
Щоб створити гру використайте команду `' + GAME_INITIATE_CMD  + '`'

ERR_MSG_ONLY_MASTER_LOCKS_TITLE =\
'Тільки майстер!'

ERR_MSG_ONLY_MASTER_LOCKS_TEXT =\
'Лише майстер гри може її заблокувати!'

ERR_MSG_USER_ALREADY_IN_A_GAME_TITLE =\
'Ви вже берете участь у грі!'

ERR_MSG_USER_ALREADY_IN_A_GAME_TEXT =\
'Ви вже берете участь у одній з ігор.\n\
Одночасна участь одного гравця в декількох\
 іграх не підтримується.'

ERR_MSG_TOO_FEW_PLAYERS_TITLE =\
'Замало гравців!'

ERR_MSG_TOO_FEW_PLAYERS_TEXT =\
'Занадто мало гравців доєдналося до гри :( .\n\
Набір у гру не може бути зупинений,\
 допоки не набереться мінімальна кількість гравців: ' +\
str(MIN_PLAYERS)

ERR_MSG_TOO_MUCH_PLAYERS_TITLE =\
'Гра вже заповнена!'

ERR_MSG_TOO_MUCH_PLAYERS_TEXT =\
'До гри доєдналася максимальна кількість гравців.\n\
На жаль, максимальна кількість гравців рівна '\
+ str(MAX_PLAYERS)


ERR_MSG_ONLY_MASTER_STARTS_TITLE =\
'Тільки майстер!'

ERR_MSG_ONLY_MASTER_STARTS_TEXT =\
'Лише майстер гри може її розпочати!'


ERR_MSG_START_ONLY_IN_GAME_CH_TITLE =\
'Тільки в ігровому каналі!'

ERR_MSG_START_ONLY_IN_GAME_CH_TEXT =\
'Гру можна розпочати лише в ігровому каналі!\n\
Ви мали б отримати запрошення в канал у особисті повідомлення!'


ERR_MSG_NOT_IN_GAME_TITLE =\
'Не у грі :( !'

ERR_MSG_NOT_IN_GAME_TEXT =\
'{user_name}, ви не знаходитесь у жодній грі :( ,\
 тож не можете запустити заблоковану гру...\n\
Щоб отримати більше інформації, використайте команду `' + HELP_CMD  + '`'


ERR_MSG_NOT_IN_LOCKED_GAME_TITLE =\
'Не у заблокованій грі :( !'

ERR_MSG_NOT_IN_LOCKED_GAME_TEXT =\
'{user_name}, гра, у якій ви знаходитеся, не заблокована :( ,\
 тож не можете запустити цю гру...\n\
Щоб отримати більше інформації, використайте команду `' + HELP_CMD  + '`'


ERR_MSG_NOT_ALL_CONNECTED_TITLE =\
'Не всі приєдналися :( !'

ERR_MSG_NOT_ALL_CONNECTED_TEXT =\
'Не всі гравці доєдналися до сервера гри. \n\
А тут - не кидають нікого :) .\n\
Запрошення до сервера (і до гри) надійшли гравцям в особисті повідомлення.'


INFO_MSG_CONNECTNESS_STATUS_TITLE =\
'Гравці що не приєднались'

INFO_MSG_CONNECTNESS_STATUS_TEXT =\
'Ось ті, на кого всі чекають:'

INFO_MSG_NOT_IN_GUILD_FIELD_NAME =\
'\nГравці, що не доєдналися до сервера: '

INFO_MSG_NOT_IN_VOICE_FIELD_NAME =\
'\nГравці, на що не увійшли у голосовий канал: '

INFO_MSG_GAME_INITIATED_TITLE =\
'Набір у гру розпочато!'

INFO_MSG_GAME_INITIATED_TEXT =\
'Щоб доєднатись до гри використайте команду `' + GAME_JOIN_CMD  + '`'

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


INFO_MSG_GAME_LOCKED_TITLE =\
'Набір у гру закрито!'

INFO_MSG_GAME_LOCKED_TEXT =\
'Набір у гру закрито Майстром гри!\n\
Тепер Майстер може розпочати гру командою `' + GAME_START_CMD  + '`\n\
Але, тільки у ігровому каналі!\n\
Запрошення до каналу майстер (і інші :) ) може знайти в особистих повідомленнях :) '

GAME_MSG_WAITING_ALL =\
'Гра почнеться не за баром. Чекаємо поки доєднаються усі гравці...'

GAME_MSG_STARTING =\
'Ми проминули бар! Ура!\
 Лишилося тільки щоб усі доєдналися до голосового чату!!!'