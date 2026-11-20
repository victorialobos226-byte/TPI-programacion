# TPI - Gestión de Datos de Países en Python

Trabajo Práctico Integrador de Programación I.  
Aplicación de consola en Python 3 para gestionar información de países desde un archivo CSV.

## Descripción del programa

El sistema carga un dataset de países (`paises.csv`) en una lista de diccionarios y permite:
- Agregar un país (validando que no haya campos vacíos ni duplicados).
- Actualizar población y superficie de un país existente.
- Buscar países por nombre (coincidencia parcial o exacta, sin distinguir mayúsculas/minúsculas).
- Filtrar países por continente, rango de población o rango de superficie.
- Ordenar países por nombre, población o superficie (ascendente o descendente).
- Mostrar estadísticas: país con mayor y menor población, promedios de población y superficie, y cantidad de países por continente.

Los cambios de alta y actualización se guardan automáticamente en el archivo CSV.

## Estructura del repositorio

```text
TPI-programacion/
├── main.py                 # Punto de entrada, menú y coordinación
├── paises.py               # Lógica de dominio, validaciones, CSV, filtros, orden y estadísticas
├── ui.py                   # Interfaz de consola (entradas/salidas y formato)
├── paises.csv              # Dataset base
├── README.md               # Descripción e instrucciones
├── guion_video.md          # Guion para la demostración en video
├── documentacion.html      # Documentación académica y técnica (fuente imprimible)
└── documentacion.pdf       # Documentación académica y técnica en PDF
```

## Requisitos

- Python 3.8 o superior.
- Sin dependencias externas (solo biblioteca estándar: `csv`, `pathlib`, `os`).

## Instrucciones de uso

1. Abrir una terminal en la carpeta del proyecto.
2. Ejecutar:

```bash
python main.py
```

En Windows también puede usarse `py main.py`.

3. Utilizar el menú numérico para operar:

| Opción | Funcionalidad |
| --- | --- |
| 1 | Agregar un país |
| 2 | Actualizar población y superficie de un país |
| 3 | Buscar país por nombre (parcial o exacta) |
| 4 | Filtrar por continente |
| 5 | Filtrar por rango de población |
| 6 | Filtrar por rango de superficie |
| 7 | Ordenar países (nombre/población/superficie, asc/desc) |
| 8 | Ver estadísticas |
| 0 | Salir |

## Ejemplos de entradas y salidas

### Inicio

```text
===== GESTOR DE PAÍSES =====
Archivo: paises.csv | Países cargados: 8

===== MENÚ PRINCIPAL =====
1) Agregar un país
2) Actualizar población y superficie
3) Buscar país por nombre
4) Filtrar por continente
5) Filtrar por rango de población
6) Filtrar por rango de superficie
7) Ordenar países
8) Ver estadísticas
0) Salir
===========================
```

### Agregar un país

```text
Elegí una opción (0-8): 1
Nombre del país: Portugal
Población (entero positivo): 10447800
Superficie en km² (entero positivo): 92212
Continente: Europa
[OK] Se agregó 'Portugal'.
[OK] Datos guardados en paises.csv.
```

### Búsqueda parcial

```text
Elegí una opción (0-8): 3
Nombre o parte del nombre a buscar: bra

Resultados para 'bra' (1):
------------------------------------------------------------------------------------------
Nombre                     Población   Superficie (km²)  Continente
------------------------------------------------------------------------------------------
Brasil                    213,993,437         8,515,767  América
------------------------------------------------------------------------------------------
```

### Estadísticas

```text
Elegí una opción (0-8): 8

===== ESTADÍSTICAS =====
Total de países: 8
Mayor población: India (1,428,627,663 hab.)
Menor población: Australia (26,464,903 hab.)
Promedio de población: 259,389,552.13 hab.
Promedio de superficie: 4,249,741.75 km²
Países por continente:
  - África: 1
  - América: 3
  - Asia: 2
  - Europa: 1
  - Oceanía: 1
=========================
```

## Validaciones y manejo de errores

- Campos de texto obligatorios (no se permiten vacíos).
- Población y superficie: enteros positivos.
- Rangos: el mínimo no puede ser mayor que el máximo.
- No se permiten países duplicados (comparación sin distinción de mayúsculas).
- Control de formato del CSV (encabezado, columnas, tipos, duplicados, codificación).
- Mensajes claros ante búsquedas/filtros sin resultados y entradas inválidas.

## Participación de los integrantes

- **[Integrante 1 - Nombre y Apellido]**: [Describir aporte: ej. lógica de dominio, validaciones, manejo de CSV, pruebas].
- **[Integrante 2 - Nombre y Apellido]**: [Describir aporte: ej. interfaz de consola, documentación, armado del video].

> Completar con los datos reales del equipo antes de entregar.

## Enlaces obligatorios

- **Repositorio del proyecto:** [Pegar enlace al repositorio de GitHub]
- **Video demostrativo (público):** [Pegar enlace de YouTube/Vimeo/Drive con permisos públicos]
- **Documentación PDF:** incluida en este repositorio como `documentacion.pdf` (y en el ZIP de entrega).

## Contenido del ZIP de entrega

El archivo `.zip` debe incluir:
- Código fuente completo (`main.py`, `paises.py`, `ui.py`).
- Dataset base (`paises.csv`).
- `README.md`.
- `documentacion.pdf` (con carátula, índice, marco teórico, decisiones técnicas, dificultades y conclusiones, bibliografía y enlaces).
- Enlace al video demostrativo público indicado en este README.
