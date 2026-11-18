# QuimBío Minería · Sistema de Monitoreo de Producción

> **Empresa ficticia.** Proyecto de portafolio desarrollado con fines de aprendizaje. Todos los datos son generados con Python y no representan a ninguna empresa real.

## Descripción

Sistema de monitoreo de producción para la **Línea 1 (floculantes)** de QuimBío Minería, una planta ficticia de reactivos químicos para la minería del cobre ubicada en Coronel, Región del Biobío.

El objetivo es **identificar dónde se pierde tiempo productivo**, a partir del registro de detenciones de las máquinas, para priorizar acciones de mejora.

## Funcionalidades actuales

- **Disponibilidad anual** de los reactores, comparada con la meta del 80%.
- **Horas-reactor detenidas** y **número de detenciones** del período.
- **Diagrama de Pareto** de las causas de detención, ponderado por tiempo perdido.
- **Evolución mensual** de las horas detenidas, con el umbral máximo para cumplir la meta.
- **Filtro por turno** (día y noche).

## Metodología

Los datos se generan con un **modelo de simulación** del ciclo de los dos reactores de la línea, que son su cuello de botella. Cada reactor procesa lotes de 8 t en 7 h y, después de cada lote, puede detenerse por limpieza (D01), espera del laboratorio (D02), falla mecánica (D03) o falta de materia prima (D04). Cada detención queda registrada con su hora de inicio y de término. Los parámetros del modelo están calibrados para ser coherentes con las metas de la ficha de la empresa.

Como los dos reactores operan en paralelo, la disponibilidad se mide en horas-reactor:

```
Disponibilidad = (Horas-reactor planificadas − Horas-reactor detenidas) / Horas-reactor planificadas
```

Con dos reactores operando todo el año, las horas-reactor planificadas son 8.760 × 2 = 17.520. El Pareto ordena las causas según las horas perdidas y no según la cantidad de eventos, porque una causa poco frecuente pero de larga duración puede afectar más la disponibilidad.

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
│   ├── simular_planta.py       # Simula los reactores y genera los datos
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
python scripts/simular_planta.py
streamlit run app.py
```

## Próximos pasos

- [x] Medir la disponibilidad sobre la máquina **cuello de botella** (reactores).
- [x] Registrar la **hora de inicio** de cada detención, sin superposiciones en un mismo reactor.
- [ ] Incorporar la **parada anual** de 14 días al modelo.
- [ ] Calcular el **OEE** completo (disponibilidad, rendimiento y calidad) con semáforo de metas.
- [ ] Incorporar las Líneas 2 y 3, mantención (MTBF y MTTR), calidad, ambiente y logística.
- [ ] Publicar el dashboard en internet.

## Autora

**Loreto Caro** · Estudiante de Ingeniería Civil Industrial (UNAB)