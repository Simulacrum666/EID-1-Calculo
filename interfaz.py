# interfaz.py

import customtkinter as ctk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from factory import crear_conica_desde_rut

from utils import sin_manual
from utils import cos_manual
from utils import PI


# =========================================================
# CONFIG
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# VENTANA
# =========================================================

app = ctk.CTk()

app.title("Proyecto MAT1186")
app.geometry("1200x700")


# =========================================================
# LAYOUT
# =========================================================

frame_izq = ctk.CTkFrame(app, width=350)

frame_izq.pack(
    side="left",
    fill="y",
    padx=10,
    pady=10
)

frame_izq.pack_propagate(False)


frame_der = ctk.CTkFrame(app)

frame_der.pack(
    side="right",
    expand=True,
    fill="both",
    padx=10,
    pady=10
)


# =========================================================
# TITULO
# =========================================================

titulo = ctk.CTkLabel(
    frame_izq,
    text="Analizador de Elipses",
    font=("Consolas", 24, "bold")
)

titulo.pack(pady=20)


# =========================================================
# ENTRADA RUT
# =========================================================

label_rut = ctk.CTkLabel(
    frame_izq,
    text="Ingrese RUT"
)

label_rut.pack(pady=(10, 0))


entry_rut = ctk.CTkEntry(
    frame_izq,
    width=250,
    height=35,
    placeholder_text="12.345.678-5"
)

entry_rut.pack(pady=10)


# =========================================================
# INFO
# =========================================================

textbox = ctk.CTkTextbox(
    frame_izq,
    width=300,
    height=400,
    font=("Consolas", 12)
)

textbox.pack(
    padx=10,
    pady=20,
    fill="both",
    expand=True
)


# =========================================================
# GRAFICO
# =========================================================

fig = plt.Figure(figsize=(7, 6))

ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(
    fig,
    master=frame_der
)

canvas.get_tk_widget().pack(
    expand=True,
    fill="both"
)


# =========================================================
# FUNCIONES
# =========================================================

conica_actual = None


def limpiar_grafico():

    ax.clear()

    ax.set_title("Gráfico")

    ax.grid(True)

    ax.axhline(0)
    ax.axvline(0)

    canvas.draw()


def mostrar_info(conica):

    textbox.delete("0.0", "end")

    textbox.insert("end", f"Tipo: {conica.tipo}\n\n")

    textbox.insert(
        "end",
        "Ecuación General:\n"
    )

    textbox.insert(
        "end",
        conica.ecuacion_general()
    )

    textbox.insert("end", "\n\n")

    textbox.insert(
        "end",
        "Ecuación Canónica:\n"
    )

    textbox.insert(
        "end",
        conica.ecuacion_canonica()
    )

    textbox.insert("end", "\n\n")

    textbox.insert(
        "end",
        f"Centro:\n({conica.h}, {conica.k})\n\n"
    )

    textbox.insert(
        "end",
        f"Orientación:\n{conica.orientacion}\n\n"
    )

    textbox.insert(
        "end",
        f"a = {conica.a}\n"
    )

    textbox.insert(
        "end",
        f"b = {conica.b}\n"
    )

    textbox.insert(
        "end",
        f"c = {conica.c}\n\n"
    )

    textbox.insert(
        "end",
        f"Focos:\n{conica.focos}"
    )


def graficar_elipse(conica):

    limpiar_grafico()

    puntos_x = []
    puntos_y = []

    pasos = 500

    for i in range(pasos + 1):

        t = 2 * PI * i / pasos

        cos_t = cos_manual(t)
        sin_t = sin_manual(t)

        if conica.orientacion == "Horizontal":

            x = conica.h + conica.a * cos_t
            y = conica.k + conica.b * sin_t

        else:

            x = conica.h + conica.b * cos_t
            y = conica.k + conica.a * sin_t

        puntos_x.append(x)
        puntos_y.append(y)

    ax.plot(puntos_x, puntos_y)

    # Centro
    ax.scatter(
        [conica.h],
        [conica.k]
    )

    # Focos
    for foco in conica.focos:

        ax.scatter(
            [foco[0]],
            [foco[1]]
        )

    ax.grid(True)

    ax.axhline(0)
    ax.axvline(0)

    ax.set_aspect("equal")

    ax.set_title(
        f"Elipse generada por {conica.rut}"
    )

    canvas.draw()


def analizar():

    global conica_actual

    rut = entry_rut.get().strip()

    if not rut:

        messagebox.showwarning(
            "Error",
            "Ingrese un RUT"
        )

        return

    try:

        conica_actual = crear_conica_desde_rut(rut)

        mostrar_info(conica_actual)

        graficar_elipse(conica_actual)

    except ValueError as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


def limpiar():

    global conica_actual

    conica_actual = None

    entry_rut.delete(0, "end")

    textbox.delete("0.0", "end")

    limpiar_grafico()


# =========================================================
# BOTONES
# =========================================================

btn_analizar = ctk.CTkButton(
    frame_izq,
    text="Analizar",
    command=analizar
)

btn_analizar.pack(
    pady=(10, 5)
)


btn_limpiar = ctk.CTkButton(
    frame_izq,
    text="Limpiar",
    command=limpiar
)

btn_limpiar.pack(
    pady=(0, 10)
)


# =========================================================
# INICIO
# =========================================================

limpiar_grafico()

app.mainloop()