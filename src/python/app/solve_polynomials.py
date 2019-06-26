
from commons import utils
from commons.constants import constants

import sys
import json
import time
import numpy
import logging
import itertools
import sqlite3

def display_progress (iteration, total_count, start):
	"""
	estimate the current solution rate.
	"""

	if iteration % constants["print_frequency"] == 0:
		end = time.time( )
		elapsed = end - start

		per_second = round(iteration / elapsed)
		seconds_remaining = round((total_count - iteration) / per_second)
		minutes_remaining = round(seconds_remaining / 60)

		logging.info('iteration {:,}, {:,} remaining'.format(iteration, total_count - iteration))
		logging.info('{:,}m / {:,}s remaining'.format(minutes_remaining, seconds_remaining))

def insert_solutions (curse, solutions):
	curse.executemany(
		"INSERT OR REPLACE INTO polynomials (id, polynomial) VALUES (?, ?)", solutions)

	conn.commit()
	solutions = []

def solve_polynomials (order, num_range, predicate, out_path):
	"""

	"""

	dimensions = utils.repeat_val(order, utils.sequence(-num_range, num_range))
	space = itertools.product(*dimensions)

	total_count = utils.product(len(val) for val in dimensions)

	start = time.time( )
	root_count = 0

	conn = sqlite3.connect('./db.sqlite')
	curse = conn.cursor()

	curse.execute("CREATE TABLE IF NOT EXISTS polynomials (id text primary key, polynomial BLOB);")
	conn.commit()

	solutions = []

	for point in space:
			root_count += 1

			id = ','.join(map(str, point))

			data = json.dumps({
				'roots': [[root.real, root.imag] for root in numpy.roots(point)]
			})

			solutions.append(tuple([id, data]))

			if len(solutions) > constants['batch_size']:
				insert_solutions(curse, solutions)

			display_progress(root_count, total_count, start)

	insert_solutions(curse, solutions)
	conn.close()
