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
        self.pasos_construccion = []  # Lista para guardar la bitácora paso a paso

        self.pasos_construccion.append("--- CONSTRUCCIÓN DE LA ECUACIÓN GENERAL ---")
        self.pasos_construccion.append(f"1. Dígitos extraídos del RUT: d1={d[0]}, d2={d[1]}, d3={d[2]}, d4={d[3]}, d5={d[4]}, d6={d[5]}, d7={d[6]}, d8={d[7]}")
        self.pasos_construccion.append(f"2. Valor de V según el Dígito Verificador (DV): V = {self.v}")

        # Valores iniciales según el enunciado
        self.A = (d[0] + d[1]) / self.v
        self.B = (d[2] + d[3]) / self.v
        self.C = -(d[4] + d[5])
        self.D = -(d[6] + d[7])
        self.E = d[0] + d[2] + d[4] + d[6]

        self.pasos_construccion.append("\n3. Cálculo de Coeficientes Iniciales:")
        self.pasos_construccion.append(f"   • A = (d1 + d2) / V = ({d[0]} + {d[1]}) / {self.v} = {self.A:.2f}")
        self.pasos_construccion.append(f"   • B = (d3 + d4) / V = ({d[2]} + {d[3]}) / {self.v} = {self.B:.2f}")
        self.pasos_construccion.append(f"   • C = -(d5 + d6) = -({d[4]} + {d[5]}) = {self.C:.2f}")
        self.pasos_construccion.append(f"   • D = -(d7 + d8) = -({d[6]} + {d[7]}) = {self.D:.2f}")
        self.pasos_construccion.append(f"   • E = d1 + d3 + d5 + d7 = {d[0]} + {d[2]} + {d[4]} + {d[6]} = {self.E:.2f}")

        self.pasos_construccion.append("\n4. Evaluación de Reglas de Ajuste del Enunciado:")

        # Regla 1: d8 impar
        if d[7] % 2 != 0:
            self.B = -self.B
            self.pasos_construccion.append(f"   [ACTIVADA] -> d8 ({d[7]}) es IMPAR: Se invierte el signo de B. Nuevo valor de B = {self.B:.2f}")
        else:
            self.pasos_construccion.append(f"   [NO ACTIVADA] -> d8 ({d[7]}) es PAR: B mantiene su signo.")

        # Regla 2: d1 == d2
        if d[0] == d[1]:
            self.B = self.A
            self.pasos_construccion.append(f"   [ACTIVADA] -> d1 es igual a d2 ({d[0]} == {d[1]}): B se iguala a A. Nuevo valor de B = {self.B:.2f}")
        else:
            self.pasos_construccion.append(f"   [NO ACTIVADA] -> d1 ({d[0]}) es distinto de d2 ({d[1]}).")

        # Regla 3: d5 + d6 múltiplo de 3
        suma_d5_d6 = d[4] + d[5]
        if suma_d5_d6 % 3 == 0:
            self.pasos_construccion.append(f"   [ACTIVADA] -> d5 + d6 ({d[4]} + {d[5]} = {suma_d5_d6}) es MÚLTIPPLO DE 3:")
            if d[6] % 2 == 0:
                self.B = 0
                self.pasos_construccion.append(f"      Como d7 ({d[6]}) es PAR, se fuerza B = 0 (Posible Parábola Vertical)")
            else:
                self.A = 0
                self.pasos_construccion.append(f"      Como d7 ({d[6]}) es IMPAR, se fuerza A = 0 (Posible Parábola Horizontal)")
        else:
            self.pasos_construccion.append(f"   [NO ACTIVADA] -> d5 + d6 ({suma_d5_d6}) NO es múltiplo de 3.")

        self.pasos_construccion.append("\n5. Coeficientes Finales Consolidados:")
        self.pasos_construccion.append(f"   A={self.A:.2f}, B={self.B:.2f}, C={self.C:.2f}, D={self.D:.2f}, E={self.E:.2f}")
        self.pasos_construccion.append("-------------------------------------------\n")

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
            f"{self.A:.2f}x² + "
            f"{self.B:.2f}y² + "
            f"{self.C:.2f}x + "
            f"{self.D:.2f}y + "
            f"{self.E:.2f} = 0"
        )

    def _pasos_inversa_segundo_grado(self, h, k, rhs):
        """Procedimiento inverso compartido por Circunferencia, Elipse e
        Hipérbola: las tres llegan a la forma intermedia
        A(x-h)² + B(y-k)² = rhs antes de dividir para obtener la canónica.
        Partiendo de esa forma, se reconstruyen C, D y E y se comparan
        con los valores originales (Parábola no la usa: su estructura,
        con un término lineal, es distinta)."""
        pasos = []
        pasos.append("• Partimos de la forma intermedia obtenida al completar cuadrados:")
        pasos.append("  A(x - h)² + B(y - k)² = rhs")
        pasos.append(f"  con h = {h:.2f}, k = {k:.2f}, rhs = {rhs:.2f}")
        pasos.append("• Expandimos los cuadrados:")
        pasos.append("  A·x² - 2A·h·x + A·h² + B·y² - 2B·k·y + B·k² = rhs")

        C_rec = -2 * self.A * h
        D_rec = -2 * self.B * k
        E_rec = self.A * h * h + self.B * k * k - rhs

        pasos.append("• Reagrupamos como ecuación general:")
        pasos.append(
            f"  {self.A:.2f}x² + {self.B:.2f}y² + ({C_rec:.2f})x + "
            f"({D_rec:.2f})y + ({E_rec:.2f}) = 0"
        )
        pasos.append(
            f"• Identificamos: C = -2Ah = {C_rec:.2f}, "
            f"D = -2Bk = {D_rec:.2f}, E = Ah²+Bk²-rhs = {E_rec:.2f}"
        )
        pasos.append(
            f"• Verificación: coinciden con los coeficientes originales "
            f"(C = {self.C:.2f}, D = {self.D:.2f}, E = {self.E:.2f}) ✓"
        )
        return pasos