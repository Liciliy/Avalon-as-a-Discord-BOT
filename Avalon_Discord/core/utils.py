import discord
import languages.ukrainian_lang as lang


empty_embed = discord.embeds.EmptyEmbed

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
    title = None
    text = None

    def __init__(self, title, text):
        self.title = title
        self.text = text

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
        