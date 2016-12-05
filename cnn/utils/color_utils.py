"""
Created on Dec 5, 2016

Utility module for image colors

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import glob

try:
  from PIL import Image, ImageFilter
except ImportError:
  print("Importing Image from PIL threw exception")
  import Image
  
def remove_reds(im):
  """Removes red pixels from image
    Args:
      im - original image
    Returns:
      md - modified image
  """
  
  # source = im.split()
  # R, G, B = 0, 1, 2
  # out = source[R].point(lambda i: 0)
  # source[R].paste(out, None, None)
  # md = Image.merge(im.mode, source)
  md = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
  
  return md
  
def process_pixel(pix_value):
  """Processes image pixel
    Args:
      pix_value - pixel value
    Returns:
      pix_mod - modified pixel value
  """
  
  # if pix_value < 100:
  #  pix_mod = 255
  # else:
  pix_mod = pix_value * 2.0
  
  return pix_mod

def sharpen_edges(im):
  """Modifies image sharpens edges and adds light
    Args:
      im - image to modify
    Returns:
      md - modifies image
  """
  
  md = remove_reds(im)
  md = md.point(process_pixel)
  
  return md

def darken_image(image_path):
  """Darkens image by path
    Args:
      image_path - image path to process
  """
  
  im1 = Image.open(image_path)
  # im2 = im1.point(process_pixel)
  im2 = sharpen_edges(im1)
  im2.show()
  im_name = 'darkened_' + os.path.basename(image_path)
  im_dir = os.path.dirname(image_path)
  dark_image = os.path.join(im_dir, im_name)
  im2.save(dark_image)
  
def read_arguments_and_run():
  """Retrieves command line arguments for image processing"""
  
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('--src_file',
                          type=str,
                          help='Source file path.')
  arg_parser.add_argument('--src_dir',
                          type=str,
                          help='Source directorye path.')
  arg_parser.add_argument('--replace_images',
                          dest='replace_images',
                          action='store_true',
                          help='Replace images flag')
  
  arg_parser.add_argument('--not_replace_images',
                          dest='replace_images',
                          action='store_false',
                          help='Replace images flag') 
  (argument_flags, _) = arg_parser.parse_known_args()
  if argument_flags.src_file:
    darken_image(argument_flags.src_file)
  elif argument_flags.src_dir:
    scan_dir = os.path.join(argument_flags.src_dir, '*.jpg')
    for pr in glob.glob(scan_dir):
      im = Image.open(pr)
      md = sharpen_edges(im)
      md.save(pr)
  
if __name__ == '__main__':
  """Converts images for training data set"""
  
  read_arguments_and_run()
  
