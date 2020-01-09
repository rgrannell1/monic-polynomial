
ranges = [
  {
    'x': [-0.3, +0.3],
    'y': [-0.7, -1.3],
    'colour_mode': 'hue'
  },
  {
    'x': [-0.15, +0.15],
    'y': [-0.35, -0.65],
    'colour_mode': 'hue'
  },
  {
      'x': [-0.075, +0.075],
      'y': [-0.175, -0.325],
      'colour_mode': 'hue'
  }
]

def config() -> dict:
  """
  load configuration for the graph to be drawn.
  """
  return {
    'solve_polynomial': {
      'order': 5,
      'range': 22
    },
    'render_pixels': {
      'ranges': ranges[2],
      'width': 5_000
    }
  }
