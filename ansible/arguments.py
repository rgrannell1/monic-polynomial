#!/usr/bin/env python3





import json





# +- 1.5

arguments = {
	'solve_polynomial': {
		'order':  5,
		'range':  35
	},
	'render_pixels': {
		'ranges': {
			'x': [-1, +1],
			'y': [-0.5, -1.5]

		},
		'width':  15 * 1000
	}
}






print(json.dumps(arguments))
