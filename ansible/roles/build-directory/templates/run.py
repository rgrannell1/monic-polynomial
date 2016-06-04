#!/usr/bin/env python3

import os
import sys
import json
import math
import time
import numpy
import functools
import subprocess
import itertools
import operator
import errno

from PIL import Image





task_folder   = '/root/tasks/{{start_time}}'
argument_path = os.path.join(task_folder, 'jobs', '{{argument_script}}')
here          = os.path.dirname(os.path.abspath(__file__))
current_link  = os.path.join(here, '/root/tasks/current')




constants = {
	'print_frequency': 10000,
	'flush_threshold': 10000,

	'project_root': os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')),

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
	'point_range': 255 * 255 * 255,

	'required_folders': [
		task_folder,
		task_folder + '/logs',
		task_folder + '/output/json',
		task_folder + '/output/images',
		'/root/archives'
	],
	'paths': {
		'archives':      '/root/archives',
		'current_link':  current_link,
		'solution':      os.path.join(current_link, 'output/json/solutions.jsonl'),
		'pixels':        os.path.join(current_link, 'output/json/pixels.jsonl')
	}
}





def create_symlink ( ):
	"""
	symlink a build to  current.
	"""

	if os.path.islink(constants['paths']['current_link']):
		os.remove(constants['paths']['current_link'])

	os.symlink(task_folder, constants['paths']['current_link'])

	for path in constants['required_folders']:
		mkdir_p(path)

def read_arguments ( ):

	argument_output = subprocess.check_output(['python3', argument_path])

	try:
		return json.loads(argument_output.decode("utf-8"))
	except Exception as err:
		print(err)

def create_images (argument_sets):
	"""

	"""

	count = 0

	for argument_set in argument_sets:

		if 'solve_polynomial' in argument_set:

			solve_polynomials(
				order      = argument_set['solve_polynomial']['order'],
				num_range  = argument_set['solve_polynomial']['range'],
				assume_yes = True,
				out_path   = constants['paths']['solution']
			)

		if 'render_pixels' in argument_set:

			render_pixels(
				paths = {
					'input':  constants['paths']['solution'],
					'output': constants['paths']['pixels']
				},
				ranges = {
					'x': argument_set['render_pixels']['ranges']['x'],
					'y': argument_set['render_pixels']['ranges']['y']
				},
				width = argument_set['render_pixels']['width'])

		if 'render_pixels' in argument_set:

			draw_solutions(
				paths = {
					'input':  constants['paths']['pixels'],
					'output': os.path.join(current_link, 'output/images/{{start_time}}-' + str(count) + '.png')
				}
			)

		count += 1





# ++ ++ ++ ++ ++ ++ ++
# utilities
# ++ ++ ++ ++ ++ ++ ++

def sequence (lower, upper):
	"""
	generate an integer sequence between two numbers.
	"""

	seq = [ ]
	current = lower

	while current <= upper:
		seq.append(current)
		current += 1

	return seq

def get_file_size (filename):
	"""
	get the bytes in a file.
	"""

	return os.stat(filename).st_size

def repeat_val (num, val):
	"""
	repeat a value several times.
	"""
	return [val for _ in range(num - 1)]

def product (nums):
	"""
	get the product of numbers in an array.
	"""
	return functools.reduce(operator.mul, nums, 1)

def erase_lines (count):
	"""
	erase a certain number of lines from stderr.
	"""

	for _ in range(count):
		sys.stderr.write(constants['escapes']['line_up'])
		sys.stderr.write(constants['escapes']['line_delete'])

def mkdir_p (path):
    try:

        os.makedirs(path)

    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise




# ++ ++ ++ ++ ++ ++ ++
# solve equations.
# ++ ++ ++ ++ ++ ++ ++

def prompt_start (order, total_count):
	"""
	prompt.
	"""

	message = 'attempting to solve ' + '{:,}'.format(total_count) + ' polynomials. Do you want to start?'
	answer  = yesno(message, default = 'no')

	if not answer:
		exit(0)

def print_solution_progress (iteration, total_count, start):
	"""
	estimate the current solution rate.
	"""

	if iteration % constants["print_frequency"] == 0:

		end        = time.time( )
		elapsed    = end - start

		per_second         = round(iteration / elapsed)
		seconds_remaining  = round((total_count - iteration) / per_second)
		minutes_remaining  = round(seconds_remaining / 60)

		sys.stderr.write(json.dumps({
			'level': 'info',
			'data': {
				'solved':     '{:,}'.format(iteration),
				'remaining:': '{:,}'.format(total_count - iteration),
				'time_remaining': {
					'seconds': '{:,}'.format(seconds_remaining),
					'minutes': '{:,}'.format(minutes_remaining)
				},
				'solution_rate': {
					'seconds': '{:,}'.format(per_second),
					'minutes': '{:,}'.format(per_second * 60),
					'hours':   '{:,}'.format(per_second * 60 * 60)
				}
			}
		}) + '\n')

def write_solutions (solution, solution_buffer, out_path, force = False):
	"""
	write the polynomial solutions to a file.
	"""

	if len(solution_buffer) == constants["flush_threshold"] or force:

		with open(out_path, "a") as fconn:
			for old_solution in solution_buffer:
				fconn.write(json.dumps(old_solution) + '\n')

		del solution_buffer[:]

	solution_buffer.append(solution)

def solve_polynomial (point):
	"""
	solve a polynomial.
	"""

	return {
		'coefficients': point,
		'roots':        [ [root.real, root.imag] for root in numpy.roots(point) ]
	}

def solve_polynomials (order, num_range, assume_yes, out_path):
	"""
	solve every polynomial in the space:

		[ -num_range, ..., +num_range ] ^ order

	"""

	dimensions  = repeat_val(order, sequence(-num_range, num_range))
	space       = itertools.product(*dimensions)

	total_count = product(len(val) for val in dimensions)

	if not assume_yes:
		prompt_start(order, num_range, total_count)

	start           = time.time( )
	root_count      = 0
	solution_buffer = [ ]

	for point in space:

		solution = solve_polynomial(point)

		root_count += 1

		print_solution_progress(root_count, total_count, start)
		write_solutions(solution, solution_buffer, out_path)

	write_solutions(solution, solution_buffer, out_path, force = True)






# ++ ++ ++ ++ ++ ++ ++
# render equations
# ++ ++ ++ ++ ++ ++ ++

def get_point_colour (index):
	"""
	get the ith sequence in [0, 0, 0] ... [255, 255, 255]
	"""

	blue  = (index) & 255
	green = (index >> 8) & 255
	red   = (index >> 16) & 255

	return [red, green, blue]

def convert_root_to_pixel (coefficients, point, extrema, width):
	"""

	"""

	coefficient_product = product(coefficients)

	x_offset                   = extrema['x']['min']
	y_offset                   = extrema['y']['min']
	coefficient_product_offset = extrema['coefficient_product']['min']

	normalised = [
		point[0]            - x_offset,
		point[1]            - y_offset,
		coefficient_product - coefficient_product_offset
	]

	percentage = [
		normalised[0] / (extrema['x']['max']                   - extrema['x']['min']),
		normalised[1] / (extrema['y']['max']                   - extrema['y']['min']),
		normalised[2] / (extrema['coefficient_product']['max'] - extrema['coefficient_product']['min'])
	]

	index = min(
		math.floor(percentage[2] * constants['point_range']),
		constants['point_range'] - 1)

	x_diff = extrema['x']['max'] - extrema['x']['min']
	y_diff = extrema['y']['max'] - extrema['y']['min']

	height = (y_diff / x_diff) * width

	for percent in percentage:

		if percent < 0 or percent > 1:

			sys.stderr.write( json.dumps({
				'level':  'error',
				'message': 'invalid percentage value',
				'data': {
					'percentage': percentage
				}
			}) + '\n')

	return [
		math.floor(percentage[0] * width),
		math.floor(percentage[1] * height),
		get_point_colour(index)
	]

def find_pixel_extrema (fconn, ranges):
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
		'coefficient_product': {
			'min': +float('inf'),
			'max': -float('inf')
		}
	}

	for line in fconn:

		solution = json.loads(line)

		for x, y in solution['roots']:

			x_in_range = x >= ranges['x'][0] and x <= ranges['x'][1]
			y_in_range = y >= ranges['y'][0] and y <= ranges['y'][1]

			if x_in_range and y_in_range:

				coefficient_product = product(solution['coefficients'])

				if x > extrema['x']['max']:
					extrema['x']['max'] = x

				if x < extrema['x']['min']:
					extrema['x']['min'] = x

				if y > extrema['y']['max']:
					extrema['y']['max'] = y

				if y < extrema['y']['min']:
					extrema['y']['min'] = y

				if coefficient_product > extrema['coefficient_product']['max']:
					extrema['coefficient_product']['max'] = coefficient_product

				if coefficient_product < extrema['coefficient_product']['min']:
					extrema['coefficient_product']['min'] = coefficient_product

	return extrema

def render_pixels (width, ranges, paths):
	"""
	input solutions from a jsonl file, and write to an output file.
	"""

	with open(paths['input']) as fconn:
		extrema = find_pixel_extrema(fconn, ranges)

	with open(paths['input']) as fconn:

		with open(paths['output'], 'a') as out_fconn:

			for line in fconn:

				data_buffer = [ ]
				solution    = json.loads(line)

				for x, y in solution['roots']:

					x_in_range = x >= ranges['x'][0] and x <= ranges['x'][1]
					y_in_range = y >= ranges['y'][0] and y <= ranges['y'][1]

					if x_in_range and y_in_range:

						pixel = convert_root_to_pixel(solution['coefficients'], (x, y), extrema, width)
						out_fconn.write(json.dumps(pixel) + '\n')






# ++ ++ ++ ++ ++ ++ ++
# draw equations
# ++ ++ ++ ++ ++ ++ ++

def draw_solutions (paths):
	"""
	read pixels from an input file, and write the image out
	to another file.
	"""

	image_size = {
		'x': 0,
		'y': 0
	}

	with open(paths['input']) as fconn:

		for line in fconn:

			x, y, colour = json.loads(line)

			if x > image_size['x']:
				image_size['x'] = x

			if y > image_size['y']:
				image_size['y'] = y

	with open(paths['input']) as fconn:

		image_dimensions = (image_size['x'], image_size['y'])

		img        = Image.new('RGB', image_dimensions, constants['colours']['background'])
		img_pixels = img.load( )

	with open(paths['input']) as fconn:

		for line in fconn:

			x, y, colour = json.loads(line)

			x_in_range = x > 0 and x < image_size['x']
			y_in_range = x > 0 and y < image_size['y']

			try:

				if x_in_range and y_in_range:

					img_pixels[x, y] = (colour[0], colour[1], colour[2])

			except Exception as err:

				sys.stderr.write( json.dumps({
					'level':  'error',
					'message': 'failed to write pixel to image',
					'data': {
						'x':      x,
						'y':      y,
						'colour': colour
					}
				}) + '\n')

				exit(1)

		img.save(paths['output'])






# ++ ++ ++ ++ ++ ++ ++
# draw equations
# ++ ++ ++ ++ ++ ++ ++

create_symlink( )
create_images(read_arguments( ))
