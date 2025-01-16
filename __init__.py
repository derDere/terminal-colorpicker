""" This Module contains a ColorPicker that can be used as a standalone application or as a TUI control.
"""


from unicguard import UnicursesGuard


# Constants ##########################################################################################################################################
from constants import *


# Calculations #######################################################################################################################################
from calculations import *


# Functions ##########################################################################################################################################
from functions import *


# Class ##############################################################################################################################################
from color_picker import ColorPicker


def main():
  """ Main function that runs the ColorPicker as a standalone application.
  """
  with UnicursesGuard() as stdscr:
    color_picker = ColorPicker(stdscr)
    color_picker.run()


if __name__ == "__main__":
  main()
