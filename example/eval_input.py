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
    self.foo = Path('my/path')
    self.data = DataConfig()
    self.yo = 'yo'
    self.help = 'asdas'
    self.class_ = WrongConfig()
    self.ones = np.ones((1, 10))
    self.ll = [1, 2] * 10
    # self = LocalConfig()


class WrongConfig():
  def __init__(self):
    self.foo = 'asd'


@anyfig.config_class
class SecondConfig():
  def __init__(self):
    self.experiment_note = 'Number 2'


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
