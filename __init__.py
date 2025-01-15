import unicurses as uc
from unicguard import UnicursesGuard


# Constants ##########################################################################################################################################
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


def calc_color_256(r:int, g:int, b:int):
  """C
  """
  color = int(RGB_COLOR_START + (RGB_COLOR_COUNT**2) * r + RGB_COLOR_COUNT * g + b)
  return color


# Calculations #######################################################################################################################################
def brightness_range(full_color_range:int=RGB_COLOR_COUNT, skip_black:bool=RGB_SKIP_BLACK, skip_white:bool=RGB_SKIP_WHITE):
  """Generates a range of brightness values for the color picker.
  The range will give a list of tuples with two float values each between 0.0 and 1.0.
  The first value being the dim-multiplier and the second value being the bright-multiplier.
  For the first {full_color_range} values the dim-multiplier will be increased by 1/{full_color_range-1} and the bright-multiplier will be 0.
  After that the next {full_color_range - 1} values will have the dim-multiplier at 1 and the bright-multiplier will be increased by 1/{full_color_range-1}.
  if skip_black is True, the first value will be skipped. This is default because black is already in the basic colors.
  if skip_white is True, the last value will be skipped. This is default because white is already in the basic colors.

  This range will allow the user to generate a color gradient from black to any color to white.

  For that the dim-multiplier will be used to darken the color by simply multiplying the color value with the dim-multiplier.
  RGB = (RGB * dim-multiplier)

  The bright-multiplier will be used to brighten the color by multiplying the delta to the colors maximum value with the bright-multiplier and adding it to the color value.
  RGB = RGB + ((RGB_MAX - RGB) * bright-multiplier)

  The resulting formula will be:
  RGB = (RGB * dim-multiplier) + ((RGB_MAX - RGB) * bright-multiplier)

  You can calculate each channel by using the brightness function!!!!!!!!!!

  Example:
  Here is an example bases on the 256-color range where each channel has 6 values (0-5) and the maximum value is 5.
  We will call the dim-multiplier = dm and the bright-multiplier = bm.

  RGB_MAX = 5
  R = 3, G = 2, B = 1
  dm = 1, bm = 0.5

  R = brightness(R, dm, bm) # Same as: (R * dm) + ((RGB_MAX - R) * bm)
  G = brightness(G, dm, bm) # Same as: (G * dm) + ((RGB_MAX - G) * bm)
  B = brightness(B, dm, bm) # Same as: (B * dm) + ((RGB_MAX - B) * bm)

  Color = (R, G, B)

  Args:
    full_color_range:int: The number of values for each color channel. Default is 6 for the 256-color range (8bit) used in terminals. Set this to 256 to use the full 24bit color range.

  Returns:
    A range of brightness values as tuples. (dim-multiplier:float, bright-multiplier:float)
  """
  m1, m2 = 0, 0
  max_value = full_color_range - 1
  start = 0
  if skip_black:
    start = 1
  for i in range(start, full_color_range): # if skip_black: skip the first one because black is already in the basic colors
    m1 = i / max_value
    yield m1, m2
  end = 0
  if skip_white:
    end = 1
  for i in range(1, full_color_range - end): # if skip_white: skip the last one because white is already in the basic colors
    m2 = i / max_value
    yield m1, m2


def color_range(max_value:int=RGB_MAX_VALUE, min_value:int=RGB_MIN_VALUE, yield_end:bool=True):
  """Generates a range of color values representing a gradient over all colors.
  The range will give a list of tuples with three values for REG, GREEN and BLUE.
  The gradient will start at Red and go through all colors to Red again. (Red -> Yellow -> Green -> Cyan -> Blue -> Magenta -> Red)
  The gradient will be generated by increasing the color value for the next channel by 1 and decreasing the color value for the previous channel by 1.
  This will result in a smooth gradient from one color to the next.
  This color range can be used cross with the brightness_range to generate a color gradient from black to any color to white displaying all colors in between in a field for a color picker.

  If the min value is 0 and the max value is 5 this steps would look like this:
  1. Red: (5, 0, 0)
  2. Increasing Green to Yellow
  3. Yellow: (5, 5, 0)
  4. Decreasing Red to Green
  5. Green: (0, 5, 0)
  6. Increasing Blue to Cyan
  7. Cyan: (0, 5, 5)
  8. Decreasing Green to Blue
  9. Blue: (0, 0, 5)
  10. Increasing Red to Magenta
  11. Magenta: (5, 0, 5)
  12. Decreasing Blue to Red
  13. Red: (5, 0, 0)

  If yield_end is True, the last color (which is the same as the first color) will be yielded as well to close the loop.

  This range is by default set to the 256-color range (8bit) where each channel has 6 values (0-5) and the maximum value is 5.
  You can pass a max_value of 255 to use the full 24bit color range. However, this will also increase the length of the range.

  Args:
    max_value:int: The maximum value for each color channel. Default is 5 for the 256-color range (8bit) used in terminals. Set this to 255 to use the full 24bit color range.
    min_value:int: The minimum value for each color channel. Default is 0.
    yield_end:bool: If True, the last color (which is the same as the first color) will be yielded as well to close the loop.

  Returns:
    A range of color values as tuples. (Red, Green, Blue)
  """
  r, g, b = max_value, min_value, min_value
  for _ in range(max_value):
    yield r, g, b
    g += 1
  for _ in range(max_value):
    yield r, g, b
    r -= 1
  for _ in range(max_value):
    yield r, g, b
    b += 1
  for _ in range(max_value):
    yield r, g, b
    g -= 1
  for _ in range(max_value):
    yield r, g, b
    r += 1
  for _ in range(max_value):
    yield r, g, b
    b -= 1
  if yield_end:
    yield r, g, b


def brightness(value:int, dim_multiplier:float, bright_multiplier:float, max_value:int=RGB_MAX_VALUE):
  """Calculates the brightness of a color value.
  The brightness of a color value can be calculated by using the dim-multiplier and the bright-multiplier.
  The dim-multiplier will be used to darken the color by simply multiplying the color value with the dim-multiplier.
  RGB = (RGB * dim-multiplier)

  The bright-multiplier will be used to brighten the color by multiplying the delta to the colors maximum value with the bright-multiplier and adding it to the color value.
  RGB = RGB + ((RGB_MAX - RGB) * bright-multiplier)

  The resulting formula will be:
  RGB = (RGB * dim-multiplier) + ((RGB_MAX - RGB) * bright-multiplier)

  Args:
    value: The value of the color channel. (Red, Green, Blue)
    dim_multiplier: The dim-multiplier to darken the color. (0.0 - 1.0)
    bright_multiplier: The bright-multiplier to brighten the color. (0.0 - 1.0)
    max_value: The maximum value for the color channel. Default is 5 for the 256-color range (8bit) used in terminals. Set this to 255 to use the full 24bit color range.

  Returns:
    The color value with the given brightness.
  """
  return int(dim_multiplier * value) + int(bright_multiplier * (max_value - value))


# Functions ##########################################################################################################################################
def colored_256(color, text, return_parts=False, foreground=True, background=False):
  """ Uses the normal Escape sequences to color the text.

  Args:
    color: The color to use. Calculated by the color picker.
    text: The text to color.
    return_parts: If True, returns the color parts as a tuple. (color_start, colored_text, color_end)
    foreground: If True, the foreground color is used.
    background: If True, the background color is used.

  Returns:
    The colored text as string or a tuple of the color parts.

  Example:
    print(colored(5, "Hello World!")) # prints the text in color 5

  Explanation:
    After the color picker is used to determine the color value from 0 to 255, this function can be used to color text.
    The result can then be printed to the terminal.

    How it the excape sequence is constructed you ask?
    Easy:
      - Start Sequence: \033[38;5;???m
        - The first byte is the escape character: \033, which determines the start of the escape sequence.
        - The second byte is the bracket: [, which is used to start the color sequence.
        - The next three bytes are the color code: 38 for foreground or 48 for background, followed by a semicolon.
        - The next two bytes are the numer 5 to indicate that the color is a 256 color code, followed by a semicolon.
        - The next one to three bytes (??? in the example) are the color code, representing the color from 0 to 255.
        - The last byte is the m to indicate the end of the color code.
      - Depending if you want to set the foreground or background color, this sequence is repeated again with a 48 instead of 38.
      - Next comes the text that should be colored.
      - End Sequence: \033[0m
        - The first byte is the escape character: \033, which determines the start of the escape sequence.
        - The second byte is the bracket: [, which is used to start the color sequence.
        - The next byte is the numer '0' to indicate that the color sequence should be reset.
        - The last byte is the m to indicate the end of the color sequence.
  """
  color_start_fg = "\033[38;5;%dm" % color
  color_start_bg = "\033[48;5;%dm" % color
  if not foreground:
    color_start_fg = ""
  if not background:
    color_start_bg = ""
  colored_text = text
  color_end = "\033[0m"
  result = color_start_fg + color_start_bg + colored_text + color_end
  if return_parts:
    return color_start_fg, color_start_bg, colored_text, color_end
  return result


def display_title(stdscr):
  msg_lines = [
    "  ____      _              ____  _      _               ",
    " / ___|___ | | ___  _ __  |  _ \(_) ___| | _____ _ __ _ ",
    "| |   / _ \| |/ _ \| '__| | |_) | |/ __| |/ / _ \ '__(_)",
    "| |__| (_) | | (_) | |    |  __/| | (__|   <  __/ |   _ ",
    " \____\___/|_|\___/|_|    |_|   |_|\___|_|\_\___|_|  (_)"
  ]
  #stdscr.addstr("Color Picker:\n\n")
  for line in msg_lines:
    stdscr.addstr("     " + line + "\n")
  stdscr.addstr("\n")


def display_basic_colors(stdscr, row, col):
  if row != ROW_BASIC_INDEX:
    stdscr.attron(uc.A_DIM)
  stdscr.addstr("       ┌")
  stdscr.addstr("───" * BASIC_COLOR_COUNT)
  stdscr.addstr("─┐\n       │")
  for i in range(BASIC_COLOR_COUNT):
    stdscr.addstr(" ")
    stdscr.attron(uc.COLOR_PAIR(i))
    cell = "  "
    if row == ROW_BASIC_INDEX and col == i:
      cell = ""
    stdscr.addstr(cell)
    stdscr.attroff(uc.COLOR_PAIR(i))
  stdscr.addstr(" │")
  if row == ROW_BASIC_INDEX:
    stdscr.addstr(" ")
  stdscr.addstr("\n       │")
  colE = col
  if colE > BASIC_COLOR_COUNT - 1:
    colE = BASIC_COLOR_COUNT - 1
  stdscr.addstr("   " * colE)
  if row == ROW_BASIC_INDEX:
    stdscr.addstr(" ")
  else:
    stdscr.addstr("   ")
  stdscr.addstr("   " * (BASIC_COLOR_COUNT - colE - 1))
  stdscr.addstr(" │\n")
  stdscr.addstr("       └")
  stdscr.addstr("───" * BASIC_COLOR_COUNT)
  stdscr.addstr("─┘\n")
  stdscr.attroff(uc.A_DIM)


def display_rgb_colors(stdscr, field, row, col):
  if row <= ROW_BASIC_INDEX or row >= ROW_GRAY_INDEX:
    stdscr.attron(uc.A_DIM)
  lineI = 0
  stdscr.addstr(" ┌──")
  stdscr.addstr("──" * RGB_COLOR_COUNT * RGB_MAX_VALUE)
  stdscr.addstr("──┐\n")
  for line in field:
    colI = 0
    stdscr.addstr(" │ ")
    for cell in line:
      m1,m2,r,g,b = cell
      r = brightness(r, m1, m2)
      g = brightness(g, m1, m2)
      b = brightness(b, m1, m2)
      color = calc_color_256(r, g, b)
      stdscr.attron(uc.COLOR_PAIR(color))
      cell = "  "
      if row == lineI and col == colI:
        cell = ""
      stdscr.addstr(cell)
      stdscr.attroff(uc.COLOR_PAIR(color))
      colI += 1
    stdscr.addstr(" │")
    if row == lineI:
      stdscr.addstr(" ")
    stdscr.addstr("\n")
    lineI += 1
  stdscr.addstr(" │ ")
  stdscr.addstr("  " * col)
  if row > ROW_BASIC_INDEX and row < ROW_GRAY_INDEX:
    stdscr.addstr("")
  else:
    stdscr.addstr("  ")
  stdscr.addstr("  " * (RGB_COLOR_COUNT * RGB_MAX_VALUE - col))
  stdscr.addstr(" │\n")
  stdscr.addstr(" └──")
  stdscr.addstr("──" * RGB_COLOR_COUNT * RGB_MAX_VALUE)
  stdscr.addstr("──┘\n\n")
  stdscr.attroff(uc.A_DIM)


def display_gray_colors(stdscr, row, col):
  if row < ROW_GRAY_INDEX:
    stdscr.attron(uc.A_DIM)
  stdscr.addstr("       ┌")
  stdscr.addstr("──" * GRAY_COLOR_COUNT)
  stdscr.addstr("──┐\n       │ ")
  for i in range(GRAY_COLOR_START, COLOR_MAX):
    stdscr.attron(uc.COLOR_PAIR(i))
    cell = "  "
    if row == ROW_GRAY_INDEX and col == i - GRAY_COLOR_START:
      cell = ""
    stdscr.addstr(cell)
    stdscr.attroff(uc.COLOR_PAIR(i))
  stdscr.addstr(" │")
  if row == ROW_GRAY_INDEX:
    stdscr.addstr(" ")
  stdscr.addstr("\n")
  stdscr.addstr("       │ ")
  colE = col
  if colE > GRAY_COLOR_COUNT - 1:
    colE = GRAY_COLOR_COUNT - 1
  stdscr.addstr("  " * colE)
  if row == ROW_GRAY_INDEX:
    stdscr.addstr("")
  else:
    stdscr.addstr("  ")
  stdscr.addstr("  " * (GRAY_COLOR_COUNT - colE - 1))
  stdscr.addstr(" │\n")
  stdscr.addstr("       └")
  stdscr.addstr("──" * GRAY_COLOR_COUNT)
  stdscr.addstr("──┘\n\n")
  stdscr.attroff(uc.A_DIM)


def selected_color(field, row, col):
  if row <= ROW_BASIC_INDEX:
    return col
  if row >= ROW_GRAY_INDEX:
    return col + GRAY_COLOR_START
  m1,m2,r,g,b = field[row][col]
  r = brightness(r, m1, m2)
  g = brightness(g, m1, m2)
  b = brightness(b, m1, m2)
  return calc_color_256(r, g, b)


def display_selection(stdscr, field, row, col):
  color = selected_color(field, row, col)
  lines = []
  if row <= ROW_BASIC_INDEX:
    lines = [
      " Basic Color (0 - 15)     ",
      "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾    ",
      " Choosen Basic Color:     ",
      "                          ",
      (" => " + BASIC_COLOR_NAMES[col] + (" " * 26))[:26],
      "                          ",
      " Color Value: %3i         " % col
    ]
  elif row >= ROW_GRAY_INDEX:
    lines = [
      " Gray Color (232 - 255)   ",
      "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  ",
      " Gray Value (V):  %3i     " % col,
      "                          ",
      " Calc: 232 + V            ",
      "                          ",
      " Color Value:             ",
      " 232 + %2i                 " % col,
      " = %3i                    " % color
    ]
  else:
    m1,m2,r,g,b = field[row][col]
    r = brightness(r, m1, m2)
    g = brightness(g, m1, m2)
    b = brightness(b, m1, m2)
    lines = [
      " RGB Color (16 - 231)     ",
      "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾    ",
      " Red Value:   %i  (0-5)    " % r,
      " Green Value: %i  (0-5)    " % g,
      " Blue Value:  %i  (0-5)    " % b,
      "                          ",
      " Calc: 36 * R + 6 * G + B ",
      "                          ",
      " Color Value:             ",
      " 36 * " + str(r) + " + 6 * " + str(g) + " + " + str(b) + "       ",
      " = %3i                    " % color
    ]
  height = 11
  while len(lines) < height:
    lines.append(" " * 26)
  lines = [" " * 26, *lines, " " * 26]
  # add python string escape example: print("\033[1;31;40m Bright Red \033[0m")
  # TODO: add python string escape example

  stdscr.addstr(" ┌─")
  stdscr.addstr("─" * 62)
  stdscr.addstr("─┐\n")
  stdscr.addstr(" │ ")
  uc.attron(uc.color_pair(color))
  stdscr.addstr(" " * 62)
  uc.attroff(uc.color_pair(color))
  stdscr.addstr(" │\n")
  for line in lines:
    stdscr.addstr(" │ ")
    uc.attron(uc.color_pair(color))
    stdscr.addstr(" " * 32)
    uc.attroff(uc.color_pair(color))
    uc.attron(uc.A_REVERSE)
    stdscr.addstr(" " + line + " ")
    uc.attroff(uc.A_REVERSE)
    uc.attron(uc.color_pair(color))
    stdscr.addstr("  ")
    uc.attroff(uc.color_pair(color))
    stdscr.addstr(" │\n")
  stdscr.addstr(" │ ")
  uc.attron(uc.color_pair(color))
  stdscr.addstr(" " * 62)
  uc.attroff(uc.color_pair(color))
  stdscr.addstr(" │\n")
  stdscr.addstr(" └─")
  stdscr.addstr("─" * 62)
  stdscr.addstr("─┘\n")


def display_text(stdscr):
  stdscr.addstr(" " * 25 + "Press 'q' to quit.")


def main():

  # Create a (6+6) x (6*6) big field of "  " strings
  field = [[(m1,m2,r,g,b) for r,g,b in color_range()] for m1,m2 in brightness_range()]

  with UnicursesGuard() as stdscr:
    # init basic colors
    for i in range(BASIC_COLOR_COUNT):
      bg = i
      fg = BLACK
      if i == 0 or i == BASIC_DIM_COLOR_COUNT:
        fg = WHITE
      uc.init_pair(i, fg, bg)

    # init rgb colors
    for line in field:
      for cell in line:
        m1,m2,r,g,b = cell
        r = brightness(r, m1, m2)
        g = brightness(g, m1, m2)
        b = brightness(b, m1, m2)
        color = calc_color_256(r, g, b)
        bg = color
        fg = BLACK
        if m1 < 1:
          #fg = calc_color(brightness(r, 1, 1/2), brightness(g, 1, 1/2), brightness(b, 1, 1/2))
          fg = WHITE
        else:
          #fg = calc_color(brightness(r, 0.75, 0), brightness(g, 0.75, 0), brightness(b, 0.75, 0))
          pass
        uc.init_pair(color, fg, bg)

    # init gray colors
    for i in range(GRAY_COLOR_START, COLOR_MAX):
      bg = i
      fg = BLACK
      if i < (GRAY_COLOR_START + GRAY_COLOR_COUNT // 2):
        fg = WHITE
      uc.init_pair(i, fg, bg)

    row = (ROW_GRAY_INDEX - ROW_BASIC_INDEX) // 2
    col = 0

    # draw loop
    action = 0
    while action != ord('q'):
      # clear screen
      stdscr.move(0, 0)

      # add text
      display_title(stdscr)

      # add color table (basic colors)
      display_basic_colors(stdscr, row, col)

      # add color table (rgb colors)
      display_rgb_colors(stdscr, field, row, col)

      # add color table (gray colors)
      display_gray_colors(stdscr, row, col)

      # add selection display
      display_selection(stdscr, field, row, col)

      # add text
      display_text(stdscr)

      # refresh screen
      stdscr.refresh()

      # get user input
      action = stdscr.getch()

      # handle user input
      if action == uc.KEY_UP:
        row -= 1
      elif action == uc.KEY_DOWN:
        row += 1
      elif action == uc.KEY_LEFT:
        col -= 1
      elif action == uc.KEY_RIGHT:
        col += 1

      # correct values
      if row < ROW_BASIC_INDEX:
        row = ROW_BASIC_INDEX
      if row > ROW_GRAY_INDEX:
        row = ROW_GRAY_INDEX

      max_col = RGB_COLOR_COUNT * RGB_MAX_VALUE
      if row == ROW_BASIC_INDEX:
        max_col = BASIC_COLOR_COUNT - 1
      if row >= ROW_GRAY_INDEX:
        max_col = GRAY_COLOR_COUNT - 1

      if col < 0:
        col = 0
      if col > max_col:
        col = max_col


if __name__ == "__main__":
  main()
