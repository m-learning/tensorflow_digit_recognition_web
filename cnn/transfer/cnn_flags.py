"""
Created on Nov 13, 2016
Flags for image recognition service
@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

from cnn.utils import file_utils


output_graph = None  # Where to save the trained graph
output_labels = None  # Where to save the trained graph's labels
host_nm = None
port_nm = None
box_images = None

def retrieve_args(argument_flags, tr_files):
  """Adds configuration from command line arguments
    Args:
     arg_parser - runtime parameters parser
  """
    
  global output_graph, output_labels, host_nm, port_nm, box_images
    
  if argument_flags.output_graph:
    output_graph = tr_files.join_path(argument_flags.output_graph,
                                      file_utils.WEIGHTS_FILE)
    output_labels = tr_files.join_path(argument_flags.output_graph,
                                       file_utils.LABELS_FILE)
  else:
    output_graph = tr_files.get_or_init_files_path()  # Where to save the trained graph
    output_labels = tr_files.get_or_init_labels_path()  # Where to save the trained graph's labels
  print('Output graph path was set as - ' , output_graph)
  print('Output labels path was set as - ' , output_labels)
  
  if argument_flags.box_images:
    box_images = argument_flags.box_images
  else:
    box_images = False
    
  host_nm = argument_flags.host
  port_nm = argument_flags.port     

def parse_and_retrieve(cnn_files_const=None):
  """Retrieves command line arguments"""
  
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('--output_graph',
                          type=str,
                          help='Where is saved the trained graph.')
  arg_parser.add_argument('--host',
                          type=str,
                          default='0.0.0.0',
                          help='Host name for service.')
  arg_parser.add_argument('--port',
                          type=int,
                          default=8080,
                          help='Port number for service.')
  arg_parser.add_argument('--box_images',
                          dest='box_images',
                          action='store_true',
                          help='Crop images.')
  arg_parser.add_argument('--not_box_images',
                          dest='box_images',
                          action='store_false',
                          help='Do not Crop images.')
  (argument_flags, _) = arg_parser.parse_known_args()
  if cnn_files_const is not None:
    tr_files = cnn_files_const()
  else:
    tr_files = None
  retrieve_args(argument_flags, tr_files)
