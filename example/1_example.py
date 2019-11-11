import anyfig


@anyfig.print_source
class Noise():
  def __init__(self, x, y):
    self.x = x
    self.y = y


@anyfig.print_source
class Flip():
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.noise3 = Noise(1, 2)
    self.noise1 = Noise(1, 2)


@anyfig.print_source
class Transformer():
  def __init__(self, x):
    # self.noise1 = Noise(x, x)
    self.flip = Flip(4, 0)
    # self.noise2 = Noise(4, 0)
    self.primitive = x


@anyfig.config_class
class MainConfig():
  def __init__(self):
    print("MAIN CONFIG SUPER")
    # self.start_time = time.time()
    self.img_size = 100
    self.classes = ['car', 'dog']
    self.freeze_config = False


@anyfig.config_class
class Train():
  def __init__(self):
    self.name = 'oldname'
    self.transforms111 = Transformer(100)
    # self.freeze_config = False
    # self.frozen = 123


@anyfig.config_class
class Config():
  def __init__(self):
    self.name = 'oldname1111'
    self.transforms111 = Transformer(100)
    # self.freeze_config = False
    # self.frozen = 123


def main():
  # config = anyfig.setup_config()
  config = anyfig.setup_config(default_config='Train')
  print(config)
  # anyfig.save_config('adasdas', 'config.cfg')
  # anyfig.save_config(config, 'config.cfg')
  # anyfig.load_config('config.cfg')
  # anyfig.load_config('config.cfg.txt')


if __name__ == '__main__':
  print("BEFORE MAIN")
  main()
