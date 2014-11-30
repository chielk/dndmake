#!/usr/bin/env python3
from distutils.core import setup
import sys


if sys.version_info.major < 3:
    sys.stderr.write("Please use python version 3\n")
    sys.exit(1)

setup(name='human',
      version='1.0',
      author="Chiel Kooijman",
      author_email="chiel999@gmail.com",
      description="Generate a D&D human",
      license="GPLv3",
      url="https://github.com/chielk/human",
      scripts=["human"],
      py_modules=["simpleunit"],
      )
