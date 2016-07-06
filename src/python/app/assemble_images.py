#!/usr/bin/env python3

"""
Usage:
	assemble-images --task-path=<str>
	assemble-images (-h | --help)
Options:
	-h, --help    Show this documentation.
"""

import os
import re
import sys
import json
import subprocess

from docopt import docopt
from sh import montage




def list_images(task_path):

	def sort_images (name):
		return int(re.search('^[0-9]+', name).group(0))

	image_path  = os.path.join(task_path, 'output', 'images')

	number_of_images = len(os.listdir(image_path))

	side_length = number_of_images ** 0.5

	image_paths = [os.path.join(image_path, str(ith) + '.png') for ith in range(number_of_images)]

	if round(side_length) != side_length:
		sys.stderr.write(json.dumps({
			'message': 'strange number of pngs.'
		}))
		exit(1)

	columns = [ [ ] for _ in range(int(side_length)) ]

	for colnum in range(int(side_length)):
		for rownum in range(int(side_length)):
			columns[colnum].append(image_paths.pop(0))

	for row in map(list, zip(*columns)):
		for ith in range(len(row)):
			yield row[ith]

def assemble_images(images):

	command = ['montage'] + list(images) + ['-mode concatenate', '-background "#FFFFFF"', '-limit memory 1GB', '~/assembled.png']
	os.system(' '.join(command))





if __name__ == '__main__':

	arguments = docopt(__doc__)
	assemble_images(list_images(arguments['--task-path']))
