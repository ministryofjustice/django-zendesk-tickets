#!/usr/bin/env python
import sys
import warnings

from setuptools import setup

if sys.version_info[0:2] < (3, 8):  # noqa: UP036
    warnings.warn('This package is only tested on Python version 3.8+', stacklevel=1)

setup()
