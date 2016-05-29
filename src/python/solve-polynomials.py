
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
import json
import cmath
import numpy
import itertools
from functools import reduce
from operator  import mul
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

def prompt_start (order, num_range, total_count):

	message = 'attempting to solve ' + '{:,}'.format(total_count) + ' polynomials. Do you want to start?'
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
		elapsed    = end - start
		per_second = round(iter / elapsed)

		estimated_per_hour = per_second * 60 * 60
		second_remaining   = round((total_count - iter) / per_second)

		messages           = [
			'average solved per second: ' + str(per_second) + '\n',
			'total solved:              ' + str(iter) + '\n',
			'seconds remaining:         ' + str(second_remaining) + '\n',
			'estimated per hour:        ' + str(estimated_per_hour) + '\n'
		]

		if iter >= 2 * constants["print_frequency"]:
			eraseLines(len(messages))

		for message in messages:
			sys.stderr.write(message)

def write_solutions(solution, solution_buffer, force = False):

	if len(solution_buffer) == constants["flush_threshold"] or force:

		with open(constants['paths']['output'], "a") as fpath:
			fpath.write(json.dumps(solution) + '\n')

		del solution_buffer[:]

	solution_buffer.append(solution)

def solve_polynomial (point):

	return {
		'coefficients': point,
		'roots':        [ [root.real, root.imag] for root in numpy.roots(point) ]
	}

def repeat_val (num, val):
	return [val for _ in range(num - 1)]

def product (nums):
	return reduce(mul, nums, 1)

def sequence (lower, upper):

	seq = [ ]
	current = lower

	while current <= upper:
		seq.append(current)
		current += 1

	return seq

def solve_polynomials (order, num_range):


	dimensions  = repeat_val(order, sequence(-num_range, num_range))
	space       = itertools.product(*dimensions)

	total_count = product(len(val) for val in dimensions)

	prompt_start(order, num_range, total_count)

	start       = time.time( )
	root_count  = counter( )
	solution_buffer = [ ]

	for point in space:

		solution = solve_polynomial(point)

		print_progress(next(root_count), total_count, start)
		write_solutions(solution, solution_buffer)

	write_solutions(solution, solution_buffer, force = True)





if __name__ == '__main__':

    arguments = docopt(__doc__, version = '0.1')

    solve_polynomials(
    	order     = int(arguments['--order']),
    	num_range = int(arguments['--range']) )
