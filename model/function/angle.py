import math

from model import point
from model.function.a_simplexfunction import ASimplexFunction


class Angle(ASimplexFunction):
    def __init__(self):
        self.name = "ANGLE AU SOMMET"

    def calculate(self, left_pt, mid_pt, right_pt):
        norm_ml = point.dist(mid_pt, left_pt)
        norm_mr = point.dist(mid_pt, right_pt)
        # Scalar product of ML and MR
        scal = (left_pt.x - mid_pt.x) * (right_pt.x - mid_pt.x) + (left_pt.y - mid_pt.y) * (right_pt.y - mid_pt.y)
        angle = math.acos(scal / (norm_ml * norm_mr))

        return math.pi - angle
