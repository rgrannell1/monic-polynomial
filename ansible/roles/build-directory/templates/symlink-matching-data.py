#!/usr/bin/env python3





import os
import sys





constants = {
	'paths': {
		'tasks':    '/root/tasks',
		'current':  '/root/tasks/current',
		'archives': '/root/archives',
	}
}





def read_arguments (argument_path):

	argument_output = subprocess.check_output(['python3', argument_path])

	try:
		return json.loads(argument_output.decode("utf-8"))
	except Exception as err:
		print(err)




current_arguments = read_arguments(os.path.join(constants['paths']['current'], 'jobs', 'arguments.py'))





for dir_name in os.listdir(constants['paths']['tasks']):

	if dir_name == 'current':
		next

	directory      = os.path.join(constants['paths']['tasks'], dir_name)
	arguments_file = os.path.join(directory, 'jobs', 'arguments.py')

	if os.path.exists(arguments_file):

		candidate_arguments = read_arguments(arguments_file)

		# fetch the last render pixels and solve polynomial arguments

		pass
