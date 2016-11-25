"""
Created on Jun 28, 2016

Runs retrained neural network for recognition

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
import os
import sys

from tensorflow.python.framework.errors import InvalidArgumentError

from cnn.transfer import cnn_flags as flags
from cnn.transfer.conv_neural_net import conv_net
from cnn.utils.pillow_resizing import pillow_resizer
from cnn.utils import image_utils as crop
import tensorflow as tf


try:
  from PIL import Image
except ImportError:
  print("Importing Image from PIL threw exception")
  import Image

IMAGE_RGB_FORMAT = 'RGB'
IMAGE_SAVE_FORMAT = 'jpeg'

resizer = pillow_resizer(299)

class image_recognizer:
  """Recognizes image thru trained neural networks"""
  
  def __init__(self, cnn_files_const):
    self._tr_file = cnn_files_const()
    self.labels_path = flags.output_labels
    self.model_path = flags.output_graph
  
  @property 
  def cnn_files(self):
    return self._tr_file

  def create_graph(self):
    """Creates a graph from saved GraphDef file and returns a saver."""
    
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(self.model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
        
    return graph_def
  
  def get_conv_net(self):
    """Gets net to recognize"""
    return conv_net(self.sess, self.labels_path)

  def set_session(self, sess):
    """Attaches session to object
      Args:
        sess - current TensorFlow session
    """
    self.sess = sess
    self.conv_net = self.get_conv_net()
  
  def get_image_data(self, arg_path=None):
    """Initializes image to recognize
      Args:
        arg_path - arguments path
      Return:
        image_data - image for prediction
    """
    
    if arg_path == None:
      test_image_path = self._tr_file.get_or_init_test_path()
      if not tf.gfile.Exists(test_image_path):
          self._tr_file.get_or_init_test_path()
          tf.logging.fatal('File does not exist %s', test_image_path)
          return None
    else:
      test_dir = self._tr_file.get_or_init_test_dir()
      test_image_path = os.path.join(test_dir, arg_path)
    # Reads image to recognize
    image_data = tf.gfile.FastGFile(test_image_path, 'rb').read()
    
    return image_data
  
  def to_byte_array(self, jpg_im):
    """Converts image to byte Array
      Args:
        jpg_im - image
      Return:
        img_array - byte array of image
    """
    
    img_bytes = io.BytesIO()
    jpg_im.save(img_bytes, format=IMAGE_SAVE_FORMAT)
    im_arr = img_bytes.getvalue()
    
    return im_arr
  
  def binarize_and_run(self, im):
    """Converts image to binary format 
       and runs prediction
      Args:
        im - image
      Returns:
        answer - prediction result
    """
    
    im_arr = self.to_byte_array(im)
    answer = self.conv_net.recognize_image(im_arr)
    
    return answer
    
  def convert_image(self, image_data=None):
    """Converts passed image to JPG format
      Args:
        image_data binary image
      Returns:
        jpg_im - converted image
    """
    
    im = Image.open(io.BytesIO(image_data))
    jpg_im = im.convert(IMAGE_RGB_FORMAT)
    
    return jpg_im
  
  def convert_and_recognize_image(self, image_data=None):
    """Converts image to JPG and recognizes with exception
      Args: 
        image_data - image
      Return:
        answer - prediction result
    """
    im = Image.open(io.BytesIO(image_data))
    jpg_im = im.convert(IMAGE_RGB_FORMAT)
    img = resizer.resize_thumbnail(jpg_im)
    answer = self.binarize_and_run(img)
    
    return answer
  
  def resize_image(self, image_data):
    """Resizes image for recognition
      Args:
        image_data - binary image
      Returns:
        img - resized image
    """
    
    im = Image.open(io.BytesIO(image_data))
    if flags.box_images:
      img_to_resize = crop.crop_image(im)
    else:
      img_to_resize = im
    img = resizer.resize_thumbnail(img_to_resize)
    
    return img
  
  def resize_and_recognize(self, image_data):
    """Resizes image and recognizes
      Args:
        image_data - binary image
      Returns:
        answer - prediction result
    """
    
    img = self.resize_image(image_data)
    answer = self.binarize_and_run(img)
    
    return answer
    
    
  
  def recognize_image_quietly(self, image_data=None):
    """Recognizes image with exception
      Args: 
        image_data - image
      Return:
        answer - prediction result
    """
    
    try:
      answer = self.resize_and_recognize(image_data)
    except (InvalidArgumentError, IOError):
      answer = self.convert_and_recognize_image(image_data)
    
    return answer
  
  def recognize_image_by_sess(self, image_data=None):
    """Generates forward propagation for recognition
      Args:
        image_data - image parameters
      Returns:
        answer - prediction result
    """
    
    if image_data is None:
      image_data = self.get_image_data()
    if image_data is not None:
      answer = self.recognize_image_quietly(image_data)
    else:
      answer = {}
      
    return answer
  
  def recognize_image_by_data(self, image_data):
    """Generates forward propagation for recognition
      Args:
        image_data - image parameters
      Returns:
        answer - prediction result
    """
    
    with tf.Session() as sess:
      cn_net = conv_net(sess, self.labels_path)
      print(cn_net)
      answer = cn_net.recognize_image(image_data)
    
    return answer
  
  def recognize_image(self, arg_path=None):
    """Generates forward propagation for recognition
      Args:
        arg_path - command line parameters
      Returns:
        answer - prediction result
    """
      
    answer = {}

    image_data = self.get_image_data(arg_path)
    if image_data is not None:
      answer = self.recognize_image_by_data(image_data)
    
    return answer
  
  def run_inference_on_image(self, arg_path=None):
    """Initializes graph and generates forward propagation for recognition
      Args:
        arg_path - command line parameters
      Returns:
        answer - prediction result
    """
      
    answer = {}

    image_data = self.get_image_data(arg_path)
    if image_data != None:
    # Creates graph from saved GraphDef
      self.create_graph()
      answer = self.recognize_image_by_data(image_data)
    
    return answer

if __name__ == '__main__':
  """Runs image recognition on specified file"""
  
  # Gets image path from arguments
  img_recognizer = image_recognizer()
  if len(sys.argv) > 1:
    test_img_path = sys.argv[1]
  else:
    test_img_path = None
  img_recognizer.run_inference_on_image(test_img_path)
