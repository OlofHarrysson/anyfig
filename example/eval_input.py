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

try:
  import time
except:
  pass


@anyfig.config_class
class DataConfig():
  def __init__(self):

    self.empty = 'kaoskdos'

    # THE comment promise
    self.asdas = 123

    # Variable ll
    self.ll = [1, 2] * 10
    """ First line is this one

    Empty above
    """
    self.multi = 123


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.data = DataConfig()

    # YOOYOYOYOO
    self.yo = 0
    self.shiiiet = [1, 2, 3]

    choices = [Path('main.py'), Path('train.py'), Path('eval_input.py')]
    file_exists = lambda v: v.exists()
    file_choices = lambda v: v in choices
    pattern = Path
    tests = [file_exists, file_choices]

    # A comment for sho
    self.interface = anyfig.FigValue(pattern, tests=tests)
    self.interface = Path('main.py')


@anyfig.config_class
class Main2(MainConfig):
  def __init__(self):
    super().__init__()
    # self.interface = 4

    # main2 comment
    self.interface = Path('eval_input.py')


@anyfig.config_class
class MultipleConfig():
  def __init__(self):
    self.configs = []

    c = MainConfig()
    self.configs.append(c)

    c = DataConfig()
    self.configs.append(c)


def main():
  # config = anyfig.init_config(default_config=DataConfig)
  config = anyfig.init_config(default_config=Main2)
  print(config)
  # print(config.)


if __name__ == '__main__':
  # config = anyfig.init_config(default_config=MainConfig)
  # print(config)

  main()

# Before main program / init_config is ran.
# Create another config class that help to run multiple main() runs with different configs
