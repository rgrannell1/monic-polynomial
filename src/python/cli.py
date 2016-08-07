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
from commons import logger
import json






if __name__ == '__main__':

	arguments = docopt(__doc__)

	logger.log(json.dumps(arguments))

	try:
		app(arguments)
	except Exception as err:

		traceback.print_exc( )
		print(str(err))

		logger.log(str(err))
