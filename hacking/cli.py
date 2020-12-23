import anyfig
from pathlib import Path
import time
import argparse


@anyfig.config_class  # Registers the class with anyfig
class MyConfig:
  def __init__(self):
    # Config-parameters goes as attributes
    self.experiment_note = 'Changed stuff'
    self.save_directory = Path('output')
    self.start_time = time.time()

    # self.inner_config = InnerConfig()


@anyfig.config_class
class InnerConfig():
  def __init__(self):
    self.inner_text = "Yo Dawg"


# parser = argparse.ArgumentParser()

# parser.add_argument("--start_time",
#                     type=int,
#                     help="display a square of a given number")
# dict_args = vars(parser.parse_args())
# print('known', dict_args)
# print('unknown', unknown)
# args = dict(args)
# print(args)

import sys
dict_args = sys.argv[1:]
print(dict_args)
dict_args = anyfig.parse_cli_args(dict_args)
print(dict_args)
dict_args.pop('start_time', None)

config = anyfig.init_config(default_config=MyConfig, cli_args=dict_args)
print(config)
