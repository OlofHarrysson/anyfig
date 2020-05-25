import anyfig
from pathlib import Path
import numpy as np
from datetime import datetime
import functools
import sys
from io import StringIO
import fire
import typing
import pytypes
import argparse
from collections import namedtuple
from dataclasses import dataclass

try:
  import time
except:
  pass


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


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.data = DataConfig()

    # YOOYOYOYOO
    self.yo = 0
    self.shiiiet = [1, 2, 3]

    choices = [Path('main.py'), Path('train.py'), Path('eval_input.py')]
    file_exists = lambda v: v.exists()
    # file_exists = lambda v: v / v
    # file_exists = lambda v: 1 / 0
    file_choices = lambda v: v in choices
    pattern = Path
    tests = [file_exists, file_choices]

    # A comment for sho
    self.interface = anyfig.field(pattern, tests=tests)
    # self.interface = Path('main.p2y')
    # self.interface = Path('main.py')


def main():
  config = anyfig.init_config(default_config=MainConfig)
  print(config)
  hej = 1


if __name__ == '__main__':
  main()