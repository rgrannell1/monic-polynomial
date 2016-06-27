
from commons import utils
from commons.constants import constants

import sys
import json
import time
import numpy
import itertools





def display_progress (iteration, total_count, start):
	"""
	estimate the current solution rate.
	"""

	if iteration % constants["print_frequency"] == 0:

		end        = time.time( )
		elapsed    = end - start

		per_second         = round(iteration / elapsed)
		seconds_remaining  = round((total_count - iteration) / per_second)
		minutes_remaining  = round(seconds_remaining / 60)

		sys.stdout.write(json.dumps({
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





def solve_polynomials (order, num_range, predicate, out_path):
	"""

	"""

	dimensions  = utils.repeat_val(order, utils.sequence(-num_range, num_range))
	space       = itertools.product(*dimensions)

	total_count = utils.product(len(val) for val in dimensions)

	start           = time.time( )
	root_count      = 0

	with open(out_path, "a") as fconn:
		for point in space:

			root_count += 1

			if predicate(point):

				solution =	{
					'coefficients': point,
					'roots':        [ [root.real, root.imag] for root in numpy.roots(point) ]
				}


				fconn.write(json.dumps(solution) + '\n')

				display_progress(root_count, total_count, start)
