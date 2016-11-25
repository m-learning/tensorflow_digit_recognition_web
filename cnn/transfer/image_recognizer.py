"""
Created on Jun 28, 2016

Runs retrained neural network for recognition

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from cnn.transfer.cnn_files import training_file
from cnn.transfer.recognizer_interface import image_recognizer


if __name__ == '__main__':
  """Starts image recognition service"""
  
  dirs_files = training_file()
  img_recognizer = image_recognizer(dirs_files)
  img_recognizer.run_inference_on_image()
