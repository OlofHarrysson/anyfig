import anyfig
from pathlib import Path


@anyfig.config_class
class DataConfig():
  def __init__(self):
    self.batch_size = 2
    self.name = 'data1'
    self.ll = [1, 2] * 10
    self.pp = Path('myppp')


@anyfig.config_class
class DataConfig2():
  def __init__(self):
    self.batch_size = 66666


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.foo = Path('my/path')
    self.data = DataConfig()
    self.yo = 'yo'
    self.help = 'asdas'


class WrongConfig():
  def __init__(self):
    self.foo = 'asd'


if __name__ == '__main__':
  # config = anyfig.setup_config(Path)
  # config = anyfig.setup_config(default_config=WrongConfig())
  # config = anyfig.setup_config(default_config=WrongConfig)
  config = anyfig.setup_config(default_config=MainConfig)
  # config = anyfig.setup_config(default_config=MainConfig())
  # config2 = anyfig.cfg()
  # print(config is config2)
  # config.frozen(False)
  # config.foo = 'qwe'
  print(config)
