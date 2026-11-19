# ¿Cómo se usan los aviones widebody en las rutas del mundo?

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DanEan-ux/ProyectoFinalDataExperiencie/blob/main/notebook/analisis_widebody.ipynb)

Proyecto final de Ciencia de Datos del curso **Data Xperience**.

## Introducción y contexto

Los aviones de fuselaje ancho (*widebody*) son los grandes protagonistas de la aviación de largo alcance. Este proyecto usa datos públicos para analizar en qué rutas vuelan seis familias: **A380, Boeing 747, A350, Boeing 777, A330 y Boeing 787**.

Es también un ejercicio de sistemas de información: integrar tablas relacionadas, resolver problemas de calidad de datos y documentar cada decisión para que el análisis se pueda reproducir.

## Objetivo

Describir y comparar cómo se usa cada familia de widebody según la distancia de sus rutas, su distribución geográfica y sus aerolíneas, y evaluar con un modelo simple cuánto ayuda el tipo de avión a explicar la distancia de una ruta.

## Fuentes de datos

| Fuente | Contenido | Periodo | Uso en el proyecto |
|---|---|---|---|
| [OpenFlights](https://github.com/jpatokal/openflights) | Rutas, aeropuertos, aerolíneas y aviones | Rutas hasta junio de 2014 | Fuente principal: A380, 747, 777, A330 y 787 |
| [OpenSky Network](https://doi.org/10.5281/zenodo.5815448) (CC-BY 4.0) | Vuelos observados con señales ADS-B | Octubre de 2019 | Fuente complementaria: las seis familias, con el A350 |

**¿Por qué dos fuentes?** El A350 no tiene ninguna ruta en OpenFlights, porque esa base dejó de actualizarse en junio de 2014. Las dos fuentes miden cosas distintas, así que sus conteos no se comparan entre sí, y todas las comparaciones con el A350 se hacen dentro de OpenSky.

**Cita del dataset de OpenSky:** Strohmeier, M., Olive, X., Lübbe, J., Schäfer, M. y Lenders, V. (2021). *Crowdsourced air traffic data from the OpenSky Network 2019–2020*. Earth System Science Data, 13(2), 357–366. <https://doi.org/10.5194/essd-13-357-2021>

## Estructura del repositorio

```text
ProyectoFinalDataExperiencie/
├── README.md
├── datos/
│   ├── routes.dat, airports.dat, airlines.dat, planes.dat    Originales de OpenFlights
│   ├── opensky_widebody_2019_10.csv.gz                       Extracto de widebody, sin cambiar valores
│   ├── opensky_extracto_info.json                            Datos del archivo completo y su SHA-256
│   ├── crear_extracto_opensky.py                             Descarga el original y genera el extracto
│   ├── rutas_widebody_limpio.csv                             OpenFlights depurado
│   └── opensky_widebody_limpio.csv.gz                        OpenSky depurado
├── notebook/
│   └── analisis_widebody.ipynb
└── presentacion/
    ├── presentacion.pdf                                      Presentación de apoyo
    └── figuras/                                              Gráficos generados por el notebook
```

El original de OpenSky (`flightlist_20191001_20191031.csv.gz`, 242 MB) supera el límite de 100 MB de GitHub, por eso no se sube. Se puede volver a descargar y verificar con `python crear_extracto_opensky.py`, desde la carpeta `datos/`.

## Integrantes

- Danilo Rocha Medina, Ingeniería de Sistemas, Universidad EAN

## Cómo ejecutar el notebook en Colab

1. Haz clic en el botón **Open in Colab** del inicio de esta página.
2. En la primera celda de código, comprueba que `GITHUB_USUARIO` tenga el usuario de GitHub dueño del repositorio.
3. Selecciona **Entorno de ejecución > Ejecutar todas**.

El notebook lee los datos desde la URL *raw* de este repositorio, por lo que el repositorio debe ser público. No hace falta instalar nada: usa pandas, numpy, matplotlib, seaborn y scikit-learn.

## Hallazgos principales

**Foto de 2014 (OpenFlights, 5.841 combinaciones de aerolínea, ruta y familia):**

- **Presencia:** el A330 (2.762) y el 777 (2.030) suman el 82 % de las filas. El A380 es el más escaso (179).
- **Distancia:** el A380 tiene la mediana más alta (8.403 km), y el A330 la más baja (4.204 km).
- **Grande no siempre significa lejos:** la moda del 787 es 400 km, y la del A330, 700 km. Varias familias combinan rutas cortas y de largo alcance.

**Con el A350 (OpenSky, 90.166 vuelos de octubre de 2019):**

- **Distancia:** el A350 tiene la mediana por ruta más alta (7.351 km), seguido del A380 (6.344 km), y el A330 la más baja (4.714 km).
- **Geografía y operadores:** el 53,5 % de los vuelos del A350 sale de Asia, y cinco aerolíneas concentran el 77 %.
- **Una aerolínea pesa mucho:** Emirates aporta el 55 % de los vuelos del A380, con una mediana de 5.498 km frente a 8.616 km del resto.

**Hipótesis:**

| Hipótesis | OpenFlights 2014 | OpenSky 2019 |
|---|---|---|
| 787 más largo que A330 | Apoyada | Apoyada |
| A380 más largo que 787 | Apoyada | No concluyente |
| 777 más largo que 747 | No concluyente | Apoyada (con cautela, por cargueros sin detectar) |
| A350 más largo que A330 | Sin datos | Apoyada |
| A350 más largo que 787 | Sin datos | Apoyada |

**Modelo de regresión lineal:**

| Modelo | R² OpenFlights | MAE OpenFlights | R² OpenSky | MAE OpenSky |
|---|---:|---:|---:|---:|
| Solo tipo de avión | 0,096 | 2.722 km | 0,049 | 2.733 km |
| Con región y tipo de ruta | 0,386 | 2.070 km | 0,430 | 2.034 km |

En validación cruzada, el modelo completo obtiene un R² de 0,386 en OpenFlights y de 0,377 en OpenSky. **El tipo de avión por sí solo explica poco: la distancia depende más de dónde se vuela.** El error sigue siendo grande, así que el modelo sirve para describir asociaciones, no para predecir una ruta concreta.

## Limitaciones

- Los datos terminan en 2014 y 2019, así que no describen el uso actual.
- OpenSky representa un solo mes, con cobertura desigual según dónde haya antenas, y cerca de la mitad de los vuelos widebody se pierde en la limpieza.
- Quedan cargueros y códigos compartidos que no se pudieron detectar. El resultado del 747 en OpenSky es el menos confiable.
- Los umbrales de limpieza y las exclusiones son decisiones mías, explicadas en el notebook.

## Video

[Ver el video en YouTube](https://youtu.be/epMojBvQmIc)
