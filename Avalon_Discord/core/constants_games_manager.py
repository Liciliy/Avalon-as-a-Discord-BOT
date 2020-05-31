import discord
# Створює екземпляр класу гри. Ініціює можливість приєднання до гри.
# Створює приватний чат для паті лідера. 
# В приватному чаті гра надає лідеру можливість обрати персонажів гри,
# залочити гру, розпочати гру і закінчити гру.
GAME_INITIATE_CMD = 'go'
GAME_JOIN_CMD     = 'join'

# Забороняє нові приєднання до гри. Може бути розлочена.
GAME_LOCK_CMD     = 'lock'

# Створює внутрішні дані (розподіл ролей, порядок ходу і т.д.),
# створює приватні канали для усіх гравців, які ініціювали приєднання до гри,
# і запускає першу пригоду.
GAME_START_CMD    = 'start'

# Має зупиняти усі тамери (і м'ютати гравців?)
GAME_PAUSE_CMD    = '$pause_ava'

# Видаляє усі приватні чати, видаляє внутрішню інфу.
# Надсилає результати гри в приват кожному гравцю (?)
GAME_END_CMD      = '$end_ava'

# Refresh command should be used when:
#   A) Приватний чат з гравцем видалений
#   Б) Одне з ігрових повідомлень видалене.
# Якщо команда використовується паті лідеров - гра має перестворити 
# приватні канали усіх гравців і повідомоення бота.
# Якщо використовується рядовим гравцем - тіж дії застосовуються до
# цього гравця і паті лідера.  
GAME_REFRESH_CMD  = '$refresh_ava'

# Виводить довідкову інформацію по командах
HELP_CMD          = '$help_ava'

# TODO Add restart timer CMD - restarts timer xd. 
# Useful when somebady could not talk when the tiemr started.
# Should be used only by game master?

# TODO Add clear-gamechannel_from-bot-messages command.
# Can be used when bot spamed a lot of game unrelated stuff (help, errors etc)

# TODO Add un-join game command. Can be used before game is locked and after 
# the user joined a game.

# TODO Make delete-me-from-all-games commands. 
# This command should remove user mention from all game data sets.

# TODO IF un-lock command will be ever added - consider case when 
# another game is created after this game was locked.  
# In such case unlock may lead to two initiated games exist in a guild.


AVALON_COMMANDS = [
    GAME_INITIATE_CMD,
    GAME_JOIN_CMD,
    GAME_LOCK_CMD,
    GAME_START_CMD,
    GAME_PAUSE_CMD,
    GAME_END_CMD,
    GAME_REFRESH_CMD,
    HELP_CMD
]

GUILD_TXT_CHANNEL_TYPE = discord.ChannelType.text

DM_TXT_CHANNEL_TYPE    = discord.ChannelType.private

CHANNEL_TYPE_TO_ALLOVED_COMMANDS = {
   GUILD_TXT_CHANNEL_TYPE : [GAME_INITIATE_CMD,
                             GAME_JOIN_CMD,
                             GAME_LOCK_CMD,
                             GAME_START_CMD,
                             GAME_PAUSE_CMD,
                             GAME_END_CMD,
                             GAME_REFRESH_CMD,
                             HELP_CMD],
   DM_TXT_CHANNEL_TYPE    : [HELP_CMD]
}

GAME_CHANNEL_ALLOWED_CMDS = [
    GAME_LOCK_CMD,
    GAME_START_CMD,
    GAME_PAUSE_CMD,
    GAME_END_CMD,
    GAME_REFRESH_CMD,
    HELP_CMD
]

BASE_GAME_LOCAL_ID_VAL = 0