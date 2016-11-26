"""
Created on Nov 26, 2016
Utility module for image processing
@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def crop_image(im):
  """Document image croping
    Args:
      im - image to resize
    Returns:
      croped_image - cropped image
  """
  
  [x, y] = im.size
  left = (x - x / 5) / 2
  top = (y - y / 3.5) / 2
  right = x
  bottom = (y + y / 2.6) / 2
  box = [left, top, right, bottom]
  croped_image = im.crop(box)
  
  return croped_image 