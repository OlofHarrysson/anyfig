from abc import ABC
from collections import Iterable
import inspect
from dataclasses import FrozenInstanceError
import pickle
from pathlib import Path
import copy
from typeguard import check_type
import typing
import functools

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


def line_print(code_lines, attribute_row_index):
  comment_lines = []
  attribute_line = code_lines[attribute_row_index]

  multiline_commet = False
  add_comment = lambda row_c: comment_lines.insert(0, row_c)

  for row_index in range(attribute_row_index, 0, -1):
    row_code = code_lines[row_index]
    row_code = row_code.strip(' ')

    # Break at blank line above attribute line
    if row_code.isspace() and not multiline_commet:
      break

    # Break if we reach another attribute
    if row_code.startswith('self.') and row_index != attribute_row_index:
      break

    # Hashtag # comment
    if row_code.startswith('#'):
      add_comment(row_code)

    # Starts with ''' or """
    if multiline_commet and (row_code.startswith("'''")
                             or row_code.startswith('"""')):
      add_comment(row_code)
      break

    # Line between ''' or """
    if multiline_commet:
      add_comment(row_code)

    # Ends with ''' or """
    if row_code.rstrip().endswith("'''") or row_code.rstrip().endswith('"""'):
      add_comment(row_code)
      multiline_commet = True

  comment_string = ''.join(comment_lines)
  comment_string = comment_string.strip("# \n'\"")
  return comment_string


def _print_help(class_type):
  comments = {}
  parents = class_type.__bases__

  # Find comments for parents, skip Python built in code
  for parent in parents:
    if parent.__module__ == 'builtins':
      continue
    parent_comments = _print_help(parent)
    comments.update(parent_comments)

  # Find attribute name and matching comment
  code_lines, _ = inspect.getsourcelines(class_type)
  for row_index, code_line in enumerate(code_lines):
    if code_line.lstrip().startswith('self.'):
      # Extract attribute name
      attribute_name = code_line.split('=')[0]
      attribute_name = attribute_name.strip().replace('self.', '', 1)

      comment = line_print(code_lines, row_index)

      # Override parent comment
      if comment or attribute_name not in comments:
        comments[attribute_name] = comment

  return comments


# Class which is used to define functions that goes into every config class
class MasterConfig(ABC):
  def print_help(self):
    # TODO: Should print --data.value for nested config classes
    comments = self.nested_print_help()

    # Print the config help
    help_strings = []
    for attribute_name, comment in comments.items():
      nested_indent_width = 4
      nested_level = attribute_name.count('.')
      nested_indent = ' ' * (nested_indent_width * nested_level)
      attribute_names = attribute_name.split('.')

      attribute_value = functools.reduce(getattr, attribute_names, self)

      attribute_type = attribute_value.__class__.__name__
      name_str = f"{nested_indent}--{attribute_name} ({attribute_type}):"

      width_multiple = 4  # In spaces
      n_spaces = len(name_str) + width_multiple
      n_spaces = width_multiple * round(n_spaces / width_multiple)

      # Add extra spacing for short variable names
      comment_indent = width_multiple * 8
      if n_spaces < comment_indent:
        n_spaces = comment_indent

      comment = (' ' * n_spaces).join(comment.splitlines(True)).rstrip('\n')
      hh = f"{name_str}{' ' * (n_spaces - len(name_str))}{comment}"
      help_strings.append(hh)
    return '\n'.join(help_strings)

  def nested_print_help(self):
    # NEEEESTEEEEEEEEEED
    # NEEEESTEEEEEEEEEED
    # NEEEESTEEEEEEEEEED
    # NEEEESTEEEEEEEEEED
    # NEEEESTEEEEEEEEEED
    config_class = self.__class__
    comments = _print_help(config_class)
    main_nested_comments = {}

    config_classes = get_registered_config_classes().values()
    for attribute_name, comment in comments.items():
      main_nested_comments[attribute_name] = comment

      attribute_value = getattr(self, attribute_name)
      attribute_class = attribute_value.__class__
      if attribute_class in config_classes:
        nested_comments = attribute_value.nested_print_help()
        for inner_attribute_name, inner_comment in nested_comments.items():
          nested_name = f'{attribute_name}.{inner_attribute_name}'
          main_nested_comments[nested_name] = inner_comment

    return main_nested_comments

  def frozen(self, freeze=True):
    ''' Freeze/unfreeze config '''
    self.__class__._frozen = freeze
    return self

  def get_parameters(self):
    return copy.deepcopy(vars(self))

  def __str__(self):
    ''' Prettyprints the config '''
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
    if isinstance(old_value, FigValue):
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


class FigValue():
  # Used to bind type information (and other?) to data
  # TODO: Write proper doc
  def __init__(self, type_pattern=typing.Any, tests=None):
    err_msg = f"Expected 'type_pattern' to be a type or a typing pattern but got {type(type_pattern)}"
    assert issubclass(type(type_pattern), type.__class__) or issubclass(
      type(type_pattern), typing._Final), err_msg

    self.type_pattern = type_pattern
    self.wrapping_phase = True

    if not isinstance(tests, Iterable):
      self.tests = [tests]
    else:
      self.tests = tests

  def update_value(self, name, value, config_class):
    # Updates value and return wrapped value or value if setup is finished
    if self.type_pattern:
      check_type(name, value, self.type_pattern)

    for test in self.tests:
      if test != None:
        self._check_test(test, name, value, config_class)

    self.value = value
    if self.wrapping_phase:
      return self
    return value

  def finish_wrapping_phase(self, name, config_class):
    # Validates value and finishes setup
    err_msg = f"Attribute '{name}' in '{config_class}' is required to be overridden"
    assert hasattr(self, 'value'), err_msg

    self.wrapping_phase = False
    return self.value

  def _check_test(self, test, name, value, config_class):
    # Raises error if test fails
    test_file = Path(inspect.getsourcefile(test)).absolute()
    line_number = inspect.getsourcelines(test)[-1]

    base_err_msg = f"Can't set '{name} = {value}' for config '{config_class}'. Its test defined in '{test_file}' at line {line_number}"
    try:
      test_passed = test(value)
    except Exception as e:
      test_passed = False

      # Create same exception as was raised
      exception_class = type(e)
      err_msg = f"{base_err_msg} raised the exception: \n{str(e)}"
      raise exception_class(err_msg) from None

    assert test(value), f"{base_err_msg} didn't pass"


def resolve(config):
  # TODO: Better name and doc. Resolve the inteface values
  for key, val in vars(config).items():
    if isinstance(val, FigValue):
      config_class = type(config).__name__
      value = val.finish_wrapping_phase(key, config_class)
      setattr(config, key, value)

    # Resolve nested configs
    if is_config_class(val):
      resolve(val)
