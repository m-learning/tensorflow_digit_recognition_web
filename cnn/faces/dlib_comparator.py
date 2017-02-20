"""
Created on Feb 15, 2017

Faces comparator based on DLIB faces

@author: Levan Tsinadze
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import traceback

from flask import Flask, request, json, render_template

from cnn.faces import dlib_faces as comparator 
from cnn.faces import dlib_flags as flags


TEMPLATE_NAME = 'upload.html'
PERSON_IMAGE = 'person_image'
FILE_NAME = 'fileName'
COMP_DATA = 'comp_result'
NO_RESULT = {FILE_NAME: '', COMP_DATA: {}}

app = Flask(__name__)

def _parse_arguments():
  """Parses command line arguments
    Returns:
      args - parsed command line arguments
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('--threshold',
                      type=float,
                      default=0.6,
                      help='Threshold for Euclidean distance between face embedding vectors')
  parser.add_argument('--include_gui',
                      dest='include_gui',
                      action='store_true',
                      help='Include top layers')
  parser.add_argument('--verbose',
                      dest='verbose',
                      action='store_true',
                      help='Print additional information')
  parser.add_argument('--host',
                      type=str,
                      default='0.0.0.0',
                      help='Host name for service.')
  parser.add_argument('--port',
                      type=int,
                      default=50050,
                      help='Port number for service.')
  (args, _) = parser.parse_known_args()
  
  return args

def _read_file(request, name):
  """Reads file from HTTP request
    Args:
      request - HTTP request
      name - file name
  """
  
  upload_file = request.files[name]
  if upload_file.filename:
    image_data = upload_file.read()
  else:
    image_data = None
  
  return image_data

def _compare_faces(person_image, request):
  """Compares person images
    Args:
      person_image - image for compare
      request - HTTP request with images to compare
    Returns:
      comp_result - result on each image
  """
  comp_results = {}
  
  for (name, img_data) in request.files.to_dict().iteritems():
    if name != PERSON_IMAGE:
      img = img_data.read()
      face_dists = comparator.compare_files(person_image, img, flags.network, verbose=flags.verbose)
      comp_result = {}
      comp_result[FILE_NAME] = img_data.filename
      comp_result[COMP_DATA] = face_dists
      comp_results[name] = comp_result
  
  return comp_results

def _log_request_files(request):
  """Logs request and files
    Args:
      request - HTTP request
  """
  
  print(request.body)
  if flags.verbose:
    for (name, img_data) in request.files.to_dict().iteritems():
      print(name, img_data)

def _run_comparator(request):
  """Face comparator service
    Args:
      _verbose - command line argument for debugging
    Returns:
     _response - recognition response
  """
  
  person_image = _read_file(request, PERSON_IMAGE)
  if person_image:
    comp_result = _compare_faces(person_image, request)
    result_json = json.dumps(comp_result)
  else:
    result_json = json.dumps(NO_RESULT)
  
  return result_json
  
    
def _check_and_compare(request):
  """Face comparator service
    Args:
      _verbose - command line argument for debugging
    Returns:
     _response - recognition response
  """
  try:
    _log_request_files(request)
    _response = _run_comparator(request)
  except:
    traceback.print_exc()
    _response = None
  
  return _response
    
@app.route('/', methods=['GET', 'POST'])
def cnn_recognize():
  """Web method for recognition
    Return:
      _response - recognition response
  """
  
  if request.method == 'POST':
    _response = _check_and_compare(request)
  elif request.method == 'GET':
    _response = render_template(TEMPLATE_NAME)
  
  return _response

if __name__ == '__main__':
  """Starts face comparator service"""
  
  args = _parse_arguments()
  comparator.threshold = args.threshold
  flags.verbose = args.verbose
  flags.network = comparator.load_model()
  app.run(host=args.host, port=args.port, threaded=True)
