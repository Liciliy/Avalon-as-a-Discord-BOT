import asyncio
import logging


from ..mechanics.game_info import GameInfo

class PhaseHandler:

    _phases_dict = None
    _game        = None
    _game_info   = None

    # === Callbacks to fetch data section =================================== #
    _get_merlin_pid_callback                      = None
    _get_players_num_from_mission_number_callback = None
    _get_fails_num_from_mission_number_callback   = None
    # ======================================================================= #
   
    @staticmethod
    def initiate_and_get_phase_handler(
                 game,
                 get_merlin_pid_callback,
                 get_players_num_from_mission_number_callback,
                 get_fails_num_from_mission_number_callback,
                 game_real_time_info):

        party_leader = game.players_ids_list[0] 
        first_talker = game.players_ids_list[1]

        from .talk_sub_phase_preparation  import TalkPrepSubPhase
        from .vote_sub_phase_party_select import PartySelectVoteSubPhase

        phase_handler = PhaseHandler(
            game,
            get_merlin_pid_callback,
            get_players_num_from_mission_number_callback,
            get_fails_num_from_mission_number_callback,
            game_real_time_info)

        initial_talk_phase = TalkPrepSubPhase(
                                 phase_handler, 
                                 game, 
                                 first_talker,
                                 party_leader)

        initial_vote_phase = PartySelectVoteSubPhase(
                                 phase_handler, 
                                 game, 
                                 party_leader)
        
        phase_handler._set_phases(initial_talk_phase, initial_vote_phase)

        return phase_handler


    def __init__(self,
                 game,
                 get_merlin_pid_callback,
                 get_players_num_from_mission_number_callback,
                 get_fails_num_from_mission_number_callback,
                 game_real_time_info):
        self._phases_dict = dict()
        self._game        = game

        self._game_info = game_real_time_info

        self._get_merlin_pid_callback                      = \
            get_merlin_pid_callback

        self._get_players_num_from_mission_number_callback = \
            get_players_num_from_mission_number_callback

        self._get_fails_num_from_mission_number_callback   = \
            get_fails_num_from_mission_number_callback

    def _set_phases(self, talk_phase, vote_phase):     
        from .abstract_sub_phase import SubPhaseType
           
        self._phases_dict[SubPhaseType.TALK] = talk_phase
        self._phases_dict[SubPhaseType.VOTE] = vote_phase

    def start_phases(self):
        for phase in self._phases_dict.values():
            logging.info('Going to start phase. Str repr: ' + str(phase))
            phase.start()
            logging.info('Phase started.')

        logging.info('All phases started.')        

    def sub_phase_ended(self, ended_sub_phase):
        next_sub_phase = ended_sub_phase.get_next_sub_phase()

        self._phases_dict[ended_sub_phase.type] = next_sub_phase
        
        self._phases_dict[ended_sub_phase.type].start()

    def get_current_mission_players_num(self):
        mission_number = self.game_info.get_current_mission_number()
        return \
            self._get_players_num_from_mission_number_callback(mission_number)

    def get_num_of_fails_to_fail_the_mission(self):
        mission_number = self.game_info.get_current_mission_number()
        return \
            self._get_fails_num_from_mission_number_callback(mission_number)


    def message_other_sub_phase(self, sender_type, message_dict):

        logging.info(
          f'Goind to send a message to phase. Sender type: {str(sender_type)}')
        for type, sub_phase in self._phases_dict.items():
            
            if sender_type != type:
                logging.info(f'Sendig msg to phase type: {str(type)}')
                sub_phase.react_on_other_sub_phase_action(message_dict)
                break

    @property
    def game_info(self) -> GameInfo:
        return self._game_info