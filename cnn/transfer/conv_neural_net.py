"""
Created on Jul 3, 2016

Model of neural network for image recognition

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np


FINAL_RESULTS = 'final_result:0'
DECODE_CONTENTS = 'DecodeJpeg/contents:0'
DROPOUT_KEY = 'final_training_ops/dropout/Placeholder:0'

KEEP_ALL_PROB = 1.0

softmax_tensor = None
label_array = None

def init_softmax_tensor(sess):
  """Initializes final tensor to run
    Args:
      sess - current TensorFlow session
  """
  
  if softmax_tensor is None:
    global softmax_tensor
    softmax_tensor = sess.graph.get_tensor_by_name(FINAL_RESULTS)
    
def init_labels(labels_path):
  """Initializes labels array
    Args:
      labels_path - path to labels file
  """
  
  if label_array is None:
    global label_array
    f = open(labels_path, 'rb')
    lines = f.readlines()
    label_array = [str(w).replace("\n", "") for w in lines]

class conv_net(object):
  """Image recognizer class through Inception-V3 network model"""
  
  def __init__(self, sess, labels_path):
    self.sess = sess
    self.labels_path = labels_path
    
    
  def recognize_image(self, image_data):
    """Runs image recognizer
      Args:
        image_data - image parameters
      Returns:
        answer - recognition results
    """
    
    answer = {}
    
    init_softmax_tensor(self.sess)
    init_labels(self.labels_path)
    image_dict = {DECODE_CONTENTS: image_data,
                  DROPOUT_KEY: KEEP_ALL_PROB}
    predictions = self.sess.run(softmax_tensor, image_dict)
    predictions = np.squeeze(predictions)
    # Getting top 5 predictions
    top_k = predictions.argsort()[-5:][::-1]
    for node_id in top_k:
        human_string = label_array[node_id]
        score = predictions[node_id]
        answer[human_string] = score
        print('%s (score = %.5f)' % (human_string, score))
    
    return answer
