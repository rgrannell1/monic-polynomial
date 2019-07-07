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
