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
  p = argparse.ArgumentParser()
  # p.add_argument(
  #   "--square",
  #   type=int,
  #   required=True,
  #   help="display a square of a given number",
  # )
  p.add_argument(
    "--poop",
    type=int,
    help="display a square of a given number",
  )
  p.add_argument(
    "--poo2p",
    type=int,
    default=12,
    help="display a square of a given number",
  )

  args, unknown = p.parse_known_args(
  )  # Parses input args and checks for errors
  print(args)
  print(unknown)
  print(type(args))
  print(vars(args))
  # config = anyfig.init_config(default_config=MultipleConfig)
  # config = anyfig.init_config(default_config=DataConfig)
  config = anyfig.init_config(default_config=DataConfig, cli_args={})
  # config = anyfig.init_config(default_config=DataConfig, cli_args=vars(args))
  # config = anyfig.init_config(default_config=DataConfig, cli_args=[1, 2, 3])
  # config = anyfig.init_config(default_config=Main2)
  print(config)
  # print(config.)


if __name__ == '__main__':
  main()

# Before main program / init_config is ran.
# Create another config class that help to run multiple main() runs with different configs
