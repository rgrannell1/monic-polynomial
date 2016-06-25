#!/usr/bin/env python3

import os
import functools
import operator





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
	repeat a value several ktimes.
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
