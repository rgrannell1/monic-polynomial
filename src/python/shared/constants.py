
import os

constants = {
	'print_frequency': 10_000,
	'flush_threshold': 10_000,
	'tile_size': 5_000,
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
	'batch_size': 200_000,
	'paths': {
		'db': './db.sqlite'
	}
}
