<div class="heroInner">
  <div class="heroLeft">
    <div>
      <p class="heroProjectTitle">Anyfig</p>
      <br></br>
      <p  class="heroProjectTagline">
        Create
        <span class="heroProjectKeywords">modular</span>
        and
        <span class="heroProjectKeywords">flexible</span>
        <span class="heroProjectKeywordsAlt">configurations</span>
        in Python
      </p>
    </div>
  </div>

  <div class="heroRight">
    <div class="heroLogo"><img src="../img/logo.svg" /></div>
  </div>
</div>

<div class="badges">

  [![image](https://img.shields.io/pypi/v/anyfig.svg)](https://pypi.org/project/anyfig/)
  [![image](https://img.shields.io/pypi/pyversions/anyfig.svg)](https://pypi.org/project/anyfig/)
  [![Travis](https://img.shields.io/travis/OlofHarrysson/anyfig/master.svg?logo=travis)](https://travis-ci.org/c4urself/anyfig)
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/OlofHarrysson/anyfig/master)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://choosealicense.com/licenses/mit/)

</div>


# Introduction

Anyfig is a Python library for creating configurations (settings) at runtime. Anyfig utilizes Python classes which empowers the developer to put anything, from strings to custom objects in the config. Hence the name Any(con)fig.

## Why Anyfig?

Anyfig was developed for my own machine learning experiments but has since generalized to support other types of Python projects. Since the configs are defined in normal Python code, Anyfig offers freedom and flexibility that isn't possible with other solutions.


### Features
* Code in Python. No reading from .json or .yaml (unless you want to)
* Avoid duplicated config-parameters with the help of inheritance and modularization
* Override config-values via command line input
* Freeze configs for immutability
* Save / load configs


## Basic Example

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

# Access config values with the dot notation
print(config.start_time)
```

### Online Demo
Feel free to play with the [Online Demo](https://mybinder.org/v2/gh/OlofHarrysson/anyfig/master?filepath=examples/online_demo.ipynb) hosted by Binder.

## Installation
Install Anyfig from pip or the github repo

```Python-3.7+
pip install anyfig
```
```Python-3.6
# dataclasses is a backport of the built-in dataclasses in Python 3.7
# More info at https://github.com/ericvsmith/dataclasses
pip install anyfig dataclasses
```
```Latest
# From GitHub master branch
pip install git+https://github.com/OlofHarrysson/anyfig/archive/master.zip
```


## Citing Anyfig
Feel free to cite Anyfig in your research:

```
@Misc{Anyfig,
  author =       {Olof Harrysson},
  title =        {Anyfig - Configuring complex Python applications},
  howpublished = {Github},
  year =         {2020},
  url =          {https://github.com/OlofHarrysson/anyfig}
}
```
