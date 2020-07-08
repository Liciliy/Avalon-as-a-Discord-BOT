import discord
import logging
import languages.ukrainian_lang as lang

from .messages_dispatching.task import Task, MsgActType, ContentType


empty_embed = discord.embeds.EmptyEmbed

MESASGE_DISPATCHER = None

def set_messages_dispatcher(dispatcher):
    global MESASGE_DISPATCHER
    MESASGE_DISPATCHER = dispatcher


class EmbedField():
    name   = None
    val    = None
    inline = None

    def __init__(self, name, val, inline):
        self.name   = name 
        self.val    = val 
        self.inline = inline 

def form_embed(title     = empty_embed, 
               descr     = empty_embed, 
               colour    = empty_embed,
               footer    = None,
               image_url = None,
               thumbnail = None,
               author    = None,
               fields    = list()):

    embed = discord.Embed(
            title = title,
            description = descr,
            colour = colour
        )
    if footer    : embed.set_footer(text = footer)
    if image_url : embed.set_image(url = image_url)
    if thumbnail : embed.set_thumbnail(url = thumbnail)
    if author    : embed.set_author(name = author)

    for field in fields:
        embed.add_field(name = field.name,
                        value = field.val, 
                        inline = field.inline)
    return embed

class ErrorToDisplay:
    title  = None
    text   = None
    footer = None

    def __init__(self, title, text, footer = None):
        self.title  = title
        self.text   = text
        self.footer = footer

    @staticmethod
    def wrong_cmd_to_channel_type_combination():
        return ErrorToDisplay(
            lang.ERR_MSG_WRONG_CMD_CHANNEL_COMB_TITTLE,
            lang.ERR_MSG_WRONG_CMD_CHANNEL_COMB_TEXT)
    
    @staticmethod
    def game_already_initated_here():
        return ErrorToDisplay(
            lang.ERR_MSG_GAME_ALREADY_INITIATED_HERE_TITLE,
            lang.ERR_MSG_GAME_ALREADY_INITIATED_HERE_TEXT)
    
    @staticmethod
    def game_not_initated_here():
        return ErrorToDisplay(
            lang.ERR_MSG_GAME_NOT_INITIATED_HERE_TITLE,
            lang.ERR_MSG_GAME_NOT_INITIATED_HERE_TEXT)
    
    @staticmethod
    def player_already_in_a_game():
        return ErrorToDisplay(
            lang.ERR_MSG_USER_ALREADY_IN_A_GAME_TITLE,
            lang.ERR_MSG_USER_ALREADY_IN_A_GAME_TEXT)

    @staticmethod
    def too_few_players_to_lock(current_number = None):
        return ErrorToDisplay(
            lang.ERR_MSG_TOO_FEW_PLAYERS_TITLE,
            lang.ERR_MSG_TOO_FEW_PLAYERS_TEXT,
            footer = lang.INFO_MSG_FOOTER.format(number = current_number)\
                        if current_number else None)

    @staticmethod
    def too_much_players_to_join():
        return ErrorToDisplay(
            lang.ERR_MSG_TOO_MUCH_PLAYERS_TITLE,
            lang.ERR_MSG_TOO_MUCH_PLAYERS_TEXT)

    @staticmethod
    def no_game_to_lock_here():
        return ErrorToDisplay(
            lang.ERR_MSG_NO_GAME_TO_LOCK_TITLE,
            lang.ERR_MSG_NO_GAME_TO_LOCK_TEXT)
    
    @staticmethod
    def only_master_can_lock():
        return ErrorToDisplay(
            lang.ERR_MSG_ONLY_MASTER_LOCKS_TITLE,
            lang.ERR_MSG_ONLY_MASTER_LOCKS_TEXT)

    @staticmethod
    def can_start_only_in_game_channel():
        return ErrorToDisplay(
            lang.ERR_MSG_START_ONLY_IN_GAME_CH_TITLE,
            lang.ERR_MSG_START_ONLY_IN_GAME_CH_TEXT)
    
    @staticmethod
    def only_master_can_start():
        return ErrorToDisplay(
            lang.ERR_MSG_ONLY_MASTER_STARTS_TITLE,
            lang.ERR_MSG_ONLY_MASTER_STARTS_TEXT)

    @staticmethod
    def not_in_game(username):
        return ErrorToDisplay(
            lang.ERR_MSG_NOT_IN_GAME_TITLE,
            lang.ERR_MSG_NOT_IN_GAME_TEXT.format(user_name = username))

    @staticmethod
    def not_in_locked_game(username):
        return ErrorToDisplay(
            lang.ERR_MSG_NOT_IN_LOCKED_GAME_TITLE,
            lang.ERR_MSG_NOT_IN_LOCKED_GAME_TEXT.format(user_name = username))

    @staticmethod
    def not_all_connected():
        return ErrorToDisplay(
            lang.ERR_MSG_NOT_ALL_CONNECTED_TITLE,
            lang.ERR_MSG_NOT_ALL_CONNECTED_TEXT)

    @staticmethod
    def not_all_connected_voice():
        return ErrorToDisplay(
            lang.ERR_MSG_NOT_ALL_CONNECTED_VOICE_TITLE,
            lang.ERR_MSG_NOT_ALL_CONNECTED_VOICE_TEXT)

    @staticmethod
    async def respond_with_error(msg_to_respond, error_obj):
        logging.info('Responding with ERROR: ' + str(error_obj.title))  
        embed = form_embed(colour = discord.Colour.red(),
                           descr  = error_obj.text,
                           title  = error_obj.title,
                           footer = error_obj.footer)

        task = Task(MsgActType.SEND, 
                    content_type = ContentType.EMBED,
                    content = embed, 
                    channel_id = msg_to_respond.channel.id)
                    
        MESASGE_DISPATCHER.order_task_to_execute(task)

        #await msg_to_respond.channel.send(embed = embed)


class InfoToDisplay:
    text   = None
    title  = None
    fields = None
    footer = None

    def __init__(self, 
                 title, 
                 text, 
                 fields = None, 
                 footer = None):
        self.title  = title
        self.text   = text
        self.fields = fields
        self.footer = footer

    @staticmethod
    async def respond_with_info(channel, info_obj):
        global MESASGE_DISPATCHER
        logging.info('Responding with INFO: ' + str(info_obj.title))   
        embed = form_embed(colour = discord.Colour.green(),
                           descr  = info_obj.text,
                           title  = info_obj.title,
                           fields = info_obj.fields,
                           footer = info_obj.footer)

        task = Task(MsgActType.SEND, 
                    content_type = ContentType.EMBED,
                    content = embed, 
                    channel_id = channel.id)
                    
        MESASGE_DISPATCHER.order_task_to_execute(task)
        
        #await channel.send(embed = embed)