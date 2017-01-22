"""
Created on Jan 22, 2017

Image recognizer controller

@author: Levan Tsinadze
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import Flask, request, render_template, json
from sys import argv

from cnn.mnist.keras_recognizer import mnist_model, recognize_image, _files


# Initializes web container
app = Flask(__name__)

class cnn_server:
  """Controller for image recognition"""
    
  def cnn_run(self, request):
    """Runs recognizer
      Args:
        request - HTTP request
      Returns:
        resp - recognition response
    """
      
    fls = request.data
    to_recognize_path = _files.get_to_recognize_file()
    with open(to_recognize_path, 'w') as file_:
        file_.write(fls)
    rec_numb = recognize_image(_model, _files)
    resp = json.dumps(rec_numb)
    
    return resp

@app.route('/', methods=['GET', 'POST'])
def cnn_recognize():
  """Web method for recognition
    Returns:
      resp - recognition response
  """
      
  if request.method == 'POST':
      srv = cnn_server()
      resp = srv.cnn_run(request)
  elif request.method == 'GET':
      resp = render_template("index.html")
  
  return resp
        
def get_host_info():
  """Retrieves host name from arguments
    Returns:
      host_nm - host address of recognizer
  """
    
  if len(argv) > 1:
    host_nm = argv[1]
  else:
    host_nm = '0.0.0.0'
  
  return host_nm

def get_port_info():
  """Retrieves port number from arguments
    Returns:
      host_nm - port number of server
  """
    
  if len(argv) > 2:
    port_nm = argv[1]
  else:
    port_nm = 8080
      
  return port_nm

def get_host_and_port():
  """Initializes host address and port number
    Returns:
      host_nm - host address of recognizer
      port_nm - port number of server
  """
  
  host_nm = get_host_info()
  port_nm = get_port_info()
  
  return (host_nm, port_nm)

if __name__ == "__main__":
  
  global _model
  _model = mnist_model()
  # Retrieves host and port from arguments
  (host_nm, port_nm) = get_host_and_port()
  # Binds server on host and port
  app.run(host=host_nm, port=port_nm, threaded=True)
