import logging

class EmojiHandler:
    """Used to add/delete emojies to/from game guild.
    It is planned that those emojies should be crewated from
    players avatars and used for addition of a player to party
    or select a player as a Merlin.
    """
    # TODO in future, use this static class to check if a guild has enough 
    # free emoji slots to hast a game.
    # This should be used to help in selecting of guild to host game.
    @staticmethod
    async def create_emojies_for_game(game):

        result = dict()

        guild = game.game_hosting_guild

        next_emoji_id = len(guild.emojis)

        for id, player in game.player_id_to_guild_member_dict.items():

            # TODO Make emoji be round not square picture.

            avatar_bytes = await player.avatar_url.read()

            # TODO check if emoji with the same name already exists. 
            # If yes - create new emoji with a modified name. 

            # TODO Think about using players names
            # instead of PXX emoji name format.
            emoji_name = str(next_emoji_id)

            if len(emoji_name) < 2:
                emoji_name = 'P' + emoji_name

            result[id] = await guild.create_custom_emoji(
                name  = emoji_name, 
                image = avatar_bytes)

            next_emoji_id += 1

        return result

    @staticmethod
    async def delete_game_emoji(game):
        for emoji in game.player_id_to_emoji_dict.values():
            await emoji.delete()