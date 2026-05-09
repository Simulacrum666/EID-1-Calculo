from conica import Conica
from elipse import Elipse


def crear_conica_desde_rut(rut):

    base = Conica(rut)

    if base.tipo == "Elipse":
        return Elipse(rut)

    raise ValueError(
        f"La cónica generada es '{base.tipo}' "
        "y aún no está implementada"
    )