# Fundamentals
## Config Classes

Anyfig allows you to specify configs in Python code. Instead of defining values in json or yaml, you add them to an Anyfig config-class as attributes. 

```python
import anyfig

@anyfig.config_class  # Registers the class with anyfig
class MyConfig:
  def __init__(self):
    # Config-values goes as attributes
    self.experiment_note = 'Changed stuff'
    # ... More config values
```

## What Can You Put in a Config Class?

Defining configurations in Python has multiple benefits, one of them being that you can define configs at runtime. **Any Python code** can go into the config. You can for example call a function and put the result into the config, even if the return value is a custom object.

Just because you *can* put anything into the config doesn't mean that you *should*. Keep your configs simple and readable. Complex logic code is better suited for the main program. With that said, it's ultimately up to you... With great power comes great responsibility 🕷️


```python
import anyfig
from pathlib import Path
import time

@anyfig.config_class  # Registers the class with anyfig
class MyConfig:
  def __init__(self):
    # Config-values goes as attributes
    self.experiment_note = 'Changed stuff'
    self.save_directory = Path('output')
    self.start_time = time.time()
```

## Initialize Config

To access the config-values you need to instantiate an object from the config class. This is done via Anyfig's `init_config` function. The returned object behaves as a normal class, with the exception of some added Anyfig functionality, for example a custom `__str__` function.

<!-- contains the config-values specified in the config-class along with anything else you put into along with some extra Anyfig functionality, for example a custom print function. -->


```python
import anyfig
from pathlib import Path
import time

@anyfig.config_class  # Registers the class with anyfig
class MyConfig:
  def __init__(self):
    # Config-parameters goes as attributes
    self.experiment_note = 'Changed stuff'
    self.save_directory = Path('output')
    self.start_time = time.time()

# Instantiate config object
config = anyfig.init_config(default_config=MyConfig)
print(config)

# ~~~ ⬇ Output ⬇ ~~~
MyConfig:
    experiment_note (str): Changed stuff
    save_directory (PosixPath): output
    start_time (float): 1586769550.863856
```

## Using the Config
Once the config object is initialized, the config-values can be accessed via the dot notation. 

```python
import anyfig
from pathlib import Path
import time
from myproject.io import FileWriter

@anyfig.config_class  # Registers the class with anyfig
class MyConfig:
  def __init__(self):
    # Config-parameters goes as attributes
    self.experiment_note = 'Changed stuff'
    self.save_directory = Path('output')
    self.start_time = time.time()

# Instantiate config object
config = anyfig.init_config(default_config=MyConfig)

# Use config values
writer = FileWriter(config.save_directory)
...
```


### Global Config
Most people pass the config-object around their code, accessing the config-values at various places to initilize their other components. Anyfig offers an alternative to this. The `anyfig.init_config()` function registers the config-object with Anyfig, allowing it to be accessed from any file through `anyfig.get_config()` or the proxy class `anyfig.global_cfg`.

Global objects are often considered bad practice because multiple components can change the same global object which complicates understandability and debugging. Anyfig's config-objects are **immutable by default** to mitigate this.

```python title="my_project/another_file.py"
from anyfig import global_cfg, get_config

class SomeClass:
  def __init__(self):
    # Access the config directly through an instance of the GlobalConfig helper class
    self.save_dir = global_cfg.save_directory

    # Or get the actual config-object. This is needed for e.g. isinstance(...) checks
    config = get_config()
    self.save_dir = config.save_directory
```

## Saving & Loading
Coming soon...
