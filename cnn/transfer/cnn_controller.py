"""
Created on Jun 25, 2016
Controller module for recognition
@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import Flask, request

from cnn.transfer import cnn_flags as flags
from cnn.transfer import cnn_interface_controller as controller
from cnn.transfer.cnn_files import training_file
from cnn.transfer.recognizer_interface import image_recognizer
import tensorflow as tf


app = Flask(__name__)

@app.route('/files', methods=['GET', 'POST'])
def cnn_recognizeby_file():
  """Web method for recognition
    Returns:
      recognition response
  """

  return controller.recognize_uploaded_image(request, recognizer)

@app.route('/', methods=['GET', 'POST'])
def cnn_recognize():
  """Web method for recognition
    Returns:
      recognition response
  """
  
  return controller.recognize_url_image(request, recognizer)

if __name__ == "__main__":
  """Runs controller for image recognition"""
  
  global recognizer
  flags.parse_and_retrieve(training_file)
  recognizer = image_recognizer(training_file)
  recognizer.create_graph()
  # Retrieves host and port from arguments
  with tf.Session() as sess:
    recognizer.set_session(sess)
    # Binds server on host and port
    app.run(host=flags.host_nm, port=flags.port_nm, threaded=True)
