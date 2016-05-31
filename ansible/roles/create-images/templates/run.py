#!/usr/bin/env python

import os
import json

import subprocess
from sh import solve_polynomials
from sh import render_pixels
from sh import draw_solutions
from sh import mkdir
from sh import ln
from sh import rm





task_folder   = '/root/tasks/{{start_time}}'
argument_path = os.path.join(task_folder, 'repo', 'arguments', '{{argument_script}}')

constants = {
	'here': os.path.dirname(os.path.abspath(__file__)),
	'required_folders': [
		task_folder,
		task_folder + '/logs',
		task_folder + '/output/json',
		task_folder + '/output/images'
	],
	'paths': {

	}

}

constants['paths']['current_link'] = os.path.join(constants['here'], '/root/tasks/current')

constants['paths']['solution'] = os.path.join(
	constants['paths']['current_link'], 'output/json/solutions.jsonl')

constants['paths']['pixels']   = os.path.join(
	constants['paths']['current_link'], 'output/json/pixels.jsonl')

constants['paths']['image']    = os.path.join(
	constants['paths']['current_link'], 'output/images/images.png')






if os.path.islink(constants['paths']['current_link']):
	rm(constants['paths']['current_link'])

os.symlink(task_folder, constants['paths']['current_link'])

for path in constants['required_folders']:
	mkdir(path, '--parent')





argument_output = subprocess.check_output(['python3', argument_path])

try:
	arguments_json = json.loads(argument_output.decode("utf-8"))
except Exception as err:
	print(err)





for argument_set in arguments_json:

	solve_polynomials(
		order      = argument_set['solve_polynomial']['order'],
		range      = argument_set['solve_polynomial']['range'],
		assume_yes = True,
		_out       = constants['paths']['solution']
	)

	render_pixels(
		in_path    = constants['paths']['solution'],
		height     = argument_set['render_pixels']['height'],
		width      = argument_set['render_pixels']['width'],
		_out       = constants['paths']['pixels'],
	)

	draw_solutions(
		in_path    = constants['paths']['pixels'],
		xrange     = argument_set['render_pixels']['xrange'],
		yrange     = argument_set['render_pixels']['yrange'],
		height     = argument_set['render_pixels']['height'],
		width      = argument_set['render_pixels']['width'],
		out_path   = constants['paths']['image']
	)
