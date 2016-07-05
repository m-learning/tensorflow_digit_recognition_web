'''
Created on Jun 25, 2016
Controller module for recognition
@author: Levan Tsinadze
'''

import tensorflow as tf
from flask import Flask, request, render_template, json
from sys import argv
from cnn_files import training_file
from retrain_run import image_recognizer


app = Flask(__name__)

img_recognizer = None

# Controller for image recognition
class cnn_server(object):
  
  # Runs recognizer
  def cnn_run(self, request):
      
    img_url = request.data
    tr_fl = training_file()
    tr_fl.get_file_to_recognize(img_url)
    answer = img_recognizer.recognize_image_by_sess()
    anwer_txt = {}
    for key, value in answer.iteritems():
        anwer_txt[key] = str(value)
    resp = json.dumps(anwer_txt)
    
    return resp

@app.route('/', methods=['GET', 'POST'])
def cnn_recognize():
    
  print img_recognizer
  if request.method == 'POST':
      srv = cnn_server()
      resp = srv.cnn_run(request)
      resp = resp
  elif request.method == 'GET':
      resp = render_template("index.html")
  
  return resp
        
# Retrieves host name from arguments
def get_host_info():
    
  if len(argv) > 1:
      host_nm = argv[1]
  else:
      host_nm = '0.0.0.0'
  
  return host_nm

# Retrieves port number from arguments
def get_port_info():
    
  if len(argv) > 2:
      port_nm = argv[1]
  else:
      port_nm = 8080
      
  return port_nm

# Initializes host address and port number    
def get_host_and_port():
    
  # Retrieves host and port from arguments
  host_nm = get_host_info()
  port_nm = get_port_info()
  
  return (host_nm, port_nm)

if __name__ == "__main__":
    
  
  img_recognizer = image_recognizer()
  img_recognizer.create_graph()
  # Retrieves host and port from arguments
  (host_nm, port_nm) = get_host_and_port()
  
  with tf.Session() as sess:
    img_recognizer.set_session(sess)
    # Binds server on host and port
    app.run(host=host_nm, port=port_nm, threaded=True)
