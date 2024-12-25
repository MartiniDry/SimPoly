import math
import random

from model.point import Point


def rectangle():
    return [
        Point(0, 0),
        Point(100, 0),
        Point(100, 100),
        Point(0, 100)
    ]


def invader():
    # --------------
    # --##--##--##--
    # --##########--
    # ------##------
    # --##--##--##--
    # --##########--
    # --------------
    return [
        Point(0, 0),
        Point(0, 40),
        Point(40, 40),
        Point(40, 80),
        Point(20, 80),
        Point(20, 60),
        Point(0, 60),
        Point(0, 100),
        Point(100, 100),
        Point(100, 60),
        Point(80, 60),
        Point(80, 80),
        Point(60, 80),
        Point(60, 40),
        Point(100, 40),
        Point(100, 0),
        Point(80, 0),
        Point(80, 20),
        Point(60, 20),
        Point(60, 0),
        Point(40, 0),
        Point(40, 20),
        Point(20, 20),
        Point(20, 0)
    ]


def imperfect_disc(nb_pts):
    polygon = []
    for i in range(nb_pts):
        dist = random.randint(30, 30 + int(20 * i/nb_pts))
        angle = 2*math.pi * i/nb_pts
        polygon.append(Point(50 + dist * math.cos(angle), 50 + dist * math.sin(angle)))

    return polygon


def from_file(filename):
    if filename.split('.')[-1] != "spl":
        print("Not the good extension")
        return

    polygon = []
    with open("polygon_files//" + filename, 'r') as file:
        for line in file.readlines():
            line = line.removesuffix('\n')
            if line != '':
                data = [float(x) for x in line.split(' ')]
                polygon.append(Point(data[0], data[1]))

    return polygon
