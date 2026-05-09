import matplotlib.pyplot as plt

from utils import sin_manual
from utils import cos_manual
from utils import PI


def graficar_elipse(elipse):

    fig, ax = plt.subplots()

    puntos_x = []
    puntos_y = []

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

    ax.plot(puntos_x, puntos_y)

    ax.scatter([elipse.h], [elipse.k])

    ax.axhline(0)
    ax.axvline(0)

    ax.grid()

    ax.set_aspect("equal")

    ax.set_title(
        f"Elipse generada por RUT: {elipse.rut}"
    )

    plt.show()