"""
Created on Jan 12, 2017

Compares faces throw FaceNet model
Performs face alignment and calculates L2 distance between the embeddings of two images.

@author: Levan Tsinadze

MIT License
# 
# Copyright (c) 2016 David Sandberg
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

from scipy import misc

from cnn.faces import detect_face
from cnn.faces import facenet
from cnn.faces.cnn_files import training_file
from cnn.faces.face_utils import EMBEDDINGS_LAYER, INPUT_LAYER
import numpy as np
import tensorflow as tf


def calculate_embeddings_with_graph(sess, images):
  """Calculates embeddings for images
    Args:
      sess - current TensorFlow session
      images - image files
    Returns:
      emb - embeddings for images
  """  
  
  # Get input and output tensors
  images_placeholder = tf.get_default_graph().get_tensor_by_name(INPUT_LAYER)
  embeddings = tf.get_default_graph().get_tensor_by_name(EMBEDDINGS_LAYER)

  # Run forward pass to calculate embeddings
  feed_dict = { images_placeholder: images }
  emb = sess.run(embeddings, feed_dict=feed_dict)
  
  return emb

def calculate_embeddings(model_dir, images):
  """Calculates embeddings for images
    Args:
      model_dir - model directory
      images - image files
    Returns:
      emb - embeddings for images
  """
  
  with tf.Graph().as_default():
    with tf.Session() as sess:
      # Load the model
      print('Model directory: %s' % model_dir)
      meta_file, ckpt_file = facenet.get_model_filenames(os.path.expanduser(model_dir))
      print('Metagraph file: %s' % meta_file)
      print('Checkpoint file: %s' % ckpt_file)
      facenet.load_model(model_dir, meta_file, ckpt_file)
      emb = calculate_embeddings_with_graph(sess, images)
      
      return emb

def compare_faces(args):
  """Generates many face embeddings from files and calculates L2 distances
    Args:
      args - command line arguments
  """

  images = load_and_align_data(args.image_files, args.image_size, args.margin, args.gpu_memory_fraction)
  emb = calculate_embeddings(args.model_dir, images)
          
  nrof_images = len(args.image_files)

  print('Images:')
  for i in range(nrof_images):
    print('%1d: %s' % (i, args.image_files[i]))
  print('')
  
  # Print distance matrix
  print('Distance matrix')
  print('    ', end='')
  for i in range(nrof_images):
    print('    %1d     ' % i, end='')
  print('')
  
  return (emb, nrof_images)

def compare_many_faces(args):
  """Generates many face embeddings from files and calculates L2 distances
    Args:
      args - command line arguments
  """

  (emb, nrof_images) = compare_faces(args)
  for i in range(nrof_images):
    print('%1d  ' % i, end='')
    for j in range(nrof_images):
      dist = np.sqrt(np.sum(np.square(np.subtract(emb[i, :], emb[j, :]))))
      print('  %1.4f  ' % dist, end='')
    print('')
      
def compare_two_faces(args):
  """Generates two face embeddings from files and calculates L2 distances
    Args:
      args - command line arguments
  """

  (emb, _) = compare_faces(args)
  dist = np.sqrt(np.sum(np.square(np.subtract(emb[0, :], emb[1, :]))))
  print('  %1.4f  ' % dist, end='')
  print('')
                        
def load_and_align_data(image_paths, image_size, margin, gpu_memory_fraction):
  """Loads and alighn face images from files
    Args:
      image_paths - image file paths
      image_size - image size
      margin - margin for alignment
      gpu_memory_fraction - GPU memory fraction for parallel processing
    Returns:
      images - aligned images from files
  """

  minsize = 20  # minimum size of face
  threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
  factor = 0.709  # scale factor
  
  print('Creating networks and loading parameters')
  with tf.Graph().as_default():
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
    with sess.as_default():
        pnet, rnet, onet = detect_face.create_mtcnn(sess, _files.model_dir)

  nrof_samples = len(image_paths)
  img_list = [None] * nrof_samples
  for i in xrange(nrof_samples):
    img = misc.imread(os.path.expanduser(image_paths[i]))
    img_size = np.asarray(img.shape)[0:2]
    bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
    det = np.squeeze(bounding_boxes[0, 0:4])
    bb = np.zeros(4, dtype=np.int32)
    bb[0] = np.maximum(det[0] - margin / 2, 0)
    bb[1] = np.maximum(det[1] - margin / 2, 0)
    bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
    bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
    cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
    aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
    prewhitened = facenet.prewhiten(aligned)
    img_list[i] = prewhitened
  images = np.stack(img_list)
  
  return images

def parse_arguments():
  """Parses command line arguments
    Returns:
      argument_flags - retrieved arguments
  """
  global _files
  _files = training_file()
  parser = argparse.ArgumentParser()
  parser.add_argument('--many_faces',
                         dest='many_faces',
                         action='store_true',
                         help='Flag to compare only two faces.')
  parser.add_argument('--two_faces',
                         dest='many_faces',
                         action='store_false',
                         help='Do not print data set file names and labels.')
  parser.add_argument('--model_dir',
                      type=str,
                      default=_files.model_dir,
                      help='Directory containing the meta_file and ckpt_file')
  parser.add_argument('--image_files',
                      type=str,
                      nargs='+',
                      help='Images to compare')
  parser.add_argument('--image_size',
                      type=int,
                      default=160,
                      help='Image size (height, width) in pixels.')
  parser.add_argument('--margin',
                      type=int,
                      default=44,
                      help='Margin for the crop around the bounding box (height, width) in pixels.')
  parser.add_argument('--gpu_memory_fraction',
                      type=float,
                      default=1.0,
                      help='Upper bound on the amount of GPU memory that will be used by the process.')
  (argument_flags, _) = parser.parse_known_args()
  
  return argument_flags

if __name__ == '__main__':
  """Compares faces by embeddings from image files"""
  
  argument_flags = parse_arguments()
  if argument_flags.many_faces:
    compare_many_faces(argument_flags)
  else:
    compare_two_faces(argument_flags)
