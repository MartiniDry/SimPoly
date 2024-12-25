import math

from model.function.a_simplexfunction import ASimplexFunction


class PointGap(ASimplexFunction):
    def __init__(self):
        self.name = "ÉCART DU SOMMET"

    def calculate(self, left_pt, mid_pt, right_pt):
        """
        For a given triplet, calculates the distance between the middle point and the segment defined by the two other points.
        :param left_pt: left point of the triplet
        :param mid_pt: middle point of the triplet
        :param right_pt: right point of the triplet
        :return:
        """

        if left_pt.x == right_pt.x:  # For a vertical segment, ...
            return abs(mid_pt.x - left_pt.x)  # ...the distance is defined by the horizontal gap.

        m = (left_pt.y - right_pt.y) / (left_pt.x - right_pt.x)
        p = (right_pt.y * left_pt.x - left_pt.y * right_pt.x) / (left_pt.x - right_pt.x)

        return abs(mid_pt.y - m*mid_pt.x - p) / math.sqrt(1 + m*m)