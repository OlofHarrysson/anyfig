from abc import ABC
import inspect
from dataclasses import FrozenInstanceError
from copy import deepcopy

from . import print_utils
from .fields import InterfaceField
from .figutils import is_config_class


# Class which is used to define functions that goes into every config class
class MasterConfig(ABC):
  def comments_string(self):
    ''' Returns string for config class's attributes and comments '''
    return print_utils.comments_string(self)

  def frozen(self, freeze=True):
    ''' Freeze/unfreeze config '''
    self.__class__._frozen = freeze
    return self

  def get_parameters(self, copy=True):
    ''' Returns the config attributes. Doesn't include Anyfig built-ins '''
    builtins = ['_frozen', '_build_target']
    params = {k: v for k, v in vars(self).items() if k not in builtins}
    if copy:
      return deepcopy(params)
    return params

  def __str__(self):
    return self.pretty()

  def pretty(self):
    ''' Pretty string representation of the config '''
    lines = [f'{self.__class__.__name__}:']

    for key, val in self.get_parameters(copy=False).items():
      val_str = str(val)
      if is_config_class(val):  # Remove class name info
        val_str = val_str.replace(f'{val.__class__.__name__}:', '')
      lines += f'{key} ({val.__class__.__name__}): {val_str}'.split('\n')

    return '\n    '.join(lines)

  def __setattr__(self, name, value):
    config_class = type(self).__name__

    # Handle interface values
    old_value = getattr(self, name, None)
    if isinstance(old_value, InterfaceField):
      value = old_value.update_value(name, value, config_class)

    # Raise error if frozen unless we're trying to unfreeze the config
    if hasattr(self, '_frozen') and self._frozen and name != '_frozen':
      err_msg = f"Can't set attribute '{name}'. Config object is frozen. Unfreeze the config to make it mutable"
      raise FrozenInstanceError(err_msg)

    # Check for reserved names
    name_taken_msg = (
      f"The attribute '{name}' can't be assigned to config '{config_class}' since it already has a method by that name"
    )
    methods = inspect.getmembers(self, predicate=inspect.ismethod)
    for method in methods:
      assert name != method[0], name_taken_msg

    object.__setattr__(self, name, value)

  def build(self, external_args):
    ''' Instantiates target object connected to config class '''
    config_attrs = vars(self)
    common_keys = set(config_attrs).intersection(set(external_args))
    err_msg = f"Arguments '{', '.join(common_keys)}' aren't allowed as they are already defined in the config class"
    assert common_keys == set(), err_msg
    assert self._build_target is not None, f"Config class '{type(self).__name__}' isn't connected to a target"

    class_args = inspect.getfullargspec(self._build_target)
    expected_args = class_args.args[1:]  # Remove self arg
    build_args = {**external_args, **config_attrs}
    err_msg_base = f'when instantiating {self._build_target}'

    err_msg = f"Unexpected arguments {set(build_args) - set(expected_args)} {err_msg_base}"
    assert set(build_args) <= set(expected_args), err_msg
    required_args = expected_args[:-len(class_args.defaults)]

    err_msg = f"Missing required arguments {set(required_args) - set(build_args)} {err_msg_base}"
    assert set(required_args) <= set(build_args), err_msg
    return self._build_target(**build_args)
