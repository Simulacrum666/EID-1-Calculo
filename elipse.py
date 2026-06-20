from conica import Conica
from utils import sqrt_manual


class Elipse(Conica):

    def __init__(self, rut):

        super().__init__(rut)

        if self.tipo != "Elipse":
            raise ValueError(
                f"El RUT genera una {self.tipo}, no una elipse"
            )

        self.calcular_parametros()

    def calcular_parametros(self):

        self.h = -self.C / (2 * self.A)
        self.k = -self.D / (2 * self.B)

        rhs = (
            -self.E
            + self.A * self.h * self.h
            + self.B * self.k * self.k
        )

        self.a2 = rhs / self.A
        self.b2 = rhs / self.B

        #Igual que en Circunferencia: si a² o b² da negativo, la ecuación
        #no tiene solución real (elipse imaginaria), no se puede graficar.
        if self.a2 < 0 or self.b2 < 0:
            raise ValueError(
                "La ecuación representa una elipse imaginaria "
                f"(a² = {self.a2}, b² = {self.b2}, sin solución real)."
            )

        self.a = sqrt_manual(self.a2)
        self.b = sqrt_manual(self.b2)

        self.calcular_focos()

    def calcular_focos(self):

        if self.a2 >= self.b2:

            self.orientacion = "Horizontal"

            self.c2 = self.a2 - self.b2
            self.c = sqrt_manual(self.c2)

            self.focos = [
                (self.h + self.c, self.k),
                (self.h - self.c, self.k)
            ]

        else:

            self.orientacion = "Vertical"

            self.c2 = self.b2 - self.a2
            self.c = sqrt_manual(self.c2)

            self.focos = [
                (self.h, self.k + self.c),
                (self.h, self.k - self.c)
            ]

    def ecuacion_canonica(self):

        return (
            f"(x - {self.h})²/{self.a2} + "
            f"(y - {self.k})²/{self.b2} = 1"
        )

    def obtener_vertices(self):

        if self.orientacion == "Horizontal":

            principales = [
                (self.h + self.a, self.k),
                (self.h - self.a, self.k)
            ]

            secundarios = [
                (self.h, self.k + self.b),
                (self.h, self.k - self.b)
            ]

        else:

            principales = [
                (self.h, self.k + self.a),
                (self.h, self.k - self.a)
            ]

            secundarios = [
                (self.h + self.b, self.k),
                (self.h - self.b, self.k)
            ]

        return principales, secundarios