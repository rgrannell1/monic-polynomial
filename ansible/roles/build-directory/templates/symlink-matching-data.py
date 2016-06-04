#!/usr/bin/env python3





import os
import sys
import json
import shutil
import subprocess





task_folder  = '/root/tasks/{{start_time}}'
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
	"""
	read arguments from a file.
	"""

	argument_output = subprocess.check_output(['python3', argument_path])

	try:
		return json.loads(argument_output.decode("utf-8"))
	except Exception as err:
		print(err)

def deep_equal (dict0, dict1):
	"""
	check that two dictionaries are identical.
	"""

	return json.dumps(dict0) == json.dumps(dict1)






def list_task_arguments (current_task_folder):
	"""
	list and parse all argument files.
	"""

	for dir_name in os.listdir(constants['paths']['tasks']):

		if dir_name == 'current':
			next

		task_directory = os.path.join(constants['paths']['tasks'], dir_name)

		if task_directory == current_task_folder:
			next

		arguments_file = os.path.join(task_directory, 'arguments.py')

		if os.path.exists(arguments_file):

			yield {
				'directory': task_directory,
				'arguments': read_arguments(arguments_file)
			}

def find_existing_result_symlinks (current_arguments, current_task_folder):

	old_task_paths  = { }
	other_arguments = list(list_task_arguments(current_task_folder))

	for other_argument_sets in other_arguments:

		other_directory = other_argument_sets['directory']
		other_arguments = other_argument_sets['arguments']

		for other_argument_set in other_arguments:

			for current_argument_set in current_arguments:

				if 'solve_polynomial' in current_argument_set:

					if deep_equal(current_argument_set['solve_polynomial'], current_argument_set['solve_polynomial']):
						old_task_paths['solutions'] = other_directory

				if 'render_pixels' in current_argument_set:

					if deep_equal(current_argument_set['render_pixels'], current_argument_set['render_pixels']):
						old_task_paths['pixels'] = other_directory

	return old_task_paths

def copy_task_files (task_folder, current_link):

	if os.path.isfile(task_folder['solutions']):

		src  = os.path.join(task_folder['solutions'], 'output', 'json', 'solutions.jsonl')
		dest = os.path.join(current_link,             'output', 'json', 'solutions.jsonl')

		os.link(src, dest)
		print('linking ' + src + ' -> ' + ' ' + dest)

	if os.path.isfile(task_folder['pixels']):

		src  = os.path.join(task_folder['pixels'], 'output', 'json', 'pixels.jsonl')
		dest = os.path.join(current_link,          'output', 'json', 'pixels.jsonl')

		os.link(src, dest)
		print('linking ' + src + ' -> ' + ' ' + dest)




def symlink_existing_results (task_folder, current_link):

	# get the current argument list.
	current_arguments = read_arguments(os.path.join(task_folder, 'arguments.py'))
	result_links      = find_existing_result_symlinks(current_arguments, task_folder)

	copy_task_files(result_links, current_link)




symlink_existing_results(task_folder, current_link)
