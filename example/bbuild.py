import anyfig
from datetime import datetime


@anyfig.config_class(target=datetime)
class MyConfig():
  def __init__(self):
    self.year = 1996
    self.month = 12


config = anyfig.init_config(default_config=MyConfig)
build_args = dict(day=13)
date = config.build(build_args)
print(date)
print(config)


class DataProcesser:
  def __init__(self, algorithm, data):
    self.algorithm = algorithm
    self.data = data

  # ... Other methods


@anyfig.config_class(target=DataProcesser)
class MyConfig():
  def __init__(self):
    self.algorithm = '+'


config = anyfig.init_config(default_config=MyConfig)
build_args = dict(data=my_data_object)
data_processor = config.build(build_args)