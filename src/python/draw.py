
import os
import sys
import math
from docopt import docopt
from OpenGL.GL import *

from PIL import Image





constants = {
	'print_frequency': 10000,

	'flush_threshold': 100000,

	'output_path':     os.path.join(
		os.path.dirname(__file__),
		'../../output/polynomial-roots.csv'),
	'dimensions': {
		'width':  12000,
		'height': 4000,
	}
}



def pixelise (point, extrema, dimensions):

	x_offset = extrema['x']['min']
	y_offset = extrema['y']['min']

	normalised = [
		point[0] - x_offset,
		point[1] - y_offset
	]

	percentage = [
		normalised[0] / (extrema['x']['max'] - extrema['x']['min']),
		normalised[1] / (extrema['y']['max'] - extrema['y']['min'])
	]

	return [
		math.floor(percentage[0] * constants["dimensions"]['width']),
		math.floor(percentage[1] * constants["dimensions"]['height'])
	]





with open(constants['output_path']) as fpath:

	points  = [ [float(num) for num in root.strip( ).split(',')] for root in fpath.readlines( )]
	extrema = {
		'x': {
			'min': +math.inf,
			'max': -math.inf
		},
		'y': {
			'min': +math.inf,
			'max': -math.inf
		}
	}

	for x, y in points:

		if x > extrema['x']['max']:
			extrema['x']['max'] = x

		if x < extrema['x']['min']:
			extrema['x']['min'] = x

		if y > extrema['y']['max']:
			extrema['y']['max'] = y

		if y < extrema['y']['min']:
			extrema['y']['min'] = y

	pixels     = [pixelise(point, extrema, constants['dimensions']) for point in points]
	img        = Image.new('RGB', (constants["dimensions"]["width"] + 1, constants["dimensions"]["height"] + 1), "white")
	img_pixels = img.load( )

	for x, y in pixels:
		img_pixels[x, y] = (0, 0, 0)

	img.save('/home/ryan/test.png')
