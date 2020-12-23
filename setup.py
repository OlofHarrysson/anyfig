#!/usr/bin/env python
""" Setup script for pip """

from setuptools import setup, find_packages

with open('README.md') as readme_file:
  readme = readme_file.read()

requirements = [
  'fire', 'typeguard', 'dill', "dataclasses;python_version=='3.6'"
]

setup_requirements = [
  'pytest-runner',
]

test_requirements = [
  'pytest>=3',
]

setup(
  author="Olof Harrysson",
  author_email='harrysson.olof@gmail.com',
  python_requires='>=3.6',
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  description="Create modular and scaleable configurations at runtime",
  install_requires=requirements,
  license="MIT license",
  long_description=readme,
  include_package_data=True,
  keywords=[
    'config', 'configurations', 'configuration-management',
    'argparse-alternative', 'settings', 'command line parsing',
    'python classes', 'dynamic', 'runtime'
  ],
  name='anyfig',
  packages=find_packages(include=['anyfig', 'anyfig.*']),
  setup_requires=setup_requirements,
  test_suite='tests',
  tests_require=test_requirements,
  url='https://github.com/OlofHarrysson/anyfig',
  version='0.2.0',
  zip_safe=False,
)
