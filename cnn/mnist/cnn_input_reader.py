'''
Created on Jun 17, 2016

@author: Levan Tsinadze
'''
import math
from scipy import ndimage

import cv2
import numpy as np
import copy
import sys

IMAGE_SIZE = 28

n_input = 784


# Reads and converts file for recognition
def getBestShift(img):
	cy, cx = ndimage.measurements.center_of_mass(img)

	rows, cols = img.shape
	shiftx = np.round(cols / 2.0 - cx).astype(int)
	shifty = np.round(rows / 2.0 - cy).astype(int)

	return shiftx, shifty


# Shifts image in one pixel
def shift(img, sx, sy):
	rows, cols = img.shape
	M = np.float32([[1, 0, sx], [0, 1, sy]])
	shifted = cv2.warpAffine(img, M, (cols, rows))

	return shifted


def get_global_bounding_rect(contours):
	"""Reads input data as tensor
		Args:
			contours - arguments of image
		Return:
			average min_x, min_y, max_w, max_h
		  instances
	"""
	min_x = sys.maxint
	min_y = sys.maxint
	max_w = 0
	max_h = 0
	for c in contours:
		x, y, w, h = cv2.boundingRect(c)
		if x < min_x:
			min_x = x
		if y < min_y:
			min_y = y
		if x + w > max_w:
			max_w = x + w
		if y + h > max_h:
			max_h = y + h
	return min_x, min_y, max_w, max_h


# Reads image file to tensor
def read_input_file(image_file_path):
	image_rec = np.zeros((1, n_input))

	gray = cv2.imread(image_file_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
	# rescale it
	gray = cv2.resize(255 - gray, (28, 28))
	# better black and white version
	(thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	print thresh

	# while np.sum(gray[0]) == 0:
	# 	gray = gray[1:]
	#
	# while np.sum(gray[:, 0]) == 0:
	# 	gray = np.delete(gray, 0, 1)
	#
	# while np.sum(gray[-1]) == 0:
	# 	gray = gray[:-1]
	#
	# while np.sum(gray[:, -1]) == 0:
	# 	gray = np.delete(gray, -1, 1)

	gray_copy = copy.copy(gray)
	contours, hierarchy = cv2.findContours(gray_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	del gray_copy

	x1, y1, x2, y2 = get_global_bounding_rect(contours)

	gray = gray[y1:y2, x1:x2]

	rows, cols = gray.shape

	if rows > cols:
		factor = 20.0 / rows
		rows = 20
		cols = int(round(cols * factor))
		# first cols than rows
		gray = cv2.resize(gray, (cols, rows))
	else:
		factor = 20.0 / cols
		cols = 20
		rows = int(round(rows * factor))
		# first cols than rows
		gray = cv2.resize(gray, (cols, rows))

	colsPadding = (int(math.ceil((28 - cols) / 2.0)), int(math.floor((28 - cols) / 2.0)))
	rowsPadding = (int(math.ceil((28 - rows) / 2.0)), int(math.floor((28 - rows) / 2.0)))
	gray = np.lib.pad(gray, (rowsPadding, colsPadding), 'constant')

	# shiftx, shifty = getBestShift(gray)
	# shifted = shift(gray, shiftx, shifty)
	# gray = shifted

	image_modified_file = image_file_path + '_modf.png'
	# write_image
	cv2.imwrite(image_modified_file, gray)

	flatten = gray.flatten() / 255.0
	image_rec[0] = flatten

	return image_rec
