# (c) Chiel Kooijman 2014


class Unit:
    def __init__(self, v=0):
        self.__val = v

    def __mul__(self, other):
        if type(other) in (int, float):
            return type(self)(v=self.__val * other)
        elif type(other) == type(self):
            return type(self)(v=self.__val * other.val())
        else:
            s = "Can not mutiply types: {} and {}"
            raise Exception(s.format(str(type(self)), str(type(other))))

    def __imul__(self, other):
        if type(other) in (int, float):
            self.__val *= other
        elif type(other) == type(self):
            self.__val *= other.val()
        else:
            s = "Can not mutiply types: {} and {}"
            raise Exception(s.format(str(type(self)), str(type(other))))

    def __add__(self, other):
        if type(other) == type(self):
            return type(self)(v=self.__val + other.val())
        else:
            s = "Can not add types: {} and {}"
            raise Exception(s.format(str(type(self)), str(type(other))))

    def __iadd__(self, other):
        if type(other) == type(self):
            self.__val += other.val()
        else:
            s = "Can not add types: {} and {}"
            raise Exception(s.format(str(type(self)), str(type(other))))

    def val(self):
        return self.__val


class Length(Unit):
    INCH = 0.0254
    CM = 100
    FT = 12 * INCH

    def __init__(self, cm=0, m=0, ft=0, inch=0, v=0):
        val = inch * self.INCH
        val += ft * self.FT
        val += m
        val += v
        val += cm * self.CM
        Unit.__init__(self, v=val)

    def imperial(self):
        return (str(int(self.val() / self.FT)) + "'" +
                str(int((self.val() % self.FT) / self.INCH)) + "\"")

    def metric(self):
        s = str(int(self.val()))
        cm = int(self.val() % 1 * self.CM)
        if not cm == 0:
            s += ".%02d" % int(self.val() % 1 * self.CM)
        s += "m"
        return s

    def __str__(self):
        return self.metric()

    def cm(self):
        return str(int(self.val() * self.CM)) + "cm"


class Weight(Unit):
    LB = 0.453592

    def __init__(self, kg=0, lbs=0, v=0):
        val = kg
        val += lbs * self.LB
        val += v
        Unit.__init__(self, v=val)

    def imperial(self):
        return str(int(self.val() / self.LB)) + " lbs"

    def metric(self):
        return str(round(self.val())) + "kg"

    def __str__(self):
        return self.metric()


Inch = Length(inch=1)

Foot = Length(ft=1)

Meter = Length(m=1)

Cm = Length(cm=1)

Lb = Weight(lbs=1)

Kg = Weight(kg=1)
