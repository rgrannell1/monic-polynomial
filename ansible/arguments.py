#!/usr/bin/env python3





import json





# +- 1.5

arguments = {
	'solve_polynomial': {
		'order': 5,
		'range': 30
	},
	'render_pixels': {
		'ranges': {
			'x': [-0.3, +0.3],
			'y': [-0.7, -1.3]
		},
		'width':  20 * 1000
	}
}






print(json.dumps(arguments))
