#!/usr/bin/env python

import os
from sh import solve_polynomials
from sh import render_pixels
from sh import draw_solutions
from sh import mkdir
from sh import ln
from sh import rm




task_folder = '/root/tasks/{{start_time}}'

constants = {
	'here': os.path.dirname(os.path.abspath(__file__)),
	'required_folders': [
		task_folder,
		task_folder + '/logs',
		task_folder + '/output/json',
		task_folder + '/output/images'
	]
}





symlink_path = os.path.join(constants['here'], '/root/tasks/current')

if os.path.islink(symlink_path):
	rm(symlink_path)

os.symlink(task_folder, symlink_path)

for path in constants['required_folders']:
	mkdir(path, '--parent')

solve_polynomials(
	order      = 5,
	range      = 10,
	assume_yes = True,
	_out       = os.path.join(symlink_path, 'output/json/solutions.jsonl')
)

render_pixels(
	in_path    = os.path.join(symlink_path, 'output/json/solutions.jsonl'),
	height     = 2000,
	width      = 2000,
	_out       = os.path.join(symlink_path, 'output/json/pixels.jsonl'),
)

draw_solutions(
	in_path    = os.path.join(symlink_path, 'output/json/pixels.jsonl'),
	xrange     = 2000,
	yrange     = 2000,
	_out       = os.path.join(symlink_path, 'output/images/images.png')
)
