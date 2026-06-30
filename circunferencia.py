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
        self.rhs = rhs  # Se guarda para reutilizar en el procedimiento paso a paso

        self.pasos_transformacion = self._generar_pasos_transformacion()
        self.pasos_inversa = self._generar_pasos_inversa()

    def _generar_pasos_transformacion(self):
        """Desarrollo paso a paso: ecuación general → forma canónica."""
        pasos = ["--- TRANSFORMACIÓN: ECUACIÓN GENERAL → FORMA CANÓNICA ---"]
        pasos.append(f"1. Ecuación general (criterio de Circunferencia: A = B = {self.A:.2f}):")
        pasos.append(f"   {self.ecuacion_general()}")
        pasos.append("2. Agrupamos y factorizamos A en los términos de x e y:")
        pasos.append(
            f"   {self.A:.2f}(x² + ({self.C:.2f}/{self.A:.2f})x) + "
            f"{self.A:.2f}(y² + ({self.D:.2f}/{self.A:.2f})y) + {self.E:.2f} = 0"
        )
        pasos.append(
            f"3. Completamos cuadrado en x: h = -C/(2A) = "
            f"-({self.C:.2f})/(2×{self.A:.2f}) = {self.h:.2f}"
        )
        pasos.append(
            f"4. Completamos cuadrado en y: k = -D/(2A) = "
            f"-({self.D:.2f})/(2×{self.A:.2f}) = {self.k:.2f}"
        )
        pasos.append(
            f"5. Sustituyendo: A(x-h)² + A(y-k)² = A·h² + A·k² - E = {self.rhs:.2f}"
        )
        pasos.append(
            f"6. Dividimos por A: (x-h)² + (y-k)² = {self.rhs:.2f}/{self.A:.2f} "
            f"= {self.r2:.2f} = r²"
        )
        pasos.append(f"7. Ecuación canónica: {self.ecuacion_canonica()}")
        return pasos

    def _generar_pasos_inversa(self):
        """Desarrollo paso a paso: forma canónica → ecuación general."""
        pasos = ["--- PROCEDIMIENTO INVERSO: FORMA CANÓNICA → ECUACIÓN GENERAL ---"]
        pasos.append(f"1. Partimos de la canónica: {self.ecuacion_canonica()}")
        pasos.append(
            f"2. Multiplicamos por A = {self.A:.2f} (factor común, ya que A = B "
            f"en la circunferencia, y r² = rhs/A):"
        )
        pasos.append(f"   A(x-h)² + A(y-k)² = A·r² = {self.rhs:.2f}  (rhs)")
        pasos += self._pasos_inversa_segundo_grado(self.h, self.k, self.rhs)
        return pasos

    def ecuacion_canonica(self):
        # Usar :.2f para redondear a 2 decimales en el texto final
        signo_h = f"- {abs(self.h):.2f}" if self.h >= 0 else f"+ {abs(self.h):.2f}"
        signo_k = f"- {abs(self.k):.2f}" if self.k >= 0 else f"+ {abs(self.k):.2f}"
        
        parte_x = "x²" if self.h == 0 else f"(x {signo_h})²"
        parte_y = "y²" if self.k == 0 else f"(y {signo_k})²"

        return f"{parte_x} + {parte_y} = {self.r2:.2f}"

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