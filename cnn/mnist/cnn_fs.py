'''
Created on Jun 21, 2016

Files for training data

@author: Levan Tsinadze
'''

import os


PATH_CNN_DIRECTORY = '/datas/mnist/'
PATH_FOR_PARAMETERS = 'trained_data/'
PATH_TO_RECOGNIZE = 'to_recognize/'
WEIGHTS_FILE = 'conv_model.ckpt'
TO_RECOGNIZE_FILE = 'torecogn'

# File manager
class parameters_file:
    
    # Gets current directory of script
    def get_current(self):
        
        current_dir = os.path.dirname(os.path.realpath(__file__))
        
        dirs = os.path.split(current_dir)
        for _ in range(1):
            dirs = os.path.split(dirs[0])
        current_dir = dirs[0]
        
        return current_dir
    
    # Gets directory path for images to recognize
    def get_to_recognize_directory(self):
        
        current_dir = self.get_current()
        
        current_dir += PATH_CNN_DIRECTORY 
        current_dir += PATH_TO_RECOGNIZE
        
        return current_dir   
    
    # Gets file path for images to recognize
    def get_to_recognize_file(self):
        
        current_dir = self.get_to_recognize_directory()
        current_dir += TO_RECOGNIZE_FILE 
        
        return current_dir        
    
    # Gets training data  / parameters directory path
    def get_files_directory(self):
        
        current_dir = self.get_current()
        
        current_dir += PATH_CNN_DIRECTORY 
        current_dir += PATH_FOR_PARAMETERS
        current_dir += WEIGHTS_FILE
        
        return current_dir
