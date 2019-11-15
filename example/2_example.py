import anyfig
import random
# import otherfile


class RandomClass():
  def __init__(self):
    self.seed = 0
    self.hej = 'wowowo'


@anyfig.config_class
class FooConfig(RandomClass):
  def __init__(self):
    print("INIT FOOCONFIG")
    super().__init__()
    # self.frozen = 123
    self.experiment_note = 'Changed some stuff'
    self.seed = random.randint(0, 80085)

  def myfunc(self):
    pass

  # def __str__(self):
  #   return 'strannnng'


config = anyfig.setup_config(default_config='FooConfig')
print(config)
