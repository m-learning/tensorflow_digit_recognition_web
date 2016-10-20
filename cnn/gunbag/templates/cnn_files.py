'''
Created on Jun 21, 2016

Files for training data

@author: Levan Tsinadze
'''

import os

from cnn.utils.file_utils import cnn_file_utils

# Files and directories for parameters (trained), training, validation and test
class training_file(cnn_file_utils):

    def __init__(self):
      super(self, training_file).__init__('flowers')
