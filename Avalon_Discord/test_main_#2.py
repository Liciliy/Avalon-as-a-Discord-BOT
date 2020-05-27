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


if __name__ == "__main__":
    paths()