
import csv
CAMPOS = ("nombre", "poblacion", "superficie", "continente")


def validar_texto(valor, campo):
    """Devuelve un texto limpio o lanza ValueError si está vacío."""
    if valor is None:
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    texto = str(valor).strip()
    if not texto:
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    return texto


def _convertir_entero(valor, campo):
    """Convierte un valor a entero o lanza un error descriptivo."""
    if valor is None:
        raise ValueError(f"El campo '{campo}' debe ser un número entero.")
    texto = str(valor).strip()
    try:
        return int(texto)
    except ValueError:
        raise ValueError(f"El campo '{campo}' debe ser un número entero.") from None


def validar_entero_positivo(valor, campo):
    """Valida que el entero sea mayor que cero."""
    numero = _convertir_entero(valor, campo)
    if numero <= 0:
        raise ValueError(f"El campo '{campo}' debe ser mayor que cero.")
    return numero


def validar_entero_no_negativo(valor, campo):
    """Valida enteros para filtros, donde cero sí es permitido."""
    numero = _convertir_entero(valor, campo)
    if numero < 0:
        raise ValueError(f"El campo '{campo}' no puede ser negativo.")
    return numero


def validar_registro(fila, contexto="registro"):
    """Valida un país completo y lo devuelve con tipos correctos."""
    if any(campo not in fila for campo in CAMPOS):
        raise ValueError(f"{contexto}: faltan columnas obligatorias.")

    registro = {}
    for campo in ("nombre", "continente"):
        try:
            registro[campo] = validar_texto(fila[campo], campo)
        except ValueError as error:
            raise ValueError(f"{contexto}: {error}") from None

    for campo in ("poblacion", "superficie"):
        try:
            registro[campo] = validar_entero_positivo(fila[campo], campo)
        except ValueError as error:
            raise ValueError(f"{contexto}: {error}") from None

    return registro


def cargar_paises(ruta):
    """Lee el CSV y devuelve una lista de diccionarios validados."""
    try:
        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)

            if not lector.fieldnames:
                raise ValueError("El CSV está vacío o no tiene encabezado.")

            mapa = {
                original: original.strip()
                for original in lector.fieldnames
                if original is not None
            }
            if set(mapa.values()) != set(CAMPOS):
                raise ValueError(
                    "Encabezado inválido. Se esperaban: " + ", ".join(CAMPOS) + "."
                )

            paises = []
            nombres_vistos = set()

            for fila in lector:
                numero = lector.line_num
                if None in fila or any(valor is None for valor in fila.values()):
                    raise ValueError(
                        f"Fila {numero}: cantidad de columnas incorrecta."
                    )

                canonico = {
                    nombre: (fila.get(original) or "").strip()
                    for original, nombre in mapa.items()
                }
                pais = validar_registro(canonico, contexto=f"Fila {numero}")

                clave = pais["nombre"].casefold()
                if clave in nombres_vistos:
                    raise ValueError(
                        f"Fila {numero}: el país '{pais['nombre']}' está repetido."
                    )
                nombres_vistos.add(clave)
                paises.append(pais)

            return paises
    except FileNotFoundError:
        raise ValueError(f"No se encontró el archivo '{ruta}'.") from None
    except UnicodeDecodeError:
        raise ValueError("El archivo CSV no usa codificación UTF-8.") from None
    except csv.Error as error:
        raise ValueError(f"Error al leer el CSV: {error}") from None


def guardar_paises(ruta, paises):
    """Escribe la lista de países en el CSV respetando el encabezado."""
    with open(ruta, "w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(paises)


def buscar_indice_exacto(paises, nombre):
    """Devuelve el índice del país con ese nombre exacto, o -1."""
    objetivo = validar_texto(nombre, "nombre").casefold()
    for indice, pais in enumerate(paises):
        if pais["nombre"].casefold() == objetivo:
            return indice
    return -1


def agregar_pais(paises, datos):
    """Agrega un país nuevo validado y devuelve el registro insertado."""
    pais = validar_registro(datos, contexto="Nuevo país")
    if buscar_indice_exacto(paises, pais["nombre"]) != -1:
        raise ValueError(f"El país '{pais['nombre']}' ya existe.")
    paises.append(pais)
    return pais


def actualizar_pais(paises, nombre, poblacion, superficie):
    """Actualiza sólo población y superficie de un país existente."""
    indice = buscar_indice_exacto(paises, nombre)
    if indice == -1:
        raise ValueError(f"No se encontró el país '{nombre}'.")

    datos = dict(paises[indice])
    datos["poblacion"] = validar_entero_positivo(poblacion, "población")
    datos["superficie"] = validar_entero_positivo(superficie, "superficie")
    paises[indice] = datos
    return datos


def buscar_por_nombre(paises, termino):
    """Busca coincidencias parciales e independientes de mayúsculas."""
    texto = validar_texto(termino, "búsqueda").casefold()
    return [pais for pais in paises if texto in pais["nombre"].casefold()]


def obtener_continentes(paises):
    """Devuelve la lista ordenada de continentes sin repetir."""
    vistos = {}
    for pais in paises:
        vistos.setdefault(pais["continente"].casefold(), pais["continente"])
    return sorted(vistos.values(), key=str.casefold)


def filtrar_por_continente(paises, continente):
    """Filtra por continente exacto, ignorando mayúsculas."""
    texto = validar_texto(continente, "continente").casefold()
    return [pais for pais in paises if pais["continente"].casefold() == texto]


def validar_rango(minimo, maximo):
    """Comprueba que el rango esté bien formado."""
    if minimo > maximo:
        raise ValueError("El mínimo no puede ser mayor que el máximo.")
    return minimo, maximo


def filtrar_por_rango(paises, campo, minimo, maximo):
    """Filtra por población o superficie entre dos valores inclusive."""
    if campo not in ("poblacion", "superficie"):
        raise ValueError("El campo del rango no es válido.")

    minimo = validar_entero_no_negativo(minimo, "mínimo")
    maximo = validar_entero_no_negativo(maximo, "máximo")
    minimo, maximo = validar_rango(minimo, maximo)

    return [pais for pais in paises if minimo <= pais[campo] <= maximo]


def ordenar_paises(paises, campo, descendente=False):
    """Devuelve una nueva lista ordenada; no modifica la original."""
    if campo not in ("nombre", "poblacion", "superficie"):
        raise ValueError("El criterio de ordenamiento no es válido.")

    if campo == "nombre":
        clave = lambda pais: pais["nombre"].casefold()
    else:
        clave = lambda pais: pais[campo]

    return sorted(paises, key=clave, reverse=descendente)


def calcular_estadisticas(paises):
    """Calcula extremos, promedios y cantidades por continente."""
    if not paises:
        return {
            "cantidad": 0,
            "mayor_poblacion": None,
            "menor_poblacion": None,
            "promedio_poblacion": 0,
            "promedio_superficie": 0,
            "por_continente": [],
        }

    total = len(paises)
    conteo = {}
    for pais in paises:
        clave = pais["continente"].casefold()
        if clave not in conteo:
            conteo[clave] = {"nombre": pais["continente"], "cantidad": 0}
        conteo[clave]["cantidad"] += 1

    return {
        "cantidad": total,
        "mayor_poblacion": max(paises, key=lambda pais: pais["poblacion"]),
        "menor_poblacion": min(paises, key=lambda pais: pais["poblacion"]),
        "promedio_poblacion": sum(pais["poblacion"] for pais in paises) / total,
        "promedio_superficie": sum(pais["superficie"] for pais in paises) / total,
        "por_continente": [
            conteo[clave] for clave in sorted(conteo, key=str.casefold)
        ],
    }
