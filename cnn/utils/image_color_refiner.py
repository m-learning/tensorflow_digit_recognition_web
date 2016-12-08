"""
Created on Dec 8, 2016

Utility class to refine image colors

@author: Levan Tsinadze
"""

from PIL import Image
import argparse

def validate_pixel(pixel):
  """Validates pixel color layers
    Args:
      pixel - pixels array tuple element
    Returns:
      valid_color - validation value
  """
  
  valid_color = (pixel[0] < 150 and pixel[1] < 135 and pixel[2] < 135)
  return valid_color

def color_refinement(img):
  """Changes input image color
    Args:
      img - image object
  """
  
  pixels = img.load()  # create the pixel map
  
  for i in range(img.size[0]):  # for every pixel:
    for j in range(img.size[1]):
      if not validate_pixel(pixels[i, j]): 
        pixels[i, j] = (255, 255, 255)  # change to white


def refine_color_of_file(src_file):
  """Changes input image color
    Args:
      src_file - image file path
  """
  
  img = Image.open(src_file)
  color_refinement(img)
  img.show()
  
if __name__ == '__main__':
  
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('--src_file',
                          type=str,
                          help='Source file path.')
  (argument_flags, _) = arg_parser.parse_known_args()
  if argument_flags.src_file:
    src_file = argument_flags.src_file
    refine_color_of_file(src_file)
