#!/usr/bin/env python3

import os
import sys
import time
import json
import cmath
import numpy
import itertools
from functools import reduce
from operator  import mul
from prompter import yesno





exec(open(os.path.join(os.path.dirname(__file__), 'repo/src/python/commons/constants.py')).read( ))
exec(open(os.path.join(os.path.dirname(__file__), 'repo/src/python/commons/utils.py')).read( ))












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

def erase_lines (count):

	for _ in range(count):
		sys.stderr.write(constants['escapes']['line_up'])
		sys.stderr.write(constants['escapes']['line_delete'])

def print_progress (iter, total_count, start):

	if iter % constants["print_frequency"] == 0:

		end        = time.time( )
		elapsed    = end - start
		per_second = round(iter / elapsed)

		estimated_per_hour = per_second * 60 * 60
		minutes_remaining   = round((total_count - iter) / 60 * per_second)
		messages            = [
			'rates:',
			'    solved:                    ' + '{:,}'.format(iter),
			'    solved / second:           ' + '{:,}'.format(per_second),
			'',
			'estimates:',
			'    minutes remaining:         ' + '{:,}'.format(minutes_remaining),
			'    estimated per hour:        ' + '{:,}'.format(estimated_per_hour)
		]

		if iter >= 2 * constants["print_frequency"]:
			erase_lines(len(messages))

		for message in messages:
			sys.stderr.write(message + '\n')

def write_solutions (solution, solution_buffer, out_path, force = False):

	if len(solution_buffer) == constants["flush_threshold"] or force:

		with open(out_path, "a") as fconn:
			for old_solution in solution_buffer:
				fconn.write(json.dumps(old_solution) + '\n')

		del solution_buffer[:]

	solution_buffer.append(solution)

def solve_polynomial (point):

	return {
		'coefficients': point,
		'roots':        [ [root.real, root.imag] for root in numpy.roots(point) ]
	}

def solve_polynomials (order, num_range, assume_yes, out_path):
	"""
	"""

	dimensions  = repeat_val(order, sequence(-num_range, num_range))
	space       = itertools.product(*dimensions)

	total_count = product(len(val) for val in dimensions)

	if not assume_yes:
		prompt_start(order, num_range, total_count)

	start       = time.time( )
	root_count  = counter( )
	solution_buffer = [ ]

	for point in space:

		solution = solve_polynomial(point)

		print_progress(next(root_count), total_count, start)
		write_solutions(solution, solution_buffer, out_path)

	write_solutions(solution, solution_buffer, out_path, force = True)
