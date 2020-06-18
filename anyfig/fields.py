import inspect
import typing
from typeguard import check_type
from collections.abc import Iterable
from pathlib import Path

from .figutils import is_config_class


def field(*args, **kwargs):
  ''' Returns an InterfaceField '''
  return InterfaceField(*args, **kwargs)


def constant(value, strict=False):
  ''' Returns a ConstantField '''
  return ConstantField(value, strict)


def resolve_fields(config):
  ''' Removes wrapping for InterfaceFields '''
  for key, val in vars(config).items():
    if isinstance(val, InterfaceField):
      config_class = type(config).__name__
      value = val.finish_wrapping_phase(key, config_class)
      setattr(config, key, value)

    # Resolve nested configs
    if is_config_class(val):
      resolve_fields(val)


class InterfaceField():
  ''' Used to define allowed values for a config-attribute '''
  def __init__(self, type_pattern=typing.Any, tests=None):
    err_msg = f"Expected 'type_pattern' to be a type or a typing pattern but got {type(type_pattern)}"
    assert issubclass(type(type_pattern), type.__class__) or issubclass(
      type(type_pattern), typing._Final), err_msg

    self.type_pattern = type_pattern
    self.wrapping_phase = True
    tests = [] if tests is None else tests
    self.tests = tests if isinstance(tests, Iterable) else [tests]

  def update_value(self, name, value, config_class):
    # Updates value and return wrapped value or value if setup is finished
    if self.type_pattern:
      check_type(name, value, self.type_pattern)

    for test in self.tests:
      self._check_test(test, name, value, config_class)

    self.value = value
    return self if self.wrapping_phase else value

  def finish_wrapping_phase(self, name, config_class):
    # Verifies that attribute is overridden and finishes setup
    err_msg = f"Attribute '{name}' in '{config_class}' is required to be overridden"
    assert hasattr(self, 'value'), err_msg

    self.wrapping_phase = False
    return self.value

  def _check_test(self, test, name, value, config_class):
    ''' Calls the test with the new attribute value. Raises error if test doesn't pass '''
    test_file = Path(inspect.getsourcefile(test)).absolute()
    line_number = inspect.getsourcelines(test)[-1]
    base_err_msg = (
      f"Can't set '{name} = {value}' for config '{config_class}'. Its test defined in '{test_file}' "
      f"at line {line_number}")

    try:
      test_result = test(value)
      err_msg = f"Test failed. Expected return type to be boolean but was {type(test_result)}"
      assert test_result in [True, False], err_msg

    except Exception as e:
      exception_class = type(e)  # Create same exception as was raised
      err_msg = f"{base_err_msg} raised the exception: \n{str(e)}"
      raise exception_class(err_msg) from None

    assert test_result, f"{base_err_msg} didn't pass"


class ConstantField(InterfaceField):
  ''' Used to define config-attribute that can't be overriden '''
  def __init__(self, value, strict):
    if strict:
      super().__init__(tests=lambda v: v is value)
    else:
      super().__init__(tests=lambda v: v == value)
    self.value = value

  def _check_test(self, test, name, value, config_class):
    ''' Calls the test with the new attribute value. Raises error if test doesn't pass '''
    err_msg = f"Can't override constant '{name}' with value '{value}' in config '{config_class}'"
    assert test(value), err_msg
