#!/usr/bin/env python3
from setuptools import setup
import sys


if sys.version_info.major < 3:
    sys.stderr.write("Please use Python version 3\n")
    sys.exit(1)

setup(name='dndmake',
      version='0.1',
      author="Chiel Kooijman, Patrick de Kok",
      author_email="chiel999@gmail.com",
      description="General purpose D&D 3.5 toolkit.",
      license="GPLv3",
      url="https://github.com/chielk/dndmake",
      scripts=["dndmake", "roll", "dndwildshape"],
      include_package_data=True,
      packages=["dndraces"],
      data_files=[('/etc/bash_completion.d', ['extras/dndmake']),
                  ('/usr/local/share/zsh/site-functions', ['extras/_dndmake']),
                  ('/usr/local/share/man/man1', ['extras/dndmake.1']),
                  ('/etc/dndmake/races', ['dndraces/human.py',
                                          'dndraces/elf.py',
                                          'dndraces/gnome.py',
                                          'dndraces/half_elf.py',
                                          'dndraces/half_orc.py',
                                          'dndraces/halfling.py',
                                          'dndraces/dwarf.py'])],
      install_requires=["argparse>=1.0", "numpy>=1.8.2", "pyperclip>=1.3"],
      )
