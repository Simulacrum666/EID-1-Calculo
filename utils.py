def validar_rut(rut: str):

    pasos = []

    rut_limpio = rut.replace(".", "").replace("-", "").strip().upper()

    if len(rut_limpio) < 2:
        return False, ["RUT inválido"]

    cuerpo = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]

    if not cuerpo.isdigit():
        return False, ["El cuerpo debe tener solo números"]

    pasos.append(f"RUT ingresado: {rut}")

    suma = 0
    multiplicador = 2

    for digito in reversed(cuerpo):

        producto = int(digito) * multiplicador
        suma += producto

        pasos.append(f"{digito} × {multiplicador} = {producto}")

        multiplicador += 1

        if multiplicador > 7:
            multiplicador = 2

    resto = suma % 11
    dv = 11 - resto

    if dv == 11:
        dv_esperado = "0"

    elif dv == 10:
        dv_esperado = "K"

    else:
        dv_esperado = str(dv)

    pasos.append(f"Suma = {suma}")
    pasos.append(f"Resto = {resto}")
    pasos.append(f"DV esperado = {dv_esperado}")

    return dv_esperado == dv_ingresado, pasos


def extraer_digitos(rut: str):

    rut_limpio = rut.replace(".", "").replace("-", "").strip().upper()

    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]

    digitos = [int(x) for x in cuerpo[:8]]

    return digitos, dv


def calcular_v(dv: str):

    if dv == "K":
        return 10

    if dv == "0":
        return 11

    return int(dv)


def sqrt_manual(n):

    if n <= 0:
        return 0

    x = n

    for _ in range(30):
        x = (x + n / x) / 2

    return x


PI = 3.141592653589793


def potencia(x, n):

    resultado = 1

    for _ in range(n):
        resultado *= x

    return resultado


def factorial(n):

    resultado = 1

    for i in range(2, n + 1):
        resultado *= i

    return resultado


def sin_manual(x):

    while x > 2 * PI:
        x -= 2 * PI

    resultado = 0

    for n in range(10):

        signo = -1 if n % 2 else 1

        resultado += (
            signo *
            potencia(x, 2 * n + 1) /
            factorial(2 * n + 1)
        )

    return resultado


def cos_manual(x):

    while x > 2 * PI:
        x -= 2 * PI

    resultado = 0

    for n in range(10):

        signo = -1 if n % 2 else 1

        resultado += (
            signo *
            potencia(x, 2 * n) /
            factorial(2 * n)
        )

    return resultado