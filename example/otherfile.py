import anyfig


@anyfig.config_class
class FooConfig2():
  def __init__(self):
    self.experiment_note = 'Changed some stuff'
