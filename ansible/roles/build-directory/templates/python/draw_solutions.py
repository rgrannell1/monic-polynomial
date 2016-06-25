
from commons.constants import constants

import json
from PIL import Image





def find_image_size (coords, image_size):

	if coords[0] > image_size['x']:
		image_size['x'] = coords[0]

	if coords[1] > image_size['y']:
		image_size['y'] = coords[1]

	return image_size





def create_image ( ):

	image_dimensions = (image_size['x'], image_size['y'])

	img        = Image.new('RGB', image_dimensions, constants['colours']['background'])
	img_pixels = img.load( )

	return {
		'img':    img,
		'pixels': img_pixels
	}





def draw_solutions (paths):
	"""
	read pixels from an input file, and write the image out
	to another file.
	"""

	image_size = {'x': 0, 'y': 0}

	with open(paths['input']) as fconn:

		line_count = 0

		for line in fconn:

			x, y, _ = json.loads(line)

			line_count += 1
			image_size = find_image_size((x, y), image_size)

		if line_count == 0:
			raise Exception('no pixels loaded.')

		if image_size['x'] == 0 or image_size['y'] == 0:
			raise Exception('determined image size was zero.')

	with open(paths['input']) as fconn:

		image_dimensions = (image_size['x'], image_size['y'])

		img        = Image.new('RGB', image_dimensions, constants['colours']['background'])
		img_pixels = img.load( )

	with open(paths['input']) as fconn:

		for line in fconn:

			x, y, colour = json.loads(line)

			x_in_range = x > 0 and x < image_size['x']
			y_in_range = x > 0 and y < image_size['y']

			try:

				if x_in_range and y_in_range:

					img_pixels[x, y] = (colour[0], colour[1], colour[2])

			except Exception as err:

				sys.stderr.write( json.dumps({
					'level':  'error',
					'message': 'failed to write pixel to image',
					'data': {
						'x':      x,
						'y':      y,
						'colour': colour
					}
				}) + '\n')

				exit(1)

		try:
			img.save(paths['output'])
		except Exception as err:
			raise err
