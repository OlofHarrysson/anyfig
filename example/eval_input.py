import anyfig
from pathlib import Path
import numpy as np
from datetime import datetime
import time


@anyfig.config_class
class DataConfig():
  def __init__(self):
    self.batch_size = 2
    self.name = 'data1'
    self.ll = [1, 2] * 10
    self.pp = Path('myppp')


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.data = DataConfig()
    self.yo = 'yo'
    self.f = func1


class WrongConfig():
  def __init__(self):
    self.foo = 'asd'


@anyfig.config_class
class SecondConfig():
  def __init__(self):
    self.experiment_note = 'Number 2'


def func1():
  print('im func1')
  return 'f1'


def func2():
  print('im func2')
  return 'f2'


@anyfig.config_class  # Registers the class with anyfig
class MyConfig():
  def __init__(self):
    # Config-parameters goes as attributes
    self.experiment_note = 'Changed stuff'
    self.save_directory = Path('output')
    self.start_time = time.time()

  def hej(self):
    return self.experiment_note


if __name__ == '__main__':
  # config = anyfig.setup_config(default_config=MainConfig)
  config = anyfig.setup_config(default_config=MyConfig)
  print(config)
