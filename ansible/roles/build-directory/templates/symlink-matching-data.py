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

def find_existing_result_symlinks (current_arguments, current_task_folder):

	old_task_paths  = {
		'solutions': None,
		'pixels':    None
	}

	other_arguments = list(list_task_arguments(current_task_folder))

	for other_argument_sets in other_arguments:

		other_directory = other_argument_sets['directory']
		other_arguments = other_argument_sets['arguments']

		argument_data = [
			{
				'name': 'solutions',
				'key': 'solve_polynomial',
				'path': os.path.join(other_directory, 'output', 'json', 'solutions.jsonl')
			},
			{
				'name': 'pixels',
				'key': 'render_pixels',
				'path': os.path.join(other_directory, 'output', 'json', 'pixels.jsonl')
			}
		]

		for other_argument_set in other_arguments:

			for current_argument_set in current_arguments:

				for argument_handle in argument_data:

					if argument_handle['key'] in current_argument_set:

						arguments_are_equal = deep_equal(
							current_argument_set[argument_handle['key']],
							current_argument_set[argument_handle['key']])

						file_exists = os.path.isfile(argument_handle['path'])

						if arguments_are_equal and file_exists:
							old_task_paths[argument_handle['name']] = argument_handle['path']

	return old_task_paths

def copy_task_files (task_folder, current_link):

	paths = {
		'old': task_folder,
		'new': {
			'solutions': os.path.join(current_link, 'output', 'json', 'solutions.jsonl'),
			'pixels':    os.path.join(current_link, 'output', 'json', 'pixels.jsonl')
		}
	}

	if paths['old']['solutions'] and os.path.isfile(paths['old']['solutions']):

		src  = paths['old']['solutions']
		dest = paths['new']['solutions']

		if not os.path.isfile(dest):
			os.symlink(src, dest)
			sys.stderr.write('linking ' + src + ' -> ' + ' ' + dest + '\n')

	if paths['old']['pixels'] and os.path.isfile(paths['old']['pixels']):

		src  = paths['old']['pixels']
		dest = paths['new']['pixels']

		if not os.path.isfile(dest):
			os.symlink(src, dest)
			sys.stderr.write('linking ' + src + ' -> ' + ' ' + dest + '\n')




def symlink_existing_results (task_folder, current_link):

	# get the current argument list.
	current_arguments = read_arguments(os.path.join(task_folder, 'arguments.py'))
	result_links      = find_existing_result_symlinks(current_arguments, task_folder)

	copy_task_files(result_links, current_link)




symlink_existing_results(task_folder, current_link)
