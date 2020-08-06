import json
import anyfig
from pathlib import Path


@anyfig.config_class
class InnerConfig():
  def __init__(self):
    self.inner = 'inner'


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.a = 'a'
    self.li = [1, 2, '3']
    self.i = InnerConfig()
    # self.i2 = InnerConfig()

    self.int_dict = {1: 1, 2: 2}

    # self.j = self.i

  def extra_func(self):
    print("EXTRA")


def main():
  config = anyfig.init_config(default_config=MainConfig)
  # print(config)
  # anyfig.save_config(config, 'save.pickle')
  # config = anyfig.load_config('save.pickle')

  # anyfig.save_json(config, 'save.json')
  # config = anyfig.load_json('save.json')

  print(config)
  print(type(config))


if __name__ == '__main__':
  main()
