#!/usr/bin/env python3

"""
Name:
	polynomial - plot polynomial solutions
Usage:
	polynomial
	polynomial (-h | --help)
Description:
	Polynomial is a CLI tool that plots the solution to large numbers of monic polynomials, to creaet
	beautiful fractal images.

Authors:
	Róisín Grannell
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
