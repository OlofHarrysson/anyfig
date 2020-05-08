from .mainconfig import MainConfig


@anyfig.config_class
class UserMainConfig(MainConfig):
  def __init__(self):
    super().__init__()
    use_main_config = False
    if use_main_config:
      return

    # Overwritten values...
