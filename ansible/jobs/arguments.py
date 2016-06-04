#!/usr/bin/env python3





import json





arguments = [

	{
		'solve_polynomial': {
			'order':  5,
			'range':  20
		},
		'render_pixels': {
			'ranges': {
				'x': [-2, +2],
				'y': [-2, +2]
			},
			'width':  10
		},
		'draw_solutions': { }
	}

]






print(json.dumps(arguments))
