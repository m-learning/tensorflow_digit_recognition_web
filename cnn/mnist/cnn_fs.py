'''
Created on Jun 21, 2016

Files for training data

@author: Levan Tsinadze
'''

import os

from cnn.utils.file_utils import files_and_path_utils

# Constants for files
PATH_FOR_PARAMETERS = 'trained_data'
PATH_TO_RECOGNIZE = 'to_recognize'
WEIGHTS_FILE = 'conv_model.ckpt'
TO_RECOGNIZE_FILE = 'torecogn'

# File manager
class parameters_file(files_and_path_utils):
  
  def __init__(self):
    super(parameters_file, self).__init__('mnist')
  
  # Gets directory path for images to recognize
  def get_to_recognize_directory(self):
      
    current_dir = self.join_path(self.get_current, self.path_to_cnn_directory, PATH_TO_RECOGNIZE)
    
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
