from model import point


def surface(pt_list):
    if len(pt_list) < 2:
        return None

    if len(pt_list) == 2:
        return 0.0

    area = 0.0
    pt1 = pt_list[-2]  # The previous point is stored to save time.
    pt2 = pt_list[-1]  # The previous point is stored to save time.
    for pt3 in pt_list:
        area += pt2.x * (pt1.y - pt3.y)
        pt1 = pt2
        pt2 = pt3

    return abs(area) / 2.0


def perimeter(pt_list):
    if len(pt_list) == 0:
        return None

    if len(pt_list) == 1:
        return 0.0

    peri = 0.0
    prev = pt_list[-1]  # The previous point is stored to save time.
    for pt in pt_list:
        peri += point.dist(prev, pt)
        prev = pt

    return peri
