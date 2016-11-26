"""
Created on Oct 29, 2016

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from resizeimage import resizeimage


class pillow_resizer(object):
  """Image resizing with "Pillow" resize utilities"""
  
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
  
  def resize_contain(self, img):
    """Resizes passed image with "contain" method
      Args:
        img - image to resize
      Returns:
        resized image
    """
    
    resized_image = resizeimage.resize_contain(img, self.size)
    img.close()
    
    return resized_image
    
  
  def resize_full(self, img):
    """Resizes passed image with "thumbnail" and "height" method
      Args: 
        img = image
      Returns:
        resized image
    """
    
    resized_img = self.resize_thumbnail(img)
    (width, height) = resized_img.size
    if height != self.height or width != self.width:
      full_resized_img = self.resize_contain(resized_img)
    else:
      full_resized_img = resized_img
    
    return  full_resized_img