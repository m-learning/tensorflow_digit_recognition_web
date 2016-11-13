"""
Created on Jun 25, 2016
Controller module for recognition
@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import Flask, request, render_template, json
from sys import argv

from cnn.mnist.cnn_files import parameters_file
from cnn.mnist.cnn_recognizer import image_recognizer


# Initializes web container
app = Flask(__name__)

class cnn_server:
  """Controller for image recognition"""
    
  def cnn_run(self, request):
    """Runs recognizer
      Args:
        request - HTTP request
      Return:
        resp - recognition response
    """
      
    fls = request.data
    tr_fls = parameters_file()
    to_recognize_path = tr_fls.get_to_recognize_file()
    with open(to_recognize_path, 'w') as file_:
        file_.write(fls)
    recgnizer = image_recognizer()
    rec_numb = recgnizer.recognize_image()
    resp = json.dumps(rec_numb)
    
    return resp

@app.route('/', methods=['GET', 'POST'])
def cnn_recognize():
  """Web method for recognition
    Return:
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
    Return:
      host_nm - host address of recognizer
  """
    
  if len(argv) > 1:
    host_nm = argv[1]
  else:
    host_nm = '0.0.0.0'
  
  return host_nm

def get_port_info():
  """Retrieves port number from arguments
    Return:
      host_nm - port number of server
  """
    
  if len(argv) > 2:
    port_nm = argv[1]
  else:
    port_nm = 8080
      
  return port_nm

def get_host_and_port():
  """Initializes host address and port number
    Return:
      host_nm - host address of recognizer
      port_nm - port number of server
  """
  
  # Retrieves host and port from arguments
  host_nm = get_host_info()
  port_nm = get_port_info()
  
  return (host_nm, port_nm)

if __name__ == "__main__":
    
  # Retrieves host and port from arguments
  (host_nm, port_nm) = get_host_and_port()
  # Binds server on host and port
  app.run(host=host_nm, port=port_nm, threaded=True)
