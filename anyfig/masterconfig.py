from abc import ABC
import pprint
import inspect
from dataclasses import FrozenInstanceError


def load_config(path):
  # TODO: Add checks so that object is config
  print("Loading config")
  with open(path, 'rb') as f:
    return pickle.load(f)


def save_config(config_obj, path):
  # TODO: Add checks so that object is config
  print(f"Saving config @ {path}")
  with open(path, 'wb') as f:
    pickle.dump(config_obj, f, pickle.HIGHEST_PROTOCOL)

  with open(path + '.txt', 'w') as f:
    f.write(str(config_obj))


class MasterConfig(ABC):
  def __init__(self):
    self._frozen: bool = False
    self.config_class = type(self).__name__

  def frozen(self, freeze=True):
    self._frozen = freeze

  def get_parameters(self):
    return self.__dict__

  def __str__(self):
    str_ = ""
    params = vars(self)
    params.pop('_frozen')  # Dont print frozen
    for key, val in params.items():
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
    if hasattr(self, '_frozen'):
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