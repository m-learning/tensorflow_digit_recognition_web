"""
Created on Nov 13, 2016
Flags for image recognition
@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

from cnn.utils import file_utils

output_graph = None  # Where to save the trained graph
output_labels = None  # Where to save the trained graph's labels

def retrieve_args(argument_flags, tr_files):
  """Adds configuration from command line arguments
    Args:
     arg_parser - runtime parameters parser
  """
    
  global output_graph, output_labels
    
  if argument_flags.output_graph:
    output_graph = tr_files.join_path(argument_flags.output_graph,
                                      file_utils.WEIGHTS_FILE)
    output_labels = tr_files.join_path(output_graph,
                                       file_utils.LABELS_FILE)
    print('Output graph path was set - ' , output_graph)
    print('Output labels path was set - ' , output_labels)
  else:
    output_graph = tr_files.get_or_init_files_path()  # Where to save the trained graph
    output_labels = tr_files.get_or_init_labels_path()  # Where to save the trained graph's labels      

def parse_and_retrieve(tr_files=None):
  """Retrieves command line arguments"""
  
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('--output_graph',
                          type=str,
                          help='Where to save the trained graph.')
  (argument_flags, _) = arg_parser.parse_known_args()
  retrieve_args(argument_flags, tr_files)
