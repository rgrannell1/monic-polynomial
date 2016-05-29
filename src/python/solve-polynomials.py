
"""
solve.py

Usage:
	solve.py --order=<NUM> --range=<NUM>

Options:
	-h, --help       Display the documentation.
	--order=<NUM>    The order of the polynomial to solve [default: 5].
	--range=<NUM>    The maximum / minumum integer coefficient to use for each polynomial.

"""

import os
import sys
import cmath
import numpy
import itertools
import time

from docopt   import docopt
from prompter import yesno






constants = {
	'print_frequency': 10000,

	'flush_threshold': 100000,

	'paths': {
		'output': os.path.join(os.path.dirname(__file__), '../../output/polynomial-roots.csv'),
	},
	'escapes': {
		'line_up':     '\x1b[A',
		'line_delete': '\x1b[K'
	}
}





def counter ( ):
	ith = 0
	while True:
		ith = ith + 1
		yield ith

def prompt_start (order, num_range):

	count = ((num_range * 2) + 1) ** order

	message = 'attempting to solve ' + '{:,}'.format(count) + ' polynomials. Do you want to start?'
	answer  = yesno(message, default = 'no')

	if not answer:
		exit(0)

def eraseLines (count):

	for _ in range(count):
		sys.stderr.write(constants['escapes']['line_up'])
		sys.stderr.write(constants['escapes']['line_delete'])

def print_progress (iter, total_count, start):

	if iter % constants["print_frequency"] == 0:

		end        = time.time( )
		elapsed    = round(end - start)
		per_second = round(iter / elapsed)

		estimated_per_hour = per_second * 60 * 60
		second_remaining   = round((total_count - iter) / per_second)

		if iter >= 2 * constants["print_frequency"]:
			eraseLines(4)

		sys.stderr.write('average solved per second: ' + str(per_second) + '\n')
		sys.stderr.write('total solved: '              + str(iter) + '\n')
		sys.stderr.write('seconds remaining: '        + str(second_remaining) + '\n')
		sys.stderr.write('estimated per hour: '        + str(estimated_per_hour) + '\n')


def write_roots(roots, root_buffer):

	if len(root_buffer) == constants["flush_threshold"]:

		with open(constants['paths']['output'], "a") as fpath:

			for root in root_buffer:
				fpath.write(','.join([str(num) for num in root]) + '\n')

		del root_buffer[:]

	root_buffer += roots

def to_coefficients (point, roots):
	return [[root.real, root.imag] for root in roots]



def solve_polynomials (order, num_range):

	prompt_start(order, num_range)

	dimensions  = (range(-(num_range - 1), num_range) for _ in range(order))
	space       = itertools.product(*dimensions)

	start       = time.time( )
	root_count  = counter( )
	root_buffer = [ ]

	total_count = ((2 * num_range) + 1) ** order

	for roots in (to_coefficients(point, numpy.roots(point)) for point in space):

		print_progress(next(root_count), total_count, start)
		write_roots(roots, root_buffer)





if __name__ == '__main__':

    arguments = docopt(__doc__, version = '0.1')

    solve_polynomials(
    	order     = int(arguments['--order']),
    	num_range = int(arguments['--range']) )
