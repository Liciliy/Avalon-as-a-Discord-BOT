import discord
import logging
import asyncio

import core.constants_games_manager as const
import core.constants_game as game_const
import languages.ukrainian_lang as lang

from core.utils import form_embed,\
    EmbedField,\
    ErrorToDisplay,\
    InfoToDisplay

from core.game import AvaGame

class GameManager:

    # Add game when it`s initiated and remove when it`s ended 
    __active_games_list           = list()

    # Add game when it is initiated and remove when game is locked
    __guilds_with_initiated_games = list()

    # Add player when he joins/creates game and remove when game is ended
    __active_players              = list()
    
    # Add game when it is initiated and remove when it is ended.
    # Remove guild when it has no associated games left
    __guild_to_game_ids_dict      = dict()  


    @staticmethod
    def __create_game_and_register_player(user_id, guild_id, msg):
        
        # Get local ID for the game
        local_game_id = const.BASE_GAME_LOCAL_ID_VAL
        if guild_id in GameManager.__guild_to_game_ids_dict:

            while local_game_id\
              not in GameManager.__guild_to_game_ids_dict[guild_id]:
                local_game_id = local_game_id + 1
        
        else:
            GameManager.__guild_to_game_ids_dict[guild_id] = list()

        GameManager.__guild_to_game_ids_dict[guild_id].append(local_game_id)

        new_game = AvaGame(local_game_id, 
                           guild_id, 
                           user_id, 
                           str(msg.author),
                           msg.channel.id)
        
        GameManager.__guilds_with_initiated_games.append(guild_id)
        GameManager.__active_players.append(user_id)
        GameManager.__active_games_list.append(new_game)

        return new_game

    @staticmethod
    def __add_player_to_game(msg):
        guild_id = msg.channel.guild.id
        user_id  = msg.author.id

        game_to_join = None

        game_found = False

        for game_id in GameManager.__guild_to_game_ids_dict[guild_id]:
            for game in GameManager.__active_games_list:
                if game.game_id == game_id\
                  and game.game_state == game_const.GAME_INITIATED_STATE:
                    game_to_join = game 
                    game_found = True
                    break

            if game_found: break

        game_to_join.add_player(user_id, str(msg.author))

        GameManager.__active_players.append(user_id)

        return game_to_join

    @staticmethod
    def __user_already_in_game(user_id):
        return user_id in GameManager.__active_players
    
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
        
        user_id = msg.author.id

        guild_id = msg.guild.id

        if guild_id in GameManager.__guilds_with_initiated_games:
            await GameManager.__respond_with_error(
                msg, 
                ErrorToDisplay.game_already_initated_here())
            return

        if GameManager.__user_already_in_game(user_id):
            await GameManager.__respond_with_error(
                msg, 
                ErrorToDisplay.player_already_in_a_game())
            return

        new_game = GameManager.__create_game_and_register_player(user_id, 
                                                                 guild_id, 
                                                                 msg)
        players_num = new_game.num_of_players_str

        await GameManager.__respond_with_info(
            msg,
            InfoToDisplay(
                title  = lang.INFO_MSG_GAME_INITIATED_TITLE,
                text   = lang.INFO_MSG_GAME_INITIATED_TEXT,
                footer = lang.INFO_MSG_FOOTER.format(number = players_num),
                fields = [EmbedField(lang.INFO_MSG_PARTY_LEADER_FIELD_NAME,
                                     str(msg.author) + '\n',
                                     True
                                     )
                         ])
        )
    
    @staticmethod
    async def __handle_join_cmd(msg):

        user_id  = msg.author.id
        guild_id = msg.guild.id

        if GameManager.__user_already_in_game(user_id):
            await GameManager.__respond_with_error(
                msg, 
                ErrorToDisplay.player_already_in_a_game())
            return

        if guild_id not in GameManager.__guilds_with_initiated_games:
            await GameManager.__respond_with_error(
                msg, 
                ErrorToDisplay.game_not_initated_here())
            return

        game = GameManager.__add_player_to_game(msg)

        number = game.num_of_players_str

        players_names_list = game.players_names_list

        await GameManager.__respond_with_info(
            msg,
            InfoToDisplay(
                title  = lang.INFO_MSG_GAME_INITIATED_TITLE,
                text   = lang.INFO_MSG_GAME_INITIATED_TEXT,
                footer = lang.INFO_MSG_FOOTER.format(number = number),
                fields = [EmbedField(lang.INFO_MSG_PARTY_LEADER_FIELD_NAME,
                                     game.game_master_name + '\n',
                                     True),
                          EmbedField(lang.INFO_MSG_OTHER_PALYERS_FIELD_NAME,
                                     '\n'.join(players_names_list) + '\n',
                                     True)
                         ])
        )
    
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
    async def __respond_with_info(msg_to_respond, info_obj):  
        embed = form_embed(colour = discord.Colour.green(),
                           descr  = info_obj.text,
                           title  = info_obj.title,
                           fields = info_obj.fields,
                           footer = info_obj.footer)

        await msg_to_respond.channel.send(embed = embed)

    @staticmethod
    async def handle_message(msg):
        if GameManager.__is_supported_cmd(msg): 
           await GameManager.__handle_supported_cmd(msg) 

        # TODO check if message is a game chat message