
def config():
  return {
      'solve_polynomial': {
        'order': 5,
        'range': 15
        #'range': 20
      },
      'render_pixels': {
        'ranges': {
#          'x': [-0.3, +0.3],
#          'y': [-0.7, -1.3],

          'x': [-6, 6],
          'y': [-6, 6],
          'colour_mode': 'hue'
        },
        'width': 1 * 1000
      }
  }
