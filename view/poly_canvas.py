import properties as ppt

from model.point import Point
from view.mobile_canvas import MobileCanvas


###############
#  CONSTANTS  #
###############

P_COLOR = ppt.get("poly_color")
P_BORDER_COLOR = ppt.get("poly_border_color")
P_BORDER_THICKNESS = float(ppt.get("poly_border_thickness"))

PT_COLOR = ppt.get("poly_point_color")
PT_RADIUS = float(ppt.get("poly_point_radius"))
PT_BORDER_COLOR = ppt.get("poly_point_border_color")
PT_BORDER_THICKNESS = float(ppt.get("poly_point_border_thickness"))

SP_COLOR = ppt.get("simple_poly_color")
SP_BORDER_COLOR = ppt.get("simple_poly_border_color")
SP_BORDER_THICKNESS = float(ppt.get("simple_poly_border_thickness"))

SPT_COLOR = ppt.get("simple_poly_point_color")
SPT_RADIUS = float(ppt.get("simple_poly_point_radius"))
SPT_BORDER_COLOR = ppt.get("simple_poly_point_border_color")
SPT_BORDER_THICKNESS = float(ppt.get("simple_poly_point_border_thickness"))

SPT_TEXT_COLOR = ppt.get("simple_poly_point_text_color")
SPT_TEXT_SIZE = int(ppt.get("simple_poly_point_text_size"))


#############
#  CLASSES  #
#############

class PolyCanvas(MobileCanvas):
    _poly = []
    _polyID = None
    _poly_pointsID = []

    _simple_poly = []
    _simple_polyID = None
    _simple_poly_pointsID = []
    _simple_poly_numbersID = []

    def __init__(self, root, width, height, bg, zoom=1.0, zstep=0.05, display_points=True, display_text=False):
        super().__init__(root, width=width, height=height, bg=bg)

        self._zoom = zoom
        self.zoomfactor = MobileCanvas.MULT_ZOOM(zstep)
        self._display_points = display_points
        self._display_text = display_text

        self._polyID = self.create_polygon(0, 0, fill=P_COLOR, outline=P_BORDER_COLOR, width=P_BORDER_THICKNESS)
        self._poly = [Point(0, 0)]
        self._simple_polyID = self.create_polygon(0, 0, fill=SP_COLOR, outline=SP_BORDER_COLOR, width=SP_BORDER_THICKNESS)
        self._simple_poly = [Point(0, 0)]

        self.bind("<MouseWheel>", self._wheel_handler)

        self._draw_points()

    @property
    def display_points(self):
        return self._display_points

    @display_points.setter
    def display_points(self, value):
        self._display_points = value
        self._draw_points()

    @property
    def display_text(self):
        return self._display_text

    @display_text.setter
    def display_text(self, value):
        self._display_text = value
        self._draw_points()

    def add_point(self, pt):
        self._poly.append(pt)
        self._draw_points()

    def add_points(self, pt_list):
        for pt in pt_list:
            self._poly.append(pt)

        self._draw_points()

    def remove_point(self, pt):
        if type(pt) is int:
            del self._poly[pt]
        else:
            self._poly.remove(pt)

        self._draw_points()

    def remove_points(self, pt_list):
        for pt in pt_list:
            self._poly.remove(pt)

        self._draw_points()

    def add_simple_point(self, pt):
        self._simple_poly.append(pt)
        self._draw_points()

    def add_simple_points(self, pt_list):
        for pt in pt_list:
            self._simple_poly.append(pt)

        self._draw_points()

    def remove_simple_point(self, pt):
        if type(pt) is int:
            del self._simple_poly[pt]
        else:
            self._simple_poly.remove(pt)

        self._draw_points()

    def remove_simple_points(self, pt_list):
        for pt in pt_list:
            self._simple_poly.remove(pt)

        self._draw_points()

    def clear(self):
        self._poly.clear()
        self._simple_poly.clear()

        self._draw_points()

    def reset(self):
        self._simple_poly.clear()
        for pt in self._poly:
            self._simple_poly.append(pt)

        self._draw_points()

    def _draw_points(self):
        if len(self._poly) > 0:
            # Polygon update
            pt_list = [nb for pt in self._poly for nb in pt.tuple()]
            self.coords(self._polyID, pt_list)

            for pid in self._poly_pointsID:
                self.delete(pid)

            self._poly_pointsID.clear()
            if self._display_points:
                for pt in self._poly:
                    self._poly_pointsID.append(self.create_oval(pt.x - PT_RADIUS, pt.y - PT_RADIUS, pt.x + PT_RADIUS, pt.y + PT_RADIUS, fill=PT_COLOR, outline=PT_BORDER_COLOR, width=PT_BORDER_THICKNESS))

        if len(self._simple_poly) > 0:
            # Simple polygon update
            simplept_list = [nb for pt in self._simple_poly for nb in pt.tuple()]
            self.coords(self._simple_polyID, simplept_list)
            # The simple polygon must be displayed over the polygon points, so that it is visible when seen far.
            self.tag_raise(self._simple_polyID)

            for pid in self._simple_poly_pointsID:
                self.delete(pid)

            self._simple_poly_pointsID.clear()
            if self._display_points:
                for pt in self._simple_poly:
                    self._simple_poly_pointsID.append(self.create_oval(pt.x - SPT_RADIUS, pt.y - SPT_RADIUS, pt.x + SPT_RADIUS, pt.y + SPT_RADIUS, fill=SPT_COLOR, outline=SPT_BORDER_COLOR, width=SPT_BORDER_THICKNESS))

            for nid in self._simple_poly_numbersID:
                self.delete(nid)

            self._simple_poly_numbersID.clear()
            if self._display_text:
                counter = 0
                for pt in self._simple_poly:
                    self._simple_poly_numbersID.append(self.create_text(pt.x, pt.y, text=str(counter), font=("Roboto %d bold" % SPT_TEXT_SIZE), fill=SPT_TEXT_COLOR))
                    counter += 1

    def _wheel_handler(self, event):
        super()._zoom(event)

        # The font size is linked to the zoom
        if self._display_text:
            for nid in self._simple_poly_numbersID:
                self.itemconfig(nid, font=("Roboto %d bold" % (SPT_TEXT_SIZE * self._zoom)), fill=SPT_TEXT_COLOR)
