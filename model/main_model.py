import properties as ppt

from model import polygon_generator as pgen
from model.function.linear_regression import LinearRegression
from model.function.point_gap import PointGap
from model.function.removed_area import RemovedArea
from model.function.angle import Angle
from model.kpi.area_ratio import AreaRatio
from model.kpi.perimeter_ratio import PerimeterRatio


###############
#  CONSTANTS  #
###############

# Map of functions that evaluates the approximation level of a given point
SIMPLEX_FUNCTIONS = {
    "lin_reg": LinearRegression(),
    "area": RemovedArea(),
    "distance": PointGap(),
    "angle": Angle()
}

KPIS = {
    "area": AreaRatio(),
    "peri": PerimeterRatio()
}


###############
#  VARIABLES  #
###############

_polygon_plus = dict()  # Dictionary of points with the associated
_exclusion_stack = []  # Stack of points that are excluded from the visible polygon.
# The choice of the stack enables to undo an operation and re-include polygon points in the correct order.

_slbl = ppt.get("simplex_function")  # ID of the current simplex function used in the model

# If True, the coefficients are recalculated each time a point is hidden or included in the display.
# If False, coefficients are only calculated at the beginning.
real_time_rendering = False


#############
#  CLASSES  #
#############

class Data:
    present: bool
    coeff: float

    def __init__(self, present=True, coeff=0.0):
        self.present = present
        self.coeff = coeff

    def __str__(self):
        return "(%s -> coeff=%g)" % ("present" if self.present else "absent", self.coeff)


###############
#  FUNCTIONS  #
###############

def get_polygon():
    return list(_polygon_plus.keys())


def get_simple_polygon():
    return [pt for (pt, d) in _polygon_plus.items() if d.present]


def get_simplex():
    return SIMPLEX_FUNCTIONS[_slbl]


def set_simplex(label):
    global _slbl

    if not SIMPLEX_FUNCTIONS[label]:
        raise ValueError("The given name is not a valid SIMPLEX_FUNCTIONS method.")

    _slbl = label


def load(nb):
    # At least 3 points must be used to define a polygon.
    if nb < 3:
        return None

    _exclusion_stack.clear()

    # Creation of nb random points between 0 and 100
    _polygon_plus.clear()
    ############
    # polygon = pgen.imperfect_disc(nb)
    polygon = pgen.from_file("chat.spl")
    # polygon = pgen.rectangle()
    # polygon = pgen.invader()
    ############
    for pt in polygon:
        _polygon_plus[pt] = Data()  # Initialization of the polygon data

    if len(_polygon_plus.items()) >= 3:  # At least 3 distinct points are needed to calculate coefficients.
        _calculate_all()
        for v in KPIS.values():
            v.calculate(get_simple_polygon(), get_polygon())


def reset():  # The main difference with 'load' is that we keep the existing points.
    _exclusion_stack.clear()

    for (pt, d) in _polygon_plus.items():
        d.present = True
        d.coeff = 0.0

    if len(_polygon_plus.items()) >= 3:  # At least 3 distinct points are needed to calculate coefficients.
        _calculate_all()
        for v in KPIS.values():
            v.calculate(get_simple_polygon(), get_polygon())


def select_simple_points(nb):
    # TODO: manage '_exclusion_stack' to include the worst points in the good order i.e. all elements of ...
    #  ...'sorted_index_and_data' that are not in 'new_index_and_data'. I would enable 'on/off' real-time transition.

    index_and_data = {}
    index = 0
    for (pt, d) in _polygon_plus.items():
        d.present = False  # All points are hidden only to display the selected ones at the end.
        index_and_data[index] = d
        index += 1

    sorted_index_and_data = dict(sorted(index_and_data.items(), key=lambda item: item[1].coeff, reverse=True))

    sorted_index_and_data = dict(list(sorted_index_and_data.items())[:nb])
    new_index_and_data = dict(sorted(sorted_index_and_data.items()))

    point_list = list(_polygon_plus.keys())
    for (i, d) in new_index_and_data.items():
        pt = point_list[i]
        _polygon_plus[pt].present = True
        _polygon_plus[pt].coeff = d.coeff


def include_best_point():
    best_point = _exclusion_stack.pop()
    _polygon_plus[best_point].present = True

    # Coefficient calculation for the best point and its neighbours
    _calculate(best_point)

    polygon = get_simple_polygon()
    i = polygon.index(best_point)
    _calculate(polygon[i - 1])
    _calculate(polygon[(i + 1) % len(polygon)])

    for v in KPIS.values():
        v.calculate(get_simple_polygon(), get_polygon())


def exclude_best_point():
    only_present_polygon_plus = dict([item for item in _polygon_plus.items() if item[1].present])
    (best_point, data) = min(only_present_polygon_plus.items(), key=lambda item: item[1].coeff)

    # Identify the neighbouring points
    polygon = get_simple_polygon()
    i = polygon.index(best_point)
    left_point = polygon[i - 1]
    right_point = polygon[(i + 1) % len(polygon)]

    # Now that points are identified, we can safely exclude best_point
    data.present = False
    _exclusion_stack.append(best_point)

    # Finally, recalculate the neighbouring points coefficients
    _calculate(left_point)
    _calculate(right_point)

    for v in KPIS.values():
        v.calculate(get_simple_polygon(), get_polygon())


def _calculate(pt):
    polygon = get_simple_polygon()
    i = polygon.index(pt)

    sfunc = SIMPLEX_FUNCTIONS[_slbl]
    _polygon_plus[pt].coeff = sfunc.calculate(polygon[i - 1], pt, polygon[(i + 1) % len(polygon)])


def _calculate_all():
    """
    Calculates the alignment coefficient for each point of the polygon. A coefficient of zero will be set for all absent points.
    :return: dictionary of coefficients, sorted in the reverse order.
    """
    for (pt, d) in _polygon_plus.items():
        d.coeff = 0.0  # Coefficients are reset before being evaluated

    polygon = get_simple_polygon()
    sfunc = SIMPLEX_FUNCTIONS[_slbl]

    nbpts = len(polygon)
    coefficients = [0.0] * nbpts

    # First item
    coefficients[0] = sfunc.calculate(polygon[-1], polygon[0], polygon[1])
    _polygon_plus[polygon[0]].coeff = coefficients[0]

    # Last item
    coefficients[-1] = sfunc.calculate(polygon[-2], polygon[-1], polygon[0])
    _polygon_plus[polygon[-1]].coeff = coefficients[-1]

    # The middle (c'est moins bien que Malcolm)
    for i in range(1, nbpts - 1):
        coefficients[i] = sfunc.calculate(polygon[i - 1], polygon[i], polygon[i + 1])
        _polygon_plus[polygon[i]].coeff = coefficients[i]
