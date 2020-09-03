import sys
from . import figutils
''' This file is used to offer partial Anyfig support for lower Python versions'''


def raise_error():
  err_msg = f"This feature isn't supported in Python {sys.version_info.major}.{sys.version_info.minor}. See our website '{figutils.get_website()}' for more information"
  raise RuntimeError(err_msg)


def field(*args, **kwargs):
  raise_error()


def constant(value, strict=False):
  raise_error()


def cli_input(type_pattern):
  raise_error()
