import anyfig
from pathlib import Path
from datetime import datetime


def mydatetime(year, month, day):
  return 'mydattetime func'


@anyfig.config_class
class MyDatetime:
  year: int = 1
  month: int = 2
  day: int = 3

  # year: int
  # month: int
  # day: int

  # def __init__(self, year, month=2, day=2):
  #   self.year = year
  #   self.month = month
  #   self.day = day


@anyfig.config_class
class Empty:
  def hej(self):
    return 'hej'


@anyfig.config_class(target=datetime)
class MainConfig():
  def __init__(self):
    self.year = 1996
    self.month = 12
    # self.day = 13


def main():

  # cls = MainConfig
  # print(cls)
  # print(cls.__call__)
  # print(callable(cls))

  # qew

  config = anyfig.init_config(default_config=MyDatetime)
  print(config)

  print(anyfig.registered_config_classes)
  anyfig.unregister_configs()
  print(anyfig.registered_config_classes)
  qweqw

  config = MyDatetime()
  print(config)
  emp = Empty()
  print(emp)
  qwe
  # dtime = datetime(2020, 1, 1)
  param = dict(year=3)
  param = dict(day=1, month=2, year=3)
  # param = dict(asdas=3)
  # param = dict(day=3, month=12)
  # param = dict()
  dtime = config.build(param)
  # dtime = datetime(year=1, month=2, day=3)
  print(dtime)


if __name__ == '__main__':
  main()
