#!/usr/bin/env python

from setuptools import setup

setup(name = 'qdotweb',
      version = '0.1',
      install_requires = ['flask>=0.10', 'pyvisa>=1.5', 'json']
      description = 'a Flask wrapper for PyVISA instrument control',
      author = 'Nik Hartman',
      author_email = 'nik.hartman@gmail.com',
      url = 'https://github.com/nikhartman/qdotweb',
      py_modules = ['qdotweb'],
      )
