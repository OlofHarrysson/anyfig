# from .. import anyfig
import anyfig
import random
import otherfile
# config_class(FooConfig)


class RandomClass():
  def __init__(self):
    self.seed = 0
    self.hej = 'wowowo'


@anyfig.config_class
class FooConfig(RandomClass):
  # class FooConfig(anyfig.MasterConfig):
  def __init__(self):
    print("INIT FOOCONFIG")
    super().__init__()
    # self.frozen = 123
    self.experiment_note = 'Changed some stuff'
    self.seed = random.randint(0, 80085)

  def myfunc(self):
    pass


@anyfig.config_class
class MasterConfig():
  # class FooConfig(anyfig.MasterConfig):
  def __init__(self):
    print("INIT MASTER")
    super().__init__()
    self.experiment_note = 'Changed some stuff22'
    self.seed = random.randint(0, 80085)


print("BEFORE OBJ CREATION")
# config = anyfig.setup_config(default_config='FooConfig')
config = anyfig.setup_config(default_config='MasterConfig')
print("AFTER OBJ CREATION")
print(config)
print(config.seed)  # Prints -1

# class A():
#   def __init__(self):
#     self.name = 'A'
#     print("I AM A")

# class AA():
#   def __init__(self):
#     self.name = 'AA'
#     self.aa = 'aaa'
#     print("I AM AA")

# class B(A):
#   # class B():
#   def __init__(self):

#     # class B(AA, A):
#     #   def __init__(self):
#     #     A.__init__(self)
#     #     super().__init__()
#     self.name = 'B'

# # class C(A):
# #   def __init__(self):
# #     self.name = 'C'

# # B.__bases__ = (A, )
# print(B.__bases__)
# qwe

# b = B()
# print(b.name)
# print(b.__class__.__bases__)

# class Friendly:
#   def hello(self):
#     print('Hello')

# class Person:
#   pass

# print(Person.__bases__)
# p = Person()
# Person.__bases__ = (Friendly, )
# p.hello()  # prints "Hello"

# class Fig():
#   def __init__(self):
#     print("FIG INIT")

#   def extension(self):
#     print("Some work...")

# class Master():
#   def __init__(self):
#     print("BASE INIT")

# print(Master.__bases__)
# Master = type('Master', (Fig, ), {})
# print(Master.__bases__)
# Master().extension()