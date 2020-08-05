import pytest
import anyfig

# TODO: If we want to tear down tests we can yield fixtures instead of return https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code

# TODO: How does fixture scopes work? Tests fail without the scope


def reg_main():
  @anyfig.config_class()
  class MainConfig():
    def __init__(self):
      self.int_var = 1
      self.float_var = 2.0
      self.string_var = '3'

  return MainConfig


# def reg_target(target):
#   @anyfig.config_class(target=target)
#   class TargetConfig():
#     def __init__(self):
#       self.day = 1
#       self.month = 2
#       self.year = 3

#   return TargetConfig


@pytest.fixture()
def main_config():
  yield reg_main()
  anyfig.unregister_config_classes()


# @pytest.fixture
# def target_config(target):
#   return reg_target(target)
