
from shared import utils
from shared.constants import constants

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

	# -- only print for a subset of iterations.
	if iteration % constants["print_frequency"] == 0:
		end = time.time( )
		elapsed = end - start

		per_second = round(iteration / elapsed)
		seconds_remaining = round((total_count - iteration) / per_second)
		minutes_remaining = round(seconds_remaining / 60)

		percentage_solved = round((iteration / total_count) * 100) / 100

		logging.info('solved {:,} equations ({}), {:,} remaining'.format(iteration, percentage_solved, total_count - iteration))
		logging.info('{:,}m / {:,}s remaining'.format(minutes_remaining, seconds_remaining))
		logging.info('solving {:,} per second 🔥'.format(per_second))

def create_table(order):
	"""
	create a table to store polynomial root information
	"""

	query = "CREATE TABLE IF NOT EXISTS polynomials (id text primary key, "
	params = ["root{} int, iroot{} int".format(root, root) for root in range(order)]

	return query + ', '.join(params) + ");"

def insert_row(order):
	"""
	insert polynomial root data into an SQL database
	"""

	params = ', '.join(["root{}, iroot{}".format(root, root) for root in range(order)])
	inserts = ', '.join(["?, ?" for root in range(order)])

	query = "INSERT OR REPLACE INTO polynomials (id, {}) VALUES (?, {})".format(params, inserts)
	return query

def show_spash (total_count, dimensions):
	"""
	show summary information when the program starts.
	"""

	splash_text = """
		🔥 Computing Solutions to {:,} Order-{} Polynomials 🔥
	""".format(total_count, len(dimensions) + 1)

	print(splash_text)

def solve_polynomials (order, num_range):
	"""
	solve a large number of polynomials and save the data to a database
	"""
	dimensions = utils.repeat_val(order, utils.sequence(-num_range, num_range))
	space = itertools.product(*dimensions)
	total_count = utils.product(len(val) for val in dimensions)

	show_spash(total_count, dimensions)

	start = time.time( )
	root_count = 0

	conn = sqlite3.connect('./db.sqlite')
	curse = conn.cursor()
	curse.execute('PRAGMA synchronous = OFF')

	curse.execute(create_table(len(dimensions) - 1))
	conn.commit()

	solutions = []

	for point in space:
		root_count += 1

		id = ','.join(map(str, point))
		roots = [[root.real, root.imag] for root in numpy.roots(point)]

		solution = [id] + utils.flatten(roots)
		solutions.append(solution)

		# -- write the solutions to a database occasionally
		if len(solutions) > constants['batch_size']:
			try:
				curse.executemany(insert_row(len(dimensions) - 1), solutions)
			except Exception as err:
				print(err)

			conn.commit()
			solutions = []

		display_progress(root_count, total_count, start)

	# -- flush the remaining records
	try:
		curse.executemany(insert_row(len(dimensions) - 1), solutions)
	except Exception as err:
		print(err)

	# -- close the DB connection.
	conn.commit()
	conn.close()
