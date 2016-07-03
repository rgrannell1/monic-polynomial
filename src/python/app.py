

import os
import re
import sys
import json
import math
import datetime
import subprocess

from docopt import docopt
from sh import montage

from commons           import colours
from commons.constants import constants
from solve_polynomials import solve_polynomials
from render_pixels     import render_pixels
from draw_solutions    import draw_solutions







def app (arguments):

	paths = { }

	paths['tasks']    = os.path.dirname(arguments['--task-path'])
	paths['archives'] = os.path.join(os.path.dirname(paths['tasks']), 'archives')
	paths['current_link'] = os.path.join(paths['tasks'], 'current')
	paths['solutions']    = os.path.join(paths['current_link'], 'output/json/solutions.jsonl')
	paths['pixels']       = os.path.join(paths['current_link'], 'output/json/pixels.jsonl')
	paths['images']       = os.path.join(paths['current_link'], 'output/images/')
	paths['final_image']  = os.path.join(paths['current_link'], 'output/final_image.png')

	required_folders = [
		os.path.join(arguments['--task-path']),
		os.path.join(arguments['--task-path'], '/logs'),
		os.path.join(arguments['--task-path'], '/output/json'),
		os.path.join(arguments['--task-path'], '/output/images'),
		paths['archives']
	]

	arguments = read_arguments(os.path.join(paths['current_link'], 'arguments.py'))

	generate_polynomial_image(arguments, {
		'solutions':    paths['solutions'],
		'pixels':       paths['pixels'],
		'current_link': paths['current_link']
	})

	assemble_images(list_images(paths['images']), paths['final_image'])






def list_images(image_path):

	def sort_images (name):
		return int(re.search('^[0-9]+', name).group(0))

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

def assemble_images(images, output_path):

	command = ['montage'] + list(images) + ['-mode concatenate', '-background "#FFFFFF"', '-limit memory 1GB', output_path]
	os.system(' '.join(command))






def read_arguments (argument_path):

	argument_output = subprocess.check_output(['python3', argument_path])

	try:
		return json.loads(argument_output.decode("utf-8"))
	except Exception as err:
		print(err)

	return argument_output





def generate_polynomial_image (arguments, paths):

	image_path = os.path.join(paths['current_link'], 'output', 'images')

	pixel_path    = paths['pixels']
	solution_path = paths['solutions']

	if not os.path.isfile(solution_path):

		predicate = None

		if 'predicate' in arguments['solve_polynomial']:
			predicate = constants['polynomial_predicates'][arguments['solve_polynomial']['predicate']]

		solve_polynomials(
			arguments['solve_polynomial']['order'],
			arguments['solve_polynomial']['range'],
			predicate,
			solution_path
		)

		assert os.path.isfile(solution_path), solution_path + " not created."

	if not os.path.isfile(pixel_path):

		render_pixels(
			paths = {
				'input':  solution_path,
				'output': pixel_path
			},
			ranges = arguments['render_pixels']['ranges'],
			width     =  arguments['render_pixels']['width'],
			colour_fn = colours.hue
		)

		assert os.path.isfile(pixel_path), pixel_path + " not created."

	tile_count = max(1, math.ceil(arguments['render_pixels']['width'] / constants['tile_size']))

	draw_solutions(
		paths = {
			'input':      pixel_path,
			'output_dir': image_path
		},
		tile_counts = {
			'x': tile_count,
			'y': tile_count
		}
	)
