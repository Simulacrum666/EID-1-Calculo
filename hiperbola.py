from conica import Conica
from utils import sqrt_manual

class Hiperbola(Conica):

    def __init__(self, rut):
        super().__init__(rut)

        if self.tipo != "Hiperbola":
            raise ValueError(
                f"El RUT genera una {self.tipo}, no una hipérbola."
            )

        self.calcular_parametros()

    def calcular_parametros(self):

        # Centro (h, k)
        self.h = -self.C / (2 * self.A)
        self.k = -self.D / (2 * self.B)

        #Lado derecho al completar cuadrados
        rhs = (
            -self.E
            + self.A * self.h * self.h
            + self.B * self.k * self.k
        )

        #Valores intermedios dividiendo por el término de la derecha (rhs)
        comp_x = rhs / self.A
        comp_y = rhs / self.B

        #Determinar orientación según cuál componente queda positivo
        if comp_x > 0 and comp_y < 0:
            self.orientacion = "Horizontal"
            self.a2 = comp_x
            self.b2 = -comp_y  # Convertimos a positivo para los semiejes
        elif comp_y > 0 and comp_x < 0:
            self.orientacion = "Vertical"
            self.a2 = comp_y
            self.b2 = -comp_x  # Convertimos a positivo para los semiejes
        else:
            raise ValueError("La ecuación degenera o no corresponde a una hipérbola real.")

        #Semiejes real (a) e imaginario (b) usando tu raíz manual
        self.a = sqrt_manual(self.a2)
        self.b = sqrt_manual(self.b2)
        self.rhs = rhs  # Se guarda para reutilizar en el procedimiento paso a paso

        #Relación fundamental de la hipérbola: c² = a² + b²
        self.c2 = self.a2 + self.b2
        self.c = sqrt_manual(self.c2)

        self.calcular_elementos()

        self.pasos_transformacion = self._generar_pasos_transformacion()
        self.pasos_inversa = self._generar_pasos_inversa()

    def _generar_pasos_transformacion(self):
        """Desarrollo paso a paso: ecuación general → forma canónica."""
        pasos = ["--- TRANSFORMACIÓN: ECUACIÓN GENERAL → FORMA CANÓNICA ---"]
        pasos.append("1. Ecuación general (criterio de Hipérbola: A y B con signos opuestos):")
        pasos.append(f"   {self.ecuacion_general()}")
        pasos.append(f"2. h = -C/(2A) = {self.h:.2f};   k = -D/(2B) = {self.k:.2f}")
        pasos.append(
            f"3. Sustituyendo: A(x-h)² + B(y-k)² = A·h² + B·k² - E = {self.rhs:.2f}"
        )
        pasos.append(
            "4. Dividimos por rhs. Como A y B tienen signos opuestos, uno de "
            "los términos queda con signo negativo: aparece una diferencia "
            "de cuadrados (forma propia de la hipérbola)."
        )
        pasos.append(
            f"5. a² = {self.a2:.2f};   b² = {self.b2:.2f};   "
            f"orientación: {self.orientacion}"
        )
        pasos.append(f"6. Ecuación canónica: {self.ecuacion_canonica()}")
        return pasos

    def _generar_pasos_inversa(self):
        """Desarrollo paso a paso: forma canónica → ecuación general."""
        pasos = ["--- PROCEDIMIENTO INVERSO: FORMA CANÓNICA → ECUACIÓN GENERAL ---"]
        pasos.append(f"1. Partimos de la canónica: {self.ecuacion_canonica()}")
        pasos.append(
            "2. Multiplicamos toda la ecuación por rhs (el mismo valor usado "
            "al construir a² y b²), recuperando la diferencia de cuadrados:"
        )
        pasos.append(f"   A(x-h)² + B(y-k)² = rhs = {self.rhs:.2f}")
        pasos += self._pasos_inversa_segundo_grado(self.h, self.k, self.rhs)
        return pasos

    def calcular_elementos(self):
        if self.orientacion == "Horizontal":
            self.focos = [
                (self.h + self.c, self.k),
                (self.h - self.c, self.k)
            ]
            self.vertices = [
                (self.h + self.a, self.k),
                (self.h - self.a, self.k)
            ]
        else:  # Vertical
            self.focos = [
                (self.h, self.k + self.c),
                (self.h, self.k - self.c)
            ]
            self.vertices = [
                (self.h, self.k + self.a),
                (self.h, self.k - self.a)
            ]

    def ecuacion_canonica(self):
        signo_h = f"- {abs(self.h):.2f}" if self.h >= 0 else f"+ {abs(self.h):.2f}"
        signo_k = f"- {abs(self.k):.2f}" if self.k >= 0 else f"+ {abs(self.k):.2f}"
        
        parte_x = "x²" if self.h == 0 else f"(x {signo_h})²"
        parte_y = "y²" if self.k == 0 else f"(y {signo_k})²"
        
        if self.orientacion == "Horizontal":
            return f"{parte_x}/{self.a2:.2f} - {parte_y}/{self.b2:.2f} = 1"
        else:
            return f"{parte_y}/{self.a2:.2f} - {parte_x}/{self.b2:.2f} = 1"

    def obtener_asintotas(self):
        
        if self.orientacion == "Horizontal":
            pendiente = self.b / self.a
        else:
            pendiente = self.a / self.b
            
        return pendiente, -pendiente