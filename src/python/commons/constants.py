

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






def is_polynomial (coefficents):
	return True

def is_palindromic_polynomial (coefficents):

	for elem0, elem1 in zip(coefficents, reversed(coefficents)):
		if elem0 != elem1:
			return False

	return True

def is_monic_polynomial (coefficents):
	return coefficents[0] == 1

def is_littlewood_polynomial (coefficents):

	for coefficent in coefficents:
		if coefficent != 1 and coefficent != -1:
			return False
	return True







constants['polynomial_predicates'] = {
	'any':        is_polynomial,
	'palindrome': is_palindromic_polynomial,
	'monic':      is_monic_polynomial,
	'littlewood': is_littlewood_polynomial
}
