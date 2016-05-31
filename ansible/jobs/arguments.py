#!/usr/bin/env python3





import json





arguments = [

	{
		'solve_polynomial': {
			'order':      5,
			'range':      15
		},
		'render_pixels': {
			'xrange': 5,
			'yrange': 5,
			'height': 10000,
			'width':  10000
		},
		'draw_solutions': {
			'xrange': 5,
			'yrange': 5,
			'height': 10000,
			'width':  10000
		}
	}

]






print(json.dumps(arguments))
