'''
Created on Jun 25, 2016
Controller module for recognition
@author: Levan Tsinadze
'''

import tensorflow as tf
from flask import Flask, request, render_template, json
from sys import argv
from cnn_files import training_file
from cnn.transfer import general_recognizer.image_recognizer

import cnn.utils.cnn_controller_utils as controller_utils


app = Flask(__name__)

class cnn_server(object):
  """Controller for image recognition"""
  
  def cnn_run(self, request):
    """Runs recognizer
      Args:
        request - HTTP request
      Return:
        resp - recognition response
    """
      
    img_url = request.data
    dirs_fls.get_file_to_recognize(img_url)
    answer = img_recognizer.recognize_image_by_sess()
    anwer_txt = {}
    for key, value in answer.iteritems():
        anwer_txt[key] = str(value)
    resp = json.dumps(anwer_txt)
    
    return resp

# Web method for recognition
@app.route('/', methods=['GET', 'POST'])
def cnn_recognize():
  """Web method for recognition
    Return:
      resp - recognition response
  """
      
  print img_recognizer
  if request.method == 'POST':
      srv = cnn_server()
      resp = srv.cnn_run(request)
  elif request.method == 'GET':
      resp = render_template("index.html")
  
  return resp

# Runs controller for image recognition        
if __name__ == "__main__":
  
  global dirs_fls
  global img_recognizer
  dirs_fls = training_file()
  img_recognizer = general_recognizer(dirs_fls)
  img_recognizer.create_graph()
  # Retrieves host and port from arguments
  (host_nm, port_nm) = controller_utils.get_host_and_port(argv)
  
  with tf.Session() as sess:
    img_recognizer.set_session(sess)
    # Binds server on host and port
    app.run(host=host_nm, port=port_nm, threaded=True)
