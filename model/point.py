import math


class Point:
    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __add__(self, other):
        self._x += other.x
        self._y += other.y

    def __sub__(self, other):
        self._x -= other.x
        self._y -= other.y

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            self._x *= other
            self._y *= other
        else:
            self._x *= other.x
            self._y *= other.y

    def __str__(self):
        return "{%d;%d}" % (self._x, self._y)

    def tuple(self):
        return self.x, self.y


def dist2(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    return dx*dx + dy*dy


def dist(p1, p2):
    return math.sqrt(dist2(p1, p2))


def minx(pt_list):
    if len(pt_list) == 0:
        return None

    result = pt_list[0].x
    for i in range(1, len(pt_list)):
        pt = pt_list[i]
        if pt.x < result:
            result = pt.x

    return result


def maxx(pt_list):
    if len(pt_list) == 0:
        return None

    result = pt_list[0].x
    for i in range(1, len(pt_list)):
        pt = pt_list[i]
        if pt.x > result:
            result = pt.x

    return result


def minmaxx(pt_list):
    if len(pt_list) == 0:
        return None

    resmin, resmax = (pt_list[0].x, pt_list[0].x)
    for i in range(1, len(pt_list)):
        pt = pt_list[i]
        if pt.x < resmin:
            resmin = pt.x
        elif pt.x > resmax:
            resmax = pt.x

    return resmin, resmax


def miny(pt_list):
    if len(pt_list) == 0:
        return None

    result = pt_list[0].y
    for i in range(1, len(pt_list)):
        pt = pt_list[i]
        if pt.y < result:
            result = pt.y

    return result


def maxy(pt_list):
    if len(pt_list) == 0:
        return None

    result = pt_list[0].y
    for i in range(1, len(pt_list)):
        pt = pt_list[i]
        if pt.y > result:
            result = pt.y

    return result


def minmaxy(pt_list):
    if len(pt_list) == 0:
        return None

    resmin, resmax = (pt_list[0].y, pt_list[0].y)
    for i in range(1, len(pt_list)):
        pt = pt_list[i]
        if pt.y < resmin:
            resmin = pt.y
        elif pt.y > resmax:
            resmax = pt.y

    return resmin, resmax
