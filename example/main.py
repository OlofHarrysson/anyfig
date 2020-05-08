import anyfig
try:
  from normalconfigs.userconfigs import UserMainConfig as ConfigClass
except ModuleNotFoundError:
  from normalconfigs.mainconfig import MainConfig as ConfigClass

if __name__ == '__main__':
  config = anyfig.init_config(default_config=ConfigClass)
  print(config)
