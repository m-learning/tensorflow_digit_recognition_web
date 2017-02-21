"""
Created on Feb 20, 2017

Flags for faces service

@author: Levan Tsinadze
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

# Service flags
network = None  # Network weighs
verbose = None  # Debug mode

def parse_arguments():
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

def parse_service_arguments():
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
