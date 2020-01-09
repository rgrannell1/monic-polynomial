
import math
import json
import sqlite3
import logging
import io
from shared import utils

def is_in_range (value:int, num_range) -> bool:
	return value >= min(num_range) and value <= max(num_range)

def extrema_interval (extrema:dict) -> int:
	return abs(extrema['max'] - extrema['min'])

def display_extrema_progress (iteration:int) -> None:
	if iteration % 100000 == 0:
		logging.info('🔎 finding coordinate extrema {:,}'.format(iteration))

def display_pixel_progress (iteration:int) -> None:
	if iteration % 100000 == 0:
		logging.info('⌗ writing pixel data {:,}'.format(iteration))

def polynomials():
	conn = sqlite3.connect('./db.sqlite')
	curse = conn.cursor()

	curse.execute('SELECT * from polynomials')

	polynomials_loaded = False
	for row in curse:
		polynomials_loaded = True
		yield row

	if not polynomials_loaded:
		logging.error("no polynomials loaded from database.")
		exit(1)
	else:
		logging.info("loaded polynomials from database.")

def parse_solutions(row) -> dict:
	[id, *solutions] = row

	data = {
		'id': id,
		'solutions': []
	}

	for ith in range(0, len(solutions) - 1, 2):
		data['solutions'].append({
			'real': float(solutions[ith]),
			'imag': float(solutions[ith + 1])
		})

	return data

def find_solution_extrema (coefficient_metric, ranges:dict) -> dict:
	extrema = {
		'x': {
			'min': +float('inf'),
			'max': -float('inf')
		},
		'y': {
			'min': +float('inf'),
			'max': -float('inf')
		},
		'coefficient_metric': {
			'min': +float('inf'),
			'max': -float('inf')
		}
	}

	solution_count = 0

	for polynomial in polynomials():
		data = parse_solutions(polynomial)

		for solution in data['solutions']:
			x = solution['real']
			y = solution['imag']

			solution_count += 1
			display_extrema_progress(solution_count)

			if is_in_range(x, ranges['x']) and is_in_range(y, ranges['y']):
				coefficients = [float(coeff) for coeff in data['id'].split(',')]
				measure = coefficient_metric(coefficients)

				extrema['x']['max'] = max(x, extrema['x']['max'])
				extrema['x']['min'] = min(x, extrema['x']['min'])

				extrema['y']['max'] = max(y, extrema['y']['max'])
				extrema['y']['min'] = min(y, extrema['y']['min'])

				extrema['coefficient_metric']['max'] = max(
					measure, extrema['coefficient_metric']['max'])
				extrema['coefficient_metric']['min'] = min(
					measure, extrema['coefficient_metric']['min'])

	for axis in ["x", "y"]:
		minimum = extrema[axis]["min"]
		maximum = extrema[axis]["max"]

		if minimum == maximum:
			logging.error(
				f"after inspecting {solution_count:,} solutions, {axis} axis min {minimum} was equal to {maximum}")

			exit(1)

	return extrema

def convert_root_to_pixel (coefficients, point, extrema, width, coefficient_metric, colour_fn):
	"""

	"""

	coefficient_measure = coefficient_metric(coefficients)

	normalised = [
		point[0] - extrema['x']['min'],
		point[1] - extrema['y']['min'],
		coefficient_measure - extrema['coefficient_metric']['min']
	]

	x_diff = extrema_interval(extrema['x'])
	y_diff = extrema_interval(extrema['y'])

	if x_diff == 0 or y_diff == 0:
		raise Exception('invalid extrema intervals for extrema ' + str(extrema) + ' :' + str([x_diff, y_diff]))

	percentage = [
		normalised[0] / x_diff,
		normalised[1] / y_diff
	]

	for percent in percentage:
		if percent < 0 or percent > 1:
			logging.info('invalid percentage value {}'.format(percentage))

	height = (y_diff / x_diff) * width

	return [
		math.floor(percentage[0] * width),
		math.floor(percentage[1] * height),
		colour_fn(coefficient_measure, extrema['coefficient_metric']['max'])
	]

def product_metric (coefficients):
	"""
	a product_metric used to colour the graph
	"""
	return utils.product(coefficients)

def render_pixels (width, ranges, paths, colour_fn):
	"""
	input solutions from a jsonl file, and write to an output file.
	"""

	extrema = find_solution_extrema(product_metric, ranges)

	with open(paths['output'], 'a') as out_fconn:
		count = 0
		written_count = 0
		polynomials_found = False

		for polynomial in polynomials():
			polynomials_found = True
			data = parse_solutions(polynomial)

			for solution in data['solutions']:
				x = solution['real']
				y = solution['imag']

				display_pixel_progress(count)

				count += 1

				if is_in_range(x, ranges['x']) and is_in_range(y, ranges['y']):
					written_count += 1

					coefficients = [float(coeff) for coeff in data['id'].split(',')]

					pixel = convert_root_to_pixel(coefficients, (x, y), extrema, width, product_metric, colour_fn)
					out_fconn.write(json.dumps(pixel) + '\n')

		if written_count == 0:
			if polynomials_found:
				logging.error("polynomials were loaded but none were in range & written; too few polynomials were searched or the range was restrictive.")
				exit(1)
			else:
				logging.error("no pixels written to file and no polynomials loaded; was the database empty?")
				exit(1)
		else:
			written_fraction = round(100 * (written_count / count), 2)
			logging.info("wrote {} pixels to file {} ({}%)".format(written_count, paths['output'], written_fraction))
