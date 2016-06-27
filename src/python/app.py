

import os
import sys
import json
import shutil
import datetime
import subprocess

from commons           import colours
from solve_polynomials import solve_polynomials
from render_pixels     import render_pixels
from draw_solutions    import draw_solutions







def app (arguments):

	paths = { }

	paths['tasks']    = os.path.dirname(arguments['--task-path'])
	paths['archives'] = os.path.join(os.path.dirname(paths['tasks']), 'archives')
	paths['current_link'] = os.path.join(paths['tasks'], 'current')
	paths['solution']     = os.path.join(paths['current_link'], 'output/json/solutions.jsonl')
	paths['pixels']       = os.path.join(paths['current_link'], 'output/json/pixels.jsonl')

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

	copy_images({
		'tasks':    paths['tasks'],
		'archives': paths['archives']
	})





def read_arguments (argument_path):

	argument_output = subprocess.check_output(['python3', argument_path])

	try:
		return json.loads(argument_output.decode("utf-8"))
	except Exception as err:
		print(err)

	return argument_output




def copy_images (paths):


	for dir_name in os.listdir(paths['tasks']):

		if dir_name == 'current':
			next

		directory       = os.path.join(paths['tasks'], dir_name)
		image_directory = os.path.join(directory, 'output', 'images')

		if os.path.exists(image_directory):
			for image_name in os.listdir(image_directory):

				image_path = os.path.join(image_directory, image_name)
				image_dest = os.path.join(paths['archives'], image_name)
				shutil.copy(image_path, image_dest)





def generate_polynomial_image (arguments, paths):


	image_path = os.path.join(paths['current_link'], 'output', 'images', str(datetime.datetime.now( )) + '.png')

	pixel_path    = paths['pixels']
	solution_path = paths['solution']

	if not os.path.isfile(solution_path):

		solve_polynomials(
			arguments['solve_polynomial']['order'],
			arguments['solve_polynomial']['range'],
			constants['polynomial_predicates'][arguments['solve_polynomial']['predicate']],
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

	draw_solutions(
		paths = {
			'input':  pixel_path,
			'output': image_path
		}
	)

	assert os.path.isfile(image_path), image_path + " not created."
