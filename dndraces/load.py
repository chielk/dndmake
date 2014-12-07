from importlib.machinery import SourceFileLoader
import sys
import os


def load_race(name):
    name = name.lower()
    HOME = os.getenv("HOME")
    RACES = os.path.join(HOME, ".dndmake", "races")
    os.makedirs(RACES, exist_ok=True)

    try:
        # from this library
        Race = getattr(__import__("dndraces"), name.capitalize())
    except AttributeError:
        # Don't make __pycache__ file in the races directories
        sys.dont_write_bytecode = True
        try:
            # from $HOME
            loader = SourceFileLoader(name.capitalize(),
                                      os.path.join(RACES, name + ".py"))
            races = loader.load_module()
            Race = getattr(races, name.capitalize())
        except FileNotFoundError:
            try:
                # from /etc
                RACES = "/etc/dndmake/races"
                loader = SourceFileLoader(name.capitalize(),
                                          os.path.join(RACES, name + ".py"))
                races = loader.load_module()
                Race = getattr(races, name.capitalize())
            except FileNotFoundError:
                raise FileNotFoundError("Can not find class for " + name)

    return Race
