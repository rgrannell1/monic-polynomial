#!/usr/bin/env python3





import json





arguments = [

	{
		'solve_polynomial': {
			'order':  5,
			'range':  10
		},
		'render_pixels': {
			'ranges': {
				'x': [-1, +1],
				'y': [-1, -2]
			},
			'width':  10 * 1000
		},
		'draw_solutions': { }
	}

]






print(json.dumps(arguments))
