import logging
import numpy
import re
from urllib.request import urlopen
from html.parser import HTMLParser

class Size(object):
    """Representation of size categories and their modifiers."""

    # These tuples' fields represent, in order:
    #     - size label
    #     - AC modifier
    #     - grapple modifier
    #     - multiplyer for carrying capacity for creatures on two feet
    #     - multiplyer for carrying capacity for creatures on four feet
    SIZE_MODS = [('Fine', 8, -16, 1/8., 1/4.),
                 ('Diminutive', 4, -12, 1/4., 1/2.),
                 ('Tiny', 2, -8, 1/2., 3/4.),
                 ('Small', 1, -4, 3/4., 1),
                 ('Medium', 0, 0, 1, 3/2.),
                 ('Large', -1, 4, 2, 3),
                 ('Huge', -2, 8, 4, 6),
                 ('Gargantuan', -4, 12, 8, 12),
                 ('Colossal', -8, 16, 16, 24)]

    def __init__(self, size='M', ac_modifier=None, grapple=None,
                 carrying=None, quadruped_carrying=None):
        """
        Set the fields of a size category to their defaults.

        The size parameter only inspects the first letter of the label.
        """
        if type(size) is Size:
            self.size = size.size
            self.ac_modifier = size.ac_modifier
            self.grapple = size.grapple
            self.carrying = size.carrying
            self.quadruped_carrying = size.quadruped_carrying
        else:
            initial = size.upper()[0]
            if ac_modifier is None and grapple is None:
                for size_mod in self.SIZE_MODS:
                    if size_mod[0][0] == initial:
                        self.size = size_mod[0]
                        self.ac_modifier = size_mod[1]
                        self.grapple = size_mod[2]
                        self.carrying = size_mod[3]
                        self.quadruped_carrying = size_mod[4]

    def __cmp__(self, other):
        """
        Order the size categories.

        Categories representing smaller creatures are smaller.  This results
        in the order:
            - Fine
            - Diminutive
            - Tiny
            - Small
            - Medium
            - Large
            - Huge
            - Gargantuan
            - Colossal
        """
        try:
            return cmp(self.grapple, other.grapple)
        except AttributeError:
            return cmp(self.grapple, other)

    def __str__(self):
        return self.size

    def __repr__(self):
        return _MODULE_NAME + 'Size(' + self.size[0] + ')'


class Weapon(object):
    _die_progression = {'1d2': '1d3', '1d3': '1d4', '1d4': '1d6',
                        '1d6': '1d8', '1d8': '2d6', '2d6': '3d6', '3d6': '4d6',
                        '4d6': '6d6', '6d6': '8d6', '8d6': '12d6',
                        '1d10': '2d8', '2d8': '3d8', '3d8': '4d8',
                        '4d8': '6d8', '6d8': '8d8', '8d8': '12d8'}

    def __init__(self, name, damage_die, critrange=None, primary=True,
                 number=1, ranged=False, *args, **kwargs):
        self.name = name
        self.damage_die = damage_die
        self.critrange = critrange
        self.primary = primary
        self.number = 1 if number is None else number
        self.ranged = ranged
        self.strength = 10
        self.attack_bonus = 0

    def set_ability(self, strength, dexterity):
        self.strength = strength

    def set_attack_bonus(self, melee_bonus, ranged_bonus):
        self.attack_bonus = ranged_bonus if self.ranged else melee_bonus
        self.attack_bonus = self.attack_bonus[0]

    def increase_size(self):
        try:
            self.damage_die = self._die_progression[self.damage_die]
        except ValueError:
            raise ValueError("No known damage increment for %s"
                             % self.damage_die)

    def __str__(self):
        attack_bonus = self.attack_bonus
        if not self.primary:
            attack_bonus -= 5
        if attack_bonus >= 0:
            attack_bonus = '+' + str(attack_bonus)

        damage_bonus = Character._getMod(self.strength)
        if not self.primary:
            damage_bonus = int(damage_bonus * 0.5)

        output = self.name.lower()
        if self.number != 1:
            output = str(self.number) + " " + output
        output += " " + str(attack_bonus)
        output += " ranged" if self.ranged else " melee"
        output += " (" + self.damage_die
        if damage_bonus:
            output += "+" + str(damage_bonus)
        if self.critrange:
            output += '/' + self.critrange
        output += ")"
        if not self.primary:
            output += "*"
        return output

    @staticmethod
    def parse(weapon_string=''):
        if type(weapon_string) is not str:
            return weapon_string

        # TODO: Stop ignoring the difference between "and" and "or"
        separate_weapons = re.split(r'\band\b|\bor\b|,', weapon_string)
        weapons = []
        if weapon_string == '':
            return weapons
        is_first = True
        pattern = ('(?P<number>\d+)? '
                   + '?(?P<name>.+) '
                   + '(?P<attack_bonus>[+-]?\d+) '
                   + '(?:(?P<ranged>(?:melee)|(?:ranged)) )?'
                   + '(?:(?P<touch>touch) )?'
                   + '\('
                   + '(?P<damage_die>\d+(?:d\d+)?)'
                   + '(?P<damage_bonus>[+-]\d+)?'
                   + '(?: plus (?P<special>[^)])+)?'
                   + '(?:/(?P<critrange>.*))?'
                   + '\)')
        for weapon in separate_weapons:
            primary = True
            if '*' in weapon:
                weapon = ''.join(weapon.split('*'))
                primary = False
            matches = re.search(pattern, weapon).groupdict()
            if matches['number'] is None:
                matches['number'] = 1
            ranged = True
            if 'ranged' in matches:
                if matches['ranged'] is None or 'melee' in matches['ranged']:
                    ranged = False
            matches['ranged'] = ranged
            w = Weapon(primary=is_first & primary, **matches)
            weapons.append(w)
            if is_first and primary:
                is_first = False
        return weapons


class Speed(object):
    """Container for a creature's speed.

    Each movement mode (land, burrow, swim, climb, fly) are accessible as
    fields from the object.  If it has a fly speed, it also has a
    maneuvrability field.
    """
    UNIT = 'ft.'
    MODUS = ['', 'land', 'burrow', 'swim', 'climb', 'fly']
    SPEED_PATTERN = r'(%s)? ?(\d+) %s? ?(?:\((.+)\))?' %\
                    ('|'.join('(?:%s)' % s for s in MODUS), UNIT)

    def __init__(self, speed_str='0 %s' % UNIT):
        if type(speed_str) is Speed:
            speed_str = str(speed_str)
        self._speeds = {}
        self.maneuvrability = None
        speed_str = re.sub(r'\(\d+ squares?\)', r'', speed_str.lower())
        for speed in (s.strip() for s in speed_str.split(',')):
            mode, spd, maneuv = re.search(self.SPEED_PATTERN, speed).groups()
            if not len(mode):
                mode = 'land'
            self._speeds[mode] = int(spd)
            if maneuv is not None:
                self.maneuvrability = maneuv

    @property
    def land(self):
        return self._speeds.get('land', 0)

    @property
    def burrow(self):
        return self._speeds.get('burrow', 0)

    @property
    def climb(self):
        return self._speeds.get('climb', 0)

    @property
    def swim(self):
        return self._speeds.get('swim', 0)

    @property
    def fly(self):
        return self._speeds.get('fly', 0)

    def __str__(self):
        output = []
        if self.land:
            output.append(' '.join([str(self.land), self.UNIT]))
        if self.burrow:
            output.append(' '.join(['burrow', str(self.burrow), self.UNIT]))
        if self.climb:
            output.append(' '.join(['climb', str(self.climb), self.UNIT]))
        if self.swim:
            output.append(' '.join(['swim', str(self.swim), self.UNIT]))
        if self.fly:
            output.append(' '.join(['fly', str(self.fly), self.UNIT, '(%s)' %
                                    self.maneuvrability]))
        return ', '.join(output).capitalize()

    def __repr__(self):
        return _MODULE_NAME + 'Speed("' + str(self) + '")'


class ExAbilities(list):
    def __init__(self, ex_string=''):
        if not hasattr(ex_string, 'split'):
            ex_string = str(ex_string)
        list.__init__(self, (s.strip() for s in ex_string.split(',')))

    def __str__(self):
        return ', '.join(self)


def AttackBonus(attack_bonus=''):
    if type(attack_bonus) is numpy.ndarray:
        return attack_bonus

    try:
        values = [int(s) for s in attack_bonus.split('/')]
    except:
        values = [int()]
    return numpy.array(values)


def getCarryingCapacity(strength, size):
    try:
        result = capacity[strength]
    except KeyError:
        result = capacity[20 + (strength % 10)] * (4*((strength / 10)-2))
    return result * size.carrying, result * size.quadruped_carrying


class Character(object):
    """
    Contains most combat mechanical info of a D&D character.

    Most data is accessible as a property, such as name, level, size, stats,
    hp, ac, saves, speed, and attack bonuses.

    Initialization is done through passing the constructor a dictionary with
    any of the keys in Character.FIELDS.  To adjust field values later, please
    see the set_field method.

    Because it is such a huge list of attributes, check this list of methods
    to see how to edit your character:
    - wildshape
    - damage
    - healing
    """

    FIELDS = {"Name": str,
              "Level": float,
              "Size": Size,
              "HP": int,
              "HPWounds": int,
              "ACArmor": int,
              "ACShield": int,
              "ACOther": int,
              "ACDex": int,
              "ACNat": int,
              "ACDeflect": int,
              "ACMisc": int,
              "Init": int,
              "InitDex": int,
              "InitMisc": int,
              "Str": int,
              "StrTemp": int,
              "Dex": int,
              "DexTemp": int,
              "Con": int,
              "ConTemp": int,
              "Int": int,
              "IntTemp": int,
              "Wis": int,
              "WisTemp": int,
              "Cha": int,
              "ChaTemp": int,
              "FortBase": int,
              "FortAbility": int,
              "FortMagic": int,
              "FortMisc": int,
              "FortTemp": int,
              "ReflexBase": int,
              "ReflexAbility": int,
              "ReflexMagic": int,
              "ReflexMisc": int,
              "ReflexTemp": int,
              "WillBase": int,
              "WillAbility": int,
              "WillMagic": int,
              "WillMisc": int,
              "WillTemp": int,
              "Speed": Speed,
              "Armor": str,
              "MABBase": AttackBonus,
              "MBAB": AttackBonus,
              "MABMisc": int,
              "MABTemp": int,
              "GABBase": AttackBonus,
              "GBAB": AttackBonus,
              "GABMisc": int,
              "GABTemp": int,
              "RABBase": AttackBonus,
              "RBAB": AttackBonus,
              "RABMisc": int,
              "RABTemp": int,
              'NaturalWeapons': Weapon.parse,
              'Ex': ExAbilities}

    _temp_ability_scores = ['StrTemp',
                            'DexTemp',
                            'ConTemp',
                            'IntTemp',
                            'WisTemp',
                            'ChaTemp']

    # Carrying capactiy follows a non-linear function which I did not really
    # care about to model correctly.
    CARRYING_CAPACITY = {1: numpy.array([3, 6, 10]),
                         2: numpy.array([6, 13, 20]),
                         3: numpy.array([10, 20, 30]),
                         4: numpy.array([13, 26, 40]),
                         5: numpy.array([16, 33, 50]),
                         6: numpy.array([20, 40, 60]),
                         7: numpy.array([23, 46, 70]),
                         8: numpy.array([26, 53, 80]),
                         9: numpy.array([30, 60, 90]),
                         10: numpy.array([33, 66, 100]),
                         11: numpy.array([38, 76, 115]),
                         12: numpy.array([43, 86, 130]),
                         13: numpy.array([50, 100, 150]),
                         14: numpy.array([58, 116, 175]),
                         15: numpy.array([66, 133, 200]),
                         16: numpy.array([76, 153, 230]),
                         17: numpy.array([86, 173, 260]),
                         18: numpy.array([100, 200, 300]),
                         19: numpy.array([116, 233, 350]),
                         20: numpy.array([133, 266, 400]),
                         21: numpy.array([153, 306, 460]),
                         22: numpy.array([173, 346, 520]),
                         23: numpy.array([200, 400, 600]),
                         24: numpy.array([233, 466, 700]),
                         25: numpy.array([266, 533, 800]),
                         26: numpy.array([306, 613, 920]),
                         27: numpy.array([346, 693, 1040]),
                         28: numpy.array([400, 800, 1200]),
                         29: numpy.array([466, 933, 1400])}

    # For __str__
    # Format arguments:
    #   0. self
    #   1. self.carrying[0]
    #   2. self.carrying[1]
    STR_TEMPLATE = """{0.name} ({0.size})

Str: {0.str: >2} ({0.strMod: >+3}) | HP:     {0.hpCurrent}/{0.hp}
Dex: {0.dex: >2} ({0.dexMod: >+3}) | AC:     {0.ac} (t: {0.touchAC}, ff: {0.flatFootedAC})
Con: {0.con: >2} ({0.conMod: >+3}) | Init:   {0.init}
Int: {0.int: >2} ({0.intMod: >+3}) | Fort:   {0.fort}
Wis: {0.wis: >2} ({0.wisMod: >+3}) | Reflex: {0.reflex}
Cha: {0.cha: >2} ({0.chaMod: >+3}) | Will:   {0.will}
-----------------------------------------------------------------------------
Melee:   {0.melee}
Grapple: {0.grapple}
Ranged:  {0.ranged}
Full:    {0.fullAttack}
Ex:      {0.exAttacks}
Speed:   {0.speed}
Loads:   L: {1[0]}, M: {1[1]}, H: {1[2]}
Loads,4: L: {2[0]}, M: {2[1]}, H: {2[2]}
"""

    def __init__(self, data={}):
        self._fields = {}
        for key, value in self.FIELDS.items():
            self._fields[key] = self.FIELDS[key]()
        for key in self._temp_ability_scores:
            del self._fields[key]
        for key, value in data.items():
            self.set_field(key, value)

    def set_field(self, key, value):
        if key in self.FIELDS:
            try:
                self._fields[key] = self.FIELDS[key](value)
            except ValueError as e:
                if key in self._fields:
                    if key in self._temp_ability_scores:
                        del self._fields[key]
                    else:
                        self._fields[key] = self.FIELDS[key]()
        else:
            raise ValueError("'%s' is unknown" % key)

    @staticmethod
    def _getMod(score):
        """Compute an ability score's modifier."""
        return int((score - 10) / 2)

    @property
    def str(self):
        return self._fields.get('StrTemp', self._fields['Str'])

    @property
    def strMod(self):
        return self._getMod(self.str)

    @property
    def dex(self):
        return self._fields.get('DexTemp', self._fields['Dex'])

    @property
    def dexMod(self):
        return self._getMod(self.dex)

    @property
    def con(self):
        return self._fields.get('ConTemp', self._fields['Con'])

    @property
    def conMod(self):
        return self._getMod(self.con)

    @property
    def int(self):
        return self._fields.get('IntTemp', self._fields['Int'])

    @property
    def intMod(self):
        return self._getMod(self.int)

    @property
    def wis(self):
        return self._fields.get('WisTemp', self._fields['Wis'])

    @property
    def wisMod(self):
        return self._getMod(self.wis)

    @property
    def cha(self):
        return self._fields.get('ChaTemp', self._fields['Cha'])

    @property
    def chaMod(self):
        return self._getMod(self.cha)

    @property
    def name(self):
        return self._fields['Name']

    @property
    def level(self):
        lvl = self._fields['Level']
        if lvl.is_integer():
            return int(lvl)
        return lvl

    @property
    def size(self):
        return self._fields['Size']

    @property
    def speed(self):
        return self._fields['Speed']

    @property
    def hp(self):
        return self._fields['HP']

    @property
    def hpCurrent(self):
        return self._fields['HPWounds']

    @property
    def fort(self):
        return (self.conMod
                + self._fields['FortBase']
                + self._fields['FortAbility']
                + self._fields['FortMagic']
                + self._fields['FortMisc']
                + self._fields['FortTemp'])

    @property
    def reflex(self):
        return (self.dexMod
                + self._fields['ReflexBase']
                + self._fields['ReflexAbility']
                + self._fields['ReflexMagic']
                + self._fields['ReflexMisc']
                + self._fields['ReflexTemp'])

    @property
    def will(self):
        return (self.dexMod
                + self._fields['WillBase']
                + self._fields['WillAbility']
                + self._fields['WillMagic']
                + self._fields['WillMisc']
                + self._fields['WillTemp'])

    @property
    def ac(self):
        return (10
                + self.dexMod
                + self.size.ac_modifier
                + self._fields['ACArmor']
                + self._fields['ACShield']
                + self._fields['ACOther']
                + self._fields['ACNat']
                + self._fields['ACDeflect']
                + self._fields['ACMisc'])

    @property
    def touchAC(self):
        return (10
                + self.dexMod
                + self.size.ac_modifier
                + self._fields['ACOther']
                + self._fields['ACDeflect']
                + self._fields['ACMisc'])

    @property
    def flatFootedAC(self):
        return (10
                + self.size.ac_modifier
                + self._fields['ACArmor']
                + self._fields['ACShield']
                + self._fields['ACOther']
                + self._fields['ACNat']
                + self._fields['ACDeflect']
                + self._fields['ACMisc'])

    @property
    def naturalArmor(self):
        return self._fields['ACNat']

    @property
    def init(self):
        return (self.dexMod
                + self._fields['InitMisc'])

    @property
    def bab(self):
        return self._fields['MBAB']

    @property
    def melee(self):
        return (self.strMod
                + self.size.ac_modifier
                + self.bab
                + self._fields['MABMisc']
                + self._fields['MABTemp'])

    @property
    def grapple(self):
        return (self.strMod
                + self.size.grapple
                + self.bab
                + self._fields['GABMisc']
                + self._fields['GABTemp'])

    @property
    def ranged(self):
        return (self.dexMod
                + self.size.ac_modifier
                + self.bab
                + self._fields['RABMisc']
                + self._fields['RABTemp'])

    @property
    def naturalWeapons(self):
        return self._fields['NaturalWeapons']

    @property
    def fullAttack(self):
        weapons = []
        for weapon in self._fields['NaturalWeapons']:
            weapon.set_ability(self.str, self.dex)
            weapon.set_attack_bonus(self.melee, self.ranged)
            weapons.append(weapon)
        return ' and '.join(str(w) for w in weapons)

    @property
    def exAttacks(self):
        return self._fields['Ex']

    @property
    def carrying(self):
        high_str = 4 * ((self.str / 10) - 2)
        high_cap = self.CARRYING_CAPACITY[20 + self.str % 10]
        capacity = self.CARRYING_CAPACITY.get(self.str, high_cap * high_str)
        return (capacity * self.size.carrying,
                capacity * self.size.quadruped_carrying)

    def updateConAndHP(self, newCon):
        oldConMod = self.conMod
        self._fields['Con'] = newCon
        newConMod = self.conMod
        self._fields['HP'] += self.level * (newConMod - oldConMod)

    def damage(self, dmg):
        """Inflicts damage on the character."""
        self._fields['HPWounds'] = min(self.hp, self.hpCurrent - dmg)

    def healing(self, hp):
        """Heal damage."""
        return self.damage(-hp)

    def wildshape(self, animal, level_check=False):
        """
        Generate a wildshaped version of this character with an animal.

        The animal is used as a template.
        """
        if level_check and animal.level > self.level:
            raise ValueError("Wildshape animal has too many HD")
        wildshaped = Character()
        wildshaped._fields = self._fields.copy()
        new_name = "{} - {} ({} HD)".format(self.name, animal.name,
                                            animal.level)
        wildshaped.set_field('Name', new_name)
        wildshaped.set_field('Size', animal.size)
        wildshaped.set_field('Str', str(animal.str))
        wildshaped.set_field('Dex', animal.dex)
        wildshaped.set_field('Con', animal.con)
        wildshaped.set_field('ACNat', animal.naturalArmor)
        wildshaped.set_field('ACArmor', 0)
        wildshaped.set_field('ACShield', 0)
        wildshaped.set_field('Speed', animal.speed)
        wildshaped.set_field('Ex', animal.exAttacks)
        wildshaped.set_field('NaturalWeapons', animal.naturalWeapons)
        wildshaped.healing(wildshaped.level)

        return wildshaped

    def __str__(self):
        return self.STR_TEMPLATE.format(self, self.carrying[0],
                                        self.carrying[1])


class CharacterSheetParser(HTMLParser):
    """Parse a sheet of TheTangledWeb.net and make it a Character."""
    def set_character(self, character):
        self._character = character

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if ('id' in attrs
                and 'value' in attrs
                and attrs['id'] in Character.FIELDS):
            id_ = attrs['id']
            value = attrs['value']
            self._character.set_field(id_, value)


def character_from_url(url):
    logging.info("Downloading character sheet for analysis.")
    req = urlopen(url)
    html = (b'').join(req.readlines()).decode()
    character = Character()
    parser = CharacterSheetParser()
    parser.set_character(character)
    parser.feed(html)
    return character
