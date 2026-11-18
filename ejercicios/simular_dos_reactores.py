from datetime import datetime, timedelta
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)


def simular_reactor(reactor, inicio_simulacion, fin_simulacion):
    """Simula el ciclo de un reactor y devuelve sus lotes y detenciones."""
    reloj = inicio_simulacion
    lotes = []
    detenciones = []

    while reloj < fin_simulacion:
        # Etapa 1: reacción del lote
        inicio = reloj
        reloj = reloj + timedelta(hours=7)
        lotes.append({"reactor": reactor, "inicio": inicio, "fin": reloj, "toneladas": 8})

        # Etapa 2: limpieza entre lotes (D01)
        inicio = reloj
        reloj = reloj + timedelta(minutes=int(rng.integers(50, 121)))
        detenciones.append({"reactor": reactor, "inicio": inicio, "fin": reloj, "causa": "D01"})

        # Etapa 3: a veces, espera del laboratorio (D02)
        if rng.random() < 0.30:
            inicio = reloj
            reloj = reloj + timedelta(minutes=int(rng.integers(30, 241)))
            detenciones.append({"reactor": reactor, "inicio": inicio, "fin": reloj, "causa": "D02"})

    return lotes, detenciones


# Simular una semana para los dos reactores
inicio = datetime(2026, 1, 1, 8, 0)
fin = inicio + timedelta(days=7)

lotes_r01, detenciones_r01 = simular_reactor("QBM-L1-R01", inicio, fin)
lotes_r02, detenciones_r02 = simular_reactor("QBM-L1-R02", inicio, fin)

# Juntar ambos reactores en una sola tabla de cada tipo
df_lotes = pd.DataFrame(lotes_r01 + lotes_r02)
df_detenciones = pd.DataFrame(detenciones_r01 + detenciones_r02)
df_detenciones["minutos"] = (df_detenciones["fin"] - df_detenciones["inicio"]).dt.total_seconds() / 60

print("--- Lotes y toneladas por reactor ---")
print(df_lotes.groupby("reactor")["toneladas"].agg(["count", "sum"]))
print("--- Minutos de detención por reactor y causa ---")
print(df_detenciones.groupby(["reactor", "causa"])["minutos"].sum())