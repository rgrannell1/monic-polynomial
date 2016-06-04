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
				'x': [-3, +3],
				'y': [-3, +3]
			},
			'width':  10000
		},
		'draw_solutions': { }
	}

]






print(json.dumps(arguments))
