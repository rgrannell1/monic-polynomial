#!/usr/bin/env python3

"""
Usage:
	polynomial --task-path=<str>
	polynomial (-h | --help) --task-path=<str>
Options:
	-h, --help    Show this documentation.
"""

from docopt  import docopt
from app.app import app

import traceback
import json

if __name__ == '__main__':
	arguments = docopt(__doc__)
	arguments['solve_polynomial'] = {
		'order': 5,
		'range': 15
	}
	arguments['render_pixels'] = {
		'ranges': {
			'x': [-0.3, +0.3],
			'y': [-0.7, -1.3],
			'colour_mode': 'hue'
		},
		'width': 1 * 1000
	}

	try:
		app(arguments)
	except Exception as err:

		traceback.print_exc( )
		print(str(err))
