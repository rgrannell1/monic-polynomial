#!/usr/bin/env python3





import json





# +- 1.5

arguments = {
	'solve_polynomial': {
		'order':  5,
		'range':  10,
		'predicate': 'palindrome'
	},
	'render_pixels': {
		'ranges': {
#			'x': [-1, +1],
#			'y': [-0.5, -1.5]

			'x': [-3, +3],
			'y': [-3, +3]

		},
		'width':  5 * 1000
	}
}






print(json.dumps(arguments))
