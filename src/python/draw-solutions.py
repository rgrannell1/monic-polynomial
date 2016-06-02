#!/usr/bin/env python3

import os
import sys
import json
import time
import math
import itertools
from functools import reduce
from operator  import mul
from PIL    import Image





constants = {
	'print_frequency': 10000,
	'flush_threshold': 100000,

	'project_root': os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')),

	'colours': {
		'background': 'black',
		# lazy. fix this.
		'points':     list(itertools.product(range(255), range(255), range(255)))
	}

}







def draw_saved_solutions (conn, ranges, image_size, img_pixels):

	for line in conn:

		x, y, colour = json.loads(line)

		# remove.
		x_in_range = x > 0 and x < image_size['x']
		y_in_range = x > 0 and y < image_size['y']

		if x_in_range and y_in_range:

			img_pixels[x, y] = (colour[0], colour[1], colour[2])




def draw_solutions (ranges, dimensions, input_path, output_path):

	image_size = {
		'x': 0,
		'y': 0
	}

	with open(input_path) as fconn:

		for line in fconn:

			x, y, colour = json.loads(line)

			if x > image_size['x']:
				image_size['x'] = x

			if y > image_size['y']:
				image_size['y'] = y

	with open(input_path) as fconn:

		image_dimensions = (image_size['x'], image_size['y'])

		img        = Image.new('RGB', image_dimensions, constants['colours']['background'])
		img_pixels = img.load( )

	with open(input_path) as fconn:

		draw_saved_solutions(fconn, ranges, image_size, img_pixels)

		img.save(output_path)
