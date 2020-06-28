import asyncio

from collections import deque

from .abstract_panel_handler import\
    AbsGamePanelHandler,\
    ContentType
   
class TimerPanelHandler(AbsGamePanelHandler):

    TIME_KEY      = 'time'
    TEXT_KEY      = 'text'
    REACTIONS_KEY = 'reactions'

    _timer_on = None

    def __init__(self, game, channel):
        super().__init__(game, channel, ContentType.TEXT)
        self._timer_on = False

    async def __create_and_publish(self, content):
        self._message = await self._channel.send(content = content)
        self._msg_content = self._message.content

    async def __update_and_publish(self, content):
        await self._message.edit(content = content)
        self._msg_content = self._message.content

    async def delete(self):
        if self._message != None:
            await self._message.delete()
            self._message = None

    async def publish(self, content = None):
        if self._message == None:
            await self.__create_and_publish(content)
        else: await self.__update_and_publish(content)    
    
    async def _start_time(self):
        pass

    async def update_timer(self):
        pass

    async def stop_time(self):
        pass


class Timer:
    TIMER_SLEEP_TIME_S   = 0.05
    NUM_OF_SEGMENTS      = 5
    ANIMATION_FRAME_TIME = 3

    MAX_SEGMENT_INDEX = NUM_OF_SEGMENTS - 1

    SEGMENT_1ST_EMOJI   = '⌛'
    SEGMENT_2ND_EMOJI   = '⏳'

    SEGMENT_ANIMATION = deque([SEGMENT_1ST_EMOJI, SEGMENT_2ND_EMOJI])

    EXPIRED_SEGMENT_EMOJI = '✖️'

    _max_segment_lifetime  = None
    _time_to_count         = None
    _curr_animated_segment = None
    _curr_segment_lifetime = None
    _seg_animation         = None

    _segments              = None
    
    _is_active   = None

    _timer_content_handler = None

    _end_time = None

    _current_animation_start_time = None

    def __init__(self, time, timer_content_handler):
        
        self._time_to_count = int(time)

        self._max_segment_lifetime = self._time_to_count/Timer.NUM_OF_SEGMENTS

        self._curr_animated_segment = 0

        self._curr_segment_lifetime = 0

        self._timer_content_handler = timer_content_handler

        self._segments = Timer._get_start_time_segments()

        self._seg_animation = Timer.SEGMENT_ANIMATION


    def stop(self):
        self._is_active = False


    async def start(self):
        self._is_active = True

        self._end_time = asyncio.get_running_loop().time() + self._time_to_count 
        self._current_animation_start_time = asyncio.get_running_loop().time()
        
        await self._run()

    async def _run(self): 

        if self._is_active:
            # TODO Time comparation might be too expensive. 
            # Try to add comparation of expered segments and time comparation.
            # Example: while alive_segments > 1 or loop.time() < end_time:
            if asyncio.get_running_loop().time() < self._end_time:
                
                if self._curr_segment_lifetime >= self._max_segment_lifetime\
                  and self._curr_animated_segment < Timer.MAX_SEGMENT_INDEX:
                    
                    # One of the segments has expired. Mark it as axpired and mark next 
                    # one as active.
                    self._segments[self._curr_animated_segment] = Timer.EXPIRED_SEGMENT_EMOJI    
                    self._curr_animated_segment = self._curr_animated_segment  + 1    
                    self._curr_segment_lifetime = 0
    
    
                if asyncio.get_running_loop().time() - self._current_animation_start_time\
                     >= \
                   self.ANIMATION_FRAME_TIME:

                    self._current_animation_start_time = asyncio.get_running_loop().time()

                    self._segments[self._curr_animated_segment] = self._seg_animation[0]
                    self._seg_animation.rotate()
        
                    await asyncio.gather(self._sleep_and_run_again(),
                                         self._timer_content_handler.update_panels())
                else:
                    await self._sleep_and_run_again() 

            else:
                await self._timer_content_handler.timer_expired()


    async def _run_with_while(self): 

        update_panel = False

        while (asyncio.get_running_loop().time() < self._end_time) and self._is_active: 
            
            if self._curr_segment_lifetime >= self._max_segment_lifetime\
              and self._curr_animated_segment < Timer.MAX_SEGMENT_INDEX:
                
                # One of the segments has expired. Mark it as axpired and mark next 
                # one as active.
                self._segments[self._curr_animated_segment] = Timer.EXPIRED_SEGMENT_EMOJI    
                self._curr_animated_segment = self._curr_animated_segment  + 1    
                self._curr_segment_lifetime = 0
                update_panel = True


            if asyncio.get_running_loop().time() - self._current_animation_start_time\
                 >= \
               self.ANIMATION_FRAME_TIME:

                self._current_animation_start_time = asyncio.get_running_loop().time()

                self._segments[self._curr_animated_segment] = self._seg_animation[0]
                self._seg_animation.rotate()

                update_panel = True
    
            if update_panel:
                print ('updating panel')
                update_panel = False
                await asyncio.gather(self._timer_content_handler.update_panels())                         
            
            await asyncio.sleep(Timer.TIMER_SLEEP_TIME_S)
            self._curr_segment_lifetime += Timer.TIMER_SLEEP_TIME_S
    
            
        await self._timer_content_handler.timer_expired()

    async def _sleep_and_run_again(self): 
        # TODO check if time to sleep is not less than end_time - loop.time()
        # If less - use this 'less' time instead 
        await asyncio.sleep(Timer.TIMER_SLEEP_TIME_S)  
        self._curr_segment_lifetime += Timer.TIMER_SLEEP_TIME_S
        await self._run()

            
    @staticmethod
    def _get_start_time_segments():
        return [Timer.SEGMENT_1ST_EMOJI] * Timer.NUM_OF_SEGMENTS

    @property
    def get_segments_string(self):
        return ''.join(self._segments)

        




    