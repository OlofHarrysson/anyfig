import anyfig
# from anyfig import input_argument as inp_arg
from pathlib import Path
import time

# Problem is that I have to record the arguments that are allowed but I also need to know the parent-config so I can remove the key from the help-print. Or.... set an attribute in each config that says to print-utils "get these values".
# What about input-args. Before setting the attribute, check if it's "allowed?" They must then all default to True, but when I set the first one to False, they will all change to False????
# No action - All cli allowed
# Mark one or more as allowed, they are the ONLY allowed
# Init as None?


class CleanSetAttrMeta(type):
  def setattr_overwrite(self, name, value):
    # print(name, value)
    # print(vars(self))
    # fix the metaclass so that behaves normally. Cant find the config now
    self.config.__setattr__(name, value)
    self.config.record_shit_dict[name] = self.allowed

  def __call__(cls, *args, **kwargs):
    # real_setattr = cls.__setattr__
    # cls.__setattr__ = object.__setattr__
    # cls.__setattr__ =
    self = super(CleanSetAttrMeta, cls).__call__(*args, **kwargs)
    cls.__setattr__ = cls.setattr_overwrite
    return self


class Context(metaclass=CleanSetAttrMeta):
  # __initialized = False

  def __init__(self, config, allowed):
    # TODO: Assert config class
    self.config = config
    self.allowed = allowed
    self.__initialized = True
    print("INITITIITIT", self.__initialized)
    # this aint false the second time around

  def __enter__(self):
    print("ENTERING")
    # self.config.record_shit = True  # TOOD: Set it to False in config init
    return self

  def __exit__(self, *exc):
    # self.config.record_shit = False  # TODO: Might have to return to the state it was on enter
    # self.config = None
    print("EXIIITING")
    return False

  # def __setattr__(self, name, value):
  #   if self.__initialized:
  #     # TODO: self.allowed goes here...
  #     self.config.__setattr__(name, value)
  #     self.config.record_shit_dict[name] = self.allowed
  #     print("ALLOWED", self.allowed)
  #   else:
  #     super().__setattr__(name, value)


@anyfig.config_class  # Registers the class with anyfig
class MyConfig:
  def __init__(self):
    # Note help
    self.experiment_note = 'Changed stuff'
    # Start help
    self.start_time = time.time()

    # The inner config obj
    self.innerfig = InnerConfig()

    # self.save_directory = anyfig.field(Path)
    # self.save_directory = anyfig.input_argument(type=str, help=)
    # self.save_directory = Path('output')
    # self.save_directory = 'hej'

    # with anyfig.input_argument(allowed='required') as rr:
    #   self.save_directory = anyfig.input_argument(type=str, help='asd')

    # with Context(self, allowed=True) as cfg:
    # with Context(self, allowed=False) as cfg:
    # with Context(self, allowed=True) as cfg:
    #   pass
    #   cfg.save = 'nested_two'

    # pass
    # print(self.record_shit)
    # Save help
    # cfg.save = 'nested_one'
    # cfg.save = anyfig.field(Path)

    # print(self)
    # print(self.record_shit)
    # print(self.record_shit_dict)
    # qweewewe
    self.save = 'hej'

  # def allowed_cli_args(self):
  #   # TODO: Second function to check that all the configs actually exist
  #   allowed = self.get_parameters()
  #   allowed.pop('save')
  #   return ['save1']
  #   return allowed


@anyfig.config_class
class InnerConfig:
  def __init__(self):
    # Note help
    self.inner = 'innner'


config = anyfig.init_config(default_config=MyConfig)
print(config)
