import pytest
import anyfig


def reg_main():
  @anyfig.config_class()
  class MainConfig():
    def __init__(self):
      self.int_var = 1
      self.float_var = 2.0
      self.string_var = '3'
      self.innerfig = InnerConfig()

  @anyfig.config_class()
  class InnerConfig():
    def __init__(self):
      self.inner = 'inner'

  return MainConfig


@pytest.fixture()
def main_config():
  yield reg_main()
  anyfig.unregister_config_classes()
