""" This module contains the color picker class that allows the user to pick a color from the 256 color palette within the terminal.
"""


import unicurses as uc


from constants import ROW_GRAY_INDEX, ROW_BASIC_INDEX, BASIC_COLOR_COUNT, BASIC_DIM_COLOR_COUNT, GRAY_COLOR_START, GRAY_COLOR_COUNT, COLOR_MAX,  BLACK, WHITE, RGB_COLOR_COUNT, RGB_MAX_VALUE, BASIC_COLOR_NAMES
from calculations import color_range, brightness_range, brightness, calc_color_256
from functions import *


class ColorPicker(object):

  screen:any
  field:list[list[tuple[float,float,int,int,int]]]
  row:int
  col:int

  @property
  def selected_color(self):
    if self.row <= ROW_BASIC_INDEX:
      return self.col
    if self.row >= ROW_GRAY_INDEX:
      return self.col + GRAY_COLOR_START
    m1,m2,r,g,b = self.field[self.row][self.col]
    r = brightness(r, m1, m2)
    g = brightness(g, m1, m2)
    b = brightness(b, m1, m2)
    return calc_color_256(r, g, b)

  def __init__(self, screen):
    self.screen = screen
    # creating a field of colors values with brigness multipliers
    self.field = [[(m1,m2,r,g,b) for r,g,b in color_range()] for m1,m2 in brightness_range()]
    self.row = (ROW_GRAY_INDEX - ROW_BASIC_INDEX) // 2
    self.col = 0

    self._init_colors()

  def _init_colors(self):
    # init basic colors
    for i in range(BASIC_COLOR_COUNT):
      bg = i
      fg = BLACK
      if i == 0 or i == BASIC_DIM_COLOR_COUNT:
        fg = WHITE
      uc.init_pair(i, fg, bg)

    # init rgb colors
    for line in self.field:
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

  def _display_title(self):
    msg_lines = [
      "  ____      _              ____  _      _               ",
      " / ___|___ | | ___  _ __  |  _ \(_) ___| | _____ _ __ _ ",
      "| |   / _ \| |/ _ \| '__| | |_) | |/ __| |/ / _ \ '__(_)",
      "| |__| (_) | | (_) | |    |  __/| | (__|   <  __/ |   _ ",
      " \____\___/|_|\___/|_|    |_|   |_|\___|_|\_\___|_|  (_)"
    ]
    for line in msg_lines:
      self.screen.addstr("     " + line + "\n")
    self.screen.addstr("\n")

  def _display_basic_colors(self):
    if self.row != ROW_BASIC_INDEX:
      self.screen.attron(uc.A_DIM)
    self.screen.addstr("       ┌")
    self.screen.addstr("───" * BASIC_COLOR_COUNT)
    self.screen.addstr("─┐\n       │")
    for i in range(BASIC_COLOR_COUNT):
      self.screen.addstr(" ")
      self.screen.attron(uc.COLOR_PAIR(i))
      cell = "  "
      if self.row == ROW_BASIC_INDEX and self.col == i:
        cell = ""
      self.screen.addstr(cell)
      self.screen.attroff(uc.COLOR_PAIR(i))
    self.screen.addstr(" │")
    if self.row == ROW_BASIC_INDEX:
      self.screen.addstr(" ")
    self.screen.addstr("\n       │")
    colE = self.col
    if colE > BASIC_COLOR_COUNT - 1:
      colE = BASIC_COLOR_COUNT - 1
    self.screen.addstr("   " * colE)
    if self.row == ROW_BASIC_INDEX:
      self.screen.addstr(" ")
    else:
      self.screen.addstr("   ")
    self.screen.addstr("   " * (BASIC_COLOR_COUNT - colE - 1))
    self.screen.addstr(" │\n")
    self.screen.addstr("       └")
    self.screen.addstr("───" * BASIC_COLOR_COUNT)
    self.screen.addstr("─┘\n")
    self.screen.attroff(uc.A_DIM)

  def _display_rgb_colors(self):
    if self.row <= ROW_BASIC_INDEX or self.row >= ROW_GRAY_INDEX:
      self.screen.attron(uc.A_DIM)
    lineI = 0
    self.screen.addstr(" ┌──")
    self.screen.addstr("──" * RGB_COLOR_COUNT * RGB_MAX_VALUE)
    self.screen.addstr("──┐\n")
    for line in self.field:
      colI = 0
      self.screen.addstr(" │ ")
      for cell in line:
        m1,m2,r,g,b = cell
        r = brightness(r, m1, m2)
        g = brightness(g, m1, m2)
        b = brightness(b, m1, m2)
        color = calc_color_256(r, g, b)
        self.screen.attron(uc.COLOR_PAIR(color))
        cell = "  "
        if self.row == lineI and self.col == colI:
          cell = ""
        self.screen.addstr(cell)
        self.screen.attroff(uc.COLOR_PAIR(color))
        colI += 1
      self.screen.addstr(" │")
      if self.row == lineI:
        self.screen.addstr(" ")
      self.screen.addstr("\n")
      lineI += 1
    self.screen.addstr(" │ ")
    self.screen.addstr("  " * self.col)
    if self.row > ROW_BASIC_INDEX and self.row < ROW_GRAY_INDEX:
      self.screen.addstr("")
    else:
      self.screen.addstr("  ")
    self.screen.addstr("  " * (RGB_COLOR_COUNT * RGB_MAX_VALUE - self.col))
    self.screen.addstr(" │\n")
    self.screen.addstr(" └──")
    self.screen.addstr("──" * RGB_COLOR_COUNT * RGB_MAX_VALUE)
    self.screen.addstr("──┘\n\n")
    self.screen.attroff(uc.A_DIM)

  def _display_gray_colors(self):
    if self.row < ROW_GRAY_INDEX:
      self.screen.attron(uc.A_DIM)
    self.screen.addstr("       ┌")
    self.screen.addstr("──" * GRAY_COLOR_COUNT)
    self.screen.addstr("──┐\n       │ ")
    for i in range(GRAY_COLOR_START, COLOR_MAX):
      self.screen.attron(uc.COLOR_PAIR(i))
      cell = "  "
      if self.row == ROW_GRAY_INDEX and self.col == i - GRAY_COLOR_START:
        cell = ""
      self.screen.addstr(cell)
      self.screen.attroff(uc.COLOR_PAIR(i))
    self.screen.addstr(" │")
    if self.row == ROW_GRAY_INDEX:
      self.screen.addstr(" ")
    self.screen.addstr("\n")
    self.screen.addstr("       │ ")
    colE = self.col
    if colE > GRAY_COLOR_COUNT - 1:
      colE = GRAY_COLOR_COUNT - 1
    self.screen.addstr("  " * colE)
    if self.row == ROW_GRAY_INDEX:
      self.screen.addstr("")
    else:
      self.screen.addstr("  ")
    self.screen.addstr("  " * (GRAY_COLOR_COUNT - colE - 1))
    self.screen.addstr(" │\n")
    self.screen.addstr("       └")
    self.screen.addstr("──" * GRAY_COLOR_COUNT)
    self.screen.addstr("──┘\n\n")
    self.screen.attroff(uc.A_DIM)

  def _display_selection(self):
    color = self.selected_color
    lines = []
    if self.row <= ROW_BASIC_INDEX:
      lines = [
        " Basic Color (0 - 15)     ",
        "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾    ",
        " Choosen Basic Color:     ",
        "                          ",
        (" => " + BASIC_COLOR_NAMES[self.col] + (" " * 26))[:26],
        "                          ",
        " Color Value: %3i         " % self.col
      ]
    elif self.row >= ROW_GRAY_INDEX:
      lines = [
        " Gray Color (232 - 255)   ",
        "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  ",
        " Gray Value (V):  %3i     " % self.col,
        "                          ",
        " Calc: 232 + V            ",
        "                          ",
        " Color Value:             ",
        " 232 + %2i                 " % self.col,
        " = %3i                    " % color
      ]
    else:
      m1,m2,r,g,b = self.field[self.row][self.col]
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

    self.screen.addstr(" ┌─")
    self.screen.addstr("─" * 62)
    self.screen.addstr("─┐\n")
    self.screen.addstr(" │ ")
    uc.attron(uc.color_pair(color))
    self.screen.addstr(" " * 62)
    uc.attroff(uc.color_pair(color))
    self.screen.addstr(" │\n")
    for line in lines:
      self.screen.addstr(" │ ")
      uc.attron(uc.color_pair(color))
      self.screen.addstr(" " * 32)
      uc.attroff(uc.color_pair(color))
      uc.attron(uc.A_REVERSE)
      self.screen.addstr(" " + line + " ")
      uc.attroff(uc.A_REVERSE)
      uc.attron(uc.color_pair(color))
      self.screen.addstr("  ")
      uc.attroff(uc.color_pair(color))
      self.screen.addstr(" │\n")
    self.screen.addstr(" │ ")
    uc.attron(uc.color_pair(color))
    self.screen.addstr(" " * 62)
    uc.attroff(uc.color_pair(color))
    self.screen.addstr(" │\n")
    self.screen.addstr(" └─")
    self.screen.addstr("─" * 62)
    self.screen.addstr("─┘\n")

  def _display_text(self):
    self.screen.addstr(" " * 25 + "Press 'q' to quit.")

  def draw(self):
    """Draw the color picker to the screen.
    This function should be called before reading the user input.
    If you don't have a reasont to call this function manually, use the run() function instead.

    Example:
      color_picker = ColorPicker(screen)
      while <Condition>:
        color_picker.draw()
        user_input = screen.getch()
        color_picker.handle_input(user_input)
    """
    self.screen.move(0, 0)
    self._display_title()
    self._display_basic_colors()
    self._display_rgb_colors()
    self._display_gray_colors()
    self._display_selection()
    self._display_text()
    self.screen.refresh()

  def handle_input(self, input:int):
    """Handle the user input. This function should be called after the user input is read.
    If you don't have a reasont to call this function manually, use the run() function instead.

    Args:
      input: The user input as integer. This should be the result of the getch() function.

    Example:
      color_picker = ColorPicker(screen)
      while <Condition>:
        color_picker.draw()
        user_input = screen.getch()
        color_picker.handle_input(user_input)
    """

    # handle user input
    if input == uc.KEY_UP:
      self.row -= 1
    elif input == uc.KEY_DOWN:
      self.row += 1
    elif input == uc.KEY_LEFT:
      self.col -= 1
    elif input == uc.KEY_RIGHT:
      self.col += 1

    # correct values
    if self.row < ROW_BASIC_INDEX:
      self.row = ROW_BASIC_INDEX
    if self.row > ROW_GRAY_INDEX:
      self.row = ROW_GRAY_INDEX

    max_col = RGB_COLOR_COUNT * RGB_MAX_VALUE
    if self.row == ROW_BASIC_INDEX:
      max_col = BASIC_COLOR_COUNT - 1
    if self.row >= ROW_GRAY_INDEX:
      max_col = GRAY_COLOR_COUNT - 1

    if self.col < 0:
      self.col = 0
    if self.col > max_col:
      self.col = max_col

  def run(self, exit_key:int=ord('q')):
    """Run the color picker until the exit key is pressed.

    Args:
      exit_key: The key code that will exit the color picker. default: ord('q')

    Example:
      color_picker = ColorPicker(screen)
      color_picker.run()
    """
    action = 0
    while action != exit_key:
      self.draw()
      action = self.screen.getch()
      self.handle_input(action)