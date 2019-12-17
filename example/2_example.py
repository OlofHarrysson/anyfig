import anyfig


# TODO: anyfig print registered options
@anyfig.config_option(name='bajs')
def with_p():
  print("MYFUNC")


@anyfig.config_option
def without():
  print("MYFUNC")


@anyfig.config_class
class FooConfig():
  def __init__(self):
    self.foo = 'Bar()'


config = anyfig.setup_config(default_config='FooConfig')
# print(config)
