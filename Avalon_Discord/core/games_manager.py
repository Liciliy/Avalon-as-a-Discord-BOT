import discord
import logging
import asyncio

import core.constants_games_manager as const
import languages.ukrainian_lang as lang

from core.utils import form_embed, EmbedField, ErrorToDisplay

class GameManager:

    __active_games_list = list()

    @staticmethod
    def __is_supported_cmd(msg):
        result = False
        if msg.content in const.AVALON_COMMANDS: result = True
        return result
    
    @staticmethod
    def __cmd_used_in_correct_channel(msg):
        result = True
        cntnt = msg.content
        channel_id = msg.channel.id

        if cntnt in const.CHANNEL_TYPE_TO_ALLOVED_COMMANDS[msg.channel.type]:
            channel_type = msg.channel.type

            if channel_type == const.GUILD_TXT_CHANNEL_TYPE\
              and cntnt not in const.GAME_CHANNEL_ALLOWED_CMDS:
                
                # If is a guild channel - and command is not allowed in 
                # game created channels - check if user didnt use inappropriate
                # command in game created chat.
                for game in GameManager.__active_games_list:
                    
                    for game_chnl_id in game.private_txt_channels_list:
                        if channel_id == game_chnl_id:
                            result = False
                            break
                    
                    if result == False: break                           

        else: result = False
        
        return result

    @staticmethod
    async def __handle_supported_cmd(msg):
        print (msg.channel.type)
        print (msg.content)
        if GameManager.__cmd_used_in_correct_channel(msg):
            
            logging.info('Got a supported command: ' + str(msg.content))
            dispatch = {                
                    const.GAME_INITIATE_CMD : GameManager.__handle_init_cmd,
                    const.GAME_JOIN_CMD     : GameManager.__handle_join_cmd,
                    const.GAME_LOCK_CMD     : GameManager.__handle_lock_cmd,
                    const.GAME_START_CMD    : GameManager.__handle_start_cmd,
                    const.GAME_PAUSE_CMD    : GameManager.__handle_pause_cmd,
                    const.GAME_END_CMD      : GameManager.__handle_end_cmd,
                    const.GAME_REFRESH_CMD  : GameManager.__handle_refresh_cmd,
                    const.HELP_CMD          : GameManager.__handle_help_cmd,
                }
            await dispatch[msg.content](msg)

        # Command was used in inappropriate channel.
        else: await GameManager.__respond_with_error(
                msg, 
                ErrorToDisplay.wrong_cmd_to_channel_type_combination())
    
    @staticmethod
    async def __handle_init_cmd(msg):
        await msg.channel.send('Handling ' 
                               + str(msg.content) 
                               + ' Joke, LOL! Doing nothing at all!!!')
    
    @staticmethod
    async def __handle_join_cmd(msg):
        await msg.channel.send('Handling ' 
                               + str(msg.content) 
                               + ' Joke, LOL! Doing nothing at all!!!')
    
    @staticmethod
    async def __handle_lock_cmd(msg):
        await msg.channel.send('Handling ' 
                               + str(msg.content) 
                               + ' Joke, LOL! Doing nothing at all!!!')
    
    @staticmethod
    async def __handle_start_cmd(msg):
        await msg.channel.send('Handling ' 
                               + str(msg.content) 
                               + ' Joke, LOL! Doing nothing at all!!!')
    
    @staticmethod
    async def __handle_pause_cmd(msg):
        await msg.channel.send('Handling ' 
                               + str(msg.content) 
                               + ' Joke, LOL! Doing nothing at all!!!')
    
    @staticmethod
    async def __handle_end_cmd(msg):
        await msg.channel.send('Handling ' 
                               + str(msg.content) 
                               + ' Joke, LOL! Doing nothing at all!!!')
    
    @staticmethod
    async def __handle_refresh_cmd(msg):
        await msg.channel.send('Handling ' 
                               + str(msg.content) 
                               + ' Joke, LOL! Doing nothing at all!!!')
    
    @staticmethod
    async def __handle_help_cmd(msg):
        await msg.channel.send('Handling ' 
                               + str(msg.content) 
                               + ' Joke, LOL! Doing nothing at all!!!')

    @staticmethod
    async def __respond_with_error(msg_to_respond, error_obj):  
        embed = form_embed(colour = discord.Colour.red(),
                           descr  = error_obj.text,
                           title  = error_obj.title)

        await msg_to_respond.channel.send(embed = embed)

    @staticmethod
    async def handle_message(msg):
        if GameManager.__is_supported_cmd(msg): 
           await GameManager.__handle_supported_cmd(msg) 

        # TODO check if message is a game chat message
