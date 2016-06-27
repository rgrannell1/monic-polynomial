
import os






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
	'colour_functions': { },
	'polynomial_predicates': { }
}






def any_predicate (coefficents):
	return true

def palindrome_predicate (coefficents):

	for elem0, elem1 in zip(coefficents, reversed(coefficents)):
		if elem0 != elem1:
			return False

	return True






constants['polynomial_predicates'] = {
	'any':        any_predicate,
	'palindrome': palindrome_predicate
}
