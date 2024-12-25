import properties as ppt
import tkinter as tk
from tkinter import ttk

from model import main_model
from view.kpi_frame import KPIFrame
from view.poly_canvas import PolyCanvas


###############
#  VARIABLES  #
###############

_WINDOW = tk.Tk()

# Zone 1: polygon generation zone
z1_frm = tk.LabelFrame(_WINDOW, text="GÉNÉRATION")
z1_lbl = tk.Label(z1_frm, text="Nombre de points :")
z1_txt = tk.Text(z1_frm, width=5, height=1)
z1_btn = tk.Button(z1_frm, text="CRÉER", bg="lightblue", anchor="center")

# Zone 2: choice of the simplification criterion
z2_frm = tk.LabelFrame(_WINDOW, text="CRITÈRE D'ÉTUDE")
z2_stv = tk.StringVar()
z2_cmb = tk.ttk.Combobox(z2_frm, textvariable=z2_stv, state="readonly")
z2_blv = tk.BooleanVar()
z2_rad = tk.Checkbutton(z2_frm, variable=z2_blv, onvalue=True, offvalue=False, text="Calcul temps-réel")

# Zone 3: choice of the number of visible points
z3_frm = tk.Frame(_WINDOW)
z3_btnL = tk.Button(z3_frm, text="◀")
z3_btnR = tk.Button(z3_frm, text="▶")
z3_lblX = tk.Label(z3_frm, width=4, height=1, text="0")

# Zone 4: "resize" action
z4_btn = tk.Button(_WINDOW, text="CADRER", bg="lightblue")

# Zone 5: performance zone
z5_frm = tk.LabelFrame(_WINDOW, text="KPI")
z5_lbl = tk.Label(z5_frm, text="Exemple")
z5_kpis = {}

_CANVAS_WIDTH = int(ppt.get("canvas_width"))
_CANVAS_HEIGHT = int(ppt.get("canvas_height"))
canvas = PolyCanvas(_WINDOW, width=_CANVAS_WIDTH, height=_CANVAS_HEIGHT, bg='lightgrey')


###############
#  CONSTANTS  #
###############

NORMAL_FONT = "Helvetica 12 normal"
BOLD_FONT = "Helvetica 12 bold"


###############
#  FUNCTIONS  #
###############

def load(with_points=True, with_text=False):
    print("Loading main window")

    # Setting the global window configuration
    _WINDOW.title(ppt.get("app_name") + " v" + ppt.get("version"))
    _WINDOW.iconbitmap(ppt.get("app_icon"))
    _WINDOW.resizable(False, False)
    _WINDOW.configure(padx=5, pady=5)
    _WINDOW.grid_rowconfigure(4, weight=1)  # All rows will be sized to their components, except the last one.

    # Placing all components inside the window
    z1_frm.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    z1_lbl.grid(row=0, column=0)
    z1_txt.grid(row=0, column=1, padx=5)
    z1_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    z2_frm.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    z2_cmb.grid(row=0, column=0, padx=5, pady=5)
    z2_rad.grid(row=1, column=0, padx=5)

    z3_frm.grid(row=2, column=0, padx=5, pady=15)
    z3_btnL.grid(row=0, column=0)
    z3_lblX.grid(row=0, column=1)
    z3_btnR.grid(row=0, column=2)

    z4_btn.grid(row=3, column=0, padx=5)

    z5_frm.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
    z5_lbl.grid(row=0, column=0)

    canvas.grid(row=0, column=1, rowspan=6)

    # Configuration of all components
    z1_btn.configure(command=generate)

    z2_cmb["values"] = [sf.name for sf in main_model.SIMPLEX_FUNCTIONS.values()]  # Combo box items are defined
    z2_stv.set(main_model.get_simplex().name)
    z2_cmb.bind('<<ComboboxSelected>>', lambda _: choose_func())
    z2_rad.configure(command=polygon_render)

    z3_btnL.configure(command=decrement, state=tk.DISABLED, font=NORMAL_FONT)
    z3_btnR.configure(command=increment, state=tk.DISABLED, font=NORMAL_FONT)

    z4_btn.configure(command=canvas.autosize)

    for i in range(len(main_model.KPIS.items())):
        lbl, kpi = list(main_model.KPIS.items())[i]
        z5_kpis[lbl] = KPIFrame(z5_frm, kpi=kpi)
        z5_kpis[lbl].grid(row=i, padx=2, pady=2, sticky="nsew")

    _WINDOW.update()
    canvas.configure(highlightthickness=0)  # The highlight zone is deleted in order to have the required canvas dimensions.
    canvas.display_points = with_points
    canvas.display_text = with_text
    ######
    # main_model.load(30)
    # refresh()
    # canvas.autosize()
    #
    # z3_btnL.configure(state=tk.NORMAL, font=BOLD_FONT)
    # z3_lblX.configure(text=len(main_model.get_polygon()))
    # z3_btnR.configure(state=tk.DISABLED, font=NORMAL_FONT)
    ######
    refresh()
    _WINDOW.mainloop()


def refresh():
    # Reset the canvas display
    canvas.clear()
    canvas.add_points(main_model.get_polygon())
    canvas.add_simple_points(main_model.get_simple_polygon())

    for (lbl, kpi) in main_model.KPIS.items():
        kpi.calculate(main_model.get_simple_polygon(), main_model.get_polygon())
        z5_kpis[lbl].update()


def generate():
    value = int(z1_txt.get("1.0", tk.END))
    main_model.load(value)
    refresh()
    canvas.autosize()

    if value > 3:
        z3_btnL.configure(state=tk.NORMAL, font=BOLD_FONT)
    else:
        z3_btnL.configure(state=tk.DISABLED, font=NORMAL_FONT)

    z3_lblX.configure(text=len(main_model.get_polygon()))
    z3_btnR.configure(state=tk.DISABLED, font=NORMAL_FONT)


def polygon_render():
    main_model.real_time_rendering = z2_blv.get()
    main_model.reset()
    refresh()

    # Reset the point incrementer
    z3_lblX.configure(text=len(main_model.get_polygon()))
    z3_btnR.configure(state=tk.DISABLED, font=NORMAL_FONT)
    z3_btnL.configure(state=tk.NORMAL, font=BOLD_FONT)


def increment():
    value = int(z3_lblX.cget("text"))
    if value < len(main_model.get_polygon()):
        value += 1
        z3_lblX.configure(text=value)
        z3_btnL.configure(state=tk.NORMAL, font=BOLD_FONT)

    if main_model.real_time_rendering:
        main_model.include_best_point()
    else:
        main_model.select_simple_points(value)

    refresh()
    if value == len(main_model.get_polygon()):
        z3_btnR.configure(state=tk.DISABLED, font=NORMAL_FONT)
    else:
        z3_btnR.configure(state=tk.NORMAL, font=BOLD_FONT)


def decrement():
    value = int(z3_lblX.cget("text"))
    if value > 3:
        value -= 1
        z3_lblX.configure(text=value)
        z3_btnR.configure(state=tk.NORMAL, font=BOLD_FONT)

    if main_model.real_time_rendering:
        main_model.exclude_best_point()
    else:
        main_model.select_simple_points(value)

    refresh()
    if value == 3:
        z3_btnL.configure(state=tk.DISABLED, font=NORMAL_FONT)
    else:
        z3_btnL.configure(state=tk.NORMAL, font=BOLD_FONT)


def choose_func():
    name = str(z2_stv.get())
    label = [k for (k, v) in main_model.SIMPLEX_FUNCTIONS.items() if v.name == name]
    main_model.set_simplex(label[0])

    # Once the new function is defined, the model and the canvas are reset to initiate it.
    main_model.reset()
    canvas.reset()

    for (lbl, kpi) in main_model.KPIS.items():
        kpi.calculate(main_model.get_simple_polygon(), main_model.get_polygon())
        z5_kpis[lbl].update()

    z3_btnR.configure(state=tk.DISABLED, font=NORMAL_FONT)
    z3_lblX.configure(text=len(main_model.get_polygon()))
    z3_btnL.configure(state=tk.NORMAL, font=BOLD_FONT)
