import discord
import logging

class VoiceChannelHandler:
    __game                 = None
    __voice_channel        = None
    __voice_channel_invite = None
    _voice_client_instance = None

    def __init__(self, game):
        self.__game = game     

    async def connect_bot_to_voice_channel(self):
        # TODO check if the bot can join the server - it may happen, that it is 
        # already connected to other game voice channel - then he can't be used 
        # here.

        self._voice_client_instance = await self.__voice_channel.connect() 


    async def create_channel_with_invite(self):
        game_guild = self.__game.game_hosting_guild   

        overwrites = dict()

        # This will forbid users from other games to join the channel.
        overwrites[game_guild.default_role] = \
                    discord.PermissionOverwrite(connect              = False, 
                                                speak                = False,
                                                use_voice_activation = False) 

        for role in self.__game.player_id_to_role_dict.values():
            overwrites[role] = discord.PermissionOverwrite(
                                            connect              = True, 
                                            speak                = True,
                                            use_voice_activation = True)

        logging.debug('Voice channel overwrites: ' +str(overwrites))
        self.__voice_channel = \
            await game_guild.create_voice_channel(
                name       = 'Game voice of ' +self.__game.game_master_name, 
                overwrites = overwrites)

        self.__voice_channel_invite = \
            await self.__voice_channel.create_invite()
        
     
    @property
    def get_voice_channel(self):
        return self.__voice_channel

    @property
    def voice_ch_id(self):
        return self.__voice_channel.id

    @property
    def get_voice_ch_invite(self):
        return self.__voice_channel_invite
    
    def get_players_not_in_voice(self):
        result = list()

        for member in self.__game.player_id_to_guild_member_dict.values():
            if member not in self.__voice_channel.members:
                result.append(member.name)  

        return result

    @property
    def _voice_client(self) -> discord.VoiceClient:
        return self._voice_client_instance

    def play_sound_file(self, file_path):
        vc = self._voice_client
        
        if vc == None:
            logging.warning(
              'A request to play sound was recieved but Voice Client is None.')
        
        else:
            if vc.is_playing() or vc.is_paused():
                logging.info('Stopping previous sound.')
                vc.stop()
                

            sound_source = discord.FFmpegPCMAudio(file_path)

            logging.info('Starting sound.')
            vc.play(sound_source)

    def pause_sounds(self):
        vc = self._voice_client

        if vc == None:
            logging.warning(
              'A request to pause sound was recieved but Voice Client is None.')
        
        elif vc.is_playing():
            vc.pause()
            logging.info('Pausing sound.')
        else:
            logging.info('Sound is already paused/stopped.')

    def resume_sounds(self):
        vc = self._voice_client

        if vc == None:
            logging.warning(
             'A request to resume sound was recieved but Voice Client is None.')
        
        elif vc.is_paused():
            logging.info('Resuming sound.')
            vc.resume()
        else:
            logging.info('Sound is not paused.')

    def stop_sounds(self):
        vc = self._voice_client

        if vc == None:
            logging.warning(
              'A request to stop sound was recieved but Voice Client is None.')
        
        elif vc.is_playing() or vc.is_paused():
            logging.info('Stopping sound.')
            vc.stop()
        else:
            logging.info('Nothing to stop.')