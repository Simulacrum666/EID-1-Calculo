from utils import validar_rut
from utils import extraer_digitos
from utils import calcular_v


class Conica:

    def __init__(self, rut):

        self.rut = rut

        self.es_valido, self.pasos_validacion = validar_rut(rut)

        if not self.es_valido:
            raise ValueError("RUT inválido")

        self.digitos, self.dv = extraer_digitos(rut)

        self.v = calcular_v(self.dv)

        self.construir_coeficientes()

        self.tipo = self.clasificar()

    def construir_coeficientes(self):

        d = self.digitos

        self.A = (d[0] + d[1]) / self.v
        self.B = (d[2] + d[3]) / self.v

        self.C = -(d[4] + d[5])
        self.D = -(d[6] + d[7])

        self.E = d[0] + d[2] + d[4] + d[6]

        # Ajustes del enunciado

        if d[7] % 2 != 0:
            self.B = -self.B

        if d[0] == d[1]:
            self.B = self.A

        if (d[4] + d[5]) % 3 == 0:

            if d[6] % 2 == 0:
                self.B = 0

            else:
                self.A = 0

    def clasificar(self):

        if self.A == self.B and self.A != 0:
            return "Circunferencia"

        if self.A != 0 and self.B != 0:

            mismo_signo = (
                (self.A > 0 and self.B > 0) or
                (self.A < 0 and self.B < 0)
            )

            if mismo_signo and self.A != self.B:
                return "Elipse"

            if not mismo_signo:
                return "Hiperbola"

        if self.A == 0 or self.B == 0:
            return "Parabola"

        return "Degenerada"

    def ecuacion_general(self):

        return (
            f"{self.A}x² + "
            f"{self.B}y² + "
            f"{self.C}x + "
            f"{self.D}y + "
            f"{self.E} = 0"
        )