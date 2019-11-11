from io import StringIO
import fire
import inspect
import argparse
import sys
from .masterconfig import MasterConfig, is_anyfig_class

registered_config_classes = {}


def setup_config(default_config=None):
  config_str = parse_args(default_config)
  config = choose_config(config_str)
  return config


def parse_args(default_config):
  p = argparse.ArgumentParser()

  p.add_argument('--config',
                 type=str,
                 default=default_config,
                 help='What config class to choose')

  args, _ = p.parse_known_args()
  return args.config


def choose_config(config_str):
  # Create config object
  err_msg = (
    "Specify which config to use by either starting your python script with "
    "the input argument --config=YourConfigClass or set "
    "'default_config=YourConfigClass' in anyfigs 'setup_config' method")
  if config_str == None:
    raise RuntimeError(err_msg)

  err_msg = ("There aren't any registered config classes. Decorate a class "
             "with '@anyfig.config_class' and make sure that the class is "
             "imported to the file where the function 'anyfig.setup_config' "
             "is called from")
  assert len(registered_config_classes), err_msg

  try:
    config_class_ = registered_config_classes[config_str]
    config_obj = config_class_()
  except KeyError as e:
    err_msg = (
      f"Config class '{config_str}' wasn't found. Feel free to create "
      "it as a new config class or use one of the existing ones "
      f"{list(registered_config_classes)}")
    raise KeyError(err_msg) from e

  # Overwrite parameters via optional input flags
  config_obj = overwrite(config_obj)

  # Freezes config
  config_obj.frozen(freeze=True)
  return config_obj


def overwrite(config_obj):
  ''' Overwrites parameters with input flags. Function is needed for the
  convenience of specifying parameters via a combination of the config classes
  and input flags. '''
  class NullIO(StringIO):
    def write(self, txt):
      pass

  def parse_unknown_flags(**kwargs):
    return kwargs

  sys.stdout = NullIO()
  extra_arguments = fire.Fire(parse_unknown_flags)
  sys.stdout = sys.__stdout__

  for key, val in extra_arguments.items():
    if key == 'config':  # Argparse deals with this one
      continue
    if key not in vars(config_obj):
      err_str = (
        f"The input parameter '{key}' isn't allowed. It's only possible "
        "to overwrite attributes that exist in the active config class")
      raise NotImplementedError(err_str)
    setattr(config_obj, key, val)

  return config_obj


def config_class(func):
  class_name = func.__name__
  module_name = sys.modules[__name__]

  # Makes sure that nothing fishy is going on...
  err_msg = (f"Can't decorate '{class_name}' of type {type(func)}. "
             "Can only be used for classes")
  assert inspect.isclass(func), err_msg

  err_msg = (
    f"The config class '{class_name}' has already been registered. "
    "Duplicated names aren't allowed. Either change the name or avoid "
    "importing the duplicated classes at the same time. "
    f"The registered classes are '{registered_config_classes}'")
  assert class_name not in registered_config_classes, err_msg

  # Config class functions
  members = inspect.getmembers(func, inspect.isfunction)
  members = {name: function for name, function in members}

  # Transfers functions from MasterConfig to config class
  for name, member in inspect.getmembers(MasterConfig, inspect.isfunction):
    if name not in members:  # Only transfer not implemented functions
      setattr(func, name, member)

  # Manually add attributes to config class
  setattr(func, "_frozen", False)
  setattr(func, "config_class", func.__name__)

  registered_config_classes[class_name] = func
  return func


def print_source(func):
  class_name = func.__name__
  err_msg = (f"Can't decorate '{class_name}' of type {type(func)}. "
             "Can only be used for classes")

  assert inspect.isclass(func), err_msg

  def __print_source__(self):
    ''' Get my source. Get my childrens sources '''

    # Newline makes indention better
    src = '\n' + inspect.getsource(self.__class__)

    unique_classes = {v.__class__: v for k, v in vars(self).items()}
    for key, val in unique_classes.items():
      if hasattr(val, '__anyfig_print_source__'):
        src += __print_source__(val)

    # TODO: Source code can have different indention than \t
    # Make it a config to anyfig? Check the first indention and add that
    # Adds indention
    src = src.replace('\n', '\n  ')
    return src

  setattr(func, '__anyfig_print_source__', __print_source__)
  return func