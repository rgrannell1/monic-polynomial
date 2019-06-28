
import math
import json
import logging
from commons import utils

def is_in_range (value, num_range):
	return value >= min(num_range) and value <= max(num_range)

def extrema_interval (extrema):
	return abs(extrema['max'] - extrema['min'])

def display_extrema_progress (iteration):
	if iteration % 100000 == 0:
		logging.info('finding coordinate extrema {}'.format(iteration))

def display_pixel_progress (iteration):
	if iteration % 100000 == 0:
		logging.info('writing pixel data {}'.format(iteration))

def find_solution_extrema (fconn, coefficient_metric, ranges):
	"""

	"""

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

	for line in fconn:
		solution = json.loads(line)

		solution_count += 1

		display_extrema_progress(solution_count)

		for x, y in solution['roots']:
			if is_in_range(x, ranges['x']) and is_in_range(y, ranges['y']):

				measure = coefficient_metric(solution['coefficients'])

				extrema['x']['max'] = max(x, extrema['x']['max'])
				extrema['x']['min'] = min(x, extrema['x']['min'])

				extrema['y']['max'] = max(y, extrema['y']['max'])
				extrema['y']['min'] = min(y, extrema['y']['min'])

				extrema['coefficient_metric']['max'] = max(measure, extrema['coefficient_metric']['max'])
				extrema['coefficient_metric']['min'] = min(measure, extrema['coefficient_metric']['min'])

	if extrema['x']['max'] == extrema['x']['min'] or extrema['y']['max'] == extrema['y']['min']:
		raise Exception( 'pixel min value was equal to pixel max value: ' + str(extrema) )

	return extrema

def convert_root_to_pixel (coefficients, point, extrema, width, coefficient_metric, colour_fn):
	"""

	"""

	coefficient_measure = coefficient_metric(coefficients)

	normalised = [
		point[0]            - extrema['x']['min'],
		point[1]            - extrema['y']['min'],
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
			sys.stdout.write( json.dumps({
				'level':  'error',
				'message': 'invalid percentage value',
				'data': {
					'percentage': percentage
				}
			}) + '\n')

	height = (y_diff / x_diff) * width

	return [
		math.floor(percentage[0] * width),
		math.floor(percentage[1] * height),
		colour_fn(coefficient_measure, extrema['coefficient_metric']['max'])
	]

def metric (coefficients):
	return utils.product(coefficients)

def render_pixels (width, ranges, paths, colour_fn):
	"""
	input solutions from a jsonl file, and write to an output file.
	"""

	with open(paths['input']) as fconn:
		extrema = find_solution_extrema(fconn, metric, ranges)

	with open(paths['input']) as fconn:
		with open(paths['output'], 'a') as out_fconn:
			count         = 0
			written_count = 0

			for line in fconn:
				solution = json.loads(line)

				display_pixel_progress(count)

				count += 1

				for x, y in solution['roots']:
					if is_in_range(x, ranges['x']) and is_in_range(y, ranges['y']):
						written_count += 1

						pixel = convert_root_to_pixel(solution['coefficients'], (x, y), extrema, width, metric, colour_fn)
						out_fconn.write(json.dumps(pixel) + '\n')

			if written_count == 0:
				raise Exception('no pixels written to file.')
