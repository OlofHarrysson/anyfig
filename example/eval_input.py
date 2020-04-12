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


if __name__ == '__main__':
  # config = anyfig.setup_config(Path)
  # config = anyfig.setup_config(default_config=WrongConfig())
  # config = anyfig.setup_config(default_config=WrongConfig)
  config = anyfig.setup_config(default_config=MainConfig)
  # config2 = anyfig.setup_config(default_config=SecondConfig)
  # config = anyfig.setup_config(default_config=LocalConfig)
  # config = anyfig.setup_config(default_config=MainConfig())
  # config2 = anyfig.cfg()
  # print(config is config2)
  # config.frozen(False)
  # config.foo = 'qwe'
  print(config)
  # print(config2)
