#!/usr/bin/env python3

import os
import functools
import operator
from typing import List

def sequence (lower:int, upper:int) -> List[int]:
	"""
	generate an integer sequence between two numbers.
	"""

	seq = [ ]
	current = lower

	while current <= upper:
		seq.append(current)
		current += 1

	return seq

def repeat_val (num:int, val):
	"""
	repeat a value several k times.
	"""
	return [val for _ in range(num - 1)]

def product (nums):
	"""
	get the product of numbers in an array.
	"""
	return functools.reduce(operator.mul, nums, 1)


def flatten(lists):
	"""
	flatten a list of lists
	"""
	result = []

	for sublist in lists:
		result += sublist

	return result
