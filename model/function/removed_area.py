from model.function.a_simplexfunction import ASimplexFunction


class RemovedArea(ASimplexFunction):
    def __init__(self):
        self.name = "SURFACE RETIRÉE"

    def calculate(self, left_pt, mid_pt, right_pt):
        return abs((left_pt.y - right_pt.y)*(right_pt.x - mid_pt.x) - (left_pt.x - right_pt.x)*(right_pt.y - mid_pt.y)) / 2.0