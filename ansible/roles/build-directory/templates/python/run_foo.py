
import os
import json
import datetime
import subprocess

from commons           import colours
from commons.constants import constants
from solve_polynomials import solve_polynomials
from render_pixels     import render_pixels
from draw_solutions    import draw_solutions




def read_arguments (argument_path):

	argument_output = subprocess.check_output(['python3', argument_path])

	try:
		return json.loads(argument_output.decode("utf-8"))
	except Exception as err:
		print(err)

	return argument_output





def list_task_arguments ( ):
	"""
	list and parse all argument files.
	"""

	current_link = os.path.realpath(constants['paths']['current_link'])

	for dir_name in os.listdir(constants['paths']['tasks']):

		candidate_task_directory = os.path.join(constants['paths']['tasks'], dir_name)

		is_current_symlink   = dir_name == 'current'
		is_current_directory = candidate_task_directory == current_task_folder

		if not (is_current_directory or is_current_symlink):

			arguments_file = os.path.join(candidate_task_directory, 'arguments.py')

			if os.path.exists(arguments_file):

				yield {
					'directory': candidate_task_directory,
					'arguments': read_arguments(arguments_file)
				}





def find_cached_paths (arguments):

	solution_path   = constants['paths']['solution']
	pixel_path      = constants['paths']['pixels']
	other_arguments = list_task_arguments( )

	return {
		'solution': solution_path,
		'pixels':   pixel_path
	}





def run_foobar (arguments, paths):

	image_path = os.path.join(constants['paths']['current_link'], 'output', 'images', str(datetime.datetime.now( )) + '.png')

	pixel_path    = paths['pixels']
	solution_path = paths['solution']

	if not os.path.isfile(solution_path):

		solve_polynomials(
			arguments['solve_polynomial']['order'],
			arguments['solve_polynomial']['range'],
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






arguments = read_arguments(os.path.join(constants['paths']['current_link'], 'arguments.py'))

run_foobar(arguments, find_cached_paths(arguments))
