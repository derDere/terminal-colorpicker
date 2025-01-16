""" Constants for the color picker.

They define the default color mode, color-names and layout settings.
"""

COLOR_MAX = 256 # 256 colors in total fits in a byte

BASIC_DIM_COLOR_COUNT = 8 # 8 basic colors
BASIC_BRIGHT_COLOR_COUNT = 8 # 8 bright basic colors
BASIC_COLOR_COUNT = BASIC_DIM_COLOR_COUNT + BASIC_BRIGHT_COLOR_COUNT # 16 basic colors in total
BASIC_COLOR_NAMES = [
  "Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "Ash (Dim White)",
  "Gray (Bright Black)", "Bright Red", "Bright Green", "Bright Yellow", "Bright Blue", "Bright Magenta", "Bright Cyan", "White (Bright Ash)"
]

RGB_COLOR_START = BASIC_COLOR_COUNT # after the basic colors the rgb colors start
RGB_COLOR_COUNT = 6 # 6 values for each color channel
RGB_MIN_VALUE = 0 # 0 is the minimum value for a color channel
RGB_MAX_VALUE = RGB_COLOR_COUNT - 1 # 5 is the maximum value for a color channel
RGB_SKIP_WHITE = True # skip the white color in the rgb colors because it is already in the basic colors
RGB_SKIP_BLACK = True # skip the black color in the rgb colors because it is already in the basic colors

GRAY_COLOR_START = RGB_COLOR_START + RGB_COLOR_COUNT ** 3 # after the rgb colors the gray colors start
GRAY_COLOR_COUNT = COLOR_MAX - GRAY_COLOR_START # 24 gray colors

ROW_COUNT = 1 + (RGB_MAX_VALUE * 2) + 1 # 1 row of basic colors, 2*RGB_MAX_VALUE rows of rgb colors dark to light, 1 row of gray colors
ROW_BASIC_INDEX = -1 # the Row containing the basic colors
ROW_GRAY_INDEX = ROW_COUNT - 1 - (1 if RGB_SKIP_BLACK else 0) - (1 if RGB_SKIP_WHITE else 0) # the Row containing the gray colors

WHITE = BASIC_COLOR_COUNT - 1 # Last basic color is bright white
BLACK = RGB_MIN_VALUE # First rgb color is dim black

_TC_W = 7 # Text Color White
_TC_G = 46 # Text Color Green
_TC_O = 208 # Text Color Orange
_TC_Y = 220 # Text Color Yellow
_TC_R = 216 # Text Color Red
_TC_B = 75 # Text Color Blue
_TC_T = [1,2,3,4,5,6,7,9,10,11,12,13,14] # Title Colors
