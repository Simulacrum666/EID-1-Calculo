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
        self.rhs = rhs  # Se guarda para reutilizar en el procedimiento paso a paso

        self.calcular_focos()

        self.pasos_transformacion = self._generar_pasos_transformacion()
        self.pasos_inversa = self._generar_pasos_inversa()

    def _generar_pasos_transformacion(self):
        """Desarrollo paso a paso: ecuación general → forma canónica."""
        pasos = ["--- TRANSFORMACIÓN: ECUACIÓN GENERAL → FORMA CANÓNICA ---"]
        pasos.append("1. Ecuación general (criterio de Elipse: A y B mismo signo, A ≠ B):")
        pasos.append(f"   {self.ecuacion_general()}")
        pasos.append("2. Agrupamos y factorizamos A en x, B en y:")
        pasos.append(
            f"   {self.A:.2f}(x² + ({self.C:.2f}/{self.A:.2f})x) + "
            f"{self.B:.2f}(y² + ({self.D:.2f}/{self.B:.2f})y) + {self.E:.2f} = 0"
        )
        pasos.append(f"3. h = -C/(2A) = {self.h:.2f};   k = -D/(2B) = {self.k:.2f}")
        pasos.append(
            f"4. Sustituyendo: A(x-h)² + B(y-k)² = A·h² + B·k² - E = {self.rhs:.2f}"
        )
        pasos.append("5. Dividimos toda la ecuación por rhs:")
        pasos.append("   (x-h)²/(rhs/A) + (y-k)²/(rhs/B) = 1")
        pasos.append(
            f"6. a² = rhs/A = {self.rhs:.2f}/{self.A:.2f} = {self.a2:.2f};   "
            f"b² = rhs/B = {self.rhs:.2f}/{self.B:.2f} = {self.b2:.2f}"
        )
        pasos.append(f"7. Ecuación canónica: {self.ecuacion_canonica()}")
        return pasos

    def _generar_pasos_inversa(self):
        """Desarrollo paso a paso: forma canónica → ecuación general."""
        pasos = ["--- PROCEDIMIENTO INVERSO: FORMA CANÓNICA → ECUACIÓN GENERAL ---"]
        pasos.append(f"1. Partimos de la canónica: {self.ecuacion_canonica()}")
        pasos.append(
            "2. Multiplicamos toda la ecuación por rhs (el mismo valor usado "
            "al construir a² y b², ya que A = rhs/a² y B = rhs/b²):"
        )
        pasos.append(f"   A(x-h)² + B(y-k)² = rhs = {self.rhs:.2f}")
        pasos += self._pasos_inversa_segundo_grado(self.h, self.k, self.rhs)
        return pasos

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
        # Redondear el centro y los denominadores a 2 decimales
        texto_h = f"- {self.h:.2f}" if self.h >= 0 else f"+ {abs(self.h):.2f}"
        texto_k = f"- {self.k:.2f}" if self.k >= 0 else f"+ {abs(self.k):.2f}"
        
        parte_x = "x²" if self.h == 0 else f"(x {texto_h})²"
        parte_y = "y²" if self.k == 0 else f"(y {texto_k})²"
        
        return f"{parte_x}/{self.a2:.2f} + {parte_y}/{self.b2:.2f} = 1"

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