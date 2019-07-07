
from commons.constants import constants

import os
import math
import json
import logging

from PIL import Image
#import Image

from typing import Generator, Dict, Callable

def find_coord_extrema (coords:tuple, extrema:Dict) -> Dict:
	if coords[0] > extrema['x']:
		extrema['x'] = coords[0]

	if coords[1] > extrema['y']:
		extrema['y'] = coords[1]

	return extrema

def create_image (image_size:Dict, tile_counts:Dict):
	image_dimensions = (
		math.floor(image_size['x'] / tile_counts['x']),
		math.floor(image_size['y'] / tile_counts['y'])
	)

	img = Image.new('RGB', image_dimensions, constants['colours']['background'])

	return img, img.load( )

def calculate_ranges (image_size:Dict, tile_counts:Dict):
	for ith in range(tile_counts['x']):
		for jth in range(tile_counts['y']):
			left_x  = (ith + 0) * ( math.floor(image_size['x'] / tile_counts['x']) )
			right_x = (ith + 1) * ( math.floor(image_size['x'] / tile_counts['x']) )

			top_y    = (jth + 0) * ( math.floor(image_size['y'] / tile_counts['y']) )
			bottom_y = (jth + 1) * ( math.floor(image_size['y'] / tile_counts['y']) )

			yield {
				'x': {
					'min': left_x,
					'max': right_x
				},
				'y': {
					'min': top_y,
					'max': bottom_y
				}
			}

def find_image_size (input_path:str) -> Dict:
	image_size = {'x': 0, 'y': 0}

	with open(input_path) as fconn:
		line_count = 0

		for line in fconn:
			x, y, _ = json.loads(line)

			line_count += 1
			image_size = find_coord_extrema((x, y), image_size)

		if line_count == 0:
			logging.error("no pixels loaded")
			exit(1)

		if image_size['x'] == 0 or image_size['y'] == 0:
			logging.error("n x 0 image dimension supplied")
			exit(1)

	return image_size

def find_pixels(input_path: str, xrange:Dict, yrange: Dict):
	logging.info('finding pixels in ranges {} → {}, {} → {}'.format(
		xrange['min'], xrange['max'], yrange['min'], yrange['max']))

	with open(input_path) as fconn:
		for line in fconn:
			x, y, colour = json.loads(line)

			if x > xrange['min']:
				if x < xrange['max']:
					if y > yrange['min']:
						if y < yrange['max']:
							yield (x, y, colour)

def draw_solutions (paths:str, tile_counts:int) -> None:
	"""
	read pixels from an input file, and write the image out
	to another file.
	"""

	image_size = find_image_size(paths['input'])
	pixel_ranges = list(calculate_ranges(image_size, tile_counts))
	image_count = 0

	for count, pixel_range in enumerate(pixel_ranges):
		logging.info('drawing pixels {} / {}'.format(count, len(pixel_ranges)))

		image, image_pixels = create_image(image_size, tile_counts)

		for x, y, colour in find_pixels(paths['input'], pixel_range['x'], pixel_range['y']):
			try:
				normal_x = x - pixel_range['x']['min']
				normal_y = y - pixel_range['y']['min']

				image_pixels[normal_x, normal_y] = (colour[0], colour[1], colour[2])

			except Exception as err:
				logging.error('failed to write pixel to image {}'.format(err))
				exit(1)

		try:
			image_path = os.path.join(paths['output_dir'], str(image_count) + '.png')

			image.save(image_path)
			image_count += 1

			logging.info('Writing image-tile to ' + image_path)

		except Exception as err:
			raise err
