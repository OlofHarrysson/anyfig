# The seed that grew into Anyfig

Normally, configurations are written in static .txt/.json/.yaml files or parsed from input commands via argparse. These solutions are rigid and often lead to duplicated code and ugly control statements to act on the configuration flag, e.g.

```python
if config['vehicle'] == 'Car':
  vehicle = Car()
elif config['vehicle'] == 'Bike':
  vehicle = Bike()
...
```

Because Anyfig utilizes normal Python classes, it can avoid duplicated code by inheritence. One can also use other Python code/modules to directly define config parameters as the config-classes are built during runtime.

A good example of this is a [random seed](https://en.wikipedia.org/wiki/Random_seed). Say that a developer is doing an experiement with some randomness. The developer wants to be able to reproduce the experiment by seeding the algorithm and saving the seed to use later.

A first approach would be to have the seed in a text file and save the file along with the experiment results

```json
{"seed": 80085}
```

Great! The program is seeded and reproducable. But... its not really random anymore. The seed is static, thus any experiments that are ran will get the same outcome which is not what we wanted. The idea was to keep the randomness but at any time reproduce an experiment. 

Aha, but argparse solves this! A default seed can be specified with the option to override it with an input flag.

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--seed", default=80085)
```

This works aslong as the developer types "--seed=~freshest of seeds~" everytime an experiment is ran. Lets be real, nobody wants to do that. The default seed must be random by default. This can be done.

```python
import argparse
import random
parser = argparse.ArgumentParser()
parser.add_argument("--seed", default=random.randint(0, 80085))
```

Voila! This demonstrates the power of generating a config at runtime. If this is the peak complexity of your config needs there isn't really much need to look further than argparse.

But are there situtations where argparse isn't enough? Yes there is. One scenario is where there are two modes a script can be ran in, e.g. normal and debug mode. 

With argparse, one has to construct these complex control flow structures which can be hard to follow. Look at the example below and imagine if there were five more if else statements, not exactly the nicest code right?

```python
import argparse
import random
parser = argparse.ArgumentParser()
debug_default = False
parser.add_argument("--debug", default=debug_default)

if debug_default:
  parser.add_argument("--seed", default=0)
else:
  parser.add_argument("--seed", default=random.randint(0, 80085))
```

So how can Anyfig help the situtation?

```python
import anyfig
import random

@anyfig.config_class
class Normal():
  def __init__(self):
    self.seed = random.randint(0, 80085)
    ... # Other parameters

@anyfig.config_class
class Debug(Normal):
  def __init__(self):
    super().__init__()
    self.seed = 0
```

By using this structure it's clear to the developer that all that has changed whilst running the program in debug mode are the overwritten attributes.

This is why anyfig came to life but it has since then grown to encorporate other config needs. Stay tuned :D
