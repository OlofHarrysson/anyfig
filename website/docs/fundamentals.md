---
id: fundamentals
title: Fundamentals
sidebar_label: Fundamentals
---

Before 

great power comes great responsibility.
Normal Python code - can do whatever.
Don't put shit in that doesn't belong.
Sort of like a plugin system?

command line input
multiple config classes
modular configs

## Config Classes

Anyfig allows you to specify your configs in Python code. Instead of defining values in json or yaml you add it to a Python class as an attribute and decorate that class with `@anyfig.config_class`. 

```python
import anyfig

@anyfig.config_class  # Registers the class with anyfig
class MyConfig():
  def __init__(self):
    # Config-values goes as attributes
    self.experiment_note = 'Changed stuff'
    ...
```

## What Can You Put in a Config Class?

Defining configurations in Python has multiple benefits, one of them being that you can define configs at runtime. **Any Python code** can go into the config. You can for example call a function and put the result into the config, even if the return value is a custom object.

Just because you *can* put anything into the config doesn't mean that you *should*. Keep your configs simple. The complex code is better left for the main program. With that said, it's ultimately up to you... With great power comes great responsibility 🕷️


```python
import anyfig
from pathlib import Path
import time

@anyfig.config_class  # Registers the class with anyfig
class MyConfig():
  def __init__(self):
    # Config-values goes as attributes
    self.experiment_note = 'Changed stuff'
    self.save_directory = Path('output')
    self.start_time = time.time()
```

## Initialize Config

To access the config-values you need to instantiate an object from the config class. This is done via Anyfig's `setup_config` function.


```python
import anyfig
from pathlib import Path
import time

@anyfig.config_class  # Registers the class with anyfig
class MyConfig():
  def __init__(self):
    # Config-parameters goes as attributes
    self.experiment_note = 'Changed stuff'
    self.save_directory = Path('output')
    self.start_time = time.time()

# Instantiate config object
config = anyfig.setup_config(default_config=MyConfig)

# Access config values with the dot notation
print(config.start_time)
```

## Multiple Config Classes

Sometimes it's useful to have multiple config-classes e.g. one for every main script. This is seamless with Anyfig.

```python
import anyfig
from pathlib import Path
import time

@anyfig.config_class  # Registers the class with anyfig
class MyConfig():
  def __init__(self):
    # Config-parameters goes as attributes
    self.experiment_note = 'Changed stuff'
    self.save_directory = Path('output')
    self.start_time = time.time()

@anyfig.config_class
class SecondConfig():
  def __init__(self):
    self.experiment_note = 'Number 2'

# The "deafault_config" argument decides which class is used to create the config
config = anyfig.setup_config(default_config=SecondConfig)

```

## Command Line Input

It's possible to overwrite existing config values through command line arguments e.g.


```bash
python path/to/file.py --experiment_note=A new note
```

```python
import anyfig
from pathlib import Path
import time

@anyfig.config_class  # Registers the class with anyfig
class MyConfig():
  def __init__(self):
    # Config-parameters goes as attributes
    self.experiment_note = 'Changed stuff'
    self.save_directory = Path('output')
    self.start_time = time.time()

config = anyfig.setup_config(default_config=MyConfig)

```

If the input argument doesn't exist in the config class, Anyfig will throw an error.

## Modular Configs
### Inheritance
### Nested

### Multiple configs & class inheritence

It's possible to have multiple config classes defined and select one at runtime. This could be useful if you e.g. have one default config and one for debugging.

To select a config class, specify the config class in the input arguments with the '--config' flag

```bash
python path/to/file.py --config=MainConfig
python path/to/file.py --config=DebugConfig
```

```python
import anyfig
import random

@anyfig.config_class
class MainConfig():
  def __init__(self):
    self.experiment_note = 'Changed some stuff'
    self.seed = random.randint(0, 80085)

@anyfig.config_class
class DebugConfig(FooConfig):
  def __init__(self):
    super().__init__() # Inherit all parameters from MainConfig
    self.seed = -1 # Overwrite
    self.new = 'Parameter not found in MainConfig'

config = anyfig.setup_config(default_config=MainConfig)
print(config) # Different output depending on which config class that was selected via the command line
```

## Multiple Configs
placeholder

## Inheritance
placeholder


## Nested Configs
placeholder
