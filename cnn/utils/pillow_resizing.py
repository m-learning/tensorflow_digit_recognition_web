"""
Created on Oct 29, 2016

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from resizeimage import resizeimage


class pillow_resizer(object):
  """Image resizing with image "Pillow" resize utilities"""
  
  def __init__(self, height, width=None):
    self.height = height
    if width is None:
      self.width = height
      self.size = [height, height]    
    else:
      self.width = width
      self.size = [width, height]

  def resize_thumbnail(self, img):
    """Resizes passed image with "thumbnail" method
      Args: 
        img = image
      Returns:
        resized image
    """
    return resizeimage.resize_thumbnail(img, self.size)
  
  def resize_cover(self, img):
    """Resizes passed image with "cover" method
      Args: 
        img = image
      Returns:
        resized image
    """
    return resizeimage.resize_cover(img, self.size)
