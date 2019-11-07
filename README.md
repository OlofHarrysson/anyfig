# Anyfig

Anyfig is a Python library for creating configurations (settings) at runtime. Anyfig utilizes Python classes which empowers the developer to put anything, from strings to custom objects in the config. Hence the name Any(con)fig.


## The seed that grew into Anyfig

Normally, configurations are written in static .txt/.json/.yaml files or parsed from input commands via argparse. These solutions are rigid and often lead to duplicated code and ugly control statements to act on the configuration flag, e.g.

```python # TODO: better example + can I even avoid this?
if config['move'] == 'turn left':
  move = TurnLeftClass()
elif config['move'] == 'turn right':
  move = TurnRightClass()
...
```

Because Anyfig utilizes normal Python classes, it can avoid duplicated code by inheritence. One can also use other Python code/modules to directly define config parameters as the config-classes are built during runtime.

A good example of this is a random seed. Say that a developer is doing an experiement with some randomness. The developer wants to be able to reproduce the experiment by seeding and saving the seed.

TODO link to seed?

A first approach would be to have the seed in a text file and save the file along with the experiment results

```json
{"seed": 80085}
```

Great! The program is seeded and reproducable. But... its not really random anymore. The seed is static, thus 

This particular seed turned out be really bad and doesn't represent the outcome of an average seed. The static seed hinders the developer to understand how the experiment behaves under different seeds.

Aha, but argparse solves this! A default seed can be specified with the option to override it with an input flag.
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--seed", default=80085)
```

All is well. Except that the developer has to type "--seed=~freshest of seeds~" everytime the program is executed. How many of your developer friends enjoys pondering which seed that should be next?


So the developer wants to have different seeds but believes that manual seed-selecting labor is for suckers (and rightfully so). If only it was possible to automatically generate a seed on the fly...


```python
import argparse
import random
parser = argparse.ArgumentParser()
parser.add_argument("--seed", default=random.randint(0, 80085))
```

Voila! This demonstrates the power of generating a config at runtime. But what doesn't argparse solve?

Have to different entrypoints with different default values without duplicated code


```python
import argparse
import random
parser = argparse.ArgumentParser()
debug_default = False
parser.add_argument("--debug", default=debug_default)

if debug_default:
  parser.add_argument("--seed", default=80085)
else:
  parser.add_argument("--seed", default=random.randint(0, 80085))
```






move to what anyfig offers

TODO: Possibly go from file seed -> solved by argparse -> but argparse doesnt solve this case.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

### The basics
Create a class, decorate & inherit from Anyfig. Add parameters!

```python
import anyfig
import random

@anyfig.config_class
class FooConfig(anyfig.MasterConfig):
  def __init__(self):
    super().__init__()
    self.experiment_note = 'Changed some stuff'
    self.seed = random.randint(0, 80085)

config = anyfig.setup_config(default_config='FooConfig')
print(config)
print(config.seed)
```

### Command line input

It's possible to overwrite the config values by starting the python script with command line inputs e.g.
```bash
python path/to/file.py --seed=-1
```

```python
import anyfig
import random

@anyfig.config_class
class FooConfig(anyfig.MasterConfig):
  def __init__(self):
    super().__init__()
    self.experiment_note = 'Changed some stuff'
    self.seed = random.randint(0, 80085)

config = anyfig.setup_config(default_config='FooConfig')
print(config.seed) # Output: -1
```

### Multiple Configs & Class Inheritence

It's possible to have multiple config classes defined and select one at runtime. This could be useful if you e.g. have one default config and one for debugging.

To select a config class, specify the config class in the input arguments with the --config flag

```bash
python path/to/file.py --config=FooConfig
python path/to/file.py --config=BarConfig
```

It's possible for a config class to inherit from any Python class as long as that class ultimately inherits from the Anyfig.MasterConfig class.

```python
import anyfig
import random

@anyfig.config_class
class FooConfig(anyfig.MasterConfig):
  def __init__(self):
    super().__init__()
    self.experiment_note = 'Changed some stuff'
    self.seed = random.randint(0, 80085)

@anyfig.config_class
class BarConfig(FooConfig):
  def __init__(self):
    super().__init__()
    self.seed = -1
    self.bar = 'beer'

config = anyfig.setup_config() # Removed the default class
print(config) # Different output depending on which config class that was selected
```

### Complex Config Attributes
Anyfig lets you put anything within your config object, even complicated objects. Unfortunately, this can be troublesome as objects are often undescriptive when printed.
blabla


### Saving & Loading Configs
Anyfig offers functions for both saving and loading a config. When saving, Anygif serializes the config object with the pickle module as well as a .txt file.  

```python
import anyfig
config = ...
anyfig.save_config(config, 'path/to/save.cfg')
loaded_config = anyfig.load_config('path/to/save.cfg')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)