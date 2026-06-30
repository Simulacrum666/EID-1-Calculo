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

            self.termino_independiente = termino_independiente  # Se guarda para los pasos
            self.pasos_transformacion = self._generar_pasos_transformacion_vertical()
            self.pasos_inversa = self._generar_pasos_inversa_vertical()

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

            self.termino_independiente = termino_independiente  # Se guarda para los pasos
            self.pasos_transformacion = self._generar_pasos_transformacion_horizontal()
            self.pasos_inversa = self._generar_pasos_inversa_horizontal()
            
        else:
            raise ValueError("Los coeficientes no corresponden a una parábola válida.")

        #El lado recto es el valor absoluto de 4p
        self.lado_recto = self.cuatro_p if self.cuatro_p >= 0 else -self.cuatro_p

    def ecuacion_canonica(self):
        signo_h = f"- {abs(self.h):.2f}" if self.h >= 0 else f"+ {abs(self.h):.2f}"
        signo_k = f"- {abs(self.k):.2f}" if self.k >= 0 else f"+ {abs(self.k):.2f}"
        
        parte_x = "x" if self.h == 0 else f"(x {signo_h})"
        parte_y = "y" if self.k == 0 else f"(y {signo_k})"
        
        if self.orientacion == "Vertical":
            # Eleva al cuadrado la parte de X y redondea 4p
            parte_x_cuad = "x²" if self.h == 0 else f"(x {signo_h})²"
            return f"{parte_x_cuad} = {self.cuatro_p:.2f} * {parte_y}"
        else:
            # Eleva al cuadrado la parte de Y y redondea 4p
            parte_y_cuad = "y²" if self.k == 0 else f"(y {signo_k})²"
            return f"{parte_y_cuad} = {self.cuatro_p:.2f} * {parte_x}"

    def obtener_directriz(self):
        return f"{self.directriz_eje} = {self.directriz_valor:.2f}"

    def _generar_pasos_transformacion_vertical(self):
        """Desarrollo paso a paso: ecuación general → forma canónica (B=0)."""
        pasos = ["--- TRANSFORMACIÓN: ECUACIÓN GENERAL → FORMA CANÓNICA ---"]
        pasos.append("1. Ecuación general (criterio de Parábola: B = 0):")
        pasos.append(f"   {self.ecuacion_general()}")
        pasos.append(
            f"2. Completamos cuadrado en x: A(x² + (C/A)x) = A(x-h)² - A·h², "
            f"con h = -C/(2A) = {self.h:.2f}"
        )
        pasos.append(
            f"3. Sustituyendo: A(x-h)² - A·h² + D·y + E = 0  →  "
            f"D·y = -A(x-h)² + (A·h² - E)"
        )
        pasos.append(
            f"4. Despejamos y: y = -(A/D)(x-h)² + (A·h² - E)/D, "
            f"con k = (A·h² - E)/D = {self.k:.2f} (ordenada del vértice)"
        )
        pasos.append("5. Reescribimos: y - k = -(A/D)(x-h)²")
        pasos.append(
            f"6. Multiplicamos por -D/A: (x-h)² = (-D/A)(y-k) = 4p(y-k), "
            f"con 4p = -D/A = {self.cuatro_p:.2f}"
        )
        pasos.append(f"7. Ecuación canónica: {self.ecuacion_canonica()}")
        return pasos

    def _generar_pasos_inversa_vertical(self):
        """Desarrollo paso a paso: forma canónica → ecuación general (B=0)."""
        pasos = ["--- PROCEDIMIENTO INVERSO: FORMA CANÓNICA → ECUACIÓN GENERAL ---"]
        pasos.append(f"1. Partimos de la canónica: {self.ecuacion_canonica()}")
        pasos.append("2. Expandimos el cuadrado: x² - 2h·x + h² = 4p·y - 4p·k")
        pasos.append("3. Reagrupamos: x² - 2h·x - 4p·y + (h² + 4p·k) = 0")
        pasos.append(
            f"4. Multiplicamos por A = {self.A:.2f} (coeficiente original de x²):"
        )

        C_rec = -2 * self.A * self.h
        D_rec = -self.A * self.cuatro_p
        E_rec = self.A * (self.h * self.h + self.cuatro_p * self.k)

        pasos.append(
            f"   {self.A:.2f}x² + ({C_rec:.2f})x + ({D_rec:.2f})y + "
            f"({E_rec:.2f}) = 0"
        )
        pasos.append(
            f"5. Como 4p = -D/A, se cumple que -A·4p = D, así: "
            f"C = -2Ah = {C_rec:.2f}, D = -A·4p = {D_rec:.2f}, "
            f"E = A(h²+4pk) = {E_rec:.2f}"
        )
        pasos.append(
            f"6. Verificación: coinciden con los coeficientes originales "
            f"(C = {self.C:.2f}, D = {self.D:.2f}, E = {self.E:.2f}) ✓"
        )
        return pasos

    def _generar_pasos_transformacion_horizontal(self):
        """Desarrollo paso a paso: ecuación general → forma canónica (A=0)."""
        pasos = ["--- TRANSFORMACIÓN: ECUACIÓN GENERAL → FORMA CANÓNICA ---"]
        pasos.append("1. Ecuación general (criterio de Parábola: A = 0):")
        pasos.append(f"   {self.ecuacion_general()}")
        pasos.append(
            f"2. Completamos cuadrado en y: B(y² + (D/B)y) = B(y-k)² - B·k², "
            f"con k = -D/(2B) = {self.k:.2f}"
        )
        pasos.append(
            f"3. Sustituyendo: B(y-k)² - B·k² + C·x + E = 0  →  "
            f"C·x = -B(y-k)² + (B·k² - E)"
        )
        pasos.append(
            f"4. Despejamos x: x = -(B/C)(y-k)² + (B·k² - E)/C, "
            f"con h = (B·k² - E)/C = {self.h:.2f} (abscisa del vértice)"
        )
        pasos.append("5. Reescribimos: x - h = -(B/C)(y-k)²")
        pasos.append(
            f"6. Multiplicamos por -C/B: (y-k)² = (-C/B)(x-h) = 4p(x-h), "
            f"con 4p = -C/B = {self.cuatro_p:.2f}"
        )
        pasos.append(f"7. Ecuación canónica: {self.ecuacion_canonica()}")
        return pasos

    def _generar_pasos_inversa_horizontal(self):
        """Desarrollo paso a paso: forma canónica → ecuación general (A=0)."""
        pasos = ["--- PROCEDIMIENTO INVERSO: FORMA CANÓNICA → ECUACIÓN GENERAL ---"]
        pasos.append(f"1. Partimos de la canónica: {self.ecuacion_canonica()}")
        pasos.append("2. Expandimos el cuadrado: y² - 2k·y + k² = 4p·x - 4p·h")
        pasos.append("3. Reagrupamos: y² - 2k·y - 4p·x + (k² + 4p·h) = 0")
        pasos.append(
            f"4. Multiplicamos por B = {self.B:.2f} (coeficiente original de y²):"
        )

        D_rec = -2 * self.B * self.k
        C_rec = -self.B * self.cuatro_p
        E_rec = self.B * (self.k * self.k + self.cuatro_p * self.h)

        pasos.append(
            f"   {self.B:.2f}y² + ({C_rec:.2f})x + ({D_rec:.2f})y + "
            f"({E_rec:.2f}) = 0"
        )
        pasos.append(
            f"5. Como 4p = -C/B, se cumple que -B·4p = C, así: "
            f"D = -2Bk = {D_rec:.2f}, C = -B·4p = {C_rec:.2f}, "
            f"E = B(k²+4ph) = {E_rec:.2f}"
        )
        pasos.append(
            f"6. Verificación: coinciden con los coeficientes originales "
            f"(C = {self.C:.2f}, D = {self.D:.2f}, E = {self.E:.2f}) ✓"
        )
        return pasos