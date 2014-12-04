dndmake
=====
Generate a D&D NPC.

Summary
-------
Generate a D&D human with a gender and a height and weight based on the gender.
Furthermore they have a hair and eye colour and a personality based on the
five-factor model (FFM), which influences their alignment. Gender, height,
weight and alignment can also be influenced or forced through arguments.

Usage
-----
```
human.py [-h] [-m] [-f] [-t] [-s] [-b] [-l] [-n NAME] [alignment]
```
Positional arguments:
```
  race					e.g. human, elf
  alignment             Lawfulness and goodness: [LNC][GNE]
```

Optional arguments:
```
  -h, --help            show this help message and exit
  -m, --male            Make a male human
  -f, --female          Make a female human
  -t, --tall            Make a tall human
  -s, --short           Make a short human
  -b, --heavy           Make a heavy human
  -l, --light           Make a light human
  -n NAME, --name NAME  Character name
```

Installation
------------
To run this program, you need to have python version 3 installed.
To install, run:
```
sudo ./setup.py install
```
