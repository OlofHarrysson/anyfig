import anyfig
from pathlib import Path


@anyfig.config_class
class DataConfig():
  def __init__(self):
    self.batch_size = 2
    self.name = 'data1'
    self.ll = [1, 2]
    self.pp = Path('myppp')


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.foo = Path('my/path')
    self.data = DataConfig()
    self.yo = 'yo'


config = anyfig.setup_config(default_config=MainConfig)
print(config)
