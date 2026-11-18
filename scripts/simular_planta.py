"""
Simulador de la Línea 1 (floculantes) de QuimBío Minería.

Simula el ciclo de los dos reactores (cuello de botella de la línea) durante 2026
y genera las tablas de lotes y detenciones en la carpeta data/.
"""
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# ===== Parámetros del modelo (calibrados) =====
SEMILLA = 42
INICIO = datetime(2026, 1, 1, 0, 0)
FIN = datetime(2027, 1, 1, 0, 0)
REACTORES = ["QBM-L1-R01", "QBM-L1-R02"]

# Parada anual programada (mantención mayor de verano)
INICIO_PARADA = datetime(2026, 2, 1, 8, 0)
DIAS_PARADA = 14

HORAS_REACCION = 7
TONELADAS_POR_LOTE = 8

# Causa: (probabilidad después de cada lote, minutos mínimos, minutos máximos)
DETENCIONES = {
    "D01": (1.00, 45, 90),    # Limpieza y cambio entre lotes
    "D02": (0.15, 30, 150),   # Espera de liberación del laboratorio
    "D03": (0.05, 30, 180),   # Falla mecánica
    "D04": (0.04, 60, 300),   # Falta de materia prima
}

rng = np.random.default_rng(SEMILLA)


def simular_reactor(reactor):
    """Simula un reactor durante todo el período y devuelve sus lotes y detenciones."""
    reloj = INICIO
    lotes = []
    detenciones = []
    numero = 0
    parada_realizada = False

    while reloj < FIN:
        # Parada anual: comienza al terminar el lote en curso
        if not parada_realizada and reloj >= INICIO_PARADA:
            reloj = reloj + timedelta(days=DIAS_PARADA)
            parada_realizada = True

        # Reacción del lote
        numero = numero + 1
        inicio = reloj
        reloj = reloj + timedelta(hours=HORAS_REACCION)
        lotes.append({"reactor": reactor, "lote": numero, "inicio": inicio,
                      "fin": reloj, "toneladas": TONELADAS_POR_LOTE})

        # Detenciones que pueden ocurrir después del lote
        for causa, (probabilidad, minimo, maximo) in DETENCIONES.items():
            if rng.random() < probabilidad:
                inicio = reloj
                reloj = reloj + timedelta(minutes=int(rng.integers(minimo, maximo + 1)))
                detenciones.append({"maquina": reactor, "causa": causa,
                                    "inicio": inicio, "fin": reloj})

    return lotes, detenciones


# ===== Simulación de los dos reactores =====
todos_los_lotes = []
todas_las_detenciones = []
for reactor in REACTORES:
    lotes, detenciones = simular_reactor(reactor)
    todos_los_lotes = todos_los_lotes + lotes
    todas_las_detenciones = todas_las_detenciones + detenciones

df_lotes = pd.DataFrame(todos_los_lotes)
df_det = pd.DataFrame(todas_las_detenciones)

# ===== Cierre del período: solo cuenta lo ocurrido dentro de 2026 =====
df_lotes = df_lotes[df_lotes["fin"] <= FIN]
df_det = df_det[df_det["inicio"] < FIN]
df_det["fin"] = df_det["fin"].clip(upper=FIN)

# ===== Columnas calculadas =====
df_det["minutos"] = (df_det["fin"] - df_det["inicio"]).dt.total_seconds() / 60
df_det["fecha"] = df_det["inicio"].dt.date
df_det["turno"] = np.where(df_det["inicio"].dt.hour.between(8, 19), "Día", "Noche")

# ===== Guardar =====
df_lotes.to_csv("data/lotes_L1_2026.csv", index=False)
df_det.to_csv("data/detenciones_L1_2026.csv", index=False)

# ===== Validación del modelo =====
horas_parada = DIAS_PARADA * 24
horas_planificadas = ((FIN - INICIO).total_seconds() / 3600 - horas_parada) * len(REACTORES)
horas_detenidas = df_det["minutos"].sum() / 60
disponibilidad = (horas_planificadas - horas_detenidas) / horas_planificadas * 100

print("Lotes completados:", len(df_lotes), "| Toneladas:", df_lotes["toneladas"].sum())
print("Detenciones registradas:", len(df_det))
print("Disponibilidad de los reactores:", round(disponibilidad, 1), "%")
print("--- Horas detenidas por causa ---")
print((df_det.groupby("causa")["minutos"].sum() / 60).round(1))