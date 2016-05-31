#!/usr/bin/env python

import os
from sh import solve_polynomials
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
	out_path   = os.path.join(task_folder, 'output/json/solutions.jsonl'),
	order      = 5,
	range      = 10,
	assume_yes = True
)

render_pixels(
	in_path    = os.path.join(task_folder, 'output/json/solutions.jsonl'),
	out_path   = os.path.join(task_folder, 'output/json/pixels.jsonl'),
	height     = 2000,
	width      = 2000,
)
