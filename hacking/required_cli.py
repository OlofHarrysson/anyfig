import anyfig
# from anyfig import input_argument as inp_arg
from pathlib import Path
import time
import typing


@anyfig.config_class  # Registers the class with anyfig
class MyConfig:
  def __init__(self):
    # Note help
    self.experiment_note = 'Changed stuff'
    # Start help
    self.start_time = time.time()

    # The inner config obj
    # self.innerfig = InnerConfig()

    # self.save = anyfig.field(int, lambda x: x > 10)

    # TEST1
    # self.save = anyfig.field(typing.Union[Path, str])

    # self.save = anyfig.constant(12312)

    # self.save = anyfig.field(str)
    # self.save = anyfig.field(str)
    # self.save = 'bajs'

    # self.save = anyfig.cli_input(str)
    # self.save = anyfig.cli_input(int)
    # self.save = anyfig.cli_input(list)
    # self.save = anyfig.cli_input(dict)
    # self.save = anyfig.cli_input(typing.List[int])

    # self.save = 'hej'

    # self.post_init = 'asdas'

  # def allowed_cli_args(self):
  # return ['save', 'asdasd']
  # return ['save', 'innerfig']

  def post_init(self):
    print("POST INIIIIIT")


@anyfig.config_class
class InnerConfig:
  def __init__(self):
    # ''' Hej
    # det går
    # braa'''
    # self.inner = anyfig.cli_input(str)

    # An integer between the values of 1 and 10 because the world has never seen such apples
    self.inner = 'innner'

    # HEHE
    self.innerasdasdasdasdasd = 'iasdasdasdasdnnner'

  # def allowed_cli_args(self):
  # return ['inner']
  # return []


@anyfig.config_class
class InnerConfig2:
  def __init__(self):
    # Note help
    self.inner = 'innner2'


# tt = typing.Union[Path, str]
# tt = str
# print(tt)
# print(type(tt))
config = anyfig.init_config(default_config=MyConfig)
print(config)

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('s', help='hahahah')
# parser.parse_args()
