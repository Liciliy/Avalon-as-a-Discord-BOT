import os
import inspect
import asyncio

IMAGES_DIRECTORY = r'images\text.png'

IMAGE_NEEDED = 'text.png'

from pathlib import Path


from core.panels.timer_panel_handler import Timer
from core.messages_dispatching.task_queue import TaskQueue

def paths():
    print('=======================================================')
    path_to_this_script = os.path.abspath(inspect.getfile(inspect.currentframe()))
    print('Path to this script file ' + path_to_this_script)
    print('=======================================================\n')

    string_directory = os.path.dirname(path_to_this_script)
    path_to_this_directory = Path(string_directory)
    print('Path to this file dirtectory ' + str(path_to_this_directory))
    print('=======================================================\n')
    

    
    path_to_parent_dir = path_to_this_directory.parent
    print('Path to this dirtectory ' + str(path_to_parent_dir))
    print('=======================================================\n')

    
    print('=======================================================\n')
    image_dir_path = os.path.join(path_to_parent_dir, IMAGES_DIRECTORY)
    print('Path to this dirtectory ' + image_dir_path)

    image_file_path = os.path.join(image_dir_path, IMAGE_NEEDED)
    print('IMG file dirtectory ' + image_file_path)

    print('=======================================================\n')

class GeometryPoint:
    x_coord = None
    y_coord = None

    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = x

    def __truediv__(self, dividor_int):

        #if (type(dividor_int) == type(int)):

        return GeometryPoint(x = int(self.x_coord/dividor_int),
                             y = int(self.y_coord/dividor_int))

        #if (type(dividor_int) == type(GeometryPoint)):
               

    def __sub__(self, other_point):

        return GeometryPoint(x = self.x_coord - other_point.x_coord,
                             y = self.y_coord - other_point.y_coord) 

    def __str__(self):
        return '(' + str(self.x_coord) + ', ' + str(self.y_coord) + ')'

    def to_tuple(self):
        return (self.x_coord, self.y_coord)

class test_author:
    id   = None
    name = None

    def __init__(self, id, name):
        self.id   = id
        self.name = name

class test_msg:
    author  = None
    content = None

    def __init__(self, content, aid, aname):
        self.content = content
        self.author  = test_author(aid, aname)

    async def delete (self):
        pass

def test_main():
    from core.content_handlers.game_chat_handler import\
        MessageBlock, ChatHandler

    t_m_1 = test_msg('lolkek\ncheburek', 2, 'Lalkan')
    t_m_2 = test_msg('juoiuo\nqewqeqw',  7, 'Roflan')
    t_m_3 = test_msg('hahah\nqwewqe',    3, 'Tolkan')
    t_m_4 = test_msg('lol', 2, 'Lalkan')
    t_m_5 = test_msg('lol', 6, 'Parkan')
    t_m_6 = test_msg('What the fuck?? hello?\n R u idiots?', 4, 'Jeram')
    t_m_7 = test_msg('idk wtf is this\nmb a joke', 4, 'Jeram')

    messages = [t_m_1, 
                t_m_2, 
                t_m_3, 
                t_m_4, 
                t_m_5, 
                t_m_6, 
                t_m_7, 
    ]

    #mb1 = MessageBlock(t_m_1)
    #mb2 = MessageBlock(t_m_2)
    #mb3 = MessageBlock(t_m_3)
    #mb4 = MessageBlock(t_m_4)
#
    #messages = [mb1, mb2, mb3, mb4]

    #for mb in messages:
    #    print (mb)
    #    print ('    size   ' + str(mb.size) )
    #    print ('    size m ' + str(mb.messages_size) )
#
    #print (mb1.shrink(28))
    #
    #print ('  ')
    #print (mb1)
    #print ('    size   ' + str(mb1.size) )
    #print ('    size m ' + str(mb1.messages_size) )    
    #print ('  ')
    #mb1.append(t_m_2)
    #print (mb1)
    #print ('    size   ' + str(mb1.size) )
    #print ('    size m ' + str(mb1.messages_size) )  
    #print ('  ')
    #print ('Shrink result: ' + str(mb1.shrink(17)))
    #print ('  ')
    #print (mb1)

    ch = ChatHandler(None)

    for msg in messages:
        print(ch.get_chat_str('lohan'))
        print('=============================')
        ch.handle_new_player_message(msg)

    print(ch.get_chat_str('lohan'))


if __name__ == "__main__":
    #my_point   = GeometryPoint(80, 80)
#
    #print ('my_point ', my_point)
    #this_point = GeometryPoint(30, 30)
#
    #print ('this_point ', this_point)
#
    #new_point = my_point - (this_point / 2)
#
    #print('new_point ', new_point)
#
    #print ('new_point tuple', new_point.to_tuple())
    #print (type (new_point.to_tuple()))

    #test_main()

    #SEGMENT_1ST_EMOJI   = '⌛'
    #print (len(SEGMENT_1ST_EMOJI))
    #string = '12345'
#
    #position = 0
#
    #new_character = 'q'
    #
    #print(string)
    #string = string[:position] + new_character + string[position+1:]
#
    #print(string)


    
    #SEGMENT_1ST_EMOJI      = '⌛'
    #SEGMENT_2ND_EMOJI      = '⏳'
    #EXPIRED_SEGMENT_EMOJI  = '✖️'
#
    #timer = Timer(60, None)

    new_q = TaskQueue()

    if new_q.is_empty: print('Q is empty')    
    else: print('Q is not empty')

    new_q.add_task('Lol')
    new_q.add_task('kek')
    new_q.add_task('cheburek')
    
    if new_q.is_empty: print('Q is empty')    
    else: print('Q is not empty')

    for item in new_q.get_tasks():
        print ('item is: ', item)


    if new_q.is_empty: print('Q is empty')    
    else: print('Q is not empty')