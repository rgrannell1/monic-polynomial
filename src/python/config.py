
from typing import List

def zoom(pair: List[float], factor: int) -> List[float]:
  """
  zoom a base set of coordinates in.
  """
  x0, x1 = pair
  x0_prime = x0 * (1 / factor)
  x1_prime = x1 * (1 / factor)

  if not x0_prime < x1_prime:
    raise Exception(
    	"invalid coordinate bounds: x0_prime:({}) -> x1_prime:({})".format(x0_prime, x1_prime))

  return [x0_prime, x1_prime]

ranges = [
  {
    'x': zoom([-0.3, +0.3], 1),
    'y': zoom([-1.3, -0.7], 1),
    'colour_mode': 'hue',
    'metric_mode': 'product'
  },
  {
    'x': zoom([-0.3, +0.3], 2),
    'y': zoom([-1.3, -0.7], 2),
    'colour_mode': 'hue',
    'metric_mode': 'min'
  }
]

def config() -> dict:
  """
  load configuration for the graph to be drawn.
  """
  return {
    'solve_polynomial': {
      'order': 5,
      'range': 10
    },
    'render_pixels': {
      'ranges': ranges[0],
      'width': 5_000
    }
  }
