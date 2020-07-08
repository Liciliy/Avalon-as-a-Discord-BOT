import discord
import logging
import asyncio

import core.constants_games_manager as const
import core.constants_game as game_const
import languages.ukrainian_lang as lang

from .utils import form_embed,\
    EmbedField,\
    ErrorToDisplay,\
    InfoToDisplay

from .game import AvaGame


class GameManager:

    # Add game when it`s initiated and remove when it`s ended 
    __active_games_list           = list()

    # Add game when it is initiated and remove when game is locked
    __guilds_with_initiated_games = list()

    # Add player when he joins/creates game and remove when game is ended
    __active_players_ids              = list()
    
    # Add game when it is initiated and remove when it is ended.
    # Remove guild when it has no associated games left
    __guild_to_game_ids_dict      = dict()  

    __client_object = None

    _messages_dispatcher = None

    @staticmethod
    def set_client_object(client):
        GameManager.__client_object = client

    @staticmethod
    def set_messages_dispatcher_object(message_dispatcher):
        GameManager._messages_dispatcher = message_dispatcher

    @staticmethod
    def get_client():
        return GameManager.__client_object

    @staticmethod
    def get_messages_dispatcher():
        return GameManager._messages_dispatcher
    
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
                           msg.channel.id,
                           GameManager.get_client(),
                           GameManager.get_messages_dispatcher())
        
        GameManager.__guilds_with_initiated_games.append(guild_id)
        GameManager.__active_players_ids.append(user_id)
        GameManager.__active_games_list.append(new_game)

        return new_game

    @staticmethod
    async def __lock_game(game, msg):
        GameManager.__guilds_with_initiated_games.remove(msg.guild.id)
        await game.lock_game(msg)

    @staticmethod
    def __locked_games():
        result_list = list()

        for game in GameManager.__active_games_list:
            if game.game_state == game_const.GAME_LOCKED_STATE:
                result_list.append(game)

        return result_list

    @staticmethod
    def __get_initiated_active_game(msg):
        guild_id = msg.channel.guild.id

        game_to_join = None

        game_found = False

        if guild_id in GameManager.__guild_to_game_ids_dict:            
            for game_id in GameManager.__guild_to_game_ids_dict[guild_id]:
                for game in GameManager.__active_games_list:
                    if game.game_id == game_id\
                      and game.game_state == game_const.GAME_INITIATED_STATE:
                        game_to_join = game 
                        game_found = True
                        break
    
                if game_found: break
        
        return game_to_join

    @staticmethod
    def __add_player_to_game(msg):
        # TODO make this method to take user ID and game object as input
        # and add a player to the provided game.
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

        GameManager.__active_players_ids.append(user_id)

        return game_to_join

    @staticmethod
    def __user_already_in_game(user_id):
        return user_id in GameManager.__active_players_ids
    
    @staticmethod
    def __user_in_the_games(user_id, games):
        result = False
        
        user_game = None

        for game in games:
            for player_id in game.players_ids_list:
                if player_id == user_id:
                    result = True
                    user_game = game
                    break
            if result: break

        return result, user_game

    @staticmethod
    def __is_supported_cmd(msg):
        result = False
        if msg.content.lower() in const.AVALON_COMMANDS: result = True
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
                is_game_channel, _ = GameManager.__is_game_txt_channel(channel_id)
                if is_game_channel: result = False 
                
        else: result = False
        
        return result

    @staticmethod
    def __is_game_txt_channel(channel_id):
        result = False
        game   = None
        for game in GameManager.__active_games_list:
                    
            for game_chnl_id in [hd.id for hd in game.txt_channels_handlers]:
                if channel_id == game_chnl_id:
                    result = True
                    break
            if result == True: break

        return result, game

    @staticmethod
    async def __handle_supported_cmd(msg):
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
        else: 
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.wrong_cmd_to_channel_type_combination())
    
    @staticmethod
    async def __handle_init_cmd(msg):
        
        user_id = msg.author.id

        guild_id = msg.guild.id

        if guild_id in GameManager.__guilds_with_initiated_games:
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.game_already_initated_here())
            return

        if GameManager.__user_already_in_game(user_id):
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.player_already_in_a_game())
            return

        new_game = GameManager.__create_game_and_register_player(user_id, 
                                                                 guild_id, 
                                                                 msg)
        players_num = new_game.num_of_players_str

        await InfoToDisplay.respond_with_info(
            msg.channel,
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
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.player_already_in_a_game())
            return

        if guild_id not in GameManager.__guilds_with_initiated_games:
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.game_not_initated_here())
            return
        
        game = GameManager.__get_initiated_active_game(msg)

        if game.num_of_players >= game_const.MAX_PLAYERS:
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.too_much_players_to_join())
            return
        
        game = GameManager.__add_player_to_game(msg)

        number = game.num_of_players_str

        players_names_list = game.non_master_players_names

        await InfoToDisplay.respond_with_info(
            msg.channel,
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
        game = GameManager.__get_initiated_active_game(msg)
       
        if game == None:
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.no_game_to_lock_here())
            return
        
        number = game.num_of_players_str

        if int(number) < game_const.MIN_PLAYERS:
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.too_few_players_to_lock(number))
            return

        user_id  = msg.author.id

        if user_id != game.game_master_id:
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.only_master_can_lock())
            return        

        await GameManager.__lock_game(game, msg)

        number = game.num_of_players_str

        players_names_list = game.non_master_players_names

        await InfoToDisplay.respond_with_info(
            msg.channel,
            InfoToDisplay(
                title  = lang.INFO_MSG_GAME_LOCKED_TITLE,
                text   = lang.INFO_MSG_GAME_LOCKED_TEXT,
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
    async def __handle_start_cmd(msg):
        
        user_id   = msg.author.id
        user_name = str(msg.author)

        if user_id not in GameManager.__active_players_ids:
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.not_in_game(user_name))
            return 

        locked_games_list = GameManager.__locked_games()

        user_in_locked_game, game =\
            GameManager.__user_in_the_games(user_id, locked_games_list)
       
        if not user_in_locked_game:
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.not_in_locked_game(user_name))
            return        

        if msg.channel.id not in [hd.id for hd in game.txt_channels_handlers]:
            logging.info('Responing with error...')
            await ErrorToDisplay.respond_with_error(
                msg, 
                ErrorToDisplay.can_start_only_in_game_channel())
            return  

        if user_id != game.game_master_id:
            logging.info('Responing with error...')            
            await game.display_error_msg(
                msg, 
                ErrorToDisplay.only_master_can_start())
            return     

        # TODO check if game master changed game settings. 
         
        if len(game.get_players_not_in_guild) > 0:
            logging.info('Responing with not in guild error in game chat...')            
            await game.display_error_msg(
                msg, 
                ErrorToDisplay.not_all_connected())
            return            

        if len(game.get_players_not_in_voice) > 0:
            logging.info('Responing with not in voice error in game chat...')            
            await game.display_error_msg(
                msg, 
                ErrorToDisplay.not_all_connected_voice())
            return   

        await game.start_game(msg)
    
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
    async def handle_message(msg):
          
        if GameManager.__is_supported_cmd(msg):
            msg.content = msg.content.lower()
            await GameManager.__handle_supported_cmd(msg) 

        else:

            game_channel, game = GameManager.__is_game_txt_channel(msg.channel.id)
            if game_channel:                
                await game.handle_player_chat_message(msg)

    @staticmethod
    async def handle_join_event(member):
        
        if member.id in GameManager.__active_players_ids:
            
            for game in GameManager.__active_games_list:
                if await game.check_if_joined_member_is_game_player(member):
                    break

    @staticmethod
    async def handle_voice_change_event(member, before, after):
        if before.channel != after.channel and after.channel != None \
          and member.id in GameManager.__active_players_ids:

            for game in GameManager.__active_games_list:
                if await game.check_if_player_joined_locked_game_voice(
                    member,
                    after.channel):
                    break

    @staticmethod
    async def handle_reaction_added_event(payload):

        guild_id = payload.guild_id
        user_id  = payload.user_id

        if user_id in GameManager.__active_players_ids:

            for game in GameManager.__active_games_list:

                if game.game_hosting_guild_id == guild_id \
                  and user_id in game.players_ids_list:
                    await game.handle_player_add_reaction(user_id, payload)
                    break