#!/usr/bin/env python3

"""
render-pixels.py

Usage:
	render-pixels.py (--width=<NUM>) (--xrange=<NUM>) (--yrange=<NUM>) (--in-path=<STRING>)

Options:
	--in-path=<STRING>    The path to read points from.
	--width=<NUM>         The image width .
	--xrange=<NUM>        The image width .
	--yrange=<NUM>        The image height.
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
	'flush_threshold': 100,

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

	x_diff = extrema['x']['max'] - extrema['x']['min']
	y_diff = extrema['y']['max'] - extrema['y']['min']

	height = (y_diff / x_diff) * dimensions['width']

	return [
		math.floor(percentage[0] * dimensions['width']),
		math.floor(percentage[1] * height),
		constants['colours']['points'][index]
	]

def find_extrema (conn, ranges):

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

			x_in_range = x >= -ranges['x'] and x <= ranges['x']
			y_in_range = y >= -ranges['y'] and y <= ranges['y']

			if x_in_range and y_in_range:

				print(x)
				print(y)

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

def save_pixels (input_path, extrema, ranges, dimensions):

	with open(input_path) as fconn:

		for line in fconn:

			data_buffer = [ ]
			solution    = json.loads(line)

			for point in solution['roots']:

				x, y, colour = pixelise(solution['coefficients'], point, extrema, dimensions)

				x_in_range = x >= -ranges['x'] and x <= ranges['x']
				y_in_range = y >= -ranges['y'] and y <= ranges['y']

				if x_in_range and y_in_range:

					buffered_write((x, y, colour), data_buffer)

			buffered_write((x, y, colour), data_buffer, force = True)

def buffered_write (data, data_buffer, force = False):

	if len(data_buffer) == constants["flush_threshold"] or force:
		for old_datum in data_buffer:
			print(json.dumps(old_datum))
		del data_buffer[:]

	data_buffer.append(data)

def draw (dimensions, ranges, input_path):

	with open(input_path) as fconn:
		extrema = find_extrema(fconn, ranges)

	save_pixels(input_path, extrema, ranges, dimensions)





if __name__ == '__main__':

	arguments = docopt(__doc__, version = '0.1')

	draw(
		dimensions = {
			'width':  int(arguments['--width'])
		},
		ranges = {
			'x': int(arguments['--xrange']),
			'y': int(arguments['--yrange'])
		},
		input_path  = arguments['--in-path']
	)
