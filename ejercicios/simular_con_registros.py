from datetime import datetime, timedelta
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

inicio_simulacion = datetime(2026, 1, 1, 8, 0)
fin_simulacion = inicio_simulacion + timedelta(days=1)

reloj = inicio_simulacion
lotes = []
detenciones = []

while reloj < fin_simulacion:
    # Etapa 1: reacción del lote (8 toneladas en 7 horas)
    inicio = reloj
    reloj = reloj + timedelta(hours=7)
    lotes.append({"inicio": inicio, "fin": reloj, "toneladas": 8})

    # Etapa 2: limpieza entre lotes (D01), siempre ocurre
    inicio = reloj
    reloj = reloj + timedelta(minutes=int(rng.integers(50, 121)))
    detenciones.append({"inicio": inicio, "fin": reloj, "causa": "D01"})

    # Etapa 3: espera de liberación del laboratorio (D02), ocurre solo a veces
    if rng.random() < 0.30:
        inicio = reloj
        reloj = reloj + timedelta(minutes=int(rng.integers(30, 241)))
        detenciones.append({"inicio": inicio, "fin": reloj, "causa": "D02"})

# Convertir las listas en tablas
df_lotes = pd.DataFrame(lotes)
df_detenciones = pd.DataFrame(detenciones)
df_detenciones["minutos"] = (df_detenciones["fin"] - df_detenciones["inicio"]).dt.total_seconds() / 60

print("--- Lotes ---")
print(df_lotes)
print("--- Detenciones ---")
print(df_detenciones)