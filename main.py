
from pathlib import Path
import paises as dominio
import ui

RUTA_CSV = Path(__file__).with_name("paises.csv")


def cargar_datos():
    try:
        return dominio.cargar_paises(RUTA_CSV)
    except ValueError as error:
        ui.mostrar_error(f"No se pudo cargar el dataset: {error}")
        if ui.leer_si_no("¿Iniciar con una lista vacía?"):
            ui.mostrar_error()
            return []
        raise SystemExit(0) from None


def persistir(paises):
    try:
        dominio.guardar_paises(RUTA_CSV, paises)
    except OSError as error:
        ui.mostrar_error(f"No se pudo guardar el CSV: {error}")
    else:
        ui.mostrar_exito("Datos guardados en paises.csv.")


def opcion_agregar(paises):
    datos = ui.solicitar_datos_pais()
    try:
        pais = dominio.agregar_pais(paises, datos)
    except ValueError as error:
        ui.mostrar_error(str(error))
        return
    ui.mostrar_exito(f"Se agregó '{pais['nombre']}'.")
    persistir(paises)


def opcion_actualizar(paises):
    datos = ui.solicitar_datos_actualizacion()
    try:
        pais = dominio.actualizar_pais(
            paises, datos["nombre"], datos["poblacion"], datos["superficie"]
        )
    except ValueError as error:
        ui.mostrar_error(str(error))
        return
    ui.mostrar_exito(f"Se actualizó '{pais['nombre']}'.")
    persistir(paises)


def opcion_buscar(paises):
    termino = ui.leer_texto("Nombre o parte del nombre a buscar: ")
    resultados = dominio.buscar_por_nombre(paises, termino)
    ui.mostrar_paises(resultados, f"Resultados para '{termino}'")


def opcion_filtrar_continente(paises):
    """Maneja la opción 4 del menú."""
    continente = ui.seleccionar_continente(paises)
    if continente is None:
        return
    resultados = dominio.filtrar_por_continente(paises, continente)
    ui.mostrar_paises(resultados, f"Países de '{continente}'")


def opcion_filtrar_rango(paises, campo):
    """Maneja los filtros 5 y 6 del menú."""
    minimo, maximo = ui.solicitar_rango(campo)
    resultados = dominio.filtrar_por_rango(paises, campo, minimo, maximo)
    etiqueta = "población" if campo == "poblacion" else "superficie"
    ui.mostrar_paises(resultados, f"Países por {etiqueta}")


def opcion_filtrar_poblacion(paises):
    """Maneja la opción 5 del menú."""
    opcion_filtrar_rango(paises, "poblacion")


def opcion_filtrar_superficie(paises):
    """Maneja la opción 6 del menú."""
    opcion_filtrar_rango(paises, "superficie")


def opcion_ordenar(paises):
    """Maneja la opción 7 del menú."""
    campo, descendente = ui.solicitar_orden()
    resultados = dominio.ordenar_paises(paises, campo, descendente)
    sentido = "descendente" if descendente else "ascendente"
    ui.mostrar_paises(resultados, f"Orden por {campo} ({sentido})")


def opcion_estadisticas(paises):
    """Maneja la opción 8 del menú."""
    ui.mostrar_estadisticas(dominio.calcular_estadisticas(paises))


ACCIONES = {
    1: opcion_agregar,
    2: opcion_actualizar,
    3: opcion_buscar,
    4: opcion_filtrar_continente,
    5: opcion_filtrar_poblacion,
    6: opcion_filtrar_superficie,
    7: opcion_ordenar,
    8: opcion_estadisticas,
}


def procesar_opcion(opcion, paises):
    """Ejecuta la acción asociada a la opción elegida."""
    accion = ACCIONES.get(opcion)
    if accion is None:
        ui.mostrar_error("Opción no reconocida.")
        return
    accion(paises)


def main():
    """Inicia la aplicación y mantiene el ciclo del menú."""
    ui.configurar_consola()
    paises = cargar_datos()

    while True:
        ui.limpiar_pantalla()
        print("===== GESTOR DE PAÍSES =====")
        print(f"Archivo: {RUTA_CSV.name} | Países cargados: {len(paises)}")
        ui.mostrar_menu()

        opcion = ui.leer_opcion()
        if opcion == 0:
            ui.mostrar_exito("Hasta luego. Los cambios ya quedaron guardados.")
            break

        procesar_opcion(opcion, paises)
        ui.pausar()


if __name__ == "__main__":
    main()
