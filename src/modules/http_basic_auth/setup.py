from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand

VERSION = '0.0.1' 
DESCRIPTION = 'My Http Basic Authentication Module'
LONG_DESCRIPTION = 'My first Python package for Http Basic Authentication'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="HttpBasicAuth", 
    version=VERSION,
    author="Roy Liang",
    author_email="liangsehhaw@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # packages=['http_basic_auth'],
    install_requires=[], # add any additional packages that 
    keywords=['python', 'Http Basic Authentication'],
    classifiers= [
        "Development Status     :: 3 - Alpha",
        "Intended Audience      :: Education",
        "Programming Language   :: Python :: 2",
        "Programming Language   :: Python :: 3",
        "Operating System       :: MacOS :: MacOS X",
        "Operating System       :: Microsoft :: Windows",
    ]
)
