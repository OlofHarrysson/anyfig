import anyfig
# from anyfig import input_argument as inp_arg
from pathlib import Path
import time
import typing
from anyfig import print_utils


@anyfig.config_class  # Registers the class with anyfig
class MyConfig:
  def __init__(self):
    # Note help
    self.experiment_note: int = 'Changed stuff'
    # Start help
    self.start_time = time.time()

    # The inner config obj
    self.innerfig = InnerConfig()

    # self.help = 'heeelp'

  # def allowed_cli_args(self):
  #   pass

  # def cli_help(self):
  #   hej = "YOOOLLOOF"
  #   cmt = print_utils.cli_help(self)
  #   return hej + cmt
  # return "YOOOLLOOF"

  # return ['start_time1']
  # return 'start_time', 'innerfig'
  # return 'start_time'


@anyfig.config_class
class InnerConfig:
  def __init__(self):

    # An integer between the values of 1 and 10 because the world has never seen such apples
    self.inner = 'innner'
    self.inner2 = 'innner2'


class InnerConfig2:
  def __init__(self):
    # Note help
    self.inner = 'innner2'


config = anyfig.init_config(default_config=MyConfig)
print(config)
