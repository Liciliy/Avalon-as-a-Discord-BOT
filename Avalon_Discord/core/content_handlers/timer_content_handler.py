import copy
import asyncio
import logging

from collections import deque

import languages.ukrainian_lang as lang

from ..panels.abstract_panel_handler import PanelContent
from .abstract_content_handler import AbsContentHandler

from ..sound_manager import SoundManager

class TimerType:
    TALKING_TIMER          = 0
    TALK_PREPARATION_TIMER  = 1
    BALAGAN_TIMER          = 2
    MERLIN_HUNT_TALK_TIMER = 3

class TimerPanelContent(PanelContent):
    avatar_url = None
    no_pic     = None

    def __init__(self, 
                 text = None, 
                 reactions = None, 
                 avatar_url = None,
                 no_pic     = True):

        super().__init__(text = text, reactions = reactions)

        self.avatar_url = avatar_url
        self.no_pic = no_pic


class TimerContentHandler(AbsContentHandler):
    TIMER_RUNS_OUT_THR_SEC = 15
    YOU_ARE_TALKING   = lang.TIMER_YOU_ARE_TALKING
    X_IS_TALKING      = lang.TIMER_X_IS_TALKING
    X_ARE_TALKING     = lang.TIMER_X_ARE_TALKING
    TIME_LEFT         = lang.TIMER_TIME_LEFT
    LESS_THAN_X_LEFT  = lang.TIMER_LESS_THAN_X_LEFT.\
                             format(sec = str(TIMER_RUNS_OUT_THR_SEC)) 
    TIME_HAS_ENDED_UP = lang.TIMER_TIME_HAS_ENDED_UP
    PREPARE_TO_TALK   = lang.TIMER_PREPARE_TO_TALK
    X_PREPARS_TO_TALK = lang.TIMER_X_PREPARS_TO_TALK
    RED_PALYERS       = lang.TIMER_RED_PALYERS
    ALL_PLAYERS       = lang.TIMER_ALL_PLAYERS
    MERLIN_HUNT       = lang.TIMER_MERLIN_HUNT

    RESTART_REACT = '🔄'
    PAUSE_REACT   = '⏸️'
    END_REACT     = '⛔'
    RESUME_REACT  = '▶️'

    # One time initiated variables
    _master_channel_id = None    
    _panels_handlers   = None
    _game              = None

    # Per game round changed variables
    _timer = None
    _time_to_count              = None
    _talker_with_timer_ch_id    = None
    _current_talker_name        = None
    _timer_type                 = None
    _time_runs_out              = None
    _talking_entity_picture_url = None
    
    # Below variable needed to control playing of a sound when time ends.
    _stoped_by_a_user = None
    
    # TODO use master player ID isntad of channel ID
    def __init__(self, 
                 game, 
                 channels_handlers,
                 master_channel_id):
        
        super().__init__(game, master_channel_id)

        for game_ch in channels_handlers:
            self._panels_handlers.append(game_ch.timer_panel)
        
        #self._timer = Timer(60, self)

    # TODO think about move this one into init()
    # Probably impossible, because init cant be async. And here 
    # an awaited publish must be used.
    async def initial_render(self):
        
        for pannel_hdlr in self._panels_handlers:
            pannel_hdlr.set_content_handler(self)
            await pannel_hdlr.publish(lang.TIMER_NOT_STARTED_YET)
            
            if pannel_hdlr.channel_id == self._master_channel_id:
                reactions = [TimerContentHandler.PAUSE_REACT,
                             TimerContentHandler.RESTART_REACT,
                             TimerContentHandler.RESUME_REACT]
                pannel_hdlr.update_and_publish(
                    PanelContent(None, reactions))
         
    def update_panels(self, time_left, initial_update = False):      
        
        actual_timer_segments = self._timer.get_segments_string
        # TODO make a update function for each timer type. 
        # Select function to execute before below loop.
        # Execute function in the loop for each panel handler.
        
        t_type = self._timer_type
        for pannel_hdlr in self._panels_handlers:
            if t_type == TimerType.TALK_PREPARATION_TIMER:
                self._preparation_panels_update(pannel_hdlr,
                                                initial_update)

            # If time left equals 0 - then 'time expired' 
            # must be displayed to all players in all types except prep type.
            # TODO Think about unique phrases for different types. 
            # At least for merlin hunt.
            elif time_left == 0:
                pannel_hdlr.\
                    update_and_publish(TimerContentHandler.TIME_HAS_ENDED_UP)

            elif t_type == TimerType.TALKING_TIMER:
                self._talking_timer_panels_update(pannel_hdlr, 
                                                  actual_timer_segments,
                                                  initial_update,
                                                  time_left)
        
            elif t_type == TimerType.BALAGAN_TIMER:
                self._balagan_timer_panels_update(pannel_hdlr,
                                                  actual_timer_segments,
                                                  initial_update,
                                                  time_left)

            elif t_type == TimerType.MERLIN_HUNT_TALK_TIMER:
                self._merlin_hunt_panels_update(pannel_hdlr,
                                                actual_timer_segments,
                                                initial_update,
                                                time_left)

            else:
                logging.error('Unknown timer type received: ' + str(t_type))
         
        if time_left < TimerContentHandler.TIMER_RUNS_OUT_THR_SEC\
              and \
           not self._time_runs_out:
            self._time_runs_out = True

    def _preparation_panels_update(self,
                                   pannel_hdlr,
                                   initial_update):
        if initial_update:
            reactions = None
            text = ''
            if pannel_hdlr.channel_id == self._talker_with_timer_ch_id:
                text = TimerContentHandler.PREPARE_TO_TALK
            else:
                text =\
                    TimerContentHandler.X_PREPARS_TO_TALK.format(
                        name = self._current_talker_name)            

            pannel_hdlr.update_and_publish(PanelContent(text, reactions))

    def _talking_timer_panels_update(self, 
                                     pannel_hdlr, 
                                     actual_timer_segments,
                                     initial_update,
                                     time_left):
        
        text      = None
        reactions = None

        # Handling talker
        if pannel_hdlr.channel_id == self._talker_with_timer_ch_id:
            text = TimerContentHandler.YOU_ARE_TALKING \
                    + TimerContentHandler.TIME_LEFT \
                    + actual_timer_segments
            if initial_update: 
                reactions = [TimerContentHandler.END_REACT]
            pannel_hdlr.update_and_publish(
                TimerPanelContent(text, reactions, None, True))
        
        # Handling master
        elif pannel_hdlr.channel_id == self._master_channel_id:
            text = TimerContentHandler.X_IS_TALKING.\
                        format(name = self._current_talker_name) \
                    + TimerContentHandler.TIME_LEFT \
                    + actual_timer_segments

            pannel_hdlr.update_and_publish(
                TimerPanelContent(text, reactions, None, True))
       
        # Handling non-talkers
        else:
            if initial_update:
                content = TimerContentHandler.X_IS_TALKING.\
                            format(name = self._current_talker_name)
                pannel_hdlr.update_and_publish(content)

            elif time_left < TimerContentHandler.TIMER_RUNS_OUT_THR_SEC\
              and not self._time_runs_out:
                SoundManager.play_heart_beat_14_5_sec()
                #self._time_runs_out = True
                content = TimerContentHandler.X_IS_TALKING.\
                            format(name = self._current_talker_name)\
                        + TimerContentHandler.LESS_THAN_X_LEFT
                pannel_hdlr.update_and_publish(content)

    def _balagan_timer_panels_update(self,
                                     pannel_hdlr,
                                     actual_timer_segments,
                                     initial_update,
                                     time_left):

        # Handling master and party leader 
        if pannel_hdlr.channel_id == self._master_channel_id\
          or pannel_hdlr.channel_id == self._talker_with_timer_ch_id:
            text      = None
            reactions = None
        
            text =  TimerContentHandler.X_ARE_TALKING.\
                        format(group = TimerContentHandler.ALL_PLAYERS) \
                    + TimerContentHandler.TIME_LEFT \
                    + actual_timer_segments  
            
            pannel_hdlr.update_and_publish(PanelContent(text, reactions))

        # Handling non-masters first render.
        elif initial_update:
            content = TimerContentHandler.X_ARE_TALKING.\
                        format(group = TimerContentHandler.ALL_PLAYERS)
            pannel_hdlr.update_and_publish(content)
        
        # Handling non-master players last X sec.
        elif time_left < TimerContentHandler.TIMER_RUNS_OUT_THR_SEC\
          and not self._time_runs_out:
            SoundManager.play_heart_beat_14_5_sec()
            #self._time_runs_out = True
            content = TimerContentHandler.X_ARE_TALKING.\
                        format(group = TimerContentHandler.ALL_PLAYERS)\
                    + TimerContentHandler.LESS_THAN_X_LEFT
            pannel_hdlr.update_and_publish(content)

    def _merlin_hunt_panels_update(self,
                                   pannel_hdlr,
                                   actual_timer_segments,
                                   initial_update,
                                   time_left):

        # Handling master and main talker  
        if pannel_hdlr.channel_id == self._master_channel_id\
          or pannel_hdlr.channel_id == self._talker_with_timer_ch_id:
            text      = None
            reactions = None
            text = TimerContentHandler.MERLIN_HUNT\
                    + TimerContentHandler.X_ARE_TALKING.\
                        format(group = TimerContentHandler.RED_PALYERS) \
                    + TimerContentHandler.TIME_LEFT \
                    + actual_timer_segments

            pannel_hdlr.update_and_publish(PanelContent(text, reactions))
        
        # Handling non-talking players.
        elif initial_update:
            content = TimerContentHandler.MERLIN_HUNT\
                    + TimerContentHandler.X_ARE_TALKING.\
                        format(group = TimerContentHandler.RED_PALYERS)
            pannel_hdlr.update_and_publish(content)

        # Handling non-talking players last seconds.
        elif time_left < TimerContentHandler.TIMER_RUNS_OUT_THR_SEC\
          and not self._time_runs_out:
            SoundManager.play_heart_beat_14_5_sec()
            #self._time_runs_out = True
            content = TimerContentHandler.MERLIN_HUNT\
                    + TimerContentHandler.X_ARE_TALKING.\
                        format(group = TimerContentHandler.RED_PALYERS)\
                    + TimerContentHandler.LESS_THAN_X_LEFT
            pannel_hdlr.update_and_publish(content)

    def notify_game_timer_expired(self):
        logging.debug('Timer notified about its expiration.')

        self._talking_entity_picture_url = None

        if not self._stoped_by_a_user \
              and\
           self._timer_type != TimerType.TALK_PREPARATION_TIMER:
            SoundManager.play_clock_alarm_2_s()

        if self._timer_type == TimerType.TALKING_TIMER:

            for pannel_hdlr in self._panels_handlers:    
                if pannel_hdlr.channel_id == self._talker_with_timer_ch_id:

                    pannel_hdlr.order_del_own_reaction(TimerContentHandler.END_REACT,
                                                       pannel_hdlr.id)
                    break 

        self.update_panels(0)       
        res_dict = self.get_base_action_end_dict() 
        self._coordinating_sub_phase.react_or_content_handler_action(res_dict)

    def get_talking_entity_picture_url(self):
        return self._talking_entity_picture_url

    def _set_talking_entity_picture_url(self):
        result = None

        if self._timer_type in [TimerType.TALKING_TIMER, 
                                TimerType.TALK_PREPARATION_TIMER]:
            result = self._coordinating_sub_phase.get_talker_avatar_url()

        # TODO gor balagan and merlin hunt add constant images return
        self._talking_entity_picture_url = result          

    # TODO use start as a high priot awaited task.
    async def start_timer(self, 
                          timer_type,
                          time_to_count,
                          talking_entity_name,
                          talker_with_timer_ch_id):

        logging.info('Starting timer. Type: ' + str(timer_type) +
                     '. Talking entitity: '   + talking_entity_name +
                     '. Talker channel ID '   + str(talker_with_timer_ch_id)+
                     '. Time: '               + str(time_to_count))

        self._time_runs_out = False  
        
        self._stoped_by_a_user = False           

        self._timer                   = Timer(time_to_count, self)
        self._time_to_count           = time_to_count
        self._timer_type              = timer_type
        self._current_talker_name     = talking_entity_name
        self._talker_with_timer_ch_id = talker_with_timer_ch_id
        
        self._set_talking_entity_picture_url()

        self.update_panels(time_to_count, True)

        

        # TODO find a way to make below awaited task to be higg prio
        # TODO think about starting of the timer in a separate thread.
        await self._timer.start()

    def handle_reaction(self, emoji_str):
        if emoji_str   == TimerContentHandler.RESTART_REACT:
            self._timer.restart()
            self._time_runs_out = False
            self._stoped_by_a_user = False
               
            SoundManager.stop_sounds()

        elif emoji_str == TimerContentHandler.PAUSE_REACT:
            self._timer.pause() 
            SoundManager.pause_sounds()

        elif emoji_str == TimerContentHandler.END_REACT:
            self._stoped_by_a_user = True
            self._timer.stop()
            SoundManager.stop_sounds()

        elif emoji_str == TimerContentHandler.RESUME_REACT:
            self._timer.resume()
            SoundManager.resume_sounds()


class Timer:
    TIMER_SLEEP_TIME_S   = 0.05

    # ==================== Animation part ==================
    NUM_OF_SEGMENTS      = 5
    ANIMATION_FRAME_TIME = 3

    MAX_SEGMENT_INDEX = NUM_OF_SEGMENTS - 1

    SEGMENT_1ST_EMOJI   = '⌛'
    SEGMENT_2ND_EMOJI   = '⏳'

    SEGMENT_ANIMATION = deque([SEGMENT_1ST_EMOJI, SEGMENT_2ND_EMOJI])

    EXPIRED_SEGMENT_EMOJI = '✖️'

    # Below data is calculated/defined by the timer itself.
    _max_segment_lifetime  = None
    
    _curr_animated_segment = None
    _curr_segment_lifetime = None
    _seg_animation         = None

    _segments              = None
    # ==================== Animation part END ==============    
    _update_panel                 = None
    _current_animation_start_time = None   
    _end_time                     = None
    _time_left                    = None
    _pause_time                   = None


    # Below data is received from top execution layer
    _timer_content_handler = None
    _time_to_count         = None
    _is_active             = None
    _is_paused             = None


    def __init__(self, time, timer_content_handler):
        
        self._time_to_count = int(time)

        self._max_segment_lifetime = self._time_to_count/Timer.NUM_OF_SEGMENTS

        self._curr_animated_segment = 0

        self._curr_segment_lifetime = 0

        self._timer_content_handler = timer_content_handler

        self._segments = Timer._get_start_time_segments()

        self._seg_animation = Timer.SEGMENT_ANIMATION

        self._is_paused = False

        self._update_panel = False

        logging.info('Timer created.')

    def stop(self):
        self._is_active  = False
        self._is_paused  = False
        logging.info('Timer is stoped.')

    def pause(self):
        if not self._is_paused and self._is_active:        
            self._is_paused  = True
            self._time_left  = self._end_time - asyncio.get_running_loop().time() 
            self._pause_time = asyncio.get_running_loop().time() 
    
            logging.info('Timer is paused.')
            
        else: logging.info('Already paused or stopped.')

    def resume(self): 
        if self._is_paused and self._is_active:     
            self._end_time = asyncio.get_running_loop().time() + self._time_left
            self._current_animation_start_time =\
                self._current_animation_start_time +\
                (asyncio.get_running_loop().time() - self._pause_time)
            self._is_paused = False
            logging.info('Timer is resumed.')

        else: logging.info('Cant resume - either stopped or not paused.')

    async def start(self):
        self._is_active = True

        self._end_time = asyncio.get_running_loop().time() + self._time_to_count 
        self._current_animation_start_time = asyncio.get_running_loop().time()
        logging.info('Timer is launched.')
        await self._run_with_while()
        
    def restart(self):
        if self._is_active: 
            self._end_time     = asyncio.get_running_loop().time() + self._time_to_count        
            self._current_animation_start_time = asyncio.get_running_loop().time()
            self._update_panel = True
            self._segments = Timer._get_start_time_segments()
            self._curr_animated_segment = 0
            self._curr_segment_lifetime = 0
            self._seg_animation = Timer.SEGMENT_ANIMATION
            self._is_paused = False
            self._is_active = True
            logging.info('Timer is restarted.')
        else: logging.info('Cant restart - timer is stopped.')

    def _handle_timer_iteration_actions(self):
        if self._curr_segment_lifetime >= self._max_segment_lifetime\
          and self._curr_animated_segment < Timer.MAX_SEGMENT_INDEX:
            
            # One of the segments has expired. Mark it as axpired and mark next 
            # one as active.
            self._segments[self._curr_animated_segment] = Timer.EXPIRED_SEGMENT_EMOJI    
            self._curr_animated_segment = self._curr_animated_segment  + 1    
            self._curr_segment_lifetime = 0
            self._update_panel = True

        if asyncio.get_running_loop().time() - self._current_animation_start_time\
             >= \
           self.ANIMATION_FRAME_TIME:

            self._current_animation_start_time = asyncio.get_running_loop().time()

            self._segments[self._curr_animated_segment] = self._seg_animation[0]
            self._seg_animation.rotate()

            self._update_panel = True
    
        if self._update_panel:                
            self._update_panel = False
            time_left = self._end_time - asyncio.get_running_loop().time() 
            self._timer_content_handler.update_panels(int(time_left))

    async def _run_with_while(self):        

        while (asyncio.get_running_loop().time() < self._end_time) \
            and self._is_active: 

            # If timer is paused it will cycled in the below loop until
            # being resumed by a user.
            while self._is_paused:
                await asyncio.sleep(Timer.TIMER_SLEEP_TIME_S)
            
            self._handle_timer_iteration_actions()                         
            
            await asyncio.sleep(Timer.TIMER_SLEEP_TIME_S)
            self._curr_segment_lifetime += Timer.TIMER_SLEEP_TIME_S
    
        logging.info('Timer loop ended. Notifying timer content handler.') 
        self._timer_content_handler.notify_game_timer_expired()
            
    @staticmethod
    def _get_start_time_segments():
        return [Timer.SEGMENT_1ST_EMOJI] * Timer.NUM_OF_SEGMENTS

    @property
    def get_segments_string(self):
        return ''.join(self._segments)