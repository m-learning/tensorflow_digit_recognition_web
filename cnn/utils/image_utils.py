"""
Created on Nov 26, 2016
Utility module for image processing
@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from cnn.transfer import cnn_flags as flags
from cnn.utils import file_utils as files

CROPPED_IMAGE_FILE = 'cropped_image.jpg'

def write_image(img):
  """Writes cropped image
    Args:
      img - cropped image
  """
  if flags.log_image_path:
    files.ensure_dir_exists(flags.log_image_path)
    file_path = files.join(flags.log_image_path, CROPPED_IMAGE_FILE)
    img.save(file_path)

def crop_image(im):
  """Document image croping
    Args:
      im - image to resize
    Returns:
      cropped_image - cropped image
  """
  
  [x, y] = im.size
  left = (x - x / 5) / 2
  top = (y - y / 3.5) / 2
  right = x
  bottom = (y + y / 2.6) / 2
  box = [left, top, right, bottom]
  cropped_image = im.crop(box)
  im.close()
  
  return cropped_image 