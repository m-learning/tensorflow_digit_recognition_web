'''
Created on Jun 28, 2016

Runs retrained neural network for recognition

@author: Levan Tsinadze
'''

from cnn.transfer.recognizer_interface import image_recognizer
from cnn_files import training_file


if __name__ == '__main__':
  """Starts image recognizer service"""
  
  dirs_files = training_file()
  img_recognizer = image_recognizer(dirs_files)
  img_recognizer.run_inference_on_image()
