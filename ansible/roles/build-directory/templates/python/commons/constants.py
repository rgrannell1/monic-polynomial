
import os





here          = os.path.dirname(os.path.abspath(__file__))
current_link  = '/root/tasks/current'

constants = {
	'print_frequency': 10000,
	'flush_threshold': 10000,

	'project_root': os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../')),

	'colours': {
		'background': 'black'
	},
	'escapes': {
		'line_up':     '\x1b[A',
		'line_delete': '\x1b[K'
	},
	'units': {
		'bytes_per_gibibyte': 2 ** 30
	},
	'paths': {
		'tasks':         '/root/tasks',
		'archives':      '/root/archives',
		'current_link':  current_link,
		'solution':      os.path.join(current_link, 'output/json/solutions.jsonl'),
		'pixels':        os.path.join(current_link, 'output/json/pixels.jsonl'),
		'task_folder':   '/root/tasks/{{start_time}}'
	},
	'colour_functions': { }
}

constants['required_folders'] = [
	constants['paths']['task_folder'],
	constants['paths']['task_folder'] + '/logs',
	constants['paths']['task_folder'] + '/output/json',
	constants['paths']['task_folder'] + '/output/images',
	'/root/archives'
]
