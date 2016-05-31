#!/usr/bin/env python3





import json





arguments = [

	{
		'solve_polynomial': {
			'order':      5,
			'range':      10
		},
		'render_pixels': {
			'xrange': 2,
			'yrange': 2,
			'width':  10000
		},
		'draw_solutions': {
			'xrange': 2,
			'yrange': 2,
			'height': 3000,
			'width':  10000
		}
	}

]






print(json.dumps(arguments))
