'''
Created on Jun 28, 2016

Runs retrain neural network for recognition

@author: Levan Tsinadze
'''

import numpy as np
import tensorflow as tf
from cnn_files import training_file
from cnn.transfer.retrain_recognizer import image_recognizer

# Runs image recognizer
if __name__ == '__main__':
  
  dirs_fls = training_file()
  img_recognizer = image_recognizer(dirs_fls)
  img_recognizer.run_inference_on_image()
