''''
main python file for importing the python code



'''
import json
import os

from .constants import *
from .statements import *

__all__ = [
    'constants',
    'statements',
    'json_save',
    'json_read',
    'text_save',
]



#   █▀▀▀▄ █▀▀▀ ▄▀▀▀▄ █▀▀▀▄    ▄▀▀▀▄ █▄    █ █▀▀▀▄    █     █ █▀▀▀▄ ▀▀█▀▀ ▀▀█▀▀ █▀▀▀    █▀▀▀ ▀▀█▀▀ █    █▀▀▀ ▄▀▀▀▀ 
#   █▄▄▄▀ █▄▄  █▄▄▄█ █   █    █▄▄▄█ █ ▀▄  █ █   █    █  ▄  █ █▄▄▄▀   █     █   █▄▄     █▄▄    █   █    █▄▄  ▀▄▄▄  
#   █  ▀█ █    █   █ █   █    █   █ █   ▀▄█ █   █    █ █ █ █ █  ▀█   █     █   █       █      █   █    █        █ 
#   ▀   ▀ ▀▀▀▀ ▀   ▀ ▀▀▀▀     ▀   ▀ ▀     ▀ ▀▀▀▀      ▀   ▀  ▀   ▀ ▀▀▀▀▀   ▀   ▀▀▀▀    ▀    ▀▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀  
#
#   █ █▀ █▀█ █▄ █    █▀█ █▀▀ ▄▀█ █▀▄ 
# █▄█ ▄█ █▄█ █ ▀█ ▄▄ █▀▄ ██▄ █▀█ █▄▀ 
# 
def json_read(dir: str) -> dict:
    '''
    simplifies reading a json file
    
    #### Parameters
    <!------------>
    dir: str
        directory for json file to be read
    
    #### Returns
    <!---------->
    : dict
        dictionary representing read json file
        
    --------
    '''
    
    with open(dir, 'r') as file:
        object = json.load(file)

    return object

#   █ █▀ █▀█ █▄ █    █▀ ▄▀█ █ █ █▀▀ 
# █▄█ ▄█ █▄█ █ ▀█ ▄▄ ▄█ █▀█ ▀▄▀ ██▄ 
# 
def json_save(object: dict, dir: str):
    '''
    simplifies saving a json file
    
    #### Parameters
    <!------------>
    object : dict
        dictionary to be save to json file

    dir: str
        directory for json file to be saved to
    
    --------
    '''
    with open(dir, 'w', encoding='utf-8') as file:
        json.dump(object, file, ensure_ascii=False, indent=4)
        
# ▀█▀ █▀▀ ▀▄▀ ▀█▀    █▀ ▄▀█ █ █ █▀▀ 
#  █  ██▄ █ █  █  ▄▄ ▄█ █▀█ ▀▄▀ ██▄ 
# 
def text_save(object: dict, dir: str):
    '''
    simplifies saving a text file
    
    #### Parameters
    <!------------>
    object : dict
        object to turn into text and same

    dir: str
        directory for json file to be saved to
    
    --------
    '''
    with open(dir, 'w', encoding='utf-8') as file:
        file.write (str(object))
        file.close()



#  █▀ █▀▀ █   █▀▀ █▀▀ ▀█▀   █▀▄▀█ █▀█ █▀ ▀█▀   █▀█ █▀▀ █▀▀ █▀▀ █▄ █ ▀█▀ 
#  ▄█ ██▄ █▄▄ ██▄ █▄▄  █    █ ▀ █ █▄█ ▄█  █    █▀▄ ██▄ █▄▄ ██▄ █ ▀█  █  
#  
def select_most_recent(dir_path: str):

    # get a list of all files in the directory
    files = os.listdir(dir_path)
    
    # check if the list is not empty
    if files:
        
        # creates full list
        full_paths = [os.path.join(dir_path, file) for file in files]

        # creates a list of times
        files_with_times = {os.path.getctime(file_path): file_path for file_path in full_paths}
        
        # return the latest file
        return files_with_times[max(files_with_times.keys())]
    else:
        # return None if no files found
        raise FileNotFoundError('could not find a file or folder inside ' + dir_path)