import asyncio
import logging
from .abstract_sub_phase import SubPhaseType

from .talk_sub_phase_preparation import TalkPrepSubPhase

class PhaseHandler:

    _phases_dict = None
    _game        = None

    # === Callbacks to fetch data section =================================== #
    _get_merlin_pid_callback                      = None
    _get_players_num_from_mission_number_callback = None
    _get_fails_num_from_mission_number_callback   = None
    _get_current_mission_sequence_number_callback = None
    # ======================================================================= #
   
    @staticmethod
    def initiate_and_get_phase_handler(
                 game,
                 get_merlin_pid_callback,
                 get_players_num_from_mission_number_callback,
                 get_fails_num_from_mission_number_callback,
                 get_current_mission_sequence_number_callback):

        party_leader = game.players_ids_list[0] 
        first_talker = game.players_ids_list[1]

        phase_handler = PhaseHandler(
            game,
            get_merlin_pid_callback,
            get_players_num_from_mission_number_callback,
            get_fails_num_from_mission_number_callback,
            get_current_mission_sequence_number_callback)

        initial_talk_phase = TalkPrepSubPhase(
                                 phase_handler, 
                                 game, 
                                 first_talker,
                                 party_leader)

        # TODO in the below function replce None with init_vote_phase when
        # vote phases will be added.
        phase_handler._set_phases(initial_talk_phase, None)

        return phase_handler


    def __init__(self,
                 game,
                 get_merlin_pid_callback,
                 get_players_num_from_mission_number_callback,
                 get_fails_num_from_mission_number_callback,
                 get_current_mission_sequence_number_callback):
        self._phases_dict = dict()
        self._game        = game

        self._get_merlin_pid_callback                      = \
            get_merlin_pid_callback

        self._get_players_num_from_mission_number_callback = \
            get_players_num_from_mission_number_callback

        self._get_fails_num_from_mission_number_callback   = \
            get_fails_num_from_mission_number_callback

        self._get_current_mission_sequence_number_callback   = \
            get_current_mission_sequence_number_callback


    def _set_phases(self, talk_phase, vote_phase):        
        self._phases_dict[SubPhaseType.TALK] = talk_phase
        # TODO uncomment below code when VOTE sub phase will be added.
        #self._phases_dict[SubPhaseType.VOTE] = vote_phase

    def start_phases(self):
        for phase in self._phases_dict.values():
            phase.start()

    def sub_phase_ended(self, ended_sub_phase):
        next_sub_phase = ended_sub_phase.get_next_sub_phase()

        self._phases_dict[ended_sub_phase.type] = next_sub_phase
        
        self._phases_dict[ended_sub_phase.type].start()

    def get_current_mission_players_num(self):
        mission_number = self._get_current_mission_sequence_number_callback()
        return \
            self._get_players_num_from_mission_number_callback(mission_number)