from abc import ABC
import inspect
from dataclasses import FrozenInstanceError
import pickle
from pathlib import Path
import copy
import typing

from . import print_utils
from .interfacefield import InterfaceField

registered_config_classes = {}
global_configs = {}


def register_config_class(class_name, class_def):
  ''' Saves the config class name and definition '''
  err_msg = (
    f"The config class '{class_name}' has already been registered. "
    "Duplicated names aren't allowed. Either change the name or avoid "
    "importing the duplicated classes at the same time. "
    f"The registered classes are '{registered_config_classes}'")
  assert class_name not in registered_config_classes, err_msg

  registered_config_classes[class_name] = class_def


def get_registered_config_classes(class_name=None):
  if class_name:
    return registered_config_classes[class_name]
  return registered_config_classes


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


def is_config_class(obj):
  ''' Returns True if config class definition registered with anyfig '''
  if obj.__class__ != type.__class__:
    obj = type(obj)
  return inspect.isclass(obj) and obj.__name__ in registered_config_classes


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


def resolve_fields(config):
  # TODO: Better name and doc. Resolve the inteface values
  for key, val in vars(config).items():
    if isinstance(val, InterfaceField):
      config_class = type(config).__name__
      value = val.finish_wrapping_phase(key, config_class)
      setattr(config, key, value)

    # Resolve nested configs
    if is_config_class(val):
      resolve_fields(val)


# Class which is used to define functions that goes into every config class
class MasterConfig(ABC):
  def comments_string(self):
    return print_utils.comments_string(self)

  def frozen(self, freeze=True):
    ''' Freeze/unfreeze config '''
    self.__class__._frozen = freeze
    return self

  def get_parameters(self):
    return copy.deepcopy(vars(self))

  def __str__(self):
    return self.pretty()

    # lines = [self.__class__.__name__ + ':']

    # for key, val in vars(self).items():
    #   val_str = str(val)
    #   if is_config_class(val):  # Remove class name info
    #     val_str = val_str.replace(f'{val.__class__.__name__}:', '')
    #   lines += f'{key} ({val.__class__.__name__}): {val_str}'.split('\n')

    # return '\n    '.join(lines) + '\n'

  def pretty(self):
    ''' Pretty string representation of the config '''
    lines = [self.__class__.__name__ + ':']

    for key, val in vars(self).items():
      val_str = str(val)
      if is_config_class(val):  # Remove class name info
        val_str = val_str.replace(f'{val.__class__.__name__}:', '')
      lines += f'{key} ({val.__class__.__name__}): {val_str}'.split('\n')

    return '\n    '.join(lines) + '\n'

  def __setattr__(self, name, value):
    config_class = type(self).__name__

    # Handle interface values
    old_value = getattr(self, name, None)
    if isinstance(old_value, InterfaceField):
      value = old_value.update_value(name, value, config_class)

    # Raise error if frozen unless we're trying to unfreeze the config
    if self._frozen and name != '_frozen':
      err_msg = (f"Cannot set attribute '{name}'. Config object is frozen. "
                 "Unfreeze the config for a mutable config object")
      raise FrozenInstanceError(err_msg)

    # Check for reserved names
    name_taken_msg = f"The attribute '{name}' can't be assigned to config '{config_class}' since it already has a method by that name"
    methods = inspect.getmembers(self, predicate=inspect.ismethod)
    for method in methods:
      assert name != method[0], name_taken_msg

    object.__setattr__(self, name, value)
