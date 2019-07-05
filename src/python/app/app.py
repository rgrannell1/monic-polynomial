
import os
import re
import sys
import json
import math
import datetime
import subprocess
import logging
import coloredlogs

coloredlogs.install()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from typing import Generator, Dict, Callable

from docopt import docopt
from sh import montage

from commons import colours
from commons.constants  import constants

from app.solve_polynomials import solve_polynomials
from app.render_pixels import render_pixels
from app.draw_solutions import draw_solutions

def create_required_folder(paths:Dict) -> None:
	required_folders = [
		paths['current_link'],
		os.path.join(paths['current_link'], 'output'),
		os.path.join(paths['current_link'], 'output', 'json'),
		os.path.join(paths['current_link'], 'output', 'images')
	]

	for path in required_folders:
		if not os.path.exists(path):
			os.makedirs(path)

def app (arguments:Dict) -> None:
	"""top-level of the polynomial solving app.
	"""

	root = os.path.dirname('./')
	paths = {
		'tasks': root,
		'current_link': os.path.join(root, 'current'),
		'solutions': os.path.join(root, 'current/output/json/solutions.jsonl'),
		'pixels': os.path.join('current/output/json/pixels.jsonl'),
		'images': os.path.join('current/output/images/'),
		'final_image': os.path.join('current/output/final_image.png')
	}

	create_required_folder(paths)

	generate_polynomial_image(arguments, {
		'solutions': paths['solutions'],
		'pixels': paths['pixels'],
		'current_link': paths['current_link']
	})

	assemble_images(list_images(paths['images']), paths['final_image'])

def list_images (image_path:str) -> Generator[str, float, str]:
	"""list images in a directory.
	"""
	number_of_images = len(os.listdir(image_path))

	side_length = number_of_images ** 0.5

	image_paths = [os.path.join(image_path, str(ith) + '.png') for ith in range(number_of_images)]

	if round(side_length) != side_length:
		logging.error('strange number of PNGs')
		exit(1)

	columns = [ [ ] for _ in range(int(side_length)) ]

	for colnum in range(int(side_length)):
		for _ in range(int(side_length)):
			columns[colnum].append(image_paths.pop(0))

	for row in map(list, zip(*columns)):
		for ith in range(len(row)):
			yield row[ith]

def assemble_images (images:str, output_path:str) -> None:
	"""use montage to assemble each image
	"""
	command = ' '.join(['montage'] + list(images) + ['-mode concatenate', '-limit memory 3GB', output_path])

	logging.info('assembing image "{}" ({})'.format(output_path, len(list(images))))

	os.system(command)

	if not os.path.isfile(output_path):
		logging.error('failed to create image {}'.format(output_path))


def choose_colour_fn(arguments: Dict):
	colour_fn = colours.hue

	if 'colour_mode' in arguments['render_pixels']:
		colour_fn = colours[arguments['render_pixels']['colour_mode']]

	return colour_fn

def generate_polynomial_image (arguments:Dict, paths:Dict) -> None:
	"""solve equations, then draw the solutions
	"""

	solve_args = arguments['solve_polynomial']
	solve_polynomials(solve_args['order'], solve_args['range'])

	logging.info('🎨 rendering images')

	render_pixels(
		paths={
			'output': paths['pixels']
		},
		ranges=arguments['render_pixels']['ranges'],
		width=arguments['render_pixels']['width'],
		colour_fn=choose_colour_fn(arguments)
	)

	tile_count = max(1, math.ceil(arguments['render_pixels']['width'] / constants['tile_size']))

	draw_solutions(
		paths={
			'input': paths['pixels'],
			'output_dir': os.path.join(paths['current_link'], 'output', 'images')
		},
		tile_counts={
			'x': tile_count,
			'y': tile_count
		}
	)
