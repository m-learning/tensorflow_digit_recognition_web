"""
Created on Feb 15, 2017

Faces comparator based on DLIB faces

@author: Levan Tsinadze
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import traceback

from flask import Flask, request, json, render_template

from cnn.faces import dlib_faces as comparator 
from cnn.faces import dlib_flags as flags


TEMPLATE_NAME = 'upload.html'
PERSON_IMAGE = 'person_image'
FILE_NAME = 'fileName'
COMP_DATA = 'comp_result'
COMP_STATUS = 'status'
STATUS_CODE = 'code'
STATUS_MESSAGE = 'message'
# Error messages
OK_CODE = 0
ERROR_CODE = -1
NO_IMAGE_ERROR = 'Person image is not uploaded'
NO_FACE_IN_PERSON_IMAGE = 'Could not find face in person image'
NO_FACE_IN_IMAGE = 'Could not find face in image'

NO_RESULT = {COMP_STATUS: {STATUS_CODE:ERROR_CODE,
                           STATUS_MESSAGE:NO_IMAGE_ERROR},
             FILE_NAME: '',
             COMP_DATA: {}}

app = Flask(__name__)

def _init_ok_status():
  """Initializes OK status
    Returns:
      OK status object
  """
  return {STATUS_CODE:OK_CODE, STATUS_MESSAGE:''}

def _init_no_face_main_status():

  return {COMP_STATUS: {STATUS_CODE:ERROR_CODE,
                       STATUS_MESSAGE:NO_FACE_IN_PERSON_IMAGE},
          COMP_DATA: {}}

def _init_no_face_status():
  """Initializes OK status
    Returns:
      OK status object
  """
  return {STATUS_CODE:ERROR_CODE, STATUS_MESSAGE:NO_FACE_IN_IMAGE}

def _read_valid_file(_files, name):
  """Reads file from HTTP request
    Args:
      request - files from HTTP request
      name - file name
  """

  upload_file = _files[name]
  if upload_file.filename:
    image_data = (upload_file.filename, upload_file.read())
  else:
    image_data = None
  
  return image_data

def _read_file(_files, name):
  """Reads file from HTTP request
    Args:
      _files - files from HTTP request
      name - file name
  """
  
  if name in _files:
    image_data = _read_valid_file(_files, name)
  else:
    image_data = None
  
  return image_data

def _add_compared_distances(img_data, face_dists):
  """Validates and adds compared distances
    Args:
      img_data - image to compare
      face_dists - compared vectors
    Returns:
      comp_result - result for image
  """
  
  comp_result = {}
  comp_result[FILE_NAME] = img_data.filename
  comp_result[COMP_DATA] = face_dists
  if len(face_dists) > 0:
    comp_result[COMP_STATUS] = _init_ok_status()
  else:
    comp_result[COMP_STATUS] = _init_no_face_status()
  
  return comp_result

def _compare_all_images(person_embs, _files):
  """Compares person images
    Args:
      person_embs - face vectors for compare
      request - HTTP request with images to compare
    Returns:
      comp_results - result for each image
  """
  comp_results = {}
  
  for (name, img_data) in _files.iteritems():
    if name != PERSON_IMAGE:
      img = img_data.read()
      face_dists = comparator.compare_faces(person_embs, img, flags.network, verbose=flags.verbose)
      comp_result = _add_compared_distances(img_data, face_dists)
      comp_results[name] = comp_result
  
  return comp_results

def _compare_faces(person_image, _files):
  """Compares person images
    Args:
      person_image - person image
      request - HTTP request with images to compare
    Returns:
      comp_results - result for each image
  """
  
  (filename, img_buff) = person_image
  person_embs = comparator.calculate_embeddings_from_buffer(img_buff, flags.network, verbose=flags.verbose)
  if len(person_embs) > 0:
    comp_results = _compare_all_images(person_embs, _files)
  else:
    comp_results = _init_no_face_main_status()
    comp_results[FILE_NAME] = filename
  
  return comp_results

def _log_request_files(request, _files):
  """Logs request and files
    Args:
      request - HTTP request
  """
  
  if flags.verbose:
    print(request)
    for (name, img_data) in _files.iteritems():
      print(name, img_data)

def _log_response_event():
  """Logs HTTP response event"""
  print('Response sent')

def _run_comparator(_files):
  """Face comparator service
    Args:
      _verbose - command line argument for debugging
    Returns:
     _response - recognition response
  """
  
  person_image = _read_file(_files, PERSON_IMAGE)
  if person_image:
    comp_result = _compare_faces(person_image, _files)
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
    _files = request.files.to_dict()
    _log_request_files(request, _files)
    _response = _run_comparator(_files)
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
    _log_response_event()
  elif request.method == 'GET':
    _response = render_template(TEMPLATE_NAME)
  
  return _response

if __name__ == '__main__':
  """Starts face comparator service"""
  
  args = flags.parse_service_arguments()
  comparator.threshold = args.threshold
  flags.verbose = args.verbose
  flags.network = comparator.load_model()
  app.run(host=args.host, port=args.port, threaded=True)
