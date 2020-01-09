
ranges = [
  {
    'x': [-0.3, +0.3],
    'y': [-0.7, -1.3],
    'colour_mode': 'hue'
  }
]

def config() -> dict:
  return {
    'solve_polynomial': {
      'order': 5,
      'range': 35
    },
    'render_pixels': {
      'ranges': ranges[0],
      'width': 5_000
    }
  }
