import unicurses as uc
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
  with UnicursesGuard() as stdscr:
    color_picker = ColorPicker(stdscr)
    color_picker.run()


if __name__ == "__main__":
  main()
