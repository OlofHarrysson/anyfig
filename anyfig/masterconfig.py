from abc import ABC
import pprint
import inspect
from dataclasses import FrozenInstanceError
import pickle
from pathlib import Path
import copy


def is_anyfig_class(obj):
  return inspect.isclass(obj) and issubclass(obj, MasterConfig)


def load_config(path):
  path = Path(path)
  with open(path, 'rb') as f:
    obj = pickle.load(f)

  assert is_anyfig_class(type(obj)), 'Can only load anyfig config objects'
  return obj


def save_config(obj, path):
  path = Path(path)
  err_msg = f"Can only save anyfig config objects, not {type(obj)}"
  assert is_anyfig_class(type(obj)), err_msg
  with open(path, 'wb') as f:
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

  with open(path.with_suffix('.txt'), 'w') as f:
    f.write(str(obj))


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
      else:
        s = pprint.pformat({key: val})

        # Prettyprint adds some extra wings that I dont like
        s = s.lstrip('{').rstrip('}').replace('\n ', '\n')
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