import anyfig
from pathlib import Path
import numpy as np


@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.help = 'normal'
    self.main_config = 'asdasd'