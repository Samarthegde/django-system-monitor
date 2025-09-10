#!/usr/bin/env python
import setuptools
import configparser
import os

# Read the version from setup.cfg
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'setup.cfg'))
version = config['metadata']['version']

if __name__ == "__main__":
    setuptools.setup(
        version=version,
    )
