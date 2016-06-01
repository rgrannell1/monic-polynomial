#!/usr/bin/env python3





import json





arguments = [

	{
		'solve_polynomial': {
			'order':      5,
			'range':      20
		},
		'render_pixels': {
			'xrange': 1,
			'yrange': 1,
			'width':  10000
		},
		'draw_solutions': {
			'xrange': 1,
			'yrange': 1,
			'height': 3000,
			'width':  10000
		}
	}

]






print(json.dumps(arguments))
