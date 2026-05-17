from conica import Conica
from utils import sqrt_manual, PI  # Asegúrate de que PI esté en tu utils.py

class Circunferencia(Conica):

    def __init__(self, rut):
        super().__init__(rut)

        if self.tipo != "Circunferencia":        #Validacion de Circunferencia
            raise ValueError(
                f"El RUT genera una {self.tipo}, no una circunferencia."
            )

        self.calcular_parametros()

    def calcular_parametros(self):
       
        #Centro (h, k)
        self.h = -self.C / (2 * self.A)
        self.k = -self.D / (2 * self.B)

        #Lado derecho al completar cuadrados
        rhs = (
            -self.E
            + self.A * self.h * self.h
            + self.B * self.k * self.k
        )

        # El radio al cuadrado r² es igual a rhs / A (ya que A = B)
        self.r2 = rhs / self.A

        if self.r2 < 0:
            raise ValueError(
                "La ecuación representa una circunferencia imaginaria (r² < 0)."
            )

        self.r = sqrt_manual(self.r2)     #Radio

    def ecuacion_canonica(self):
        signo_h = f"- {abs(self.h)}" if self.h >= 0 else f"+ {abs(self.h)}"
        signo_k = f"- {abs(self.k)}" if self.k >= 0 else f"+ {abs(self.k)}"
        
        parte_x = "x²" if self.h == 0 else f"(x {signo_h})²"
        parte_y = "y²" if self.k == 0 else f"(y {signo_k})²"

        return f"{parte_x} + {parte_y} = {self.r2}"

    def calcular_area(self):
        return PI * self.r2

    def calcular_perimetro(self):
        return 2 * PI * self.r

    def obtener_puntos_cardinales(self):       #Devuelve los 4 puntos extremos de la circunferencia (N,S,E,O)
        
        norte = (self.h, self.k + self.r)
        sur = (self.h, self.k - self.r)
        este = (self.h + self.r, self.k)
        oeste = (self.h - self.r, self.k)
        
        return norte, sur, este, oeste