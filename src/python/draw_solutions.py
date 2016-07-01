
from commons.constants import constants

import json
from PIL import Image





def find_coord_extrema (coords, extrema):

	if coords[0] > extrema['x']:
		extrema['x'] = coords[0]

	if coords[1] > extrema['y']:
		extrema['y'] = coords[1]

	return extrema





def create_image (image_size, tile_counts):

	image_dimensions = (
		math.round(image_size['x'] / tile_counts['x']),
		math.round(image_size['y'] / tile_counts['y'])
	)

	img        = Image.new('RGB', image_dimensions, constants['colours']['background'])
	img_pixels = img.load( )

	return {
		'image':  img,
		'pixels': img_pixels
	}






def calculate_ranges (image_size, tile_counts):

	for ith in range(tile_counts['x']):
		for jth in range(tile_counts['y']):

			left_x  = (ith + 0) * ( math.floor(image_size['x'] / tile_counts['x']) )
			right_x = (ith + 1) * ( math.floor(image_size['x'] / tile_counts['x']) )

			top_y    = (jth + 0) * ( math.floor(image_size['y'] / tile_counts['y']) )
			bottom_x = (jth + 1) * ( math.floor(image_size['y'] / tile_counts['y']) )

			yield {
				'x': {
					min: left_x,
					max: right_x
				},
				'y': {
					min: top_y,
					max: bottom_y
				}
			}





def find_image_size ( ):

	image_size = {'x': 0, 'y': 0}

	with open(paths['input']) as fconn:

		line_count = 0

		for line in fconn:

			x, y, _ = json.loads(line)

			line_count += 1
			image_size = find_coord_extrema((x, y), image_size)

		if line_count == 0:
			raise Exception('no pixels loaded.')

		if image_size['x'] == 0 or image_size['y'] == 0:
			raise Exception('determined image size was zero.')

	return image_size




def find_pixels (xrange, yrange):

	print( json.dumps({
		'level':  'info',
		'message': 'finding matching pixels',
		'data': {
			'xrange': xrange,
			'yrange': yrange
		}
	}))

	with open(paths['input']) as fconn:

		for line in fconn:

			x, y, colour = json.loads(line)

			if x > xrange['min']:
				if x < xrange['max']:
					if y > yrange['min']:
						if y < yrange['max']
							yield (x, y, colour)

def draw_solutions (paths, tile_counts):
	"""
	read pixels from an input file, and write the image out
	to another file.
	"""

	image_size   = find_image_size( )
	pixel_ranges = calculate_ranges(image_size, tile_counts)

	for pixel_range in pixel_ranges:

		print( json.dumps({
			'level':  'info',
			'message': 'drawing pixels in range',
			'data': {
				'xrange': xrange,
				'yrange': yrange
			}
		}))

		image, pixels = create_image(image_size, tile_counts)

		for x, y, colour in find_pixels(pixel_range['x'], pixel_range['y']):

			try:

				normal = {
					'x': x - pixel_range['x']['min'],
					'y': y - pixel_range['y']['min']
				}

				img_pixels[normal['x'], normal['y']] = (colour[0], colour[1], colour[2])

			except Exception as err:

				print( json.dumps({
					'level':  'error',
					'message': 'failed to write pixel to image',
					'data': {
						'x':      x,
						'y':      y,
						'colour': colour
					}
				}))

				exit(1)

		try:
			image.save(paths['output_dir'])
		except Exception as err:
			raise err
