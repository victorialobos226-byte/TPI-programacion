import os

MENU = (
    "\n===== MENÚ PRINCIPAL =====\n"
    "1) Agregar un país\n"
    "2) Actualizar población y superficie\n"
    "3) Buscar país por nombre\n"
    "4) Filtrar por continente\n"
    "5) Filtrar por rango de población\n"
    "6) Filtrar por rango de superficie\n"
    "7) Ordenar países\n"
    "8) Ver estadísticas\n"
    "0) Salir\n"
    "===========================\n"
)


def configurar_consola():
    if os.name == "nt":
        try:
            os.system("")
        except Exception:
            pass


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_menu():
    print(MENU)


def pausar():
    input("\nPresioná Enter para continuar...")


def mostrar_error(mensaje):
    print(f"[ERROR] {mensaje}")


def mostrar_exito(mensaje):
    print(f"[OK] {mensaje}")


def leer_texto(mensaje, obligatorio=True):
    while True:
        texto = input(mensaje).strip()
        if texto or not obligatorio:
            return texto
        mostrar_error("No se permite dejar este campo vacío.")


def leer_entero_positivo(mensaje):
    while True:
        texto = leer_texto(mensaje)
        try:
            numero = int(texto)
        except ValueError:
            mostrar_error("Ingresá un número entero válido.")
            continue
        if numero <= 0:
            mostrar_error("El valor debe ser mayor que cero.")
            continue
        return numero


def leer_entero_no_negativo(mensaje):
    while True:
        texto = leer_texto(mensaje)
        try:
            numero = int(texto)
        except ValueError:
            mostrar_error("Ingresá un número entero válido.")
            continue
        if numero < 0:
            mostrar_error("El valor no puede ser negativo.")
            continue
        return numero


def leer_si_no(mensaje):
    while True:
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        mostrar_error("Respondé con 's' o 'n'.")


def leer_opcion():
    while True:
        texto = leer_texto("Elegí una opción (0-8): ")
        try:
            opcion = int(texto)
        except ValueError:
            mostrar_error("Ingresá un número de opción válido.")
            continue
        if 0 <= opcion <= 8:
            return opcion
        mostrar_error("Opción fuera de rango (0-8).")


def solicitar_datos_pais():
    print("\n--- Agregar país ---")
    return {
        "nombre": leer_texto("Nombre del país: "),
        "poblacion": leer_entero_positivo("Población (entero positivo): "),
        "superficie": leer_entero_positivo("Superficie en km² (entero positivo): "),
        "continente": leer_texto("Continente: "),
    }


def solicitar_datos_actualizacion():
    print("\n--- Actualizar país ---")
    return {
        "nombre": leer_texto("Nombre exacto del país a actualizar: "),
        "poblacion": leer_entero_positivo("Nueva población (entero positivo): "),
        "superficie": leer_entero_positivo("Nueva superficie en km² (entero positivo): "),
    }


def seleccionar_continente(paises):
    continentes = sorted({p["continente"] for p in paises}, key=str.casefold)
    if continentes:
        print("\nContinentes disponibles: " + ", ".join(continentes))
    else:
        print("\nNo hay continentes cargados.")
    continente = leer_texto("Continente a filtrar: ")
    return continente


def solicitar_rango(campo):
    etiqueta = "Población" if campo == "poblacion" else "Superficie"
    print(f"\n--- Filtrar por rango de {etiqueta.lower()} ---")
    while True:
        minimo = leer_entero_no_negativo(f"{etiqueta} mínima (0 o más): ")
        maximo = leer_entero_no_negativo(f"{etiqueta} máxima (0 o más): ")
        if minimo > maximo:
            mostrar_error("El mínimo no puede ser mayor que el máximo.")
            continue
        return minimo, maximo


def solicitar_orden():
    print("\nCriterios de ordenamiento:")
    print("1) Nombre")
    print("2) Población")
    print("3) Superficie")
    while True:
        opcion = leer_texto("Elegí el criterio (1-3): ")
        if opcion == "1":
            campo = "nombre"
            break
        if opcion == "2":
            campo = "poblacion"
            break
        if opcion == "3":
            campo = "superficie"
            break
        mostrar_error("Criterio inválido. Elegí 1, 2 o 3.")
    descendente = leer_si_no("¿Querés orden descendente?")
    return campo, descendente


def mostrar_paises(paises, titulo="Países"):
    if not paises:
        mostrar_error("No hay resultados para mostrar.")
        return
    print(f"\n{titulo} ({len(paises)}):")
    print("-" * 90)
    print(f"{'Nombre':<25} {'Población':>15} {'Superficie (km²)':>18}  {'Continente'}")
    print("-" * 90)
    for p in paises:
        print(
            f"{p['nombre']:<25} {p['poblacion']:>15,} {p['superficie']:>18,}  {p['continente']}"
        )
    print("-" * 90)


def mostrar_estadisticas(stats):
    if not stats or stats.get("cantidad", 0) == 0:
        mostrar_error("No hay datos para calcular estadísticas.")
        return
    print("\n===== ESTADÍSTICAS =====")
    print(f"Total de países: {stats['cantidad']}")
    mayor = stats["mayor_poblacion"]
    menor = stats["menor_poblacion"]
    print(f"Mayor población: {mayor['nombre']} ({mayor['poblacion']:,} hab.)")
    print(f"Menor población: {menor['nombre']} ({menor['poblacion']:,} hab.)")
    print(f"Promedio de población: {stats['promedio_poblacion']:,.2f} hab.")
    print(f"Promedio de superficie: {stats['promedio_superficie']:,.2f} km²")
    print("Países por continente:")
    for item in stats["por_continente"]:
        print(f"  - {item['nombre']}: {item['cantidad']}")
    print("=========================")
