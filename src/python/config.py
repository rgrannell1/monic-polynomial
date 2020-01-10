
from typing import List

#x0 = -1.2
#x0 = -1.2

x0 = -5
x1 = +5
y0 = -6.2
y1 = +3.8

ranges = [
  {
    'x': [x0 / 1.0, x1 / 1.0],
    'y': [y0 / 1.0, y1 / 1.0],
    'colour_mode': 'hue',
    'metric_mode': 'product'
  },
  {
    'x': [x0 / 4.0, x1 / 4.0],
    'y': [y0 / 4.0, y1 / 4.0],
    'colour_mode': 'hue',
    'metric_mode': 'product'
  }
]

def config() -> dict:
  """
  load configuration for the graph to be drawn.
  """
  return {
    'solve_polynomial': {
      'order': 5,
      'range': 12
    },
    'render_pixels': {
      'ranges': ranges[1],
      'width': 5_000
    }
  }
