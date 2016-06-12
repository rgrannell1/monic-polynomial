#!/usr/bin/env python3





import json





arguments = [

	{
		'solve_polynomial': {
			'order':  5,
			'range':  15
		},
		'render_pixels': {
			'ranges': {
				'x': [-1, +1],
				'y': [+2, +3]
			},
			'width':  2 * 1000
		},
		'draw_solutions': { }
	}

]






print(json.dumps(arguments))
