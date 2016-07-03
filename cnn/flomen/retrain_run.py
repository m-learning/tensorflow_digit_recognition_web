'''
Created on Jun 28, 2016

Runs retrained neural network for recognition

@author: Levan Tsinadze
'''

import sys
import os

import numpy as np
import tensorflow as tf
from cnn_files import training_file

# Recognizes image thru trained neural networks
class image_recognizer:

  # Initializes trained neural network graph
  def create_graph(self, model_path):
    
      """Creates a graph from saved GraphDef file and returns a saver."""
      # Creates graph from saved graph_def.pb.
      with tf.gfile.FastGFile(model_path, 'rb') as f:
          graph_def = tf.GraphDef()
          graph_def.ParseFromString(f.read())
          _ = tf.import_graph_def(graph_def, name='')
  
  # Generates forward propagation for recognition
  def run_inference_on_image(self, arg_path=None):
      
      answer = None
  
      tr_file = training_file()
      if arg_path == None:
        test_image_path = tr_file.get_or_init_test_path()
        if not tf.gfile.Exists(test_image_path):
            tr_file.get_or_init_test_path
            tf.logging.fatal('File does not exist %s', test_image_path)
            return answer
      else:
        test_dir = tr_file.get_or_init_test_dir()
        test_image_path = os.path.join(test_dir, arg_path)
  
      # Reads image to recognize
      image_data = tf.gfile.FastGFile(test_image_path, 'rb').read()
  
      # Creates graph from saved GraphDef
      model_path = tr_file.get_or_init_files_path()
      self.create_graph(model_path)
  
      # initializes labels path
      labels_path = tr_file.get_or_init_labels_path()
      with tf.Session() as sess:
  
          softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
          predictions = sess.run(softmax_tensor,
                                 {'DecodeJpeg/contents:0': image_data})
          predictions = np.squeeze(predictions)
  
          top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions
          f = open(labels_path, 'rb')
          lines = f.readlines()
          labels = [str(w).replace("\n", "") for w in lines]
          answer = []
          for node_id in top_k:
              human_string = labels[node_id]
              score = predictions[node_id]
              answer.append((human_string, score))
              print('%s (score = %.5f)' % (human_string, score))
          
          return answer

if __name__ == '__main__':
  
    # Gets image path from arguments
    img_recognizer = image_recognizer()
    if len(sys.argv) > 1:
      test_img_path = sys.argv[1]
    else:
      test_img_path = None
    img_recognizer.run_inference_on_image(test_img_path)
