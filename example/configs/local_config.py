import anyfig

from .main_config import MainConfig


@anyfig.config_class
class LocalConfig(MainConfig):
  # Shadow config
  # Initially registered with git, but then
  def __init__(self):
    super().__init__()
    self.foo = 'LOCAaaaa'
