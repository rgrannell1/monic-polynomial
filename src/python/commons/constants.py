#!/usr/bin/env python3





constants = {
	'print_frequency': 10000,
	'flush_threshold': 100000,

	'project_root': os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')),

	'colours': {
		'background': 'black'
	},
	'print_frequency': 10000,

	'flush_threshold': 10000,

	'escapes': {
		'line_up':     '\x1b[A',
		'line_delete': '\x1b[K'
	},
	'units': {
		'bytes_per_gibibyte': 2 ** 30
	},
	'point_range': 255 ** 3
}
