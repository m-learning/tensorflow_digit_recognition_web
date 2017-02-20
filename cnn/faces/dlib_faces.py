"""
Created on Feb 14, 2017

Compares two faces by dlib library

@author: Levan Tsinadze
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Image
import argparse
import collections
from io import BytesIO
import math

from cnn.faces.cnn_files import training_file
import dlib
import numpy as np


LANDMARKS_WEIGHTS = 'shape_predictor_68_face_landmarks.dat'
RESNET_WEIGHTS = 'dlib_face_recognition_resnet_model_v1.dat'
EMBEDDING_LENGTH = 128
threshold = None
face_desc = collections.namedtuple('face_desc', ['emb', 'det'])

def load_model():
  """Loads network model weights
    Returns:
      tuple of -
        detector - face descriptor
        sp - shape detector
        facerec - face recognizer
  """
  
  _files = training_file()
  
  predictor_path = _files.model_file(LANDMARKS_WEIGHTS)
  face_rec_model_path = _files.model_file(RESNET_WEIGHTS)
  
  # Load all the models we need: a detector to find the faces, a shape predictor
  # to find face landmarks so we can precisely localize the face, and finally the
  # face recognition model.
  detector = dlib.get_frontal_face_detector()
  sp = dlib.shape_predictor(predictor_path)
  facerec = dlib.face_recognition_model_v1(face_rec_model_path)
  
  return (detector, sp, facerec)

def calculate_embeddings(img, _network, dets):
  """Calculates embedding from detected faces in image
    Args:
      img - face image
      _network - pre-trained network module
      dets - detected faces
  """
  
  face_descriptors = []
  
  (_, sp, facerec) = _network
  for (k, d) in enumerate(dets):
        
      print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
          k, d.left(), d.top(), d.right(), d.bottom()))
      # Get the landmarks/parts for the face in box d.
      shape = sp(img, d)
      
      face_descriptor = facerec.compute_face_descriptor(img, shape)
      face_descriptors.append(face_descriptor)
  
  return face_descriptors
  
def calculate_embedding(img, _network, verbose=False):
  """Calculates embedding from image
    Args:
      img - face image
      _network - pre-trained network module
    Returns:
      face_descriptors - embedding vectors and detected face coordinates
  """
  
  face_descriptors = []
  (detector, sp, facerec) = _network
  
  dets = detector(img, 1)
  if dets and len(dets) > 0:
    _detecteds = len(dets)
    if verbose:
      print("Number of faces detected: {}".format(_detecteds))
    # Now process each face we found.
    for (k, d) in enumerate(dets):
      
      detected = (k, d.left(), d.top(), d.right(), d.bottom())  
      if verbose:
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
      # Get the landmarks/parts for the face in box d.
      shape = sp(img, d)
      
      face_embedding = facerec.compute_face_descriptor(img, shape)
      face_descriptor = face_desc(emb=face_embedding, det=detected)
      face_descriptors.append(face_descriptor)
    
  return face_descriptors

def compare_embeddings(emb1, emb2):
  """Compares embeddings
    Args:
      emb1 - first embedding
      emb2 - second embedding
    Returns:
      tuple of
        dist - distance between embeddings
        match_faces - boolean flag if faces match 
  """
  
  dist_sum = 0.0
  for i in range(EMBEDDING_LENGTH):
    dist_sub = emb1[i] - emb2[i]
    dist_sum += math.pow(dist_sub, 2)
  dist = math.sqrt(dist_sum)
  match_faces = dist < threshold
  
  return (dist, match_faces)

def calculate_buffer_embedding(_img, _network, verbose=False):
  """Calculates embedding from image buffer
    Args:
      _img - image buffer
      _network - loaded network weights
      verbose - debug mode
    Returns:
      descs - embeddings for detected faces
  """
  img_buff = Image.open(BytesIO(_img))
  img = np.array(img_buff)
  descs = calculate_embedding(img, _network, verbose=verbose)
  
  return descs

def compare_faces(descs1, _img2, _network, verbose=False):
  """Compares detected faces and faces from image
    Args:
      descs1 - embeddings
      _img - image buffer
      _network - loaded network weights
      verbose - debug mode
    Returns:
      face_dsts - distances between embeddings       
  """
  face_dsts = []
  
  descs2 = calculate_buffer_embedding(_img2, _network, verbose=verbose)
  for desc1 in descs1:
    (emb1, det1) = (desc1.emb, desc1.det)
    for desc2 in descs2:
      (emb2, det2) = (desc2.emb, desc2.det)
      (dist, match_faces) = compare_embeddings(emb1, emb2)
      face_dsts.append((dist, match_faces, det1, det2))
  
  return face_dsts
# Now process all the images
def compare_files(_img1, _img2, _network, verbose=False):
  """Compares two faces from images
    Args:
      _image1 - first image
      _image2 - second image
      _network - pre-trained network module
    Returns:
      face_dsts - distances between embeddings
  """
  
  face_dsts = []
  
  descs1 = calculate_buffer_embedding(_img1, _network, verbose=verbose)
  descs2 = calculate_buffer_embedding(_img2, _network, verbose=verbose)

  for desc1 in descs1:
    (emb1, det1) = (desc1.emb, desc1.det)
    for desc2 in descs2:
      (emb2, det2) = (desc2.emb, desc2.det)
      (dist, match_faces) = compare_embeddings(emb1, emb2)
      face_dsts.append((dist, match_faces, det1, det2))
  
  return face_dsts
  
def _parse_arguments():
  """Parses command line arguments
    Returns:
      args - parsed command line arguments
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('--image1',
                      type=str,
                      help='Path to first image')
  parser.add_argument('--image2',
                      type=str,
                      help='Path to second image')
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
  (args, _) = parser.parse_known_args()
  
  return args

def print_faces(face_dists):
  """Prints compared results
    Args:
      face_dists - face distances and detections
  """
  
  for (dist, match_faces, det1, det2) in face_dists:
      print(dist, match_faces, det1, det2)
  
if __name__ == '__main__':
  """Compare face images"""
  
  args = _parse_arguments()
  if args.image1 and args.image2:
    global threshold
    threshold = args.threshold
    _network = load_model()
    face_dists = compare_files(args.image1, args.image2, _network, args.verbose)
    print_faces(face_dists)
  else:
    print('No images to be compared')
