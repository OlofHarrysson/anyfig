import anyfig
from pathlib import Path
import time


class Unfrozen:
  def __init__(self, config):
    self.config = config
    self.frozen_enter = config._frozen
    config.frozen(False)

  def __enter__(self):
    return self.config

  def __exit__(self, exc_type, exc_val, exc_tb):
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
with config.frozen(False):
  config.start_time = 123
# with some_lock:

config.start_time = 123

# with open() as f:
#   lines = f.read().splitlines()
