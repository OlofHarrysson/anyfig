import anyfig
import configs
# from configs.main_config import MainConfig
# from configs.local_config import LocalConfig

if __name__ == '__main__':
  config = anyfig.setup_config(default_config=configs.MainConfig)
  # config = anyfig.setup_config(default_config=LocalConfig)
  print(config)
