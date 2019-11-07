import anyfig
import random


@anyfig.config_class
class FooConfig(anyfig.MasterConfig):
  def __init__(self):
    super().__init__()
    self.experiment_note = 'Changed some stuff'
    self.seed = random.randint(0, 80085)


config = anyfig.setup_config(default_config='FooConfig')
print(config)
print(config.seed)  # Prints -1