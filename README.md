dndmake
=======
Provides:
dndmake - Generate a D&D NPC.
roll - roll dice and add constants as appropriate

Summary
-------
Generate a D&D human with a gender and a height and weight based on the gender.
Furthermore they have a hair and eye colour and a personality based on the
five-factor model (FFM), which influences their alignment. Gender, height,
weight and alignment can also be influenced or forced through arguments.

Usage (dndmake)
---------------
```
dndmake [-h] [-m] [-f] [-t] [-s] [-b] [-l] [-n NAME] race [alignment]
```
Positional arguments:
```
  race					e.g. human, elf
  alignment             Lawfulness and goodness: [LNC][GNE]
```

Optional arguments:
```
  -h, --help            show this help message and exit
  -m, --male            Make a male character
  -f, --female          Make a female character
  -t, --tall            Make a tall character
  -s, --short           Make a short character
  -b, --heavy           Make a heavy character
  -l, --light           Make a light character
  -n NAME, --name NAME  Character name
```

Usage (roll)
------------
```
 roll [-h] [-v] [-e] expression [expression ...]
```

Positional arguments
```
  expression        Expression (e.g. 3d6+3)
```

Optional arguments:
```
  -h, --help        show this help message and exit
  -v, --verbosity   Print individual dice and constants
  -e, --expectancy  Print expectancy instead of roll
```


Installation
------------
To run this program, you need to have python version 3 installed.
To install, run:
```
sudo ./setup.py install
```
