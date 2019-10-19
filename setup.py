from distutils.core import setup
setup(
  name='anyfig',
  packages=['anyfig'],
  version='0.0.1',
  license='MIT',
  description='Config parameters in Python code. Anything is possible ;)',
  author='Olof Harrysson',
  author_email='harrysson.olof@gmail.com',
  url=
  'https://github.com/user/reponame',  # Provide either the link to your github or to your website
  download_url=
  'https://github.com/user/reponame/archive/v_01.tar.gz',  # I explain this later on
  keywords=['SOME', 'MEANINGFULL',
            'KEYWORDS'],  # Keywords that define your package best
  install_requires=[  # I get to this in a second
    'validators',
    'beautifulsoup4',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',  # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  # Again, pick a license
    'Programming Language :: Python :: 3',  #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)