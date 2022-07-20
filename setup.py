#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='python-experimenter',
    version='0.1.0',
    description='Experiment management package',
    author='Arumugam Ramaswamy',
    packages=[package for package in find_packages() if package.startswith("experimenter")],
    scripts=[],
)
