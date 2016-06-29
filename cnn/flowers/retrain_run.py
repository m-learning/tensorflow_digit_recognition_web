'''
Created on Jun 28, 2016

Runs retrain neural network for recognition

@author: Levan Tsinadze
'''

import numpy as np
import tensorflow as tf
from cnn.flowers.cnn_files import training_file

# Initializes trained neural network graph
def create_graph(model_path):
  
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

# Generates forward propagation for recognition
def run_inference_on_image():
    
    answer = None

    tr_file = training_file()
    test_image_path = tr_file.get_or_init_test_path()
    if not tf.gfile.Exists(test_image_path):
        tf.logging.fatal('File does not exist %s', test_image_path)
        return answer

    image_data = tf.gfile.FastGFile(test_image_path, 'rb').read()

    # Creates graph from saved GraphDef
    model_path = tr_file.get_or_init_files_path()
    create_graph(model_path)

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
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))

        answer = labels[top_k[0]]
        return answer


if __name__ == '__main__':
    run_inference_on_image()
