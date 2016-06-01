#!/usr/bin/env python3





import json





arguments = [

	{
		'solve_polynomial': {
			'order':  5,
			'range':  20
		},
		'render_pixels': {
			'xrange': 5,
			'yrange': 5,
			'width':  50000
		},
		'draw_solutions': {
			'xrange': 5,
			'yrange': 5,
			'height': 3000,
			'width':  10000
		}
	},

	{
		'draw_solutions': {
			'xrange': 3,
			'yrange': 3,
			'height': 3000,
			'width':  10000
		}
	},

	{
		'draw_solutions': {
			'xrange': 1,
			'yrange': 1,
			'height': 3000,
			'width':  10000
		}
	}

]






print(json.dumps(arguments))
