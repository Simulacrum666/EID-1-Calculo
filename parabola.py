from conica import Conica
from utils import sqrt_manual

class Parabola(Conica):

    def __init__(self, rut):
        super().__init__(rut)

        if self.tipo != "Parabola":
            raise ValueError(
                f"El RUT genera una {self.tipo}, no una parábola."
            )

        self.calcular_parametros()

    def calcular_parametros(self):

        #Caso 1: Parábola Vertical (Tiene x², por lo que B = 0)
        if self.A != 0 and self.B == 0:
            self.orientacion = "Vertical"
            
            #Completando cuadrados
            self.h = -self.C / (2 * self.A)
            
            #El término lineal restante absorbe el desplazamiento
            termino_independiente = -self.E + (self.A * self.h * self.h)
            
            #4p es el coeficiente que acompaña a 'y' en el lado derecho
            self.cuatro_p = -self.D / self.A
            self.p = self.cuatro_p / 4
            
            #Despejando y: D*y = -A*(x-h)² + (A*h² - E)  →  y = (A*h² - E)/D - (A/D)*(x-h)²
            #Por lo tanto k = (A*h² - E)/D = termino_independiente / D (sin signo extra)
            self.k = termino_independiente / self.D if self.D != 0 else 0
            
            #Vértice y Foco
            self.vertice = (self.h, self.k)
            self.foco = (self.h, self.k + self.p)
            
            #Directriz
            self.directriz_eje = "y"
            self.directriz_valor = self.k - self.p

        #Caso 2: Parábola Horizontal (Tiene y², por lo que A = 0)
        elif self.B != 0 and self.A == 0:
            self.orientacion = "Horizontal"
            
            #Completando cuadrados
            self.k = -self.D / (2 * self.B)
            
            termino_independiente = -self.E + (self.B * self.k * self.k)
            
            #4p es el coeficiente que acompaña a 'x' en el lado derecho
            self.cuatro_p = -self.C / self.B
            self.p = self.cuatro_p / 4
            
            #Misma derivación que en el caso vertical, intercambiando x↔y: h = termino_independiente / C
            self.h = termino_independiente / self.C if self.C != 0 else 0
            
            #Vértice y Foco
            self.vertice = (self.h, self.k)
            self.foco = (self.h + self.p, self.k)
            
            #Directriz
            self.directriz_eje = "x"
            self.directriz_valor = self.h - self.p
            
        else:
            raise ValueError("Los coeficientes no corresponden a una parábola válida.")

        #El lado recto es el valor absoluto de 4p
        self.lado_recto = self.cuatro_p if self.cuatro_p >= 0 else -self.cuatro_p

    def ecuacion_canonica(self):
        signo_h = f"- {abs(self.h)}" if self.h >= 0 else f"+ {abs(self.h)}"
        signo_k = f"- {abs(self.k)}" if self.k >= 0 else f"+ {abs(self.k)}"
        
        parte_x = "x" if self.h == 0 else f"(x {signo_h})"
        parte_y = "y" if self.k == 0 else f"(y {signo_k})"

        if self.orientacion == "Vertical":
            return f"{parte_x}² = {self.cuatro_p} * {parte_y}"
        else:
            return f"{parte_y}² = {self.cuatro_p} * {parte_x}"

    def obtener_directriz(self):
        return f"{self.directriz_eje} = {self.directriz_valor}"