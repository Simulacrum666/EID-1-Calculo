from conica import Conica
from elipse import Elipse
from circunferencia import Circunferencia
from parabola import Parabola
from hiperbola import Hiperbola


def crear_conica_desde_rut(rut):

    base = Conica(rut)

    if base.tipo == "Elipse":
        return Elipse(rut)
    
    if base.tipo == "Circunferencia":
        return Circunferencia(rut)
    
    if base.tipo == "Parabola":
        return Parabola(rut)
    
    if base.tipo == "Hiperbola":
        return Hiperbola(rut)

    raise ValueError(
        f"La cónica generada es '{base.tipo}' "
        "y aún no está implementada"
    )