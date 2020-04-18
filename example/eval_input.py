import anyfig
from pathlib import Path
import numpy as np
from datetime import datetime
import time
import functools


@anyfig.config_class
class DataConfig():
  def __init__(self):
    self.ll = [1, 2] * 10
    self.pp = Path('myppp')


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.data = DataConfig()
    self.yo = 'yo'
    self.f = func1


def func1():
  print('im func1')
  return 'f1'


def func2():
  print('im func2')
  return 'f2'


class Part():
  def __init__(self, x, y):
    self.x = x
    self.y = y


@anyfig.config_class  # Registers the class with anyfig
class MyConfig():
  def __init__(self):
    # Config-parameters goes as attributes
    self.save_directory = Path('output')


if __name__ == '__main__':
  # config = anyfig.setup_config(default_config=MainConfig)
  config = anyfig.setup_config(default_config=MyConfig)
  print(config)
