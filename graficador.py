# graficador.py
#
# Responsabilidad única: calcular y dibujar los puntos de cada cónica
# sobre un eje de matplotlib ya existente (ax). No conoce Tkinter ni
# la ventana — solo recibe el eje y la cónica a graficar.
# Limpiar el eje, poner título y refrescar el canvas es responsabilidad
# de quien llama (interfaz.py), no de este módulo.

from utils import sin_manual, cos_manual, PI


def _exp_manual(x):
    """e^x aproximado con serie de Taylor (20 términos), sin usar la librería math."""
    resultado = 1.0
    termino = 1.0
    for n in range(1, 20):
        termino *= x / n
        resultado += termino
    return resultado


def dibujar_conica(ax, conica):
    """Dibuja la curva y los elementos relevantes de 'conica' sobre 'ax'."""
    tipo = conica.tipo
    pasos = 400

    if tipo == "Circunferencia":
        _dibujar_circunferencia(ax, conica, pasos)
    elif tipo == "Elipse":
        _dibujar_elipse(ax, conica, pasos)
    elif tipo == "Parabola":
        _dibujar_parabola(ax, conica, pasos)
    elif tipo == "Hiperbola":
        _dibujar_hiperbola(ax, conica, pasos)
    else:
        raise ValueError(f"Tipo de cónica no reconocido: {tipo}")


def _dibujar_circunferencia(ax, conica, pasos):
    puntos_x, puntos_y = [], []
    for i in range(pasos + 1):
        t = 2 * PI * i / pasos
        puntos_x.append(conica.h + conica.r * cos_manual(t))
        puntos_y.append(conica.k + conica.r * sin_manual(t))
    ax.plot(puntos_x, puntos_y, color="royalblue", linewidth=2, label="Circunferencia")
    ax.scatter([conica.h], [conica.k], color="red", zorder=5, label="Centro")


def _dibujar_elipse(ax, conica, pasos):
    puntos_x, puntos_y = [], []
    for i in range(pasos + 1):
        t = 2 * PI * i / pasos
        if conica.orientacion == "Horizontal":
            puntos_x.append(conica.h + conica.a * cos_manual(t))
            puntos_y.append(conica.k + conica.b * sin_manual(t))
        else:
            puntos_x.append(conica.h + conica.b * cos_manual(t))
            puntos_y.append(conica.k + conica.a * sin_manual(t))
    ax.plot(puntos_x, puntos_y, color="seagreen", linewidth=2, label="Elipse")
    ax.scatter([conica.h], [conica.k], color="black", zorder=5, label="Centro")


def _dibujar_parabola(ax, conica, pasos):
    # Rango de graficación adaptativo para la parábola
    if conica.orientacion == "Vertical":
        xs = [conica.h - 10 + (i * 20 / pasos) for i in range(pasos + 1)]
        ys = [((x - conica.h) ** 2 / (4 * conica.p)) + conica.k for x in xs]
    else:
        ys = [conica.k - 10 + (i * 20 / pasos) for i in range(pasos + 1)]
        xs = [((y - conica.k) ** 2 / (4 * conica.p)) + conica.h for y in ys]
    ax.plot(xs, ys, color="darkorange", linewidth=2, label="Parábola")
    ax.scatter([conica.vertice[0]], [conica.vertice[1]], color="red", zorder=5, label="Vértice")


def _dibujar_hiperbola(ax, conica, pasos):
    # Dibujar las dos ramas de la hipérbola
    t_vals = [-2.5 + (i * 5 / pasos) for i in range(pasos + 1) if i != pasos // 2]
    for signo in [-1, 1]:
        xs, ys = [], []
        for t in t_vals:
            # cosh(t) y sinh(t) calculados manualmente a partir de e^t y e^-t
            # (sin usar la librería math)
            e_pos = _exp_manual(t)
            e_neg = _exp_manual(-t)
            cosh_t = (e_pos + e_neg) / 2
            sinh_t = (e_pos - e_neg) / 2
            if conica.orientacion == "Horizontal":
                xs.append(conica.h + conica.a * cosh_t * signo)
                ys.append(conica.k + conica.b * sinh_t)
            else:
                xs.append(conica.h + conica.b * sinh_t)
                ys.append(conica.k + conica.a * cosh_t * signo)
        ax.plot(xs, ys, color="crimson", linewidth=2)
    ax.scatter([conica.h], [conica.k], color="black", zorder=5, label="Centro")