#!/usr/bin/env python3
from distutils.core import setup
import sys


if sys.version_info.major < 3:
    sys.stderr.write("Please use python version 3\n")
    sys.exit(1)

setup(name='dndmake',
      version='1.1',
      author="Chiel Kooijman",
      author_email="chiel999@gmail.com",
      description="Generate a D&D NPC or roll dice",
      license="GPLv3",
      url="https://github.com/chielk/human",
      scripts=["dndmake", "roll"],
      py_modules=["simpleunit", "dice"],
      packages=["races"]
      )
