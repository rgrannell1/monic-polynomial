#!/usr/bin/env python3





import json





arguments = [

	{
		'solve_polynomial': {
			'order':      5,
			'range':      15,
			'assume_yes': True
		},
		'render_pixels': {
			'height': 2000,
			'width':  2000
		},
		'draw_solutions': {
			'xrange': 2000,
			'yrange': 2000,
			'height': 2000,
			'width':  2000
		}
	}

]






print(json.dumps(arguments))
