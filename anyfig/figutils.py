import inspect
import pickle
from pathlib import Path

registered_config_classes = {}
global_configs = {}


def get_website():
  return 'https://anyfig.now.sh/'


def register_config_class(class_name, class_def):
  ''' Saves the config class name and definition '''
  err_msg = (
    f"The config class '{class_name}' has already been registered. Duplicated names aren't allowed. "
    "Either change the name or avoid importing the duplicated classes at the same time. "
    f"The registered classes are '{registered_config_classes}'")
  assert class_name not in registered_config_classes, err_msg

  registered_config_classes[class_name] = class_def


def get_config_classes(class_name=None):
  if class_name:
    return registered_config_classes[class_name]
  return registered_config_classes


def is_config_class(obj):
  ''' Returns True if the config class definition is registered with anyfig '''
  if obj.__class__ != type.__class__:
    obj = type(obj)
  return inspect.isclass(obj) and obj.__name__ in registered_config_classes


def register_globally(config):
  ''' Registers the config with anyfig to be accessible anywhere '''
  assert is_config_class(config), "Can only register anyfig config object"
  global_configs[type(config).__name__] = config


def cfg():
  ''' Returns the config object that is registed with anyfig '''

  # Normal case
  if len(global_configs) == 1:
    return next(iter(global_configs.values()))

  # init_config function adds one so this should never happen
  elif len(global_configs) == 0:
    raise RuntimeError("No global config has been registered")

  # If multiple config objects has been marked as global
  raise RuntimeError(
    "Multiple config objects aren't supported. Create an issue if this is something you want to see"
  )


def load_config(path):
  path = Path(path)
  with open(path, 'rb') as f:
    obj = pickle.load(f)

  assert is_config_class(type(obj)), 'Can only load anyfig config objects'
  return obj


def save_config(obj, path):
  path = Path(path)
  err_msg = f"Can only save anyfig config objects, not {type(obj)}"
  assert is_config_class(type(obj)), err_msg
  with open(path, 'wb') as f:
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

  with open(path.with_suffix('.txt'), 'w') as f:
    f.write(str(obj))


def find_arguments(callable_):
  ''' Returns the arguments and required arguments for a function/class'''
  parameters = dict(inspect.signature(callable_).parameters)
  # Remove self argument
  parameters.pop('self', None)

  required_args = [
    name for name, param in parameters.items()
    if param.default == inspect.Parameter.empty
  ]
  return list(parameters), required_args
