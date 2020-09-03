import inspect
import dill

from pathlib import Path

registered_config_classes = {}
global_configs = {}


def get_website():
  return 'https://anyfig.now.sh/'


def register_config_class(class_name, class_def):
  ''' Saves the config class name and definition '''
  err_msg = (
    f"The config class '{class_name}' has already been registered. Duplicated names aren't allowed. "
    f"The registered classes are '{registered_config_classes}'")
  assert class_name not in registered_config_classes, err_msg

  registered_config_classes[class_name] = class_def


def unregister_config_classes():
  ''' Unregisteres config classes with anyfig '''
  registered_config_classes.clear()
  global_configs.clear()


def register_globally(config):
  ''' Registers the config with anyfig to be accessible anywhere '''
  assert is_config_class(config), "Can only register anyfig config object"
  global_configs[type(config).__name__] = config


def get_config_classes(class_name=None):
  if class_name:
    return registered_config_classes[class_name]
  return registered_config_classes


def is_config_class(obj):
  ''' Returns True if the config class definition is registered with anyfig '''
  if type(obj) != type(type):
    obj = type(obj)
  return inspect.isclass(obj) and obj.__name__ in registered_config_classes


def get_config():
  ''' Returns the config object that is registered with anyfig '''

  # Normal case
  if len(global_configs) == 1:
    return next(iter(global_configs.values()))

  # init_config function adds one so this should never happen
  elif len(global_configs) == 0:
    raise RuntimeError("No config object has been registered")

  # If multiple config objects has been marked as global
  raise RuntimeError(
    "Multiple config objects aren't supported. Create an issue if this is something you want to see"
  )


def save_config(config, path, save_readable=True):
  ''' Serialize and saves the config. If save_readable is True, a *path*.txt is also created '''
  path = Path(path)
  err_msg = f"Can only save anyfig config objects, not {type(config)}"
  assert is_config_class(config), err_msg
  with open(path, 'wb') as f:
    dill.dump(config, f, dill.HIGHEST_PROTOCOL)

  if save_readable:
    source_codes = list(_get_source(config).values())
    with open(path.with_suffix('.txt'), 'w') as f:
      f.write(str(config))
      f.write('\n\n\n')
      f.write('\n'.join(source_codes))

  return config


def _get_source(config, source_codes=None):
  ''' Retrieves source code for a config object including nested configs '''
  if source_codes is None:
    source_codes = dict()

  config_class = type(config)
  source_codes[config_class.__name__] = inspect.getsource(config_class)

  for _, value in config.get_parameters(copy=False).items():
    if is_config_class(value):
      source_codes = _get_source(value, source_codes)

  return source_codes


def load_config(path):
  ''' Loads the config from file '''
  path = Path(path)
  with open(path, 'rb') as f:
    config = dill.load(f)

  err_msg = f"'{type(config)}' isn't a registered config class. Import the config class's file to register it"
  assert is_config_class(type(config)), err_msg
  return config


def find_arguments(callable_):
  ''' Returns the arguments and required arguments for a function/class'''
  parameters = dict(inspect.signature(callable_).parameters)
  parameters.pop('self', None)  # Remove self argument

  required_args = [
    name for name, param in parameters.items()
    if param.default == inspect.Parameter.empty
  ]
  return list(parameters), required_args


def allowed_input_argument(config_obj, name, deep_name):
  ''' Raises error if the input argument isn't marked as "allowed" '''
  allowed_args = check_allowed_cli_args(config_obj)
  if name not in allowed_args:
    err_msg = f"Input argument '{deep_name}' is not allowed to be overwritten. See --help for more info"
    raise ValueError(err_msg)


def check_allowed_cli_args(config_obj):
  ''' Returns the attribute names that can be be overwritten from command line input.
    Raises AttributeError if an attribute doesn't exist '''
  allowed_items = config_obj.allowed_cli_args()
  attr = config_obj.get_parameters()
  for item in allowed_items:
    if item not in attr:
      err_msg = (
        f"'{type(config_obj).__name__}' has no attribute '{item}' and should not be marked as an allowed command line "
        "input argument")
      raise AttributeError(err_msg)
  return allowed_items
