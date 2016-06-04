#!/usr/bin/env python3





import os
import sys
import json
import shutil
import subprocess






here         = os.path.dirname(os.path.abspath(__file__))
current_link = os.path.join(here, '/root/tasks/current')

constants = {
	'paths': {
		'tasks':    '/root/tasks',
		'current':  '/root/tasks/current',
		'archives': '/root/archives',
		'solution': os.path.join(current_link, 'output/json/solutions.jsonl'),
		'pixels':   os.path.join(current_link, 'output/json/pixels.jsonl')
	}
}





def read_arguments (argument_path):

	argument_output = subprocess.check_output(['python3', argument_path])

	try:
		return json.loads(argument_output.decode("utf-8"))
	except Exception as err:
		print(err)




current_arguments = read_arguments(os.path.join(constants['paths']['current'], 'arguments.py'))

last_argument = {
	'solve_polynomial': {
		'path':      None,
		'arguments': None
	},
	'render_pixels':    {
		'path':      None,
		'arguments': None
	}
}

for

	if 'solve_polynomial' in last_argument:
		last_argument['solve_polynomial'] = last_argument['solve_polynomial']

	if 'render_pixels' in last_argument:
		last_argument['render_pixels'] = last_argument['render_pixels']




for dir_name in os.listdir(constants['paths']['tasks']):

	if dir_name == 'current':
		next

	directory      = os.path.join(constants['paths']['tasks'], dir_name)
	arguments_file = os.path.join(directory, 'arguments.py')

	last_argument = {
		'solve_polynomial': {
			'path':      None,
			'arguments': None
		},
		'render_pixels':    {
			'path':      None,
			'arguments': None
		}
	}

	if os.path.exists(arguments_file):

		candidate_arguments = read_arguments(arguments_file)

		if 'solve_polynomial' in last_argument:
			last_argument['solve_polynomial'] = last_argument['solve_polynomial']

		if 'render_pixels' in last_argument:
			last_argument['render_pixels'] = last_argument['render_pixels']

		# fetch the last render pixels and solve polynomial arguments

	solve_polynomials_equal = json.dumps(current_arguments['solve_polynomial']) == json.dumps(last_argument['solve_polynomial'])
	render_pixels_equal     = json.dumps(current_arguments['render_pixels'])    == json.dumps(last_argument['render_pixels'])

	if solve_polynomials_equal:

		shutil.copyfile(last_argument['solve_polynomial']['path'], constants['paths']['solutions'])

	if render_pixels_equal:

		shutil.copyfile(last_argument['render_pixels']['path'], constants['paths']['pixels'])
