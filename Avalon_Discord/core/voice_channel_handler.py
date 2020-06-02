import discord
import logging

class VoiceChannelHandler:
    __game                 = None
    __voice_channel        = None
    __voice_channel_invite = None

    def __init__(self, game):
        self.__game = game        

    async def create_channel_with_invite(self):
        game_guild = self.__game.game_hosting_guild

        overwrites = dict()

        # This will forbid users from other games to join the channel.
        overwrites[game_guild.default_role] = \
                    discord.PermissionOverwrite(connect              = True, 
                                                speak                = True,
                                                use_voice_activation = True) 

        for role in self.__game.player_id_to_role_dict.values():
            overwrites[role] = discord.PermissionOverwrite(
                                            connect              = True, 
                                            speak                = True,
                                            use_voice_activation = True)

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
    def get_voice_ch_invite(self):
        return self.__voice_channel_invite