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
# import jsonpickle
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


@anyfig.config_class
class MainConfig3():
  def __init__(self):
    # Define allowed values
    # self.save_directory = anyfig.field(Path)
    # self.save_directory = anyfig.field(Path, lambda x: x.exists())
    # self.save_directory = anyfig.field(str)
    self.save_directory = anyfig.field(int)
    # self.save_directory = anyfig.field(typing.Union[Path, str])

    # Set value directly, in subclass or from command line input
    # self.save_directory = Path('output')  # OK
    # self.save_directory = 'output'  # Error. Value is not correct type


def main():
  config = anyfig.init_config(default_config=MainConfig3)
  print(config)


if __name__ == '__main__':
  main()
