#!/usr/bin/env python3

"""
Usage:
	polynomial
	polynomial (-h | --help)
Description:
	Plot an argand diagram of monic polynomial solutions.
Options:
	-h, --help    Show this documentation.
"""

from docopt  import docopt
from app.app import app
from config import config

import traceback
import json

if __name__ == '__main__':
	try:
		app(config())
	except Exception as err:
		traceback.print_exc( )
		print(str(err))
