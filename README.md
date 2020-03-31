# Anyfig

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


See [The seed that grew into Anyfig](assets/anyfig_story.md) for a more in depth view of why Anyfig has a place in this world

## Requirements
Python 3.7+

## Installation
The Anyfig package is in its infancy. Install it from pip or the github repo

```bash
# Latest "stable" realease
pip install anyfig

# From github
pip install git+https://github.com/OlofHarrysson/anyfig/archive/master.zip

```

Or try the online demo @
[pyfiddle.io](https://pyfiddle.io/fiddle/4de2f70f-e421-4326-bbb8-b06d5efa547d/?i=true)

## Usage

### The basics
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

#### Under the hood - how Anyfig works
The **@anyfig.config_class** decorator registers the class with Anyfig and adds some attributes and methods to the class.

The **anyfig.setup_config()** function checks if the class specified in its default_config argument is among the registered config-classes. If it is, a object is instantiated from the class definition and returned.

### Command line input

It's possible to overwrite existing config values by starting the python script with command line arguments e.g.

```bash
python path/to/file.py --seed=69
```

```python
import anyfig
import random

@anyfig.config_class
class FooConfig():
  def __init__(self):
    self.experiment_note = 'Changed some stuff'
    self.seed = random.randint(0, 80085)

config = anyfig.setup_config(default_config='FooConfig')
print(config.seed) # Output: 69. Overwritten from command line
```
If the input argument doesn't exist in the config class, Anyfig will throw an error.


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

### Saving and loading configs
Anyfig offers functions for both saving and loading a config. When saving, anyfig serializes the config object with the pickle module as well as a .txt file.  

```python
import anyfig
config = ...
anyfig.save_config(config, 'path/to/save.cfg')
loaded_config = anyfig.load_config('path/to/save.cfg')
```

### Large or complex configurations
Create configs folder

create config files in folder

**__init__.py** imports everything

shadow configs



### Complex config attributes
TODO: Refine section

Anyfig lets you put anything within your config object, even complicated objects. Unfortunately, this can be troublesome as objects are often undescriptive when printed or saved. This can be troublesome when one wants to go back to a saved config and see what it contains.

One way to fix this problem would be to add descriptive \__str\__ methods to the classes.

However, if the source code for these complicated objects change, it isn't enough to have its string representation. 

```python
import anyfig

class Bar():
  def __init__(self):
    self.x = 2 + 3

  def __str__(self):
    return f'{self.__class__.__name__}(x={self.x})'

@anyfig.config_class
class FooConfig():
  def __init__(self):
    self.foo = Bar()

config = anyfig.setup_config(default_config='FooConfig')
print(config) # 'foo': 'Bar(x=5)'
```

If the line `self.x = 2 + 3` change to `self.x = 7 - 2` it would look like nothing had changed in the Bar class. Perhaps the developer would like to inspect the source code rather than the value.

Anyfig offers the '@anyfig.print_source' decorator for these situations.

```python
import anyfig

@anyfig.print_source
class Bar():
  def __init__(self):
    self.x = 2 + 3

@anyfig.config_class
class FooConfig():
  def __init__(self):
    self.foo = Bar()

config = anyfig.setup_config(default_config='FooConfig')
print(config.foo) # Output ->
# class Bar():
#   def __init__(self):
#     self.x = 2 + 3

  
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
