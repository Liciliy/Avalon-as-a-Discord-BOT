import logging
import discord

class TextChannelHandler:
    __game         = None
    __text_channel = None
    __user         = None
    __invite       = None
    __user_role    = None

    def __init__(self, game, user, role):
        """[summary]

        Arguments:
            game {game}            -- the game instance to be played.
            user {discord.user}    -- the channel game user (player)
            role {discord.role}    -- role of the user o nthe server.
        """
        self.__game         = game
        self.__user         = user
        self.__user_role    = role

    async def create_channel_and_invite_player(self):
        game_guild = self.__game.game_hosting_guild
        
        # Creating a private text channel accessible only to the role
        overwrites = {
            game_guild.default_role : 
                discord.PermissionOverwrite(read_messages = False, 
                                            send_messages = False),
            self.__user_role : 
                discord.PermissionOverwrite(read_messages = True, 
                                            send_messages = True),
            game_guild.me : 
                discord.PermissionOverwrite(read_messages   = True, 
                                            send_messages   = True,
                                            manage_messages = True)
        }

        self.__text_channel = await game_guild.create_text_channel(
                'Avalon: ' + self.__user.name, 
                overwrites=overwrites)
        await self.__invite_player()

    async def send(self, 
                   content          = None, 
                   *, 
                   tts              = False, 
                   embed            = None, 
                   file             = None, 
                   files            = None, 
                   delete_after     = None, 
                   nonce            = None):
        return await self.__text_channel.send(
            content          = content          , 
            tts              = tts              , 
            embed            = embed            , 
            file             = file             , 
            files            = files            , 
            delete_after     = delete_after     , 
            nonce            = nonce            )

    async def __invite_player(self):
        # Sending the channel invite to player who will use it to play.
        
        self.__invite = \
            await self.__text_channel.create_invite()

        dmc = None

        if self.__user.dm_channel == None:
            await self.__user.create_dm()

        dmc = self.__user.dm_channel

        logging.debug('Sending game txt channel invite to: ' + self.__user.name)
        await dmc.send(self.__invite)

    @property
    def id(self):
        return self.__text_channel.id