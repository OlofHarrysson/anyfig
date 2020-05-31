import anyfig
from pathlib import Path
import numpy as np
from datetime import datetime
import functools
import sys
from io import StringIO
import fire
import typing
import argparse
from collections import namedtuple
from dataclasses import dataclass


@anyfig.config_class
class DataConfig():
  def __init__(self):
    self.empty = 'kaoskdos'

    # THE comment promise
    self.verylongvariablenameislong = 123

    # Variable ll
    self.ll = [1, 2] * 10
    """ First line is this one

    Empty above
    """
    self.multi = 123

    # this shoulc be last comment
    self.other = 12


class Hej():
  def __init__(self):
    self.x = 'hej'

  # def __call__(self):
  #   print(self.x)


@anyfig.config_class
class MainConfig():
  def __init__(self):
    # Define tests
    # file_exists = lambda new_value: new_value.exists()
    # allowed_files = [Path('this_file.py'), Path('other_file.py')]
    # file_allowed = lambda new_value: new_value in allowed_files
    # file_tests = [file_exists, file_allowed]
    # self.python_file = anyfig.field(tests=file_tests)

    # # Set value directly, in subclass or from command line input
    # self.python_file = Path('this_file.py')  # OK
    # self.python_file = Path('other_file.py')  # Error. File doesn't exist
    # self.python_file = Path(
    #   'anyfig.txt')  # Error. File exist but isn't allowed

    # self.save_directory = anyfig.field(str)
    # self.save_directory = anyfig.field(Path)
    self.save_directory = anyfig.field(typing.List)
    # self.save_directory = Path('e')


@anyfig.config_class
class InnerConfig(MainConfig):
  def __init__(self):
    self.yo = 1


# @anyfig.config_class
# class MainConfig():
#   def __init__(self):
#     self.data = DataConfig()

#     # YOOYOYOYOO
#     self.yo = 0
#     self.shiiiet = [1, 2, 3]

#     choices = [Path('main.py'), Path('train.py'), Path('eval_input.py')]
#     file_exists = lambda v: v.exists()
#     # file_exists = lambda v: v / v
#     # file_exists = lambda v: 1 / 0
#     file_choices = lambda v: v in choices
#     pattern = Path
#     tests = [file_exists, file_choices]

#     # A comment for sho
#     self.interface = anyfig.field(pattern, tests=tests)
#     # self.interface = Path('main.p2y')
#     self.interface = Path('main.py')

#     constant = Path('main.py')
#     # self.HATS = anyfig.field(tests=lambda x: x is constant)
#     self.HATS = anyfig.constant(Path('main.py'), strict=False)

#     self.HATS = Path('main.py')

#     # self.HATS = Path('main.py')


def main():
  config = anyfig.init_config(default_config=MainConfig)
  print(config)
  hej = 1


if __name__ == '__main__':
  main()