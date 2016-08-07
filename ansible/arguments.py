#!/usr/bin/env python3





import json





# +- 1.5

arguments = {
	'solve_polynomial': {
		'order': 5,
		'range': 15
	},
	'render_pixels': {
		'ranges': {

			'x': [-0.3, +0.3],
			'y': [-0.7, -1.3],

#			'x': [-3, +3],
#			'y': [-3, +3],

			'colour_mode': 'hue'

		},
		'width': 25 * 1000
	}
}





print(json.dumps(arguments))
