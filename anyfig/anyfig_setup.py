from io import StringIO
import fire
import inspect
import sys
from . import figutils


def setup_config(default_config):
  assert default_config is not None
  err_msg = "Expected default config to be a class definition but most likely got an object. E.g. expected ConfigClass but got ConfigClass() with parentheses."
  assert default_config.__class__ == type.__class__, err_msg
  err_msg = f"Expected default config to be an anyfig config class, was {default_config}"
  assert figutils.is_config_class(default_config), err_msg

  # Parse args and create config
  args = parse_args()
  config_str = default_config.__name__
  if 'config' in args:
    config_str = args.pop('config')
  config = create_config(config_str)

  # Print config help
  if 'help' in args:
    config_classes = list(figutils.get_registered_config_classes())
    print(f"Available config classes {config_classes}",
          "\nSet config with --config=OtherConfigClass\n")

    print("Current config")
    print(config)
    sys.exit(0)

  # Overwrite parameters via optional input flags
  config = overwrite(config, args)

  # Freezes config
  config.frozen(freeze=True)

  # Registers config with anyfig
  figutils.register_globally(config)
  return config


def parse_args():
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

  return config_obj


def overwrite(main_config_obj, args):
  ''' Overwrites parameters with input flags. Function is needed for the
  convenience of specifying parameters via a combination of the config classes
  and input flags. '''

  config_classes = figutils.get_registered_config_classes()

  for argument_key, val in args.items():
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

    # Class definition
    value_class = type(getattr(config_obj, inner_key))

    # Create new anyfig class object
    if figutils.is_config_class(value_class):
      value_class = config_classes[val]
      value_obj = value_class()

    # Create new object of previous value type with new value
    else:
      try:
        value_obj = value_class(val)
      except Exception:
        err_msg = f"Input argument '{argument_key}' with value {val} can't create an object of the expected type {value_class}"
        raise RuntimeError(err_msg)

    # Overwrite old value
    setattr(config_obj, inner_key, value_obj)

  return main_config_obj


def config_class(class_def):
  class_name = class_def.__name__

  # Makes sure that nothing fishy is going on...
  err_msg = (f"Can't decorate '{class_name}' of type {type(class_def)}. "
             "Can only be used for classes")
  assert inspect.isclass(class_def), err_msg

  # Config class functions
  functions = inspect.getmembers(class_def, inspect.isfunction)
  functions = {name: function for name, function in functions}

  # Transfers functions from MasterConfig to config class
  for name, function in inspect.getmembers(figutils.MasterConfig,
                                           inspect.isfunction):
    if name not in functions:  # Only transfer not implemented functions
      setattr(class_def, name, function)

  # Manually add attributes to config class
  setattr(class_def, '_frozen', False)

  figutils.register_config_class(class_name, class_def)
  return class_def
