import tkinter as tk


class KPIFrame(tk.Frame):
    name_lbl = None
    info_lbl = None
    value_lbl = None

    def __init__(self, master=None, kpi=None):
        super().__init__(master)

        self.kpi = kpi

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.name_lbl = tk.Label(self, name="name", text=kpi.name, fg="black", anchor="w")
        self.name_lbl.grid(row=0, column=0, sticky="ew")
        self.name_lbl.config(font="Helvetica 8 bold", borderwidth=0)

        self.info_lbl = tk.Label(master=self, name="info", text=kpi.info, fg="#333", anchor="w")
        self.info_lbl.grid(row=1, column=0, padx=3, sticky="ew")
        self.info_lbl.config(font="Helvetica 7 normal", borderwidth=0)

        self.value_lbl = tk.Label(master=self, name="value", fg="#22C")
        self.value_lbl.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.value_lbl.config(text=(("%.3f" % kpi.value) if kpi.value else "-"), font="Helvetica 10 bold", borderwidth=0)

    def update(self):
        self.name_lbl.config(text=self.kpi.name)
        self.info_lbl.config(text=self.kpi.info)
        self.value_lbl.config(text=(("%.3f" % self.kpi.value) if self.kpi.value else "-"))
