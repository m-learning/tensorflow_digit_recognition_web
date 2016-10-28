"""
Created on Jul 6, 2016

Utility class for evaluation files and directories

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import requests
import shutil
import types


# General parent directory for files
DATAS_DIR_NAME = 'datas'

# Files and directory constant parameters
PATH_FOR_PARAMETERS = 'trained_data'
WEIGHTS_FILE = 'output_graph.pb'
LABELS_FILE = 'output_labels.txt'
TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_NAME = 'test_image'

class files_and_path_utils(object):
  """Utility class for file management
  """
  
  def __init__(self, parent_cnn_dir):
    self.path_to_cnn_directory = os.path.join(DATAS_DIR_NAME, parent_cnn_dir)
    
  # Joins path from method
  def join_path(self, path_inst, *other_path):
    """Joins passed file paths
      Args:
        paths_inst - function to get path string
                     or path string itself
        *other_path - paths to join varargs
      Return:
        result - joined paths
    """
    
    if isinstance(path_inst, types.StringType):
      init_path = path_inst
    else:
      init_path = path_inst()
    result = os.path.join(init_path, *other_path)
    
    return result
  
  # Gets current directory of script
  def get_current(self):
      
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    dirs = os.path.split(current_dir)
    dirs = os.path.split(dirs[0])
    current_dir = dirs[0]
    
    return current_dir
  

# Utility class for training and testing files and directories
class cnn_file_utils(files_and_path_utils):
  """Utility class for network files management"""
  
  def __init__(self, parent_cnn_dir):
    super(cnn_file_utils, self).__init__(parent_cnn_dir)
  
  # Gets or creates directories
  def get_data_general_directory(self):
    return self.join_path(self.get_current, self.path_to_cnn_directory)

  # Gets or creates directory for trained parameters
  def init_files_directory(self):
      
    current_dir = self.join_path(self.get_data_general_directory, PATH_FOR_PARAMETERS)
    
    if not os.path.exists(current_dir):
        os.makedirs(current_dir)
    
    return current_dir

  # Initializes trained files path
  def get_or_init_files_path(self):
    return self.join_path(self.init_files_directory, WEIGHTS_FILE)
      
  # Gets training data  / parameters directory path
  def get_or_init_labels_path(self):
    return self.join_path(self.init_files_directory, LABELS_FILE)

  # Gets directory for test images
  def get_or_init_test_dir(self):
    
    current_dir = self.join_path(self.get_data_general_directory, TEST_IMAGES_DIR)
    
    if not os.path.exists(current_dir):
      os.mkdir(current_dir)  
    
    return current_dir
    
  # Gets or initializes test image
  def get_or_init_test_path(self):
    return self.join_path(self.get_or_init_test_dir, TEST_IMAGE_NAME)
  
  # Reads data binary from URL address
  def get_file_bytes_to_recognize(self, file_url):
    
    response = requests.get(file_url, stream=True)
    buff = response.raw.read()
    del response
    
    return buff
    
  def get_file_to_recognize(self, file_url):
    """Downloads file from passed URL address
      Args:
        file_url - file URL address
      Return:
        response - file as byte array
    """
    
    response = requests.get(file_url, stream=True)
    test_img_path = self.get_or_init_test_path()
    with open(test_img_path, 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)
    del response
