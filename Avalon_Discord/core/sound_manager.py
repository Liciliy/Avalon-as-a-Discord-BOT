import os
import logging

from pathlib import Path

class SoundManager:

    _voice_channel_handler = None
    _sounds_dir_path       = None


    SOUNDS_DIR_NAME = 'sounds'    

    @staticmethod
    def setup_sound_manager(vch):
        """Sets up Sound manager needed settings:
             1) Path to directory with sounds.
             2) Link to voice channel handler.

        Args:
            vch (VoiceChannelHandler): used to play sounds.
        """
        SoundManager._voice_channel_handler = vch

        this_script_path = Path(os.path.dirname(os.path.realpath(__file__)))
        
        root_path = this_script_path.parent

        SoundManager._sounds_dir_path =\
            os.path.join(str(root_path), SoundManager.SOUNDS_DIR_NAME)

    @staticmethod
    def play_heart_beat_14_5_sec():
        # TODO Think about checking if the manager is set up.
        HEART_BEAT_FILE_NAME = 'hearbeat_quiet_14_5_sec.wav'
        
        # TODO find a way to make this join only once and reuse the path
        file_path = os.path.join(SoundManager._sounds_dir_path,
                                 HEART_BEAT_FILE_NAME)

        SoundManager._voice_channel_handler.play_sound_file(file_path)

    @staticmethod
    def play_clock_alarm_2_s():
        # TODO Think about checking if the manager is set up.
        CLOCK_ALARM_FILE_NAME = 'analog-alarm-clock_quiter_2_sec.wav'

        # TODO find a way to make this join only once and reuse the path
        file_path = os.path.join(SoundManager._sounds_dir_path,
                                 CLOCK_ALARM_FILE_NAME)

        SoundManager._voice_channel_handler.play_sound_file(file_path)

    @staticmethod
    def pause_sounds():
        SoundManager._voice_channel_handler.pause_sounds()

    @staticmethod
    def resume_sounds():
        SoundManager._voice_channel_handler.resume_sounds()

    @staticmethod
    def stop_sounds():
        SoundManager._voice_channel_handler.stop_sounds()



