import os
import inspect

IMAGES_DIRECTORY = r'images\text.png'

IMAGE_NEEDED = 'text.png'

from pathlib import Path

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



if __name__ == "__main__":
    my_point   = GeometryPoint(80, 80)

    print ('my_point ', my_point)
    this_point = GeometryPoint(30, 30)

    print ('this_point ', this_point)

    new_point = my_point - (this_point / 2)

    print('new_point ', new_point)

    print ('new_point tuple', new_point.to_tuple())
    print (type (new_point.to_tuple()))