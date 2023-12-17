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
    'move_statements',
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
    '''
    finds the most recent file in a directory

    ------
    parameters
    dir_path: str
        directory for the file ending in '...folder/'

    ------
    return
    : str
        full path for most recent file in said directory as '...folder/file.ext'

    '''

    # get a list of all files in the directory
    files = os.listdir(dir_path)
    
    # check if the list is not empty
    if files:
        
        # creates full list
        full_paths = [os.path.join(dir_path, file) for file in files]

        # creates a list of times
        files_with_times = {os.path.getmtime(file_path): file_path for file_path in full_paths}   # TODO: is getmtime the best? getctime was funky.

        print(f'\t most recent selected to be: {files_with_times[max(files_with_times.keys())]}')

        # return the latest file
        return files_with_times[max(files_with_times.keys())]
    else:
        # return None if no files found
        raise FileNotFoundError('could not find a file or folder inside ' + dir_path)






def move_statements():
    """
    moves files from 
    UNSORTED_BANK_STATEMENTS_DIR 
    to their specific bank account folders using
    ACCOUNT_NUMBERS
    """
    print('moving files...')
    # get a list of all files in the directory
    files = os.listdir(ROOT_DIR + UNSORTED_BANK_STATEMENTS_DIR)

    # check if the list is not empty
    for file in files:
        
        print('\tmoving ' + file)
        if file[0:9] in ACCOUNT_NUMBERS.keys():
            
            try:
                # moves the file by renaming
                os.rename(
                    ROOT_DIR + UNSORTED_BANK_STATEMENTS_DIR + file, 
                    ROOT_DIR + BANK_STATEMENTS_DIR + ACCOUNT_NUMBERS[file[0:9]] + '/' + file
                    )
            except FileExistsError:
                print('\t\t file already exists, skipping')

        else:
            print(f"\taccount {file[0:9]} not recognised")

    print('moved all files!')