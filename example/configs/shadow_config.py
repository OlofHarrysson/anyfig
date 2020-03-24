import anyfig

from .main_config import MainConfig


@anyfig.config_class
class ShadowConfig(MainConfig):
  # ShadowConfig. Initially registered with git, but then ignored.
  # Useful for projects with multiple collaborators as experimental changes in the config wont accidently be added to git

  # git update-index --skip-worktree <file_name>
  def __init__(self):
    super().__init__()
