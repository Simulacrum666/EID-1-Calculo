import matplotlib.pyplot as plt

from utils import sin_manual, cos_manual, sqrt_manual, PI


# ─────────────────────────────────────────────
#  ELIPSE
# ─────────────────────────────────────────────

def graficar_elipse(elipse):

    fig, ax = plt.subplots()

    puntos_x, puntos_y = [], []
    pasos = 400

    for i in range(pasos + 1):
        t = 2 * PI * i / pasos
        cos_t = cos_manual(t)
        sin_t = sin_manual(t)

        if elipse.orientacion == "Horizontal":
            x = elipse.h + elipse.a * cos_t
            y = elipse.k + elipse.b * sin_t
        else:
            x = elipse.h + elipse.b * cos_t
            y = elipse.k + elipse.a * sin_t

        puntos_x.append(x)
        puntos_y.append(y)

    ax.plot(puntos_x, puntos_y, color="royalblue", linewidth=2)

    # Centro
    ax.scatter([elipse.h], [elipse.k], color="black", zorder=5, label="Centro")

    # Focos
    fx = [f[0] for f in elipse.focos]
    fy = [f[1] for f in elipse.focos]
    ax.scatter(fx, fy, color="red", zorder=5, label="Focos")

    # Vértices
    princ, secun = elipse.obtener_vertices()
    todos = princ + secun
    ax.scatter([v[0] for v in todos], [v[1] for v in todos],
               color="green", zorder=5, label="Vértices")

    _ejes_y_titulo(ax, f"Elipse — RUT: {elipse.rut}")
    plt.show()


# ─────────────────────────────────────────────
#  CIRCUNFERENCIA
# ─────────────────────────────────────────────

def graficar_circunferencia(circunferencia):

    fig, ax = plt.subplots()

    puntos_x, puntos_y = [], []
    pasos = 400

    for i in range(pasos + 1):
        t = 2 * PI * i / pasos
        x = circunferencia.h + circunferencia.r * cos_manual(t)
        y = circunferencia.k + circunferencia.r * sin_manual(t)
        puntos_x.append(x)
        puntos_y.append(y)

    ax.plot(puntos_x, puntos_y, color="royalblue", linewidth=2)

    # Centro
    ax.scatter([circunferencia.h], [circunferencia.k],
               color="black", zorder=5, label="Centro")

    # Puntos cardinales
    norte, sur, este, oeste = circunferencia.obtener_puntos_cardinales()
    cardinales = [norte, sur, este, oeste]
    nombres = ["N", "S", "E", "O"]
    ax.scatter([p[0] for p in cardinales], [p[1] for p in cardinales],
               color="green", zorder=5, label="Cardinales")
    for punto, nombre in zip(cardinales, nombres):
        ax.annotate(nombre, punto, textcoords="offset points",
                    xytext=(6, 6), fontsize=9)

    _ejes_y_titulo(ax, f"Circunferencia — RUT: {circunferencia.rut}")
    plt.show()


# ─────────────────────────────────────────────
#  PARÁBOLA
# ─────────────────────────────────────────────

def graficar_parabola(parabola):

    fig, ax = plt.subplots()

    # Rango de puntos alrededor del vértice
    rango = max(abs(parabola.p) * 12, 6)
    pasos = 400

    puntos_x, puntos_y = [], []

    if parabola.orientacion == "Vertical":
        # x varía, y = k + (x-h)²/(4p)
        paso = 2 * rango / pasos
        for i in range(pasos + 1):
            x = parabola.h - rango + i * paso
            if parabola.cuatro_p != 0:
                y = parabola.k + (x - parabola.h) ** 2 / parabola.cuatro_p
            else:
                continue
            puntos_x.append(x)
            puntos_y.append(y)
    else:
        # y varía, x = h + (y-k)²/(4p)
        paso = 2 * rango / pasos
        for i in range(pasos + 1):
            y = parabola.k - rango + i * paso
            if parabola.cuatro_p != 0:
                x = parabola.h + (y - parabola.k) ** 2 / parabola.cuatro_p
            else:
                continue
            puntos_x.append(x)
            puntos_y.append(y)

    ax.plot(puntos_x, puntos_y, color="royalblue", linewidth=2)

    # Vértice
    ax.scatter([parabola.vertice[0]], [parabola.vertice[1]],
               color="black", zorder=5, label="Vértice")
    ax.annotate("V", parabola.vertice, textcoords="offset points",
                xytext=(6, 6), fontsize=9)

    # Foco
    ax.scatter([parabola.foco[0]], [parabola.foco[1]],
               color="red", zorder=5, label="Foco")
    ax.annotate("F", parabola.foco, textcoords="offset points",
                xytext=(6, 6), fontsize=9)

    # Directriz
    limite_inf = min(puntos_x) if parabola.orientacion == "Vertical" else min(puntos_y)
    limite_sup = max(puntos_x) if parabola.orientacion == "Vertical" else max(puntos_y)

    if parabola.directriz_eje == "y":
        ax.axhline(parabola.directriz_valor, color="orange",
                   linestyle="--", linewidth=1.4,
                   label=f"Directriz y = {parabola.directriz_valor:.3f}")
    else:
        ax.axvline(parabola.directriz_valor, color="orange",
                   linestyle="--", linewidth=1.4,
                   label=f"Directriz x = {parabola.directriz_valor:.3f}")

    _ejes_y_titulo(ax, f"Parábola — RUT: {parabola.rut}")
    plt.show()


# ─────────────────────────────────────────────
#  HIPÉRBOLA
# ─────────────────────────────────────────────

def graficar_hiperbola(hiperbola):

    fig, ax = plt.subplots()

    pasos = 600
    rango_t = 3.0   # unidades de "sinh" que se barren

    rama1_x, rama1_y = [], []
    rama2_x, rama2_y = [], []

    for i in range(pasos + 1):
        # t va de -rango_t a +rango_t usando parametrización cosh/sinh manual
        t_val = -rango_t + 2 * rango_t * i / pasos

        # cosh y sinh a partir de la exponencial (solo necesitamos estas dos)
        e_pos = _exp_manual(t_val)
        e_neg = _exp_manual(-t_val)
        cosh_t = (e_pos + e_neg) / 2
        sinh_t = (e_pos - e_neg) / 2

        if hiperbola.orientacion == "Horizontal":
            # rama derecha
            rama1_x.append(hiperbola.h + hiperbola.a * cosh_t)
            rama1_y.append(hiperbola.k + hiperbola.b * sinh_t)
            # rama izquierda
            rama2_x.append(hiperbola.h - hiperbola.a * cosh_t)
            rama2_y.append(hiperbola.k + hiperbola.b * sinh_t)
        else:
            # rama superior
            rama1_x.append(hiperbola.h + hiperbola.b * sinh_t)
            rama1_y.append(hiperbola.k + hiperbola.a * cosh_t)
            # rama inferior
            rama2_x.append(hiperbola.h + hiperbola.b * sinh_t)
            rama2_y.append(hiperbola.k - hiperbola.a * cosh_t)

    ax.plot(rama1_x, rama1_y, color="royalblue", linewidth=2)
    ax.plot(rama2_x, rama2_y, color="royalblue", linewidth=2)

    # Centro
    ax.scatter([hiperbola.h], [hiperbola.k],
               color="black", zorder=5, label="Centro")

    # Focos
    fx = [f[0] for f in hiperbola.focos]
    fy = [f[1] for f in hiperbola.focos]
    ax.scatter(fx, fy, color="red", zorder=5, label="Focos")

    # Vértices
    ax.scatter([v[0] for v in hiperbola.vertices],
               [v[1] for v in hiperbola.vertices],
               color="green", zorder=5, label="Vértices")

    # Asíntotas  (obtener_asintotas devuelve las dos pendientes)
    p_pos, p_neg = hiperbola.obtener_asintotas()

    x_lim = max(abs(x) for x in rama1_x + rama2_x) * 1.1
    xs = [-x_lim, x_lim]
    ax.plot(xs,
            [hiperbola.k + p_pos * (x - hiperbola.h) for x in xs],
            "k--", linewidth=1, alpha=0.5, label="Asíntotas")
    ax.plot(xs,
            [hiperbola.k + p_neg * (x - hiperbola.h) for x in xs],
            "k--", linewidth=1, alpha=0.5)

    _ejes_y_titulo(ax, f"Hipérbola — RUT: {hiperbola.rut}")
    plt.show()


# ─────────────────────────────────────────────
#  FUNCIÓN UNIVERSAL  (usa factory internamente)
# ─────────────────────────────────────────────

def graficar_conica(conica):
    """Detecta el tipo y llama a la función correcta."""
    tipo = conica.tipo
    if tipo == "Elipse":
        graficar_elipse(conica)
    elif tipo == "Circunferencia":
        graficar_circunferencia(conica)
    elif tipo == "Parabola":
        graficar_parabola(conica)
    elif tipo == "Hiperbola":
        graficar_hiperbola(conica)
    else:
        raise ValueError(f"Tipo de cónica no reconocido: {tipo}")


# ─────────────────────────────────────────────
#  HELPERS INTERNOS
# ─────────────────────────────────────────────

def _ejes_y_titulo(ax, titulo):
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.axvline(0, color="gray", linewidth=0.8)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.set_aspect("equal")
    ax.legend(fontsize=8)
    ax.set_title(titulo)


def _exp_manual(x):
    """e^x aproximado con serie de Taylor (20 términos)."""
    resultado = 1.0
    termino = 1.0
    for n in range(1, 20):
        termino *= x / n
        resultado += termino
    return resultado