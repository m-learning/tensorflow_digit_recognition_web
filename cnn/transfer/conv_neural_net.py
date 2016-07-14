'''
Created on Jul 3, 2016

Runs neural network for recognition

@author: Levan Tsinadze
'''

import numpy as np

FINAL_RESULTS = 'final_result:0'
DECODE_CONTENTS = 'DecodeJpeg/contents:0'

# Image recognizer neural network
class conv_net(object):
  
  def __init__(self, sess, labels_path):
    self.sess = sess
    self.labels_path = labels_path
    
    
  # Runs image recognition thru neural network
  def recognize_image(self, image_data):
    
    answer = {}
    
    softmax_tensor = self.sess.graph.get_tensor_by_name(FINAL_RESULTS)
    image_dict = {DECODE_CONTENTS: image_data}
    predictions = self.sess.run(softmax_tensor, image_dict)
    predictions = np.squeeze(predictions)

    top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions
    f = open(self.labels_path, 'rb')
    lines = f.readlines()
    labels = [str(w).replace("\n", "") for w in lines]
    for node_id in top_k:
        human_string = labels[node_id]
        score = predictions[node_id]
        answer[human_string] = score
        print('%s (score = %.5f)' % (human_string, score))
    
    return answer
