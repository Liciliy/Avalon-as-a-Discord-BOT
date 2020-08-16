import languages.ukrainian_lang as lang
import discord

from ..utils import form_embed, EmbedField

class Team:
    RED  = 0
    BLUE = 1

    TEAM_TO_STRING = {
        BLUE : 'Сині',
        RED  : 'Червоні'
    }


class AbstractRole:
    _game = None
    
    # List of roles that this role knows
    sees          = None
    
    # Role string name.
    real_name     = None

    # Role string name to show for Red players (if needed)
    name_for_red  = None

    # Role string name to show for Blue players (if needed)
    name_for_blue = None

    # Role string name for Merlin
    name_for_merlin = None    

    team          = None
    _secret_info  = None

    def __init__(self, 
                 game):
        self._game = game

    def get_secret_info_embed(self, pid):
        
        color = None
        if self.team == Team.BLUE:
            color = discord.Color.blue()
        else:
            color = discord.Color.red()

        return\
            form_embed(descr  = lang.SECRET_INFO_YOUR_ROLE.format(
                                    role = self.real_name,
                                    team = Team.TEAM_TO_STRING[self.team]),
                       author = lang.SECRET_INFO_HEADER,
                       colour = color)
            

    def knows_player_role(self, role):
        pass


class BluePlayer(AbstractRole):
    team = Team.BLUE
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name     = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_blue = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red  = lang.SIMPLE_BLUE_ROLE_NAME

        self.sees = []


class RedPlayer(AbstractRole):
    team = Team.RED
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name       = lang.SIMPLE_RED_ROLE_NAME
        self.name_for_blue   = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red    = lang.SIMPLE_RED_ROLE_NAME
        self.name_for_merlin = lang.SIMPLE_RED_ROLE_NAME

        self.sees = [RedPlayer, Morgana, Mordred, Assassin]
        
    def get_secret_info_embed(self, this_player_pid):
        # TODO Think if red players should now each others role.
            # In real life game they would not now. 
            # But if they would - they could, for example, support Morgana, 
            # making Persival think that Morgana is the Merlin.
        color = discord.Color.red()
        fields = list()
        for pid, role in self._game.player_id_to_role_dict.items():
            if type(role) in self.sees and pid != this_player_pid:
                em = self._game.player_id_to_emoji_dict[pid]
                
                emoji = f'<:{em.name}:{str(em.id)}>'
                name  = self._game.player_id_to_name_dict[pid]

                role_data = lang.OTHER_PLAYER_SECRET_INFO.format(
                                    role  = role.real_name,
                                    team  = Team.TEAM_TO_STRING[role.team])
                
                fields.append(EmbedField(f'{emoji} {name}',
                                         role_data))

        return \
            form_embed(
                descr  = lang.SECRET_INFO_YOUR_ROLE.format(
                                role = self.real_name,
                                team = Team.TEAM_TO_STRING[self.team]),
                author = lang.SECRET_INFO_HEADER,
                colour = color,
                fields = fields)


class Merlin(AbstractRole):
    team = Team.BLUE
    name_for_persival = None
    name_for_persival_no_oponent = None
    
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name         = lang.MERLIN_ROLE_NAME
        self.name_for_persival = lang.MORGANA_OR_MERLIN_ROLE_NAME
        self.name_for_red      = lang.SIMPLE_BLUE_ROLE_NAME

        self.name_for_persival_no_oponent = lang.MERLIN_ROLE_NAME

        self.sees = [Morgana, Assassin, Oberon, RedPlayer]

    def get_secret_info_embed(self, this_player_pid):
        color = discord.Color.blue()
        fields = list()
        for pid, role in self._game.player_id_to_role_dict.items():
            if type(role) in self.sees:
                em = self._game.player_id_to_emoji_dict[pid]
                
                emoji = f'<:{em.name}:{str(em.id)}>'
                name  = self._game.player_id_to_name_dict[pid]
                role_data = lang.OTHER_PLAYER_SECRET_INFO.format(
                                    role  = role.name_for_merlin,
                                    team  = Team.TEAM_TO_STRING[role.team])
                
                fields.append(EmbedField(f'{emoji} {name}',
                                         role_data))

        return \
            form_embed(
                descr  = lang.SECRET_INFO_YOUR_ROLE.format(
                                role = self.real_name,
                                team = Team.TEAM_TO_STRING[self.team]),
                author = lang.SECRET_INFO_HEADER,
                colour = color,
                fields = fields)


class Morgana(AbstractRole):
    
    team = Team.RED
    name_for_persival = None
    name_for_persival_no_oponent = None

    def __init__(self, game):
        super().__init__(game)
        
        self.real_name         = lang.MORGANA_ROLE_NAME
        self.name_for_persival = lang.MORGANA_OR_MERLIN_ROLE_NAME
        self.name_for_red      = lang.MORGANA_ROLE_NAME
        self.name_for_merlin   = lang.SIMPLE_RED_ROLE_NAME

        self.name_for_persival_no_oponent = lang.MORGANA_ROLE_NAME

        self.sees = [Assassin, Mordred, RedPlayer]

    def get_secret_info_embed(self, this_player_pid):
        # TODO Think if red players should now each others role.
            # In real life game they would not now. 
            # But if they would - they could, for example, support Morgana, 
            # making Persival think that Morgana is the Merlin.
        color = discord.Color.red()
        fields = list()
        for pid, role in self._game.player_id_to_role_dict.items():
            if type(role) in self.sees:
                em = self._game.player_id_to_emoji_dict[pid]
                
                emoji = f'<:{em.name}:{str(em.id)}>'
                name  = self._game.player_id_to_name_dict[pid]
                role_data = lang.OTHER_PLAYER_SECRET_INFO.format(
                                    role  = role.real_name,
                                    team  = Team.TEAM_TO_STRING[role.team])
                
                fields.append(EmbedField(f'{emoji} {name}',
                                         role_data))

        return \
            form_embed(
                descr  = lang.SECRET_INFO_YOUR_ROLE.format(
                                role = self.real_name,
                                team = Team.TEAM_TO_STRING[self.team]),
                author = lang.SECRET_INFO_HEADER,
                colour = color,
                fields = fields)


class Persival(AbstractRole):    
    team = Team.BLUE
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name     = lang.PERSIVAL_ROLE_NAME
        self.name_for_blue = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red  = lang.SIMPLE_BLUE_ROLE_NAME

        self.sees = [Morgana, Merlin]

    def get_secret_info_embed(self, this_player_pid):
        
        merlin_in_game  = False
        morgana_in_game = False

        for _, role in self._game.player_id_to_role_dict.items():
            if type(role) == Merlin:
                merlin_in_game = True
            
            if type(role) == Morgana:
                morgana_in_game = True

        both_merlin_morgana_in_game = merlin_in_game and morgana_in_game
        color = discord.Color.blue()
        fields = list()

        for pid, role in self._game.player_id_to_role_dict.items():
            if type(role) in self.sees:
                name_to_use = None
                if both_merlin_morgana_in_game:
                    name_to_use = role.name_for_persival
                else:
                    name_to_use = role.name_for_persival_no_oponent

                em = self._game.player_id_to_emoji_dict[pid]   
                
                emoji = f'<:{em.name}:{str(em.id)}>'
                name  = self._game.player_id_to_name_dict[pid]
                role_data = lang.OTHER_PLAYER_SECRET_INFO_NO_TEAM.format(
                                    role = name_to_use)
                
                fields.append(EmbedField(f'{emoji} {name}',
                                         role_data))

        return \
            form_embed(
                descr  = lang.SECRET_INFO_YOUR_ROLE.format(
                                role = self.real_name,
                                team = Team.TEAM_TO_STRING[self.team]),
                author = lang.SECRET_INFO_HEADER,
                colour = color,
                fields = fields)


class Mordred(AbstractRole):    
    team = Team.RED
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name     = lang.MORDRED_ROLE_NAME
        self.name_for_blue = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red  = lang.MORDRED_ROLE_NAME

        self.sees = [Assassin, Morgana, RedPlayer]

    def get_secret_info_embed(self, this_player_pid):
        # TODO Think if red players should now each others role.
            # In real life game they would not now. 
            # But if they would - they could, for example, support Morgana, 
            # making Persival think that Morgana is the Merlin.
        color = discord.Color.red() 
        fields = list()
        for pid, role in self._game.player_id_to_role_dict.items():
            if type(role) in self.sees:
                em = self._game.player_id_to_emoji_dict[pid]
                
                emoji = f'<:{em.name}:{str(em.id)}>'
                name  = self._game.player_id_to_name_dict[pid]
                role_data = lang.OTHER_PLAYER_SECRET_INFO.format(
                                    role  = role.real_name,
                                    team  = Team.TEAM_TO_STRING[role.team])
                
                fields.append(EmbedField(f'{emoji} {name}',
                                         role_data))

        return \
            form_embed(
                descr  = lang.SECRET_INFO_YOUR_ROLE.format(
                                role = self.real_name,
                                team = Team.TEAM_TO_STRING[self.team]),
                author = lang.SECRET_INFO_HEADER,
                colour = color,
                fields = fields)


class Oberon(AbstractRole):
    team = Team.RED
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name     = lang.OBERON_ROLE_NAME
        self.name_for_blue = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red  = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_merlin = lang.SIMPLE_RED_ROLE_NAME


class Assassin(AbstractRole):
    team = Team.RED
    def __init__(self, game):
        super().__init__(game)
        
        self.real_name     = lang.ASSASSIN_ROLE_NAME
        self.name_for_blue = lang.SIMPLE_BLUE_ROLE_NAME
        self.name_for_red  = lang.ASSASSIN_ROLE_NAME
        self.name_for_merlin = lang.SIMPLE_RED_ROLE_NAME

        self.sees = [Mordred, Morgana, RedPlayer]
    
    def get_secret_info_embed(self, this_player_pid):
        # TODO Think if red players should now each others role.
            # In real life game they would not now. 
            # But if they would - they could, for example, support Morgana,
            # making Persival think that Morgana is the Merlin.
        color = discord.Color.red()
        fields = list()
        for pid, role in self._game.player_id_to_role_dict.items():
            if type(role) in self.sees:
                em = self._game.player_id_to_emoji_dict[pid]
                
                emoji = f'<:{em.name}:{str(em.id)}>'
                name  = self._game.player_id_to_name_dict[pid]
                role_data = lang.OTHER_PLAYER_SECRET_INFO.format(
                                    role  = role.real_name,
                                    team  = Team.TEAM_TO_STRING[role.team])
                
                fields.append(EmbedField(f'{emoji} {name}',
                                         role_data))

        return \
            form_embed(
                descr  = lang.SECRET_INFO_YOUR_ROLE.format(
                                role = self.real_name,
                                team = Team.TEAM_TO_STRING[self.team]),
                author = lang.SECRET_INFO_HEADER,
                colour = color,
                fields = fields)