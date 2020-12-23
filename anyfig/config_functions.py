import inspect
from abc import ABC
from dataclasses import FrozenInstanceError
from copy import deepcopy
from collections.abc import Mapping

from . import print_utils
from .fields import InterfaceField
from . import figutils


# Class which is used to define functions that goes into every config class
class MasterConfig(ABC):
  def __init__(self):
    pass  # Add empty init if config doesn't have one

  def allowed_cli_args(self):
    ''' Returns the attribute names that can be be overwritten from command line input '''
    return self.get_parameters()

  def post_init(self):
    ''' A function that is called after overwriting from command line input '''
    pass

  def cli_help(self):
    return print_utils.cli_help(self)

  def frozen(self, freeze=True):
    ''' Freeze/unfreeze config '''
    self._frozen = freeze
    for _, val in self.get_parameters(copy=False).items():
      if figutils.is_config_class(val):
        val.frozen(freeze)
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
    lines = [f'{type(self).__name__}:']

    for key, val in self.get_parameters(copy=False).items():
      val_str = str(val)
      if figutils.is_config_class(val):  # Remove class name info
        val_str = val_str.replace(f'{type(val).__name__}:', '')
      lines += f'{key} ({type(val).__name__}): {val_str}'.split('\n')

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

  def build(self, external_args=None):
    ''' Instantiates target object connected to config class '''
    if external_args is None:
      external_args = dict()

    config_name = type(self).__name__
    assert self._build_target is not None, f"Config class '{config_name}' isn't connected to a target"
    err_msg = f"Expected 'external_args' to be dict like object, was type '{type(external_args)}'"
    assert isinstance(external_args, Mapping), err_msg

    config_attrs = self.get_parameters()
    common_keys = set(config_attrs).intersection(set(external_args))
    err_msg = f"Arguments '{', '.join(common_keys)}' aren't allowed as they are already defined in '{config_name}'"
    assert common_keys == set(), err_msg

    build_args = {**external_args, **config_attrs}
    err_msg_base = f'when building {self._build_target} for config {config_name}'

    target = self._build_target
    # If target is a class and not implemented in C-code
    if inspect.isclass(target) and target.__init__ != object.__init__:
      target = target.__init__

    # Validate inspected arguments
    try:
      all_args, required_args = figutils.find_arguments(target)
      err_msg = f"Unexpected arguments {set(build_args) - set(all_args)} {err_msg_base}"
      assert set(build_args) <= set(all_args), err_msg
      err_msg = f"Missing required arguments {set(required_args) - set(build_args)} {err_msg_base}"
      assert set(required_args) <= set(build_args), err_msg

    # C-code (CPython) can't be inspected so arguments can't be validated
    except ValueError:
      try:
        return self._build_target(**build_args)
      except Exception as e:
        # Add to error message if instantiation didn't succeed
        raise type(e)(f"{e} {err_msg_base}") from None

    return self._build_target(**build_args)
