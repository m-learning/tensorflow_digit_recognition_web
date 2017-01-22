"""
Created on Jun 17, 2016
Image processing before recognition
@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io

from PIL import Image, ImageOps

import numpy as np


IMAGE_SIZE = 28

n_input = 784
border_color = 'black'

def read_image(image_file_path, image_data=None):
	"""Reads image from binaries or path
		Args:
			image_file_path - image file path
			image_data - binary image
		Retunrs:
			img - image matrix
	"""
	if image_data:
		img = Image.open(io.BytesIO(image_data))
	else:
		img = Image.open(image_file_path)
	
	return img

def read_input_file(image_file_path, image_data=None):
	"""Reads image file to tensor
		Args:
			image_file_path - image path
		Returns:
			img_array - array of image pixels
	"""
	with read_image(image_file_path, image_data=image_data) as img:
		img = img.convert("L")  # convert into greyscale
		img = img.point(lambda i: i < 150 and 255)  # better black and white
		img = ImageOps.expand(img, border=8, fill=border_color)  # add padding
		img.thumbnail((IMAGE_SIZE, IMAGE_SIZE), Image.BILINEAR)  # resize back to the same size
		image_modified_file = image_file_path + '_modf.png'
		img.save(image_modified_file)
		array = np.asarray(img.getdata(), dtype=np.float32)
		array /= 255.0
		img_array = array.reshape(1, n_input)
	
	return img_array
