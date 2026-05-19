# interfaz.py

import customtkinter as ctk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from factory import crear_conica_desde_rut
from utils import sin_manual, cos_manual, PI
import math


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
frame_izq.pack(side="left", fill="y", padx=10, pady=10)
frame_izq.pack_propagate(False)

frame_der = ctk.CTkFrame(app)
frame_der.pack(side="right", expand=True, fill="both", padx=10, pady=10)


# =========================================================
# TÍTULO
# =========================================================

titulo = ctk.CTkLabel(
    frame_izq,
    text="Analizador de Cónicas",
    font=("Consolas", 22, "bold")
)
titulo.pack(pady=20)


# =========================================================
# ENTRADA RUT
# =========================================================

label_rut = ctk.CTkLabel(frame_izq, text="Ingrese RUT")
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
textbox.pack(padx=10, pady=20, fill="both", expand=True)


# =========================================================
# GRÁFICO
# =========================================================

fig = plt.Figure(figsize=(7, 6))
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=frame_der)
canvas.get_tk_widget().pack(expand=True, fill="both")


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

conica_actual = None


def limpiar_grafico():
    ax.clear()
    ax.set_title("Gráfico")
    ax.grid(True)
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.axvline(0, color="gray", linewidth=0.8)
    canvas.draw()


def _ejes(titulo_str):
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.axvline(0, color="gray", linewidth=0.8)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.set_aspect("equal")
    ax.legend(fontsize=8)
    ax.set_title(titulo_str)
    canvas.draw()


def _exp(x):
    resultado = 1.0
    termino = 1.0
    for n in range(1, 20):
        termino *= x / n
        resultado += termino
    return resultado


# =========================================================
# MOSTRAR INFO  (adaptado por tipo)
# =========================================================

def mostrar_info(conica):
    textbox.delete("0.0", "end")

    def línea(texto):
        textbox.insert("end", texto + "\n")

    línea(f"Tipo: {conica.tipo}\n")
    línea("Ecuación General:")
    línea(conica.ecuacion_general())
    línea("")
    línea("Ecuación Canónica:")
    línea(conica.ecuacion_canonica())
    línea("")

    tipo = conica.tipo

    if tipo == "Circunferencia":
        línea(f"Centro: ({conica.h}, {conica.k})")
        línea(f"Radio:  {conica.r:.4f}")
        línea(f"r² = {conica.r2}")
        línea(f"Área:      {conica.calcular_area():.4f}")
        línea(f"Perímetro: {conica.calcular_perimetro():.4f}")

    elif tipo == "Elipse":
        línea(f"Centro:      ({conica.h}, {conica.k})")
        línea(f"Orientación: {conica.orientacion}")
        línea(f"a = {conica.a:.4f}  (a² = {conica.a2})")
        línea(f"b = {conica.b:.4f}  (b² = {conica.b2})")
        línea(f"c = {conica.c:.4f}")
        línea(f"Focos: {conica.focos}")

    elif tipo == "Parabola":
        línea(f"Vértice:     {conica.vertice}")
        línea(f"Orientación: {conica.orientacion}")
        línea(f"p = {conica.p:.4f}")
        línea(f"Foco:        {conica.foco}")
        línea(f"Directriz:   {conica.obtener_directriz()}")
        línea(f"Lado recto:  {conica.lado_recto:.4f}")

    elif tipo == "Hiperbola":
        línea(f"Centro:      ({conica.h}, {conica.k})")
        línea(f"Orientación: {conica.orientacion}")
        línea(f"a = {conica.a:.4f}  (a² = {conica.a2})")
        línea(f"b = {conica.b:.4f}  (b² = {conica.b2})")
        línea(f"c = {conica.c:.4f}")
        línea(f"Focos:    {conica.focos}")
        línea(f"Vértices: {conica.vertices}")
        p1, p2 = conica.obtener_asintotas()
        línea(f"Asíntotas: pendientes {p1:.4f} y {p2:.4f}")


# =========================================================
# FUNCIONES DE GRAFICADO (inline, sin plt.show)
# =========================================================

def graficar_circunferencia(c):
    limpiar_grafico()
    pasos = 400
    px, py = [], []
    for i in range(pasos + 1):
        t = 2 * PI * i / pasos
        px.append(c.h + c.r * cos_manual(t))
        py.append(c.k + c.r * sin_manual(t))
    ax.plot(px, py, color="royalblue", linewidth=2)
    ax.scatter([c.h], [c.k], color="black", zorder=5, label="Centro")
    norte, sur, este, oeste = c.obtener_puntos_cardinales()
    for punto, nombre in zip([norte, sur, este, oeste], ["N", "S", "E", "O"]):
        ax.scatter([punto[0]], [punto[1]], color="green", zorder=5)
        ax.annotate(nombre, punto, textcoords="offset points", xytext=(6, 6), fontsize=9)
    _ejes(f"Circunferencia — RUT: {c.rut}")


def graficar_elipse(c):
    limpiar_grafico()
    pasos = 500
    px, py = [], []
    for i in range(pasos + 1):
        t = 2 * PI * i / pasos
        cos_t = cos_manual(t)
        sin_t = sin_manual(t)
        if c.orientacion == "Horizontal":
            px.append(c.h + c.a * cos_t)
            py.append(c.k + c.b * sin_t)
        else:
            px.append(c.h + c.b * cos_t)
            py.append(c.k + c.a * sin_t)
    ax.plot(px, py, color="royalblue", linewidth=2)
    ax.scatter([c.h], [c.k], color="black", zorder=5, label="Centro")
    for foco in c.focos:
        ax.scatter([foco[0]], [foco[1]], color="red", zorder=5)
    princ, secun = c.obtener_vertices()
    for v in princ + secun:
        ax.scatter([v[0]], [v[1]], color="green", zorder=5)
    _ejes(f"Elipse — RUT: {c.rut}")


def graficar_parabola(c):
    limpiar_grafico()
    rango = max(abs(c.p) * 12, 6)
    pasos = 400
    px, py = [], []
    paso = 2 * rango / pasos
    if c.orientacion == "Vertical":
        for i in range(pasos + 1):
            x = c.h - rango + i * paso
            y = c.k + (x - c.h) ** 2 / c.cuatro_p
            px.append(x); py.append(y)
    else:
        for i in range(pasos + 1):
            y = c.k - rango + i * paso
            x = c.h + (y - c.k) ** 2 / c.cuatro_p
            px.append(x); py.append(y)
    ax.plot(px, py, color="royalblue", linewidth=2)
    ax.scatter([c.vertice[0]], [c.vertice[1]], color="black", zorder=5, label="Vértice")
    ax.annotate("V", c.vertice, textcoords="offset points", xytext=(6, 6), fontsize=9)
    ax.scatter([c.foco[0]], [c.foco[1]], color="red", zorder=5, label="Foco")
    ax.annotate("F", c.foco, textcoords="offset points", xytext=(6, 6), fontsize=9)
    if c.directriz_eje == "y":
        ax.axhline(c.directriz_valor, color="orange", linestyle="--",
                   linewidth=1.4, label=f"Directriz y={c.directriz_valor:.3f}")
    else:
        ax.axvline(c.directriz_valor, color="orange", linestyle="--",
                   linewidth=1.4, label=f"Directriz x={c.directriz_valor:.3f}")
    _ejes(f"Parábola — RUT: {c.rut}")


def graficar_hiperbola(c):
    limpiar_grafico()
    pasos = 600
    rango_t = 3.0
    r1x, r1y, r2x, r2y = [], [], [], []
    for i in range(pasos + 1):
        t_val = -rango_t + 2 * rango_t * i / pasos
        ep = _exp(t_val); en = _exp(-t_val)
        cosh_t = (ep + en) / 2
        sinh_t = (ep - en) / 2
        if c.orientacion == "Horizontal":
            r1x.append(c.h + c.a * cosh_t);  r1y.append(c.k + c.b * sinh_t)
            r2x.append(c.h - c.a * cosh_t);  r2y.append(c.k + c.b * sinh_t)
        else:
            r1x.append(c.h + c.b * sinh_t);  r1y.append(c.k + c.a * cosh_t)
            r2x.append(c.h + c.b * sinh_t);  r2y.append(c.k - c.a * cosh_t)
    ax.plot(r1x, r1y, color="royalblue", linewidth=2)
    ax.plot(r2x, r2y, color="royalblue", linewidth=2)
    ax.scatter([c.h], [c.k], color="black", zorder=5, label="Centro")
    for f in c.focos:
        ax.scatter([f[0]], [f[1]], color="red", zorder=5)
    for v in c.vertices:
        ax.scatter([v[0]], [v[1]], color="green", zorder=5)
    p_pos, p_neg = c.obtener_asintotas()
    x_lim = max(abs(x) for x in r1x + r2x) * 1.1
    xs = [-x_lim, x_lim]
    ax.plot(xs, [c.k + p_pos * (x - c.h) for x in xs], "k--", linewidth=1, alpha=0.5, label="Asíntotas")
    ax.plot(xs, [c.k + p_neg * (x - c.h) for x in xs], "k--", linewidth=1, alpha=0.5)
    _ejes(f"Hipérbola — RUT: {c.rut}")


# =========================================================
# DISPATCHER
# =========================================================

def graficar_conica(conica):
    tipo = conica.tipo
    if tipo == "Circunferencia":
        graficar_circunferencia(conica)
    elif tipo == "Elipse":
        graficar_elipse(conica)
    elif tipo == "Parabola":
        graficar_parabola(conica)
    elif tipo == "Hiperbola":
        graficar_hiperbola(conica)
    else:
        messagebox.showwarning("Aviso", f"Tipo '{tipo}' aún no tiene gráfico implementado.")


# =========================================================
# ANALIZAR / LIMPIAR
# =========================================================

def analizar():
    global conica_actual
    rut = entry_rut.get().strip()
    if not rut:
        messagebox.showwarning("Error", "Ingrese un RUT")
        return
    try:
        conica_actual = crear_conica_desde_rut(rut)
        mostrar_info(conica_actual)
        graficar_conica(conica_actual)
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def limpiar():
    global conica_actual
    conica_actual = None
    entry_rut.delete(0, "end")
    textbox.delete("0.0", "end")
    limpiar_grafico()


# =========================================================
# BOTONES
# =========================================================

btn_analizar = ctk.CTkButton(frame_izq, text="Analizar", command=analizar)
btn_analizar.pack(pady=(10, 5))

btn_limpiar = ctk.CTkButton(frame_izq, text="Limpiar", command=limpiar)
btn_limpiar.pack(pady=(0, 10))


# =========================================================
# INICIO
# =========================================================

limpiar_grafico()
app.mainloop()