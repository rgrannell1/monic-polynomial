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






if __name__ == '__main__':
	arguments = docopt(__doc__)
	app(arguments)
