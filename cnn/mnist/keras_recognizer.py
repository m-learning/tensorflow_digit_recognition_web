"""
Created on Jan 22, 2017

Network implementation for MNIST by Keras library

@author: Levan Tsinadze
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from keras import backend as K
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.models import Sequential

from cnn.mnist.cnn_files import parameters_file
from cnn.mnist.cnn_input_reader import read_input_file
import tensorflow as tf


nb_input = 784
nb_classes = 10
nb_epoch = 12

# input image dimensions
img_rows, img_cols = 28, 28
# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
pool_size = (2, 2)
# convolution kernel size
kernel_size = (3, 3)

WEIGHTS_FILE = 'keras_weights.h5'

_files = parameters_file()
weights_path = _files.join_path(_files.model_dir, WEIGHTS_FILE)
input_shape = (img_rows, img_cols, 1)

class mnist_model(object):
  """Defines MNIST network model"""
  
  def __init__(self, is_training=False):
    self._is_training = is_training
    self.model = None
    
  @property
  def sess(self):
    """Gets TensorFlow current session
      Returns:
        TensorFlow current session
    """
    return self._sess
  
  @sess.setter
  def sess(self, _sess):
    """Sets TensorFlow session
      Args:
        sess - TensorFlow current session
    """
    self._sess = _sess 
    
  def _add_dropout(self, prob=0.5):
    """Adds dropout layer to model
      Args:
        prob - keep probability
    """
    if self._is_training:
      self.model.add(Dropout(prob))
  
  def _init_model(self):
    """Defines MNIST network model"""
    self.model = Sequential()

    self.model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                          border_mode='valid',
                          input_shape=input_shape))
    self.model.add(Activation('relu'))
    self.model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    self.model.add(Activation('relu'))
    self.model.add(MaxPooling2D(pool_size=pool_size))
    self._add_dropout(prob=0.25)
    
    self.model.add(Flatten())
    self.model.add(Dense(128))
    self.model.add(Activation('relu'))
    self._add_dropout(prob=0.5)
    self.model.add(Dense(nb_classes))
    self.model.add(Activation('softmax'))
    
  @property
  def network_model(self):
    """Gets MNIST network model
      Returns:
        network model
    """
    
    if self.model is None:
      self._init_model()
    
    return self.model
  
  def _load_model_and_weights(self):
    """Gets MNIST network model and loads weights
      Returns:
        network model
    """
    if self.model is None:
      self._is_training = False
      self._init_model()
      self.model.load_weights(weights_path)
    
    return self.model    
  
  def run_model(self, x):
    """Runs model interface
      Args:
        x - model input
      Returns:
        pred - model predictions
    """
    _network_model = self._load_model_and_weights()
    pred = _network_model(x)
    
    return pred

def define_graph(_model):
  """Initializes graph operation for network
    Args:
      _model - network model
    Returns:
      tuple of -
        x - input tensor
        _pred - prediction operation
  """
  
  x = tf.placeholder(tf.float32, [None, nb_input])
  _rs = tf.reshape(x, shape=[-1, 28, 28, 1])
  # Convolutional network
  _net = _model.network_model
  _pred = _net(_rs)
  _rec = K.argmax(_pred, 1) 
    
  return (x, _rec)
  
def recognize_image(_model, _files, x, _rec):
    
  # x = tf.placeholder(tf.float32, [None, nb_input])
  # x = tf.reshape(x, shape=[-1, 28, 28, 1])
  # Convolutional network
  # pred = _model.network_model(x)
  
  # Evaluate model
  # recognize_image = K.argmax(_pred, 1)
  # Initializing saver to read trained data
  image_directory = _files.get_to_recognize_file()
          
  print('Start session')
  # Initialize variables
  image_rec = read_input_file(image_directory)
    # Recognize image
  resp_dgt = _model.sess.run(_rec, feed_dict={x: image_rec})
  print("Recognized image:", resp_dgt[0])
  
  return resp_dgt[0]
