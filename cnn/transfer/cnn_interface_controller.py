"""
Created on Nov 14, 2016

Abstract controller module for recognition

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import render_template, json


class cnn_server(object):
  """Abstract controller for image recognition from HTTP request"""
  
  def __init__(self, recognizer):
    self.recognizer = recognizer
    self.cnn_fles = recognizer.cnn_files
  
  def recognize_by_image_data(self, image_data):
    """Recognizes binary image
      Args:
        image_data - binary image file
      Returns:
        resp - recognition response
    """
    
    answer = self.recognizer.recognize_image_by_sess(image_data)
    anwer_txt = {}
    for key, value in answer.iteritems():
        anwer_txt[key] = str(value)
    resp = json.dumps(anwer_txt)
    
    return resp
  
  def cnn_run_binary(self, request, uploaded=False):
    """Runs recognizer
      Args:
        request - HTTP request
      Returns:
        resp - recognition response
    """
    
    if uploaded:
      upload_file = request.files['image-rec']
      if upload_file.filename:
        image_data = upload_file.read()
      else:
        upload_file = None
    else:
      img_url = request.data
      image_data = self.cnn_fles.get_file_bytes_to_recognize(img_url)
    resp = self.recognize_by_image_data(image_data)
    
    return resp
  
  
  
  def cnn_run(self, request):
    """Runs recognizer
      Args:
        request - HTTP request
      Returns:
        resp - recognition response
    """
      
    img_url = request.data
    self.cnn_fles.get_file_to_recognize(img_url)
    answer = self.recognizer.recognize_image_by_sess()
    anwer_txt = {}
    for key, value in answer.iteritems():
        anwer_txt[key] = str(value)
    resp = json.dumps(anwer_txt)
    
    return resp
  
def recognize_image(request, recognizer,
                    template_name="index.html", uploaded=False):
  """Image recognition request
      Args:
        request - HTTP request
        recognizer - interface for image recognition
        template_name - template to render for GET request
        uploaded - is image uploaded or should be requested
      Returns:
        resp - HTTP response for image recognition
  """
  if request.method == 'POST':
      srv = cnn_server(recognizer)
      resp = srv.cnn_run_binary(request, uploaded=uploaded)
  elif request.method == 'GET':
      resp = render_template(template_name)
  
  return resp

def recognize_uploaded_image(request, recognizer):
  """Image recognition request for file upload
      Args:
        request - HTTP request
        recognizer - interface for image recognition
      Returns:
        resp - HTTP response for image recognition
  """
  return recognize_image(request, recognizer,
                         template_name='upload.html',
                         uploaded=True)
  
def recognize_url_image(request, recognizer):
  """Image recognition request for file URL address
      Args:
        request - HTTP request
        recognizer - interface for image recognition
      Returns:
        resp - HTTP response for image recognition
  """
  return recognize_image(request, recognizer)  
  
