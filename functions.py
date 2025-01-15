""" This file contains some useful functions for terminal colors.
"""


def escape_str(s:str) -> str:
  """ Escapes the string for the terminal.

  Args:
    s(str): The string to escape.

  Returns:
    The escaped string.
  """
  return '"' + s.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace("\b", "\\b").replace("\f", "\\f").replace("\v", "\\v") + '"'


def colored_256(color:int, text:str, return_parts:bool=False, foreground:bool=True, background:bool=False) -> str|tuple[str, str, str, str]:
  """ Uses the normal Escape sequences to color the text.

  Args:
    color(int): The color to use. Calculated by the color picker.
    text(str): The text to color.
    return_parts(bool): If True, returns the color parts as a tuple. (color_start, colored_text, color_end)
    foreground(bool): If True, the foreground color is used.
    background(bool): If True, the background color is used.

  Returns:
    The colored text as string or a tuple of the color parts. (color_start_fg, color_start_bg, text, color_end)

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
