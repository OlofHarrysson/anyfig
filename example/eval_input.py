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
    ''' This comment is so goodoasdaosdi ois hdashda sdhaosudh asuhodi asuhod aisuhd asuidh liuasdh alisudh aisud 
    qwe

    qwethat it gets ever more than one line
    end of liiiine '''
    self.asdas = 123

    # Variable ll
    self.ll = [1, 2] * 10

    # Variable hooooo aiuefhauewif aiuwef iwuehiw uefiu hwegfiuo oiwhef oiwhefo idvhasdeföioh  oiwe owieF ÖOiwhfoie HOÖIWHFÖASOKDVHJÖ OIEAHWRFOI HEOÖ
    self.hoo = 'hooo'
    """ This comment is so goodoasdaosdi ois hdashda sdhaosudh asuhodi asuhod aisuhd asuidh liuasdh alisudh aisud 
    qwe

    qwethat it gets ever more than one line
    end of liiiine
    """
    self.multi = 123


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.data = DataConfig()
    self.yo = 0
    self.shiiiet = [1, 2, 3]

    # pattern = typing.List[int]
    pattern = int
    test1 = lambda v: v < 10
    test2 = lambda v: v > 0

    # test2 = lambda v: self.yo == 0

    # def test(x):
    #   return x > 0

    # test = [test1, test2]
    # test = None

    a = [1, 2, 3]
    # test = lambda v: v in a
    test = lambda v: v.exists()
    # self.interface = anyfig.FigValue(pattern, tests=test, help='asds')
    self.interface = anyfig.FigValue(tests=test)
    # self.interface = anyfig.FigValue()
    # self.interface = anyfig.FigValue(help='asds')

    # self.interface = [1, 2]
    # self.interface = 'asdasd'
    # a = [2, 3, 4]
    self.interface = Path('main.py')
    # self.interface = -1


@anyfig.config_class
class Main2(MainConfig):
  def __init__(self):
    super().__init__()
    # self.interface = 1
    self.interface = -1


@anyfig.config_class
class MultipleConfig():
  def __init__(self):
    self.configs = []

    c = MainConfig()
    self.configs.append(c)

    c = DataConfig()
    self.configs.append(c)


def main():
  config = anyfig.init_config(default_config=DataConfig)
  print(config)
  # print(config.)


if __name__ == '__main__':
  # config = anyfig.init_config(default_config=MainConfig)
  # print(config)

  main()

# Before main program / init_config is ran.
# Create another config class that help to run multiple main() runs with different configs
