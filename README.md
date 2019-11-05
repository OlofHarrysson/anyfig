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

Because Anyfig is built on a normal Python class, it can enjoy the benefits of class-inheritance, avoiding duplicated code. It can also utilize arbitrary Python code and packages to directly create a meaningful config, without additional control statements.

A good example of this is a random seed. Say that a developer is doing an experiement with some randomness. The developer wants to seed the program and save the seed for future reproducibility.

A first approach would be to have the seed in a text file like so

```json
{"seed": 80085}
```

Great! The program is seeded and reproducable. But... its not really random anymore. This particular seed turned out be really bad and doesn't represent the outcome of an average seed. The static seed hinders the developer to understand how the experiment behaves under different seeds.

Aha, but argparse solves this! A default seed can be specified with the option to override it with an input flag.
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--seed", default=80085)
```

All is well. Except that the developer has to type "--seed=freshest of seeds" everytime the program is executed. How many of your developer friends enjoys pondering which seed that should be next? The default seed is right there, maybe I'll just go with that this one time...


So the developer wants to have different seeds but believes that manual seed-selecting labor is for suckers (and rightfully so). If only it was possible to automatically generate a seed on the fly...


```python
import argparse
import random
parser = argparse.ArgumentParser()
parser.add_argument("--seed", default=random.randint(0, 1000))
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
  parser.add_argument("--seed", default=random.randint(0, 1000))
```






move to what anyfig offers

TODO: Possibly go from file seed -> solved by argparse -> but argparse doesnt solve this case.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)