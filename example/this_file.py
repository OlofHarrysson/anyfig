import anyfig
from pathlib import Path
import numpy as np
from datetime import datetime
import functools
import sys
from io import StringIO
import fire
import typing
import argparse
from collections import namedtuple
from dataclasses import dataclass
import inspect
import jsonpickle
import json

import anyfig
from pathlib import Path


@anyfig.config_class
class MainConfig2():
  def __init__(self):
    # Define tests
    file_exists = lambda new_value: new_value.exists()
    self.python_file = anyfig.field(tests=file_exists)

    # Set value directly, in subclass or from command line input
    self.python_file = Path('this_file.py')  # OK
    # self.python_file = Path('other_file.py')  # Error. File doesn't exist
    self.python_file = 'Strings have no exists()'  # Descriptive error


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.python_file = anyfig.constant(Path('this_file.py'), strict=True)

    # Set value directly, in subclass or from command line input
    self.python_file = Path('this_file.py')  # Ok. Compares with == by default
    # self.python_file = Path('other_file.py')  # Error


def main():
  config = anyfig.init_config(default_config=MainConfig)
  print(config)
  sad

  config_path = 'config.json'
  frozen = jsonpickle.encode(config)
  thawed = jsonpickle.decode(frozen)
  print(thawed)
  print(config == thawed)

  frozen = json.dumps(json.loads(frozen), indent=4)
  with open(config_path, 'w') as f:
    f.write(frozen)

  read_json_config(config_path)
  qwe

  # print(repr(config))
  # config.frozen(freeze=False)
  # config.yo = 123


def read_json_config(file_path):
  import json
  with open(file_path) as infile:
    json_data = infile.read()

  thawed = jsonpickle.decode(json_data)
  print(thawed)


if __name__ == '__main__':
  main()
