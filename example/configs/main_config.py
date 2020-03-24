import anyfig
from pathlib import Path
import numpy as np


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
    self.help = 'asdas'
    self.class_ = WrongConfig()
    self.ones = np.ones((1, 10))
    self.ll = [1, 2] * 10
    # self = LocalConfig()


class WrongConfig():
  def __init__(self):
    self.foo = 'asd'
