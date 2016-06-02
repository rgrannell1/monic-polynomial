#!/usr/bin/env python3

import os
import json

import subprocess
from sh import solve_polynomials
from sh import render_pixels
from sh import draw_solutions
from sh import mkdir
from sh import ln
from sh import rm
from sh import cp





task_folder   = '/root/tasks/{{start_time}}'
argument_path = os.path.join(task_folder, 'jobs', '{{argument_script}}')

constants = {
	'here': os.path.dirname(os.path.abspath(__file__)),
	'required_folders': [
		task_folder,
		task_folder + '/logs',
		task_folder + '/output/json',
		task_folder + '/output/images',
		'/root/archives'
	],
	'paths': {
		'archives': '/root/archives'
	}

}

constants['paths']['current_link'] = os.path.join(constants['here'], '/root/tasks/current')

constants['paths']['solution'] = os.path.join(
	constants['paths']['current_link'], 'output/json/solutions.jsonl')

constants['paths']['pixels']   = os.path.join(
	constants['paths']['current_link'], 'output/json/pixels.jsonl')

constants['paths']['image']    = os.path.join(
	constants['paths']['current_link'], 'output/images/{{start_time}}.png')

constants['paths']['archive_image'] = os.path.join(
	constants['paths']['archives'], '{{start_time}}.png')





exec(open(os.path.join(os.path.dirname(__file__), 'repo/src/python/solve-polynomials.py')).read( ))
exec(open(os.path.join(os.path.dirname(__file__), 'repo/src/python/draw-solutions.py')).read( ))
exec(open(os.path.join(os.path.dirname(__file__), 'repo/src/python/render-pixels.py')).read( ))






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





count = 0

for argument_set in arguments_json:

	if argument_set['solve_polynomial']:

		solve_polynomials(
			order      = argument_set['solve_polynomial']['order'],
			range      = argument_set['solve_polynomial']['range'],
			assume_yes = True,
			_out       = constants['paths']['solution'],
			_err       = print)

	if argument_set['render_pixels']:

		render_pixels(
			in_path    = constants['paths']['solution'],
			xrange     = argument_set['render_pixels']['xrange'],
			yrange     = argument_set['render_pixels']['yrange'],
			width      = argument_set['render_pixels']['width'],
			_out       = constants['paths']['pixels'],
			_err       = print)

	if argument_set['render_pixels']:

		draw_solutions(
			in_path    = constants['paths']['pixels'],
			xrange     = argument_set['draw_solutions']['xrange'],
			yrange     = argument_set['draw_solutions']['yrange'],
			width      = argument_set['draw_solutions']['width'],
			out_path   = constants['paths']['image'] + '-' + str(count),
			_err       = print)

	count += 1

cp(
	constants['paths']['image'],
	constants['paths']['archive_image'])
