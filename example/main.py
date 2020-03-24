import anyfig
import configs

if __name__ == '__main__':
  config = anyfig.setup_config(default_config=configs.MainConfig)
  print(config)
