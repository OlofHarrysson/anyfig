---
id: about
title: About Anyfig
sidebar_label: About
---

Anyfig is a Python library for creating configurations (settings) at runtime. Anyfig utilizes Python classes which empowers the developer to put anything, from strings to custom objects in the config. Hence the name Any(con)fig.

## Why Anyfig?
Since the configs are defined in normal Python code, Anyfig offers freedom and flexibility that isn't possible with other solutions.

### Features in a nutshell
* Work in Python. No parsing of .json or .yaml needed
* Utilize Python code / packages to define configs at runtime
* Avoid duplicated config-parameters with the help of inheritance and modularization
* Override config-parameters via command line
* Freeze configs for immutability
* Save / load configs


## Basic Example

1. Decorate a class with '@anyfig.config_class'
2. Add config-parameters as attributes in the class
3. Call the 'setup_config' function to instantiate the config object


```python
import anyfig
import random

@anyfig.config_class
class FooConfig():
  def __init__(self):
    # Config-parameters goes as attributes
    self.experiment_note = 'Changed some stuff'
    self.seed = random.randint(0, 80085)

config = anyfig.setup_config(default_config=FooConfig)
print(config)
print(config.seed)
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

