from abc import ABC
import pprint
import inspect
from dataclasses import FrozenInstanceError
import pickle
from pathlib import Path
import copy

registered_config_classes = {}
global_configs = {}


def set_global(config):
  assert is_config_class(config), "Can only register anyfig config object"
  global_configs[type(config).__name__] = config


def cfg():
  ''' Returns the config object that is registed with anyfig '''

  # Normal case
  if len(global_configs) == 1:
    return next(iter(global_configs.values()))

  # setup_config function adds one so this should never happen
  elif len(global_configs) == 0:
    raise RuntimeError("No global config has been registered")

  # If multiple config objects has been marked as global
  raise RuntimeError(
    "Multiple config objects aren't supported. Create an issue if this is something you want to see"
  )


def is_config_class(obj):
  ''' Returns True if object is a config class that is registered with anyfig '''
  return inspect.isclass(
    type(obj)) and type(obj).__name__ in registered_config_classes


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


def register_config_class(class_name, class_def):
  err_msg = (
    f"The config class '{class_name}' has already been registered. "
    "Duplicated names aren't allowed. Either change the name or avoid "
    "importing the duplicated classes at the same time. "
    f"The registered classes are '{registered_config_classes}'")
  assert class_name not in registered_config_classes, err_msg

  registered_config_classes[class_name] = class_def


def get_registered_config_classes():
  return registered_config_classes


class MasterConfig(ABC):
  def frozen(self, freeze=True):
    self._frozen = freeze
    return self

  def get_parameters(self):
    params = copy.deepcopy(self.__dict__)
    params.pop('_frozen')
    return params

  def __str__(self):
    str_ = ""
    params = vars(self)
    for key, val in params.items():
      if key == '_frozen':  # Dont print frozen
        continue
      if hasattr(val, '__anyfig_print_source__'):
        cls_str = val.__anyfig_print_source__()
        s = f"'{key}':\n{cls_str}"

      # Recursively print anyfig classes
      elif is_config_class(val):
        inner_config_string = '\n' + str(val)
        inner_config_string = inner_config_string.replace('\n', '\n\t')
        s = f"'{key}':{inner_config_string}"

      else:
        s = pprint.pformat({key: str(val)})
        # Prettyprint adds some extra wings that I dont like
        s = s.lstrip('{').rstrip('}')
      str_ += s + '\n'

    return str_

  def __setattr__(self, name, value):
    # Raise error if frozen unless we're trying to unfreeze the config
    if name == '_frozen':
      pass
    elif self._frozen:
      err_msg = (f"Cannot set attribute '{name}'. Config object is frozen. "
                 "Unfreeze the config for a mutable config object")
      raise FrozenInstanceError(err_msg)

    # Check for reserved names
    name_taken_msg = f"The attribute '{name}' can't be assigned to config '{type(self).__name__}' since it already has a method by that name"

    def assert_name(name, method_name):
      assert name != method_name, name_taken_msg

    methods = inspect.getmembers(self, predicate=inspect.ismethod)
    [assert_name(name, m[0]) for m in methods]
    object.__setattr__(self, name, value)
