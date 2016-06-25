
import math





def tint (size, max):
	"""

	"""

	tint_colours = [
		[0,   3,   255],
		[20,  22,  255],
		[40,  41,  255],
		[59,  61,  255],
		[79,  80,  255],
		[98,  100, 255],
		[118, 119, 255],
		[138, 139, 255],
		[157, 158, 255],
		[177, 178, 255],
		[197, 197, 255],
		[216, 216, 255],
		[236, 236, 255]
	]

	index = math.floor((size / maximum) * len(tint_colours))

	return tint_colours[min(len(tint_colours) - 1, index)]

def hue (size, maximum):
	"""
	get the ith sequence in [0, 0, 0] ... [255, 255, 255]
	"""

	index = math.floor((size / maximum) * 255 ** 3)

	blue  = (index) & 255
	green = (index >> 8) & 255
	red   = (index >> 16) & 255

	return [red, green, blue]
