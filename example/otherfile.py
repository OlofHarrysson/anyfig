import anyfig
import eval_input

# @anyfig.config_class
# class FooConfig2():
#   def __init__(self):
#     self.experiment_note = 'Changed some stuff'


@anyfig.config_class
class FooConfig2(eval_input.MainConfig):
  def __init__(self):
    super().__init__()
    self.experiment_note = 'Changed some stuff'


if __name__ == '__main__':
  config = anyfig.setup_config(default_config=FooConfig2)
  print(config)
