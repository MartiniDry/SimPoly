from tkinter import Canvas


class MobileCanvas(Canvas):
    @staticmethod
    def EXP_ZOOM(coeff):
        return lambda me: coeff ** me

    @staticmethod
    def MULT_ZOOM(coeff):
        return lambda me: (1+coeff if me >= 0 else 1-coeff)

    def __init__(self, parent, zoom=1.0, **kwargs):
        super().__init__(parent, **kwargs)
        self.zoom = zoom
        self.zoomfactor = MobileCanvas.MULT_ZOOM(0.2)  # MobileCanvas.EXP_ZOOM(1.001)

        self.start_x = 0
        self.start_y = 0
        self.translate_x = 0
        self.translate_y = 0
        self.original_coords = {}

        self.bind("<ButtonPress-1>", self._start_pan)
        self.bind("<B1-Motion>", self._pan)
        self.bind("<MouseWheel>", self._zoom)

    def _start_pan(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def _pan(self, event):
        self.translate_x += (event.x - self.start_x)
        self.translate_y += (event.y - self.start_y)
        self.scan_dragto(int(self.translate_x), int(self.translate_y), gain=1)

        self.start_x = event.x
        self.start_y = event.y

    def _zoom(self, event):
        factor = self.zoomfactor(event.delta)  # Calculating the zoom factor
        self.zoom *= factor

        # Zoom is applied using the cursor as a fixed point.
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        print("event! %f_%f -> %f_%f" % (event.x, event.y, x, y))
        self.scale("all", x, y, factor, factor)

        # self.translate_x = (self.translate_x - x) * factor + x
        # self.translate_y = (self.translate_y - y) * factor + y
        # self.scan_dragto(int((self.translate_x - x) * factor + x), int((self.translate_y - y) * factor + y), gain=1)

        self.start_x = x
        self.start_y = y

    def create_oval(self, __x0, __y0, __x1, __y1, **kwargs):
        item = super().create_oval( __x0, __y0, __x1, __y1, **kwargs)
        self.original_coords[item] = [__x0, __y0, __x1, __y1]
        self.scale(item, 0, 0, self.zoom, self.zoom)
        return item

    def create_polygon(self, *coords, **kwargs):
        item = super().create_polygon(coords, **kwargs)
        self.original_coords[item] = coords
        self.scale(item, 0, 0, self.zoom, self.zoom)
        return item

    def create_text(self, __x, __y, **kwargs):
        item = super().create_text(__x, __y, **kwargs)
        self.original_coords[item] = [__x, __y]
        self.scale(item, 0, 0, self.zoom, self.zoom)
        return item

    def create_line(self, __x0, __y0, __x1, __y1, **kwargs):
        item = super().create_line(__x0, __y0, __x1, __y1, **kwargs)
        self.original_coords[item] = [__x0, __y0, __x1, __y1]
        self.scale(item, 0, 0, self.zoom, self.zoom)
        return item

    def create_rectangle(self, __x0, __y0, __x1, __y1, **kwargs):
        item = super().create_rectangle(__x0, __y0, __x1, __y1, **kwargs)
        self.original_coords[item] = [__x0, __y0, __x1, __y1]
        self.scale(item, 0, 0, self.zoom, self.zoom)
        return item

    def coords(self, *args):
        item = args[0]
        data = args[1:][0]

        coordinates = super().coords(item, data)
        self.original_coords[item] = data
        self.scale(item, 0, 0, self.zoom, self.zoom)
        return coordinates

    def autosize(self):
        min_x, min_y, max_x, max_y = self.bbox("all")
        factor = min(self.winfo_width() / (max_x - min_x), self.winfo_height() / (max_y - min_y))
        self.zoom *= factor

        self.scale("all", 0, 0, factor, factor)
        self.center_items()

    def center_items(self):
        min_x, min_y, max_x, max_y = self.bbox("all")
        offset_x = (self.winfo_width() - max_x - min_x) / 2
        offset_y = (self.winfo_height() - max_y - min_y) / 2

        self.translate_x = offset_x
        self.translate_y = offset_y
        self.scan_dragto(int(self.translate_x), int(self.translate_y), gain=1)
        self.start_x = 0
        self.start_y = 0
