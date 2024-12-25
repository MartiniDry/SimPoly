from model import util
from model.kpi.a_kpi import AKPI


class PerimeterRatio(AKPI):
    def __init__(self):
        self._name = "Ratio de périmètre"
        self._value = None
        self._info = ""

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def info(self):
        return self._info

    def calculate(self, s_poly, poly):
        p1 = util.perimeter(s_poly)
        p2 = util.perimeter(poly)

        if not (p1 and p2):
            return None

        if p2 == 0.0:
            return None

        self._value = p1 / p2
        self._info = "%.3f → %.3f" % (p2, p1)
