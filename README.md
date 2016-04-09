dndmake
=======
Provides:
- dndmake - helper tool for D&D sessions
- roll - roll dice and add constants as appropriate

Summary
-------
Generate a D&D human with a gender and a height and weight based on the gender.
Furthermore they have a hair and eye colour and a personality based on the
five-factor model (FFM), which influences their alignment. Gender, height,
weight and alignment can also be influenced or forced through arguments.

Usage (dndmake-npc)
---------------
```
dndmake npc [-h] [-m] [-f] [-t] [-s] [-b] [-l] [-a {LNC}{GNE}] [-n NAME] [race]
```
Positional arguments:
```
  race					e.g. human, elf
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
  -a --alignment        Lawfulness and goodness: [LNC][GNE]
  -n NAME, --name NAME  Character name
```

Usage (dndmake-wildshape)
--------------------
```
dndmake wildshape [-h]
				  [-o {name,size,ac,init,str,dex,con,int,wis,cha,fort,reflex,will,melee,grapple,ranged,land,burrow,climb,fly,swim}]
				  [-d] [-x EX] [-s {F,D,T,S,M,L,H,G,C}] [-a ANIMALS]
				  [-f OUTPUT_FILE]
				  [url]
```

Scrapes an online character sheet and applies all animal templates for
wildshape stats.

Positional arguments:
```
  url                   The URL of the sheet to scrape.
```

Optional arguments:
```
  -h, --help            show this help message and exit
  -o {name,size,ac,init,str,dex,con,int,wis,cha,fort,reflex,will,melee,grapple,ranged,land,burrow,climb,fly,swim}, --order {name,size,ac,init,str,dex,con,int,wis,cha,fort,reflex,will,melee,grapple,ranged,land,burrow,climb,fly,swim}
                        Sort results based on some property of the final form.
  -d, --hd-cap          Only show results of animals with less HD than your
                        level.
  -x EX, --ex EX        Only show results that have this extraordinary special
                        attack.
  -s {F,D,T,S,M,L,H,G,C}, --size {F,D,T,S,M,L,H,G,C}
                        Only show results of this size.
  -a ANIMALS, --animals ANIMALS
                        The tab-separated file with animal data.
  -f OUTPUT_FILE, --output-file OUTPUT_FILE
                        Write output to file, for easy future lookup.
```

Usage (roll)
------------
```
 roll [-h] [-v] [-e] [--min] [--max] expression [expression ...]
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
  --min             Print the minimum outcome
  --max             Print the maximum outcome
```

Installation
------------
To run this program, you need to have python version 3 installed.
To install, run:
```
sudo ./setup.py install
```
