
def config() -> dict:
  return {
      'solve_polynomial': {
        'order': 5,
        #'range': 35
        'range': 9
      },
      'render_pixels': {
        'ranges': {
          'x': [-0.3, +0.3],
          'y': [-0.7, -1.3],
          'colour_mode': 'hue'
        },
        'width': 6 * 1000
      }
  }
