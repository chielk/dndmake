from importlib.machinery import SourceFileLoader
import re
import sys
import os


def load_race(name):
    base_name = name.lower()
    file_name = base_name.replace('-', '_') + ".py"
    class_name = ''.join(part.capitalize() for part in base_name.split('-'))

    HOME = os.getenv("HOME")
    RACES = os.path.join(HOME, ".dndmake", "races")
    os.makedirs(RACES, exist_ok=True)

    try:
        # from this library
        Race = getattr(__import__("dndraces"), class_name)
    except AttributeError:
        # Don't make __pycache__ file in the races directories
        sys.dont_write_bytecode = True
        try:
            # from $HOME
            loader = SourceFileLoader(class_name,
                                      os.path.join(RACES, file_name))
            races = loader.load_module()
            Race = getattr(races, class_name)
        except FileNotFoundError:
            try:
                # from /etc
                RACES = "/etc/dndmake/races"
                loader = SourceFileLoader(class_name,
                                          os.path.join(RACES, file_name))
                races = loader.load_module()
                Race = getattr(races, class_name)
            except FileNotFoundError:
                msg = "Can not find class for " + name + "\n"
                msg += 'Looking for class "' + class_name + '" in ' + file_name
                raise FileNotFoundError()

    return Race
