import anyfig
from pathlib import Path
import jsonpickle


@anyfig.config_class
class MainConfig():
  def __init__(self):
    # YOOYOYOYOO
    self.yo = 0
    # asdasd
    self.yo = 123

    self.shiiiet = [1, 2, 3]


@anyfig.config_class
class InnerConfig():
  def __init__(self):
    self.save_directory = 12


def main():
  config = anyfig.init_config(default_config=MainConfig)
  print(config)


if __name__ == '__main__':
  main()