import anyfig
from pathlib import Path
import jsonpickle


@anyfig.config_class
class MainConfig2():
  def __init__(self):
    # self.data = DataConfig()

    # YOOYOYOYOO
    self.yo = 0
    self.shiiiet = [1, 2, 3]

    choices = [Path('main.py'), Path('train.py'), Path('eval_input.py')]
    file_exists = lambda v: v.exists()
    # file_exists = lambda v: v / v
    # file_exists = lambda v: 1 / 0
    file_choices = lambda v: v in choices
    pattern = Path
    tests = [file_exists, file_choices]

    # A comment for sho
    self.interface = anyfig.field(pattern, tests=tests)
    # self.interface = Path('main.p2y')
    self.interface = Path('main.py')

    constant = Path('main.py')
    # self.HATS = anyfig.field(tests=lambda x: x is constant)
    self.HATS = anyfig.constant(Path('main.py'), strict=False)

    self.HATS = Path('main.py')

    self.HATS = Path('main.py')


class Hej:
  def __init__(self):
    a = 1


@anyfig.config_class(target=Hej)
class MainConfig():
  def __init__(self):
    self.save_directory = 123
    self.inner = InnerConfig()


@anyfig.config_class
class InnerConfig():
  def __init__(self):
    self.save_directory = 12


# @anyfig.config_class
# class InnerConfig():
#   def __init__(self, *args, **kwargs):
#     # self.save_directory = 1
#     hej = 1
#     print(args, kwargs)
#     self.args = args
#     self.kwargs = kwargs


# @anyfig.config_class
# class InnerConfig():
#   save_directory: str = 1
def read_json_config(file_path):
  import json
  with open(file_path) as infile:
    json_data = infile.read()

  thawed = jsonpickle.decode(json_data)
  print(thawed)
  print(type(thawed))


def main():
  config = anyfig.init_config(default_config=MainConfig)
  # config = anyfig.init_config(default_config=InnerConfig)
  print(config)
  print(dir(config))
  print(config.__build_target)
  # print(config.__build_target)

  # read_json_config('config.json')


if __name__ == '__main__':
  main()