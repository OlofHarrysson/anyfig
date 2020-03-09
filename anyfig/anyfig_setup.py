from io import StringIO
import fire
import inspect
import argparse
import sys
from . import figutils


def setup_config(default_config=None):
  config_str = parse_args(default_config.__name__)
  config = choose_config(config_str)
  figutils.set_global(config)
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
  if config_str is None:
    raise RuntimeError(err_msg)

  err_msg = ("There aren't any registered config classes. Decorate a class "
             "with '@anyfig.config_class' and make sure that the class is "
             "imported to the file where the function 'anyfig.setup_config' "
             "is called from")
  registered_configs = figutils.get_registered_config_classes()
  assert len(registered_configs), err_msg

  try:
    config_class_definition = registered_configs[config_str]
    config_obj = config_class_definition()
  except KeyError as e:
    err_msg = (
      f"Config class '{config_str}' wasn't found. Feel free to create "
      "it as a new config class or use one of the existing ones "
      f"{list(registered_configs)}")
    raise KeyError(err_msg) from e

  # Overwrite parameters via optional input flags
  config_obj = overwrite(config_obj)

  # Freezes config
  config_obj.frozen(freeze=True)
  return config_obj


def overwrite(main_config_obj):
  ''' Overwrites parameters with input flags. Function is needed for the
  convenience of specifying parameters via a combination of the config classes
  and input flags. '''
  class NullIO(StringIO):
    def write(self, txt):
      pass

  sys.stdout = NullIO()
  extra_arguments = fire.Fire(lambda **kwargs: kwargs)
  sys.stdout = sys.__stdout__

  for argument_key, val in extra_arguments.items():
    if argument_key == 'config':  # Argparse deals with this one
      continue

    # Seperate nested keys into outer and inner
    outer_keys = argument_key.split('.')
    inner_key = outer_keys.pop(-1)

    # Get the innermost config object
    config_obj = main_config_obj
    for key_part in outer_keys:
      err_msg = f"Error when trying to set '{argument_key}={val}'. '{key_part}' isn't an attribute in '{type(config_obj).__name__}'"
      assert hasattr(config_obj, key_part), err_msg
      config_obj = getattr(config_obj, key_part)
      err_msg = f"Tried to set '{argument_key}' but '{'.'.join(outer_keys)}' wasn't an anyfig class"
      assert figutils.is_config_class(config_obj), err_msg

    # Error if trying to set unknown attribute key
    if inner_key not in vars(config_obj):
      err_msg = (
        f"The input parameter '{argument_key}' isn't allowed. It's only possible "
        "to overwrite attributes that exist in the active config class")
      raise NotImplementedError(err_msg)

    # Create object with new value
    value_class = type(getattr(config_obj, inner_key))
    try:
      value_obj = value_class(val)
    except Exception:
      err_msg = f"Input argument '{argument_key}' with value {val} can't create an object of the expected type {value_class}"
      raise RuntimeError(err_msg)

    # Overwrite old value
    setattr(config_obj, inner_key, value_obj)

  return main_config_obj


def config_class(func):
  class_name = func.__name__

  # Makes sure that nothing fishy is going on...
  err_msg = (f"Can't decorate '{class_name}' of type {type(func)}. "
             "Can only be used for classes")
  assert inspect.isclass(func), err_msg

  # Config class functions
  members = inspect.getmembers(func, inspect.isfunction)
  members = {name: function for name, function in members}

  # Transfers functions from MasterConfig to config class
  for name, member in inspect.getmembers(figutils.MasterConfig,
                                         inspect.isfunction):
    if name not in members:  # Only transfer not implemented functions
      setattr(func, name, member)

  # Manually add attributes to config class
  setattr(func, '_frozen', False)

  # TODO: Is this needed? Maybe if we want to print the name of the print(config)
  # setattr(func, '_config_class', class_name)

  figutils.register_config_class(class_name, func)
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
