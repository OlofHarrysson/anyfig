import anyfig


@anyfig.config_class
class Train(anyfig.MasterConfig):
  def __init__(self):
    super().__init__()
    self.name = 'this one'
