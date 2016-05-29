
"""
draw-polynomials.py

Usage:
	draw-polynomials.py (--width=<NUM>) (--height=<NUM>)

Options:
	--width=<NUM>    The image width .
	--height=<NUM>   The image height.
	-h, --help       Display the documentation.
"""

import os
import sys
import json
import math
from docopt import docopt
from PIL    import Image





constants = {
	'print_frequency': 10000,

	'flush_threshold': 100000,

	'output_path':     os.path.join(
		os.path.dirname(__file__),
		'../../output/polynomial-roots.csv')
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
		math.floor(percentage[0] * dimensions['width']),
		math.floor(percentage[1] * dimensions['height'])
	]




def draw_solutions (dimensions):

	with open(constants['output_path']) as fpath:

		solutions  = [json.loads(solution) for solution in fpath.readlines( )]
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

		for solution in solutions:
			for x, y in solution['roots']:

				if x > extrema['x']['max']:
					extrema['x']['max'] = x

				if x < extrema['x']['min']:
					extrema['x']['min'] = x

				if y > extrema['y']['max']:
					extrema['y']['max'] = y

				if y < extrema['y']['min']:
					extrema['y']['min'] = y

		pixels     = [pixelise(point, extrema, dimensions) for point in points]
		img        = Image.new('RGB', (dimensions["width"] + 1, dimensions["height"] + 1), "white")
		img_pixels = img.load( )

		for x, y in pixels:
			img_pixels[x, y] = (0, 0, 0)

		img.save('/home/ryan/test.png')





if __name__ == '__main__':

	arguments = docopt(__doc__, version = '0.1')

	draw_solutions(
		dimensions = {
			'width':  int(arguments['--width']),
			'height': int(arguments['--height'])
		}
	)
