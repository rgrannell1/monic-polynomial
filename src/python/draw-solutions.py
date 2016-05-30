#!/usr/bin/env python3

"""
draw-solutions.py

Usage:
	draw-solutions.py (--width=<NUM>) (--height=<NUM>) (--xrange=<NUM>) (--yrange=<NUM>) (--in-path=<STRING>) (--out-path=<STRING>)

Options:
	--in-path=<STRING>    The path to read points from.
	--out-path=<STRING>   The path to save the image to.
	--width=<NUM>         The image width .
	--height=<NUM>        The image height.
	--xrange=<NUM>        The maximum x value to include.
	--yrange=<NUM>        The maximum y value to include.
	-h, --help            Display the documentation.
"""

import os
import sys
import json
import time
import math
import itertools
from functools import reduce
from operator  import mul
from docopt import docopt
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






def product (nums):
	return reduce(mul, nums, 1)

def pixelise (coefficients, point, extrema, dimensions):

	coefficient_product = product(coefficients)

	x_offset                   = extrema['x']['min']
	y_offset                   = extrema['y']['min']
	coefficient_product_offset = extrema['coefficient_product']['min']

	normalised = [
		point[0]            - x_offset,
		point[1]            - y_offset,
		coefficient_product - coefficient_product_offset
	]

	percentage = [
		normalised[0] / (extrema['x']['max']                   - extrema['x']['min']),
		normalised[1] / (extrema['y']['max']                   - extrema['y']['min']),
		normalised[2] / (extrema['coefficient_product']['max'] - extrema['coefficient_product']['min'])
	]

	index = min(
		math.floor(percentage[2] * len(constants['colours']['points'])),
		len(constants['colours']['points']) - 1)

	return [
		math.floor(percentage[0] * dimensions['width']),
		math.floor(percentage[1] * dimensions['height']),
		constants['colours']['points'][index]
	]

def find_extrema (ranges, conn):

	extrema = {
		'x': {
			'min': +float('inf'),
			'max': -float('inf')
		},
		'y': {
			'min': +float('inf'),
			'max': -float('inf')
		},
		'coefficient_product': {
			'min': +float('inf'),
			'max': -float('inf')
		}
	}

	for line in conn:

		solution = json.loads(line)

		for x, y in solution['roots']:

			in_x_range = x <= ranges['x'] and x >= -ranges['x']
			in_y_range = y <= ranges['y'] and y >= -ranges['y']

			if in_x_range and in_y_range:

				coefficient_product = product(solution['coefficients'])

				if x > extrema['x']['max']:
					extrema['x']['max'] = x

				if x < extrema['x']['min']:
					extrema['x']['min'] = x

				if y > extrema['y']['max']:
					extrema['y']['max'] = y

				if y < extrema['y']['min']:
					extrema['y']['min'] = y

				if coefficient_product > extrema['coefficient_product']['max']:
					extrema['coefficient_product']['max'] = coefficient_product

				if coefficient_product < extrema['coefficient_product']['min']:
					extrema['coefficient_product']['min'] = coefficient_product

	return extrema

def draw_saved_solutions (conn, extrema, dimensions, ranges, img_pixels):

	for line in conn:

		solution = json.loads(line)

		for point in solution['roots']:

			in_x_range = point[0] <= ranges['x'] and point[0] >= -ranges['x']
			in_y_range = point[1] <= ranges['y'] and point[1] >= -ranges['y']

			if in_x_range and in_y_range:

				x, y, colour = pixelise(solution['coefficients'], point, extrema, dimensions)
				img_pixels[x, y] = colour

def draw (dimensions, ranges, input_path, output_path):

	with open(input_path) as fconn:

		extrema    = find_extrema(ranges, fconn)
		img        = Image.new('RGB', (dimensions["width"] + 1, dimensions["height"] + 1), constants['colours']['background'])
		img_pixels = img.load( )

	with open(input_path) as fconn:

		draw_saved_solutions(fconn, extrema, dimensions, ranges, img_pixels)

		img.save(output_path)





if __name__ == '__main__':

	arguments = docopt(__doc__, version = '0.1')

	draw(
		dimensions = {
			'width':  int(arguments['--width']),
			'height': int(arguments['--height'])
		},
		ranges = {
			'x': int(arguments['--xrange']),
			'y': int(arguments['--yrange'])
		},
		input_path  = arguments['--input-path'],
		output_path = arguments['--output-path']
	)
