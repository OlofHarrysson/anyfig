__author__ = """Olof Harrysson"""
__email__ = 'harrysson.olof@gmail.com'
__version__ = '0.2.0'

import sys
from functools import wraps
from anyfig.figutils import *
from anyfig.anyfig_setup import *

# Some features are only supported in Python 3.7+
python_v = sys.version_info
if python_v.major >= 3 and python_v.minor >= 7:
  from anyfig.fields import *
else:
  from anyfig.dummyfields import *


def get_global_cfg(func):
  ''' Decorator for GlobalConfig methods. Saves the config if it's not already saved '''
  @wraps(func)
  def wrapper(*args, **kwargs):
    self = args[0]
    if self.global_cfg is None:
      self.global_cfg = get_config()
    return func(*args, **kwargs)

  return wrapper


class GlobalConfig:
  global_cfg = None

  @get_global_cfg
  def __getattr__(self, name):
    return getattr(self.global_cfg, name)

  @get_global_cfg
  def __str__(self):
    return str(self.global_cfg)


global_cfg = GlobalConfig()
