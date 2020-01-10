
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

from typing import Dict, Callable

from docopt import docopt
from sh import montage
from typing import List

from shared import utils
from shared import colours
from shared.constants  import constants

from app.solve_polynomials import solve_polynomials
from app.render_pixels import render_pixels
from app.draw_solutions import draw_solutions

def create_required_folder(paths:Dict[str, str]) -> None:
	"""
	create any folders that are needed by the program.
	"""
	required_folders = [
		paths['current_link'],
		os.path.join(paths['current_link'] ),
		os.path.join(paths['current_link'], 'json'),
		os.path.join(paths['current_link'], 'images')
	]

	for path in required_folders:
		if not os.path.exists(path):
			os.makedirs(path)

def app (arguments:Dict) -> None:
	"""top-level of the polynomial solving app.
	"""

	root = os.path.dirname('/')
	paths = {
		'tasks': root,
		'current_link': os.path.join(root, 'current'),
		'solutions': os.path.join(root, 'current/json/solutions.jsonl'),
		'pixels': os.path.join(root, 'current/json/pixels.jsonl'),
		'images': os.path.join(root, 'current/images/'),
		'final_image': os.path.join(root, 'current/final_image.png')
	}

	create_required_folder(paths)

	# -- TODO wire in optional solving and drawing.
	if True:
		solve_all_polynomials(arguments, paths)

	if True:
		generate_polynomial_image(arguments, paths)
		assemble_images(list_images(paths['images']), paths['final_image'])

def list_images (image_path:str):
	"""
	list images in a directory.
	"""
	number_of_images = len(os.listdir(image_path))

	if number_of_images == 0:
		logging.error('no images to assemble in directory {}'.format(image_path))
		exit(1)

	# -- get the square root ot get the side length
	side_length = number_of_images ** 0.5

	image_paths = [os.path.join(image_path, str(ith) + '.png') for ith in range(number_of_images)]

	if round(side_length) != side_length:
		logging.error('non-square array of images to assemble')
		exit(1)

	side = int(side_length)

	columns = [ [ ] for _ in range(side) ]

	for colnum in range(side):
		for _ in range(side):
			columns[colnum].append(image_paths.pop(0))

	for row in map(list, zip(*columns)):
		for ith in range(len(row)):
			yield row[ith]

def show_assemble_splash (command):
	splash_text = """

		📸 Assembling Sub-Images 📸

		cmd:
		{}

	""".format(command)

	print(splash_text)

def assemble_images (images, output_path:str) -> None:
	"""
	use 'montage' to assemble each image
	"""

	image_list = list(images)

	if len(image_list) == 0:
		logging.error('no images to assemble')
		exit(1)

	for image in images:
		if not os.path.isfile(image):
			logging.error('subimage {} was not found'.format(image))
			exit(1)

	logging.info('all subimages appear to be exist.')

	montage_cmd = ' '.join(['montage'] + image_list + ['-mode concatenate', '-limit memory 4GB', output_path])

	show_assemble_splash(montage_cmd)

	logging.info('assembing image "{}" ({})'.format(output_path, len(image_list)))

	os.system(montage_cmd)

	if not os.path.isfile(output_path):
		logging.error('failed to create image {}'.format(output_path))

def choose_colour_fn (arguments: Dict):
	"""
	choose which colours will be used for the graph
	"""
	colour_fn = colours.hue

	if 'colour_mode' in arguments['render_pixels']:
		colour_fn = colours[arguments['render_pixels']['colour_mode']]

	return colour_fn

def product_metric(coefficients):
	"""
	a product_metric used to colour the graph
	"""
	return utils.product(coefficients)

def min_metric(coefficients):
	"""
	colour by minimum coefficient
	"""
	return min(coefficients)

def choose_metric_fn (arguments: Dict):
	"""
	choose the metric function used to determine the polynomial solution colour.
	"""
	mode = arguments['render_pixels']['ranges']['metric_mode']

	if mode == 'min':
		return min_metric
	elif mode == 'product':
		return product_metric

def solve_all_polynomials(arguments: Dict, paths: Dict) -> None:
	"""
	solve equations
	"""
	solve_args = arguments['solve_polynomial']
	solve_polynomials(solve_args['order'], solve_args['range'])

def generate_polynomial_image (arguments:Dict, paths:Dict) -> None:
	"""
	solve equations, then draw the solutions
	"""

	logging.info('🎨 rendering images')

	render_pixels(
		paths={
			'output': paths['pixels']
		},
		ranges=arguments['render_pixels']['ranges'],
		width=arguments['render_pixels']['width'],
		colour_fn=choose_colour_fn(arguments),
		metric_fn=choose_metric_fn(arguments)
	)

	tile_count = max(1, math.ceil(arguments['render_pixels']['width'] / constants['tile_size']))

	draw_solutions(
		paths={
			'input': paths['pixels'],
			'output_dir': os.path.join(paths['current_link'], 'images')
		},
		tile_counts={
			'x': tile_count,
			'y': tile_count
		}
	)
