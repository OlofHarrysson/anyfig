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
import inspect


def heej():
  return 1


@anyfig.config_class
class Hej():
  def __init__(self, x, y, z, asd=1123, qwe=123):
    self.x = x
    self.y = y

  def bla(self):
    return 1


# @anyfig.config_class
# @anyfig.config_class()
# @anyfig.config_class(Hej)
@anyfig.config_class(target=Hej)
# @anyfig.config_class(target=heej)
class DataConfig():
  def __init__(self):
    self.x = 1
    self.y = 2
    self.hej = Hej(1, 2, 3)


# @anyfig.config_class
# class MainConfig():
#   def __init__(self):
#     # Define tests
#     # file_exists = lambda new_value: new_value.exists()
#     # allowed_files = [Path('this_file.py'), Path('other_file.py')]
#     # file_allowed = lambda new_value: new_value in allowed_files
#     # file_tests = [file_exists, file_allowed]
#     # self.python_file = anyfig.field(tests=file_tests)

#     # # Set value directly, in subclass or from command line input
#     # self.python_file = Path('this_file.py')  # OK
#     # self.python_file = Path('other_file.py')  # Error. File doesn't exist
#     # self.python_file = Path(
#     #   'anyfig.txt')  # Error. File exist but isn't allowed

#     # self.save_directory = anyfig.field(str)
#     # self.save_directory = anyfig.field(Path)
#     self.save_directory = anyfig.field(typing.List)
#     self.save_directory = [1, 2]

#     # self.data = DataConfig()


@anyfig.config_class
class MainConfig2():
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
    self.interface = Path('main.py')

    constant = Path('main.py')
    # self.HATS = anyfig.field(tests=lambda x: x is constant)
    self.HATS = anyfig.constant(Path('main.py'), strict=False)

    self.HATS = Path('main.py')

    # self.HATS = Path('main.py')


@anyfig.config_class
class MainConfig():
  # save_directory: int = 9090

  def __init__(self):
    # self.save_directory = 9090
    self.save_directory = 123


@anyfig.config_class
class CConfig:
  x: str = 'c'


@anyfig.config_class
class DConfig:
  # x: str = 'd'
  # y: str = 1

  def __init__(self):
    self.x = 1
    self.c = CConfig()


@anyfig.config_class
class InnerConfig(MainConfig):
  b: int = DConfig()
  yo: int = 123
  yo1: int = 123

  # def __init__(self):
  #   self.yo = 1
  #   self.b = [1, 2, 3]

  # self.d = DConfig()


# d = DConfig()
# print(d)
# print("WOWOWO12312")
# qwe


def main():
  config = anyfig.init_config(default_config=MainConfig2)
  # config = anyfig.init_config(default_config=DConfig)
  # config = anyfig.init_config(default_config=InnerConfig)
  # print(dir(config))
  # config = InnerConfig()
  # config.b.append(4)
  print(config)
  # asd
  # print(repr(config))
  # config.frozen(freeze=False)
  # config.yo = 123

  config2 = InnerConfig()
  # config2 = anyfig.init_config(default_config=InnerConfig)
  print(config2)

  print(config == config2)
  print(id(config), id(config2))


if __name__ == '__main__':
  main()