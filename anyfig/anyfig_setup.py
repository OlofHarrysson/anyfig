from io import StringIO
import fire
import inspect
import sys
from collections import Mapping
from dataclasses import dataclass
from functools import wraps

from . import figutils
from .config_functions import MasterConfig
from . import fields


def init_config(default_config, cli_args=None):
  assert default_config is not None
  err_msg = (
    "Expected 'default_config' to be a class definition but most likely got an object. E.g. expected ConfigClass but "
    "got ConfigClass() with parentheses.")
  assert default_config.__class__ == type.__class__, err_msg
  err_msg = f"Expected 'default_config' to be an anyfig config class, was {default_config}"
  assert figutils.is_config_class(default_config), err_msg
  if cli_args is not None:
    err_msg = f"Expected 'cli_args' to be a dict like object, was {type(cli_args)}"
    assert isinstance(cli_args, Mapping), err_msg

  # Parse command line arguments
  if cli_args is None:
    cli_args = parse_cli_args()

  # Create config
  config_str = cli_args.pop('config', default_config.__name__)
  config = create_config(config_str)

  # Print config help
  if 'help' in cli_args:
    config_classes = list(figutils.get_config_classes())
    print(
      f"Available config classes {config_classes}. Set config with --config=OtherConfigClass\n",
      f"\nCurrent config is '{config_str}'. The available input arguments are",
    )

    help_string = config.comments_string()
    print(help_string)
    sys.exit(0)

  # Overwrite parameters via optional input flags
  config = overwrite(config, cli_args)

  # Resolve required values
  fields.resolve_fields(config)

  # Freezes config
  config.frozen(freeze=True)

  # Registers config with anyfig
  figutils.register_globally(config)
  return config


def parse_cli_args():
  ''' Parses input arguments '''
  class NullIO(StringIO):
    def write(self, txt):
      pass

  sys.stdout = NullIO()
  args = fire.Fire(lambda **kwargs: kwargs)
  sys.stdout = sys.__stdout__
  return args


def create_config(config_str):
  ''' Instantiates a config class object '''

  registered_configs = figutils.get_config_classes()
  if config_str not in registered_configs:
    err_msg = (
      f"Config class '{config_str}' wasn't found. Feel free to create it as a new config class "
      f"or use one of the existing ones {list(registered_configs)}")
    raise KeyError(err_msg)

  class_def = registered_configs[config_str]
  _, required_args = figutils.find_arguments(class_def.__init__)

  # Required arguments aren't allowed
  err_msg = (
    f"Can't create config class '{class_def.__name__}'. Config classes created by the 'anyfig.init_config' "
    f"function or through the command line can't contain required constructor arguments. "
    f"'{class_def.__name__}' has the required arguments '{', '.join(required_args)}'"
  )
  assert len(required_args) == 0, err_msg

  return class_def()


def overwrite(main_config_obj, args):
  ''' Overwrites parameters with input flags '''

  # Sort on nested level to override shallow items first
  args = dict(sorted(args.items(), key=lambda item: item[0].count('.')))
  for argument_key, val in args.items():
    # Seperate nested keys into outer and inner
    outer_keys = argument_key.split('.')
    inner_key = outer_keys.pop(-1)
    base_err_msg = f"Can't set '{argument_key} = {val}'"

    # Check that the nested config has the attribute and is a config class
    config_obj = main_config_obj
    for key_part in outer_keys:
      err_msg = f"{base_err_msg}. '{key_part}' isn't an attribute in '{type(config_obj).__name__}'"
      assert hasattr(config_obj, key_part), err_msg

      config_obj = getattr(config_obj, key_part)
      err_msg = f"{base_err_msg}. '{'.'.join(outer_keys)}' isn't a registered Anyfig config class"
      assert figutils.is_config_class(config_obj), err_msg

    # Error if trying to set unknown attribute key
    err_msg = f"{base_err_msg}. '{inner_key}' isn't an attribute in '{type(config_obj).__name__}'"
    assert inner_key in vars(config_obj), err_msg

    # Class definition
    value_class = type(getattr(config_obj, inner_key))

    # Create new anyfig class object
    if figutils.is_config_class(value_class):
      value_obj = create_config(val)

    # Create new object of previous value type with new value
    else:
      try:
        if isinstance(val, dict):  # Keyword specified cli-arguments
          value_obj = value_class(**val)
        else:
          value_obj = value_class(val)

      except Exception as e:
        err_msg = (
          f"Input argument '{argument_key}' with value {val} can't create an object of the expected type "
          f"{value_class}. {e}")
        raise RuntimeError(err_msg) from None

    # Overwrite old value
    setattr(config_obj, inner_key, value_obj)

  return main_config_obj


def config_class(cls=None, *, target=None):
  ''' Adds Anyfig functionality to the class and registers it to known config classes '''
  def wrap(cls):
    class_name = cls.__name__

    # Makes sure that nothing fishy is going on...
    err_msg = f"Can't decorate '{class_name}' of type {type(cls)}. Can only be used for classes"
    assert inspect.isclass(cls), err_msg
    if target is not None:
      err_msg = f"Expected target to be callable, was {type(target)}"
      assert callable(target), err_msg

      # err_msg = f"Expected target to be a class, was {type(target)}"
      # assert inspect.isclass(target), err_msg

    # Config class methods
    functions = inspect.getmembers(cls, inspect.isfunction)
    functions = {name: function for name, function in functions}

    # Transfers functions from MasterConfig to config class
    for name, function in inspect.getmembers(MasterConfig, inspect.isfunction):
      if name not in functions:  # Only transfer not implemented functions
        setattr(cls, name, function)

    # Wrap init function to add attributes
    def init_wrapper(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        self = args[0]
        self._frozen = False
        self._build_target = target
        func(*args, **kwargs)

      return wrapper

    cls.__init__ = init_wrapper(functions['__init__'])

    figutils.register_config_class(class_name, cls)
    return dataclass(cls)

  # Called as @config_class() or @config_class(target=...).
  if cls is None or target is not None:
    return wrap

  # Called as @config_class without parentheses
  return wrap(dataclass(cls))
