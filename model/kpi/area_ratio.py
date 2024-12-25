from model import util
from model.kpi.a_kpi import AKPI


class AreaRatio(AKPI):
    def __init__(self):
        self._name = "Ratio de surface"
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
        s1 = util.surface(s_poly)
        s2 = util.surface(poly)

        if not (s1 and s2):
            return None

        if s2 == 0.0:
            return None

        self._value = s1 / s2
        self._info = "%.1f → %.1f" % (s2, s1)
