"""
Created on Nov 26, 2016
Utility module for image processing
@author: Levan Tsinadze
"""

def crop_image(self, im):
  """Document image croping"""
  
  [x, y] = im.size
  left = (x - x / 5) / 2
  top = (y - y / 3.5) / 2
  right = x
  bottom = (y + y / 2.6) / 2
  box = [left, top, right, bottom]
  croped_image = im.crop(box)
  
  return croped_image 