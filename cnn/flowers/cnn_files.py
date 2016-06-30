'''
Created on Jun 21, 2016

Files for training data

@author: Levan Tsinadze
'''

import gzip
import os
import re
import sys
import tarfile
import shutil

from six.moves import urllib

PATH_CNN_DIRECTORY = '/datas/flowers/'
PATH_FOR_PARAMETERS = 'trained_data/'
PATH_FOR_TRAINING = 'training_data/'
PATH_FOR_TRAINING_PHOTOS = 'flower_photos/'
WEIGHTS_FILE = 'output_graph.pb'
LABELS_FILE = 'output_labels.txt'
TEST_IMAGES_DIR = 'test_images/'
TEST_IMAGE_NAME = 'test_image'

TRAINIG_SET_URL = 'http://download.tensorflow.org/example_images/flower_photos.tgz'
TRAINIG_ZIP_FOLDER = 'training_arch'

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
      current_dir += PATH_CNN_DIRECTORY
      
      return current_dir
    
    def get_training_directory(self):
      
      current_dir = self.get_data_general_directory()
      current_dir += PATH_FOR_TRAINING
      
      return current_dir
      
    
    # Gets directory for training set and parameters
    def get_data_directory(self):
        
      current_dir = self.get_training_directory()
      current_dir += PATH_FOR_TRAINING_PHOTOS
      
      return current_dir
    
    # Gets or creates directory for trained parameters
    def init_files_directory(self):
        
      current_dir = self.get_data_general_directory()
      
      current_dir += PATH_FOR_PARAMETERS
      if not os.path.exists(current_dir):
          os.makedirs(current_dir)
      
      return current_dir
    
    # Gets training data  / parameters directory path
    def get_or_init_files_path(self):
        
      current_dir = self.init_files_directory()
      current_dir += WEIGHTS_FILE
      
      return current_dir
      
    # Gets training data  / parameters directory path
    def get_or_init_labels_path(self):
        
      current_dir = self.init_files_directory()
      current_dir += LABELS_FILE
      
      return current_dir
    
    # Gets directory for test images
    def get_or_init_test_dir(self):
      
      current_dir = self.get_data_general_directory()
      current_dir += TEST_IMAGES_DIR
      if not os.path.exists(current_dir):
        os.mkdir(current_dir)  
      
      return current_dir
      
    # Gets or initializes test image
    def get_or_init_test_path(self):
        
      current_dir = self.get_or_init_test_dir()
      current_dir += TEST_IMAGE_NAME
      
      return current_dir
    
    # Gets or generates training set
    def get_or_init_training_set(self):
      
      dest_directory = self.get_data_general_directory()
      dest_directory += TRAINIG_ZIP_FOLDER
      
      if not os.path.exists(dest_directory):
        os.mkdir(dest_directory)  
      
      filename = TRAINIG_SET_URL.split('/')[-1]
      filepath = os.path.join(dest_directory, filename)
      if not os.path.exists(filepath):
        def _progress(count, block_size, total_size):
          sys.stdout.write('\r>> Downloading %s %.1f%%' % (filename, float(count * block_size) / float(total_size) * 100.0))
          sys.stdout.flush()
        filepath, _ = urllib.request.urlretrieve(TRAINIG_SET_URL, filepath, _progress)
      print()
      statinfo = os.stat(filepath)
      print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
      training_dir = self.get_training_directory()
      if not os.path.exists(training_dir):
        os.mkdir(training_dir)  
      else:
        shutil.rmtree(training_dir, ignore_errors=True)
        os.mkdir(training_dir)
      tarfile.open(filepath, 'r:gz').extractall(training_dir)
