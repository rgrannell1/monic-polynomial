#!/usr/bin/env python3

"""
draw-solutions.py

Usage:
	draw-solutions.py (--xrange=<NUM>) (--yrange=<NUM>) (--width=<NUM>) (--height=<NUM>) (--in-path=<STRING>) (--out-path=<STRING>)

Options:
	--in-path=<STRING>    The path to read points from.
	--out-path=<STRING>   The path to save the image to.
	--xrange=<NUM>        The maximum x value to include.
	--yrange=<NUM>        The maximum y value to include.
	--width=<NUM>         The width.
	--height=<NUM>        The height.
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







def draw_saved_solutions (conn, ranges, img_pixels):

	for line in conn:

		x, y, colour = json.loads(line)
		img_pixels[x, y] = colour

def draw (ranges, dimensions, input_path, output_path):

	with open(input_path) as fconn:

		img        = Image.new('RGB', (dimensions["width"] + 1, dimensions["height"] + 1), constants['colours']['background'])
		img_pixels = img.load( )

	with open(input_path) as fconn:

		draw_saved_solutions(fconn, ranges, img_pixels)

		img.save(output_path)





if __name__ == '__main__':

	arguments = docopt(__doc__, version = '0.1')

	draw(
		ranges = {
			'x': int(arguments['--xrange']),
			'y': int(arguments['--yrange'])
		},
		dimensions = {
			'width':  int(arguments['--width']),
			'height': int(arguments['--height'])
		},
		input_path  = arguments['--in-path'],
		output_path = arguments['--out-path']
	)
