import anyfig
import jsonpickle
import save


def main():
  # print(anyfig.get_config_classes())
  # config = anyfig.load_json('save.json')

  config = anyfig.load_config('save.pickle')

  print(config)
  print(type(config))


if __name__ == '__main__':
  main()
