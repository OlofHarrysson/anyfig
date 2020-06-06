import anyfig
from pathlib import Path


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.save_directory = 123
    self.inner = InnerConfig(**dict(heh=1, aa=212))


@anyfig.config_class
class InnerConfig():
  def __init__(self, vali, boi, ehhehe):
    self.save_directory = vali


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


def main():
  # config = anyfig.init_config(default_config=MainConfig)
  config = anyfig.init_config(default_config=InnerConfig)
  print(config)


if __name__ == '__main__':
  main()