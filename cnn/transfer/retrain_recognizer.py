'''
Created on Jun 28, 2016

Runs retrained neural network for recognition

@author: Levan Tsinadze
'''

import os
import sys

from cnn.transfer.conv_neural_net import conv_net
import tensorflow as tf


class image_recognizer:
  """Recognizes image thru trained neural networks"""
  
  def __init__(self, tr_file):
    self.tr_file = tr_file
    self.labels_path = self.tr_file.get_or_init_labels_path()
    self.model_path = self.tr_file.get_or_init_files_path()

  # Initializes trained neural network graph
  def create_graph(self):
    """Creates a graph from saved GraphDef file and returns a saver."""
    
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(self.model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
        
    return graph_def
  
  # Gets net to recognize
  def get_conv_net(self):
    return conv_net(self.sess, self.labels_path)

  # Attaches session to object
  def set_session(self, sess):
    self.sess = sess
    self.conv_net = self.get_conv_net()
  
  # Initializes image to recognize
  def get_image_data(self, arg_path=None):
    
    if arg_path == None:
      test_image_path = self.tr_file.get_or_init_test_path()
      if not tf.gfile.Exists(test_image_path):
          self.tr_file.get_or_init_test_path()
          tf.logging.fatal('File does not exist %s', test_image_path)
          return None
    else:
      test_dir = self.tr_file.get_or_init_test_dir()
      test_image_path = os.path.join(test_dir, arg_path)
    # Reads image to recognize
    image_data = tf.gfile.FastGFile(test_image_path, 'rb').read()
    
    return image_data
  
  # Generates forward propagation for recognition
  def recognize_image_by_sess(self, image_data=None):
    
    if image_data is None:
      image_data = self.get_image_data()
    if image_data is not None:
      answer = self.conv_net.recognize_image(image_data)
    else:
      answer = {}
    
    return answer
  
  # Generates forward propagation for recognition
  def recognize_image_by_data(self, image_data):
    
    with tf.Session() as sess:
      cn_net = conv_net(sess, self.labels_path)
      print cn_net
      answer = cn_net.recognize_image(image_data)
    
    return answer
  
  # Generates forward propagation for recognition
  def recognize_image(self, arg_path=None):
      
    answer = {}

    image_data = self.get_image_data(arg_path)
    if image_data is not None:
      answer = self.recognize_image_by_data(image_data)
    
    return answer
  
  # Initializes graph and generates forward propagation for recognition
  def run_inference_on_image(self, arg_path=None):
      
    answer = {}

    image_data = self.get_image_data(arg_path)
    if image_data != None:
    # Creates graph from saved GraphDef
      self.create_graph()
      answer = self.recognize_image_by_data(image_data)
    
    return answer

if __name__ == '__main__':
  
    # Gets image path from arguments
    img_recognizer = image_recognizer()
    if len(sys.argv) > 1:
      test_img_path = sys.argv[1]
    else:
      test_img_path = None
    img_recognizer.run_inference_on_image(test_img_path)
