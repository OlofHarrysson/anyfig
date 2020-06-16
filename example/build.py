import anyfig
from pathlib import Path
import numpy as np
from datetime import datetime


def mydatetime(year, month, day):
  return 'mydattetime func'


@anyfig.config_class
class MyDatetime:
  # year: int
  # month: int
  # day: int

  def __init__(self, year, month=2, day=2):
    self.year = year
    self.month = month
    self.day = day


# class MyDatetime:
#   def __init__(self, **kwargs):
#     self.year = 1


# @anyfig.config_class(target=mydatetime)
# @anyfig.config_class(target=MyDatetime)
@anyfig.config_class(target=datetime)
# @anyfig.config_class
class MainConfig():
  def __init__(self):
    self.year = 2020
    # self.month = 1
    # self.day = 12


def main():

  # cls = MainConfig
  # print(cls)
  # print(cls.__call__)
  # print(callable(cls))

  # qew

  config = anyfig.init_config(default_config=MainConfig)
  # print(config)
  # dtime = datetime(2020, 1, 1)
  # param = dict(day=3)
  # param = dict(asdas=3)
  param = dict(day=3, month=12)
  # param = dict()
  dtime = config.build(param)
  # dtime = datetime(year=1, month=2, day=3)
  print(dtime)


if __name__ == '__main__':
  main()

# TODO: C-types __init__