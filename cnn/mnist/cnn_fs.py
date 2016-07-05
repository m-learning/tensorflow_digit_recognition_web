'''
Created on Jun 21, 2016

Files for training data

@author: Levan Tsinadze
'''

import os

# Constants for files
PATH_CNN_DIRECTORY = os.path.join('datas', 'mnist')
PATH_FOR_PARAMETERS = 'trained_data'
PATH_TO_RECOGNIZE = 'to_recognize'
WEIGHTS_FILE = 'conv_model.ckpt'
TO_RECOGNIZE_FILE = 'torecogn'

# File manager
class parameters_file:
  
  # Joins path from method
  def join_path(self, path_func, *other_path):
    
    result = None
    
    init_path = path_func()
    result = os.path.join(init_path, *other_path)
    
    return result
  
  # Gets current directory of script
  def get_current(self):
      
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    dirs = os.path.split(current_dir)
    dirs = os.path.split(dirs[0])
    current_dir = dirs[0]
    
    return current_dir
  
  # Gets directory path for images to recognize
  def get_to_recognize_directory(self):
      
    current_dir = self.join_path(self.get_current, PATH_CNN_DIRECTORY, PATH_TO_RECOGNIZE)
    
    if not os.path.exists(current_dir):
      os.makedirs(current_dir)
    
    return current_dir   
  
  # Gets file path for images to recognize
  def get_to_recognize_file(self):
    return self.join_path(self.get_to_recognize_directory, TO_RECOGNIZE_FILE)
  
  # Gets training data  / parameters directory path
  def get_files_directory(self):
    return self.join_path(self.get_current, PATH_CNN_DIRECTORY,
                               PATH_FOR_PARAMETERS, WEIGHTS_FILE)
