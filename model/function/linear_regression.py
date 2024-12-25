from model.function.a_simplexfunction import ASimplexFunction


class LinearRegression(ASimplexFunction):
    def __init__(self):
        self.name = "RÉGRESSION LINÉAIRE"

    def calculate(self, left_pt, mid_pt, right_pt):
        moy_x = (left_pt.x + mid_pt.x + right_pt.x) / 3.0
        moy_y = (left_pt.y + mid_pt.y + right_pt.y) / 3.0

        var_x = (left_pt.x ** 2 + mid_pt.x ** 2 + right_pt.x ** 2) / 3.0 - moy_x ** 2
        var_y = (left_pt.y ** 2 + mid_pt.y ** 2 + right_pt.y ** 2) / 3.0 - moy_y ** 2
        cov_xy = (left_pt.x * left_pt.y + mid_pt.x * mid_pt.y + right_pt.x * right_pt.y) / 3.0 - moy_x * moy_y

        if var_x == 0 or var_y == 0:
            return 1.0

        # Linear regression function: y = a*x + b
        a = cov_xy / var_x
        b = moy_y - a * moy_x
        func = lambda x: a * x + b

        # Return the R2 coefficient
        denominator = 3.0 * var_y
        numerator = (left_pt.y - func(left_pt.x)) ** 2 + (mid_pt.y - func(mid_pt.x)) ** 2 + (right_pt.y - func(right_pt.x)) ** 2

        return numerator / denominator  # The returned value is not R2 but (1 - R2).
