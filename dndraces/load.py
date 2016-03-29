from importlib.machinery import SourceFileLoader
import re
import sys
import os

HOME = os.getenv("HOME")
HOME_RACES = os.path.join(HOME, ".config", "dndmake", "races")
ETC_RACES = "/etc/dndmake/races"


def ensure_directories():
    HOME = os.getenv("HOME")
    HOME_RACES = os.path.join(HOME, ".dndmake", "races")
    os.makedirs(HOME_RACES, exist_ok=True)


def list_races():
    ensure_directories()
    classes = os.listdir(HOME_RACES)
    classes += os.listdir(ETC_RACES)
    return [cls.split('.')[0].replace('_', '-') for cls in classes]


def load_race(name):
    ensure_directories()
    base_name = name.lower()
    file_name = base_name.replace('-', '_') + ".py"
    class_name = ''.join(part.capitalize() for part in base_name.split('-'))

    try:
        # from this library
        Race = getattr(__import__("dndraces"), class_name)
    except AttributeError:
        # Don't make __pycache__ file in the races directories
        sys.dont_write_bytecode = True
        try:
            # from $HOME
            loader = SourceFileLoader(class_name,
                                      os.path.join(HOME_RACES, file_name))
            races = loader.load_module()
            Race = getattr(races, class_name)
        except FileNotFoundError:
            try:
                # from /etc
                loader = SourceFileLoader(class_name,
                                          os.path.join(ETC_RACES, file_name))
                races = loader.load_module()
                Race = getattr(races, class_name)
            except FileNotFoundError:
                msg = "Can not find class for " + name + "\n"
                msg += 'Looking for class "' + class_name + '" in ' + file_name
                raise FileNotFoundError()

    return Race
