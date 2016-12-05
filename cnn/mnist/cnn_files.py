"""
Created on Jun 21, 2016

Files for training data

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from cnn.utils.file_utils import files_and_path_utils


# Constants for files
PATH_FOR_PARAMETERS = 'trained_data'
PATH_TO_RECOGNIZE = 'to_recognize'
WEIGHTS_FILE = 'conv_model.ckpt'
TO_RECOGNIZE_FILE = 'torecogn'

class parameters_file(files_and_path_utils):
  """Files and directories manager"""
  
  def __init__(self):
    super(parameters_file, self).__init__('mnist')
  
  def get_to_recognize_directory(self):
    """Gets directory path for images to recognize
      Returns:
        current_dir - directory path
    """
      
    current_dir = self.join_path(self.get_current, self.path_to_cnn_directory, PATH_TO_RECOGNIZE)
    
    if not os.path.exists(current_dir):
      os.makedirs(current_dir)
    
    return current_dir   
  
  def get_to_recognize_file(self):
    """Gets file path for images to recognize
      Returns:
        file path
    """
    return self.join_path(self.get_to_recognize_directory, TO_RECOGNIZE_FILE)
  
  def get_files_directory(self):
    """Gets training data  / parameters directory path
      Returns:
        training data and parameters path
    """
    return self.join_path(self.get_current, self.path_to_cnn_directory,
                               PATH_FOR_PARAMETERS, WEIGHTS_FILE)
