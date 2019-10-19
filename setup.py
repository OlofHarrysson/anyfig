from distutils.core import setup
setup(
  name='anyfig',
  packages=['anyfig'],
  version='0.0.1',
  license='MIT',
  description='Config parameters in Python code. Anything is possible ;)',
  author='Olof Harrysson',
  author_email='harrysson.olof@gmail.com',
  url='https://github.com/OlofHarrysson/anyfig',
  download_url='https://github.com/OlofHarrysson/anyfig/archive/0.0.1.tar.gz',
  keywords=['config', 'command line parsing', 'python classes', 'dynamic'],
  install_requires=['fire'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)