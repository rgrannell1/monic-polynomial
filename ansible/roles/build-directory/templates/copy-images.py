#!/usr/bin/env python3





import os
import sys
import shutil





constants = {
	'paths': {
		'tasks':    '/root/tasks',
		'archives': '/root/archives',
	}
}





for dir_name in os.listdir(constants['paths']['tasks']):

	if dir_name == 'current':
		next

	directory       = os.path.join(constants['paths']['tasks'], dir_name)
	image_directory = os.path.join(directory, 'output', 'images')

	if os.path.exists(image_directory):
		for image_name in os.listdir(image_directory):

			image_path = os.path.join(image_directory, image_name)
			image_dest = os.path.join(constants['paths']['archives'], image_name)
			shutil.copy(image_path, image_dest)
