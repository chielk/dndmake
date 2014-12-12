#!/usr/bin/env python3
# (c) Patrick de Kok 2014
import random
import re


"""
So, this sucks.  Each identifier for a named group can only occur once in a
regular expression.  This means that the below expression is invalid, and
when _EXPR_PATTERN is re.compile()d, it will raise an sre_constants.error.

Even if this is fixed, each named group only stores its most recent match.
This results in the following output:
    >>> re.match(r"(?:(?P<x>\d)\S)*", "0q1q2q").groups()
    ('2',)
    >>> re.match(r"(?:(?P<x>\d)\S)*", "0q1q2q").groupdict()
    {'x': '2'}

However, I hoped for something like this:
    >>> re.match(r"(?:(?P<x>\d)\S)*", "0q1q2q").groups()
    ('0', '1', '2')
    >>> re.match(r"(?:(?P<x>\d)\S)*", "0q1q2q").groupdict()
    {'x': ['0', '1', '2']}

This is not the case.  We should look for some elegant solution for this, of
course, instead of rolling out some ugly hack.

The patterns are still provided as a clear representation of the grammar.

UPDATE: We are probably trying to write a "recursive grammar" (see [1]).  It
is suggested to write a recursive descend parser [2] by hand, or have a look
at pyparsing [3].  That library has some examples [4] that we can build upon,
such as 'fourFn.py', 'simpleCalc.py' and 'ebnf.py', or simply 'dice2.py'.

[1]: http://stackoverflow.com/questions/5060659/python-regexes-how-to-access-multiple-matches-of-a-group
[2]: http://en.wikipedia.org/wiki/Recursive_descent_parser
[3]: http://pyparsing.wikispaces.com/
[4]: http://pyparsing.wikispaces.com/Examples
"""

_DIE_PATTERN = r"(?P<die>(?P<sides>\d*)d(?P<number>\d+))"
_ELEM_PATTERN = r"(?P<elem>(?P<number>\d+))"
_SIGN_PATTERN = r"(?:\s*(?P<sign>[+-])\s*)"
_ELEMENT_PATTERN = r"(?P<element>{die}|{elem})".\
    format(elem=_ELEM_PATTERN, die=_DIE_PATTERN)
_EXPR_PATTERN = r"(?:{sign})*{element}(?:{sign}+{element})*".\
    format(sign=_SIGN_PATTERN, element=_ELEMENT_PATTERN)


def roll(dice_expr):
    """
    Operator to evaluate DiceExpressions to its random value.

    Unparsed strings can be passed as well.
    """
    if type(dice_expr) == str:
        dice_expr = DiceExpression(dice_expr)
    return sum(dice_expr.__roll__())


def E(dice_expr):
    """
    Operator to evaluate DiceExpressions to its expectancy.

    Unparsed strings can be passed as well.
    """
    if type(dice_expr) == str:
        dice_expr = DiceExpression(dice_expr)
    return dice_expr.__expectancy__()


def min_val(dice_expr):
    """
    Operator to evaluate DiceExpressions to its minimum.

    Unparsed strings can be passed as well.
    """
    if type(dice_expr) == str:
        dice_expr = DiceExpression(dice_expr)
    return sum(dice_expr.__min__())


def max_val(dice_expr):
    """
    Operator to evaluate DiceExpressions to its maximum.

    Unparsed strings can be passed as well.
    """
    if type(dice_expr) == str:
        dice_expr = DiceExpression(dice_expr)
    return sum(dice_expr.__max__())


class Element:
    def __init__(self, number):
        number = re.sub(" ", "", number)
        self._number = int(number)

    def __max__(self):
        return self._number

    def __min__(self):
        return self._number

    def __str__(self):
        return str(self._number)

    def __roll__(self):
        return self._number

    def __expectancy__(self):
        return self._number

    def __repr__(self):
        return 'dice.Element("{}")'.format(self._number)


class Dice(Element):
    def __init__(self, expression):
        pattern = re.compile("(?P<sign>[+-]?) *(?P<number>\d*)d(?P<sides>\d+)")
        dice = pattern.match(expression).groupdict()

        self._sign = -1 if dice["sign"] == "-" else 1
        self._sides = int(dice["sides"])
        number = dice["number"] if dice["number"] else "1"
        super().__init__(number)

    def __roll_die(self):
        """Roll a single die."""
        return random.randint(1, self._sides)

    def __max__(self):
        return self._sign * self._number * self._sides

    def __min__(self):
        return self._sign * self._number

    def __str__(self):
        s = "-" if self._sign == -1 else ""
        return s + "{}d{}".format(self._number, self._sides)

    def __roll__(self):
        return (self._sign *
                sum((self.__roll_die() for _ in range(self._number))))

    def __expectancy__(self):
        expectancy = self._number * (self._sides + 1) / 2
        if expectancy.is_integer():
            expectancy = int(expectancy)  # Omit floating point
        return self._sign * expectancy

    def __repr__(self):
        return 'dice.Dice("{}")'.format(self.__str__())


class DiceExpression:
    def __init__(self, expression):
        """
        Transform the string expression into some internal representation.
        The internal representation has a templated string and an iterable
        of abstract syntax trees.
        """
        self._last_roll = None
        self._template, self._asts = self.__parse_expression(expression)

    def __max__(self):
        """Return an iterable of the maximum values of each AST."""
        return (d.__max__() for d in self._asts)

    def __min__(self):
        """Return an iterable of the minimum values of each AST."""
        return (d.__min__() for d in self._asts)

    def __str__(self):
        if not self._last_roll:
            self.__roll__()
        return self._template.format(*self._last_roll)

    def __roll__(self):
        """Return an iterable of random values generated by each AST."""
        self._last_roll = [d.__roll__() for d in self._asts]
        return self._last_roll

    def roll(self):
        return sum(self.__roll__())

    def __expectancy__(self):
        """Return an iterable of expectancy values of each AST."""
        return sum(d.__expectancy__() for d in self._asts)

    def __repr__(self):
        return self._template.format(str(ast) for ast in self._asts)

    def __parse_expression(self, expression):
        pattern = re.compile("([+-]? *\d*d?\d+)")
        template = pattern.sub("{}", expression)
        asts = []
        for substring in pattern.findall(expression):
            if "d" in substring:
                asts.append(Dice(substring))
            else:
                asts.append(Element(substring))

        return template, asts
