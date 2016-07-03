'''
Created on Jun 21, 2016

Files for training data

@author: Levan Tsinadze
'''

import os
import shutil
import requests

# Files and directory constant parameters
PATH_CNN_DIRECTORY = os.path.join('datas', 'flomen')
PATH_FOR_PARAMETERS = 'trained_data'
WEIGHTS_FILE = 'output_graph.pb'
LABELS_FILE = 'output_labels.txt'
TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_NAME = 'test_image'

# Files and directories for parameters (trained), training, validation and test
class training_file:
    
    # Gets current directory of script
    def get_current(self):
        
      current_dir = os.path.dirname(os.path.realpath(__file__))
      
      dirs = os.path.split(current_dir)
      dirs = os.path.split(dirs[0])
      current_dir = dirs[0]
      
      return current_dir
    
    # Gets or creates directories
    def get_data_general_directory(self):
      
      current_dir = self.get_current()
      current_dir = os.path.join(current_dir, PATH_CNN_DIRECTORY)
      
      return current_dir
    
    # Gets or creates directory for trained parameters
    def init_files_directory(self):
        
      current_dir = self.get_data_general_directory()
      
      current_dir = os.path.join(current_dir, PATH_FOR_PARAMETERS)
      if not os.path.exists(current_dir):
          os.makedirs(current_dir)
      
      return current_dir
    
    # Gets training data  / parameters directory path
    def get_or_init_files_path(self):
        
      current_dir = self.init_files_directory()
      current_dir = os.path.join(current_dir, WEIGHTS_FILE)
      
      return current_dir
      
    # Gets training data  / parameters directory path
    def get_or_init_labels_path(self):
        
      current_dir = self.init_files_directory()
      current_dir = os.path.join(current_dir, LABELS_FILE)
      
      return current_dir
    
    # Gets directory for test images
    def get_or_init_test_dir(self):
      
      current_dir = self.get_data_general_directory()
      current_dir = os.path.join(current_dir, TEST_IMAGES_DIR)
      if not os.path.exists(current_dir):
        os.mkdir(current_dir)  
      
      return current_dir
      
    # Gets or initializes test image
    def get_or_init_test_path(self):
        
      current_dir = self.get_or_init_test_dir()
      current_dir = os.path.join(current_dir, TEST_IMAGE_NAME)
      
      return current_dir
    
    # Downloads file from passed URL address
    def get_file_to_recognize(self, file_url):
      
      response = requests.get(file_url, stream=True)
      test_img_path = self.get_or_init_test_path()
      with open(test_img_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
      del response
