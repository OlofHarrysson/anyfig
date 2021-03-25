import anyfig
from pathlib import Path
import time


class Unfrozen:
  def __init__(self, config):
    self.config = config
    self.frozen_enter = config._frozen
    config.frozen(False)

  def __enter__(self):
    print("ENTER")
    return self.config

  def __exit__(self, exc_type, exc_val, exc_tb):
    print("EXIT")
    self.config.frozen(self.frozen_enter)


@anyfig.config_class  # Registers the class with anyfig
class MyConfig:
  def __init__(self):
    # Note help
    self.experiment_note: int = 'Changed stuff'
    # Start help
    self.start_time = time.time()

    # The inner config obj
    self.innerfig = InnerConfig()


@anyfig.config_class
class InnerConfig:
  def __init__(self):

    # An integer between the values of 1 and 10 because the world has never seen such apples
    self.inner = 'innner'


config = anyfig.init_config(default_config=MyConfig)
print(config)

# config.start_time = 123

# with Unfrozen(config):
#   config.start_time = 1234
# config.start_time = 1

# Return an Unfrozen wrapper somehow without importing it in file.
# print(config.frozen2(False))
# with config.frozen2(False) as cfg:
#   # config.start_time = 123
#   cfg.start_time = 123
#   print(cfg)
# config.start_time = 1  # Show error

# print(config.frozen3(False))
with config(freeze=False):
  config.start_time = 123
  # cfg.start_time = 123
config.start_time = 1  # Show error
