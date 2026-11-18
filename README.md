# QuimBío Minería · Sistema de Monitoreo de Producción

> **Empresa ficticia.** Proyecto de portafolio desarrollado con fines de aprendizaje. Todos los datos son generados con Python y no representan a ninguna empresa real.

## Descripción

Sistema de monitoreo de producción para la **Línea 1 (floculantes)** de QuimBío Minería, una planta ficticia de reactivos químicos para la minería del cobre ubicada en Coronel, Región del Biobío.

El objetivo es **identificar dónde se pierde tiempo productivo**, a partir del registro de detenciones de las máquinas, para priorizar acciones de mejora.

## Funcionalidades actuales

- **Disponibilidad anual** de la línea, comparada con la meta del 80%.
- **Horas detenidas** y **número de detenciones** del período.
- **Diagrama de Pareto** de las causas de detención, ponderado por tiempo perdido.
- **Evolución mensual** de las horas detenidas, con el umbral máximo para cumplir la meta.
- **Filtro por turno** (día y noche).

## Metodología

La disponibilidad se calcula como:

```
Disponibilidad = (Horas planificadas − Horas detenidas) / Horas planificadas
```

Las horas planificadas de la Línea 1 son 8.424 h al año (operación 24/7, descontando 14 días de parada anual). El Pareto ordena las causas según las horas perdidas y no según la cantidad de eventos, porque una causa poco frecuente pero de larga duración puede afectar más la disponibilidad.

La definición completa de la empresa (máquinas, turnos, catálogo de causas y metas) está en [`docs/ficha_empresa.md`](docs/ficha_empresa.md).

## Tecnologías

Python · pandas · NumPy · Streamlit · Plotly · Git y GitHub

## Estructura del proyecto

```
├── app.py                      # Dashboard web (Streamlit)
├── requirements.txt            # Librerías necesarias
├── data/                       # Datos generados (CSV)
├── docs/                       # Ficha técnica de la empresa
├── scripts/
│   ├── generar_detenciones.py  # Genera los datos de detenciones
│   └── analisis_anual.py       # Análisis anual por consola
└── ejercicios/                 # Prácticas de aprendizaje de Python
```

## Cómo ejecutarlo

```
git clone https://github.com/loreto-caro/quimbio-monitoreo-produccion.git
cd quimbio-monitoreo-produccion
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/generar_detenciones.py
streamlit run app.py
```

## Próximos pasos

- [ ] Calcular el **OEE** completo (disponibilidad, rendimiento y calidad) con semáforo de metas.
- [ ] Medir la disponibilidad sobre la máquina **cuello de botella** (reactores).
- [ ] Registrar la **hora de inicio** de cada detención y validar que no se superpongan.
- [ ] Incorporar las Líneas 2 y 3, mantención (MTBF y MTTR), calidad, ambiente y logística.
- [ ] Publicar el dashboard en internet.

## Autora

**Loreto Caro** · Estudiante de Ingeniería Civil Industrial (UNAB)