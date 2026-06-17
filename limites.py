# limites.py
from utils import extraer_digitos

class AnalizadorLimites:
    def __init__(self, rut):
        self.rut = rut
        # Extraer dígitos utilizando la función que ya tienen en utils.py
        self.digitos, self.dv = extraer_digitos(rut)
        
        # Mapear las variables del RUT según el formato del PDF
        self.d1 = self.digitos[0]
        self.d2 = self.digitos[1]
        self.d3 = self.digitos[2]
        self.d4 = self.digitos[3]
        self.d5 = self.digitos[4]
        self.d6 = self.digitos[5]
        self.d7 = self.digitos[6]
        self.d8 = self.digitos[7]
        
        # Punto crítico principal: a = d3
        self.a = self.d3
        
        # Determinar automáticamente el caso según d8
        self.caso = self._determinar_caso()
        
    def _determinar_caso(self):
        """Determina el caso matemático según las reglas de residuo de d8 / 3."""
        if self.d8 % 3 == 0:
            return 1  # Discontinuidad removible
        elif self.d8 % 3 == 1:
            return 2  # Discontinuidad de salto
        else:
            return 3  # Discontinuidad infinita

    def obtener_nombre_caso(self):
        """Devuelve una descripción textual del caso para mostrar en la interfaz."""
        if self.caso == 1:
            return "Caso 1: Discontinuidad Removible (d8 es múltiplo de 3)"
        elif self.caso == 2:
            return "Caso 2: Discontinuidad de Salto (d8 con residuo 1 al dividir por 3)"
        else:
            return "Caso 3: Discontinuidad Infinita (d8 con residuo 2 al dividir por 3)"

    def evaluar_funcion(self, x, aproximacion=False):
        """
        Evalúa de forma analítica/numérica la función por tramos en un valor x.
        'aproximacion' se usa como bandera para evitar divisiones por cero 
        cuando hacemos la tabla numérica por izquierda/derecha.
        """
        # Si x es exactamente el punto crítico 'a' y evaluamos la definición real:
        if not aproximacion and x == self.a:
            if self.caso == 1 or self.caso == 3:
                # En el caso 1 y 3, x=a anula el denominador en la expresión original,
                # por lo que matemáticamente no está definida en la función original.
                return None 
            elif self.caso == 2:
                # El tramo 2 incluye el x >= a
                return x + self.d4

        # --- EVALUACIÓN GENERAL / NUMÉRICA ---
        if self.caso == 1:
            # f(x) = ((x - a)*(x + d1)) / (x - a)
            # Al aproximar numéricamente, si x está muy cerca de a (pero x != a),
            # calculamos el valor real de la división sin simplificar simbiólicamente.
            denominador = x - self.a
            if denominador == 0:
                return None
            return ((x - self.a) * (x + self.d1)) / denominador

        elif self.caso == 2:
            # Tramo por izquierda (x < a) y derecha (x >= a)
            if x < self.a:
                return x + self.d2
            else:
                return x + self.d4

        elif self.caso == 3:
            # f(x) = (d5 + 1) / (x - a)
            denominador = x - self.a
            if denominador == 0:
                return float('inf')  # Representación simbólica nativa de infinito
            return (self.d5 + 1) / denominador

    def generar_tabla_valores(self):
        """
        Genera la evidencia computacional requerida en la Fase 4.
        Retorna dos listas de tuplas (x, f(x)): una por izquierda y otra por derecha.
        """
        desplazamientos = [1.0, 0.1, 0.01, 0.001]
        
        tabla_izquierda = []
        for h in desplazamientos:
            x_val = self.a - h
            y_val = self.evaluar_funcion(x_val, aproximacion=True)
            tabla_izquierda.append((x_val, y_val))
            
        # Revertir para que quede en orden de acercamiento hacia 'a' (a-1, a-0.1, ...)
        # tabla_izquierda.reverse() 

        tabla_derecha = []
        for h in reversed(desplazamientos): # Para que empiece desde a+0.001 hacia a+1
            x_val = self.a + h
            y_val = self.evaluar_funcion(x_val, aproximacion=True)
            tabla_derecha.append((x_val, y_val))

        return tabla_izquierda, tabla_derecha

    def obtener_analisis_teorico(self):
        """
        Retorna las respuestas correctas internas para validar el comportamiento,
        las cuales servirán para verificar si el alumno responde bien en la UI.
        """
        analisis = {}
        
        if self.caso == 1:
            lim_izq = self.a + self.d1
            lim_der = self.a + self.d1
            analisis["limite_izquierdo"] = lim_izq
            analisis["limite_derecho"] = lim_der
            analisis["existe_limite"] = "Sí"
            analisis["valor_funcion"] = "No definido"
            analisis["es_continua"] = "No"
            analisis["tipo_discontinuidad"] = "Removible"
            analisis["justificacion"] = (
                f"El límite existe por ambos lados e iguala a {lim_izq:.4f}, "
                f"pero la función original no está definida en x = {self.a} "
                f"debido a la indeterminación 0/0."
            )
            
        elif self.caso == 2:
            lim_izq = self.a + self.d2
            lim_der = self.a + self.d4
            existe = "Sí" if lim_izq == lim_der else "No"
            analisis["limite_izquierdo"] = lim_izq
            analisis["limite_derecho"] = lim_der
            analisis["existe_limite"] = existe
            analisis["valor_funcion"] = lim_der  # Evaluado en el segundo tramo
            analisis["es_continua"] = "Sí" if (existe == "Sí" and lim_izq == lim_der) else "No"
            analisis["tipo_discontinuidad"] = "No presenta (Continua)" if existe == "Sí" else "De Salto"
            analisis["justificacion"] = (
                f"Límite izquierdo = {lim_izq:.4f} y Límite derecho = {lim_der:.4f}. "
                f"Al ser distintos, se produce una ruptura o salto finito en el plano."
            )
            
        elif self.caso == 3:
            # Dependiendo de si (d5 + 1) es positivo (siempre lo será ya que d5 >= 0)
            # Por izquierda tiende a -inf, por derecha tiende a +inf
            analisis["limite_izquierdo"] = "-Infinito"
            analisis["limite_derecho"] = "+Infinito"
            analisis["existe_limite"] = "No"
            analisis["valor_funcion"] = "No definido"
            analisis["es_continua"] = "No"
            analisis["tipo_discontinuidad"] = "Infinita"
            analisis["justificacion"] = (
                f"Al acercarse a x = {self.a}, el denominador se aproxima a 0. "
                f"La función crece sin límite hacia +inf por la derecha y decrece a -inf por la izquierda, "
                f"delatando una asíntota vertical."
            )
            
        return analisis