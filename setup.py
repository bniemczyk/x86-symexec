#!/usr/bin/env python

from setuptools import setup

_depends = \
'''
symath >= 0.1.12, == git
distorm3
'''

setup( \
  name='x86-symexec', \
  version='git', \
  description='symbolic execution of x86 code', \
  author='Brandon Niemczyk', \
  author_email='brandon.niemczyk@gmail.com', \
  url='http://github.com/bniemczyk/x86-symexec', \
  packages=['x86symexec'], \
  test_suite='tests', \
  license='BSD', \
  install_requires=_depends,
  classifiers = [ \
    'Development Status :: 3 - Alpha', \
    'Intended Audience :: Developers', \
    'Intended Audience :: Science/Research', \
    'License :: OSI Approved :: BSD License'
    ]
  )
