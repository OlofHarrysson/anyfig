import anyfig
# from anyfig import input_argument as inp_arg
from pathlib import Path
import time
import typing


@anyfig.config_class  # Registers the class with anyfig
class MyConfig:
  def __init__(self):
    # Note help
    self.experiment_note: str = 'Changed stuff'
    # Start help
    self.start_time = time.time()

    # The inner config obj
    self.innerfig = InnerConfig()

  def post_init(self):
    print(type(self).__name__)


@anyfig.config_class
class InnerConfig:
  def __init__(self):

    # An integer between the values of 1 and 10 because the world has never seen such apples
    self.inner = 'innner'

  def post_init(self):
    print(type(self).__name__)


class InnerConfig2:
  def __init__(self):
    # Note help
    self.inner = 'innner2'


# tt = typing.Union[Path, str]
# tt = str
# print(tt)
# print(type(tt))
config = anyfig.init_config(default_config=MyConfig)
print(config)

# config.frozen(False)
# config.start_time = 123
# print(config)

# config.innerfig.inner = 'HEEJ'
# print(config)
