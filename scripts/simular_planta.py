"""
Simulador de la Línea 1 (floculantes) de QuimBío Minería.

Simula el ciclo de los dos reactores (cuello de botella de la línea) durante 2026
y genera las tablas de lotes y detenciones en la carpeta data/.
Incluye la parada anual, la estacionalidad del invierno y las pérdidas de
rendimiento y calidad necesarias para calcular el OEE.
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

# Lote: 8 t en 7 h ideales (velocidad ideal de 1,143 t/h por reactor)
HORAS_REACCION = 7
TONELADAS_POR_LOTE = 8

# Rendimiento: la reacción real dura más que la ideal
VARIACION_REACCION = (20, 100)   # minutos adicionales en todo lote
PROB_R04 = 0.10                  # R04 Ciclo más largo por control de temperatura
MINUTOS_R04 = (60, 180)

# Calidad: lotes rechazados y pérdidas en el tamizado
PROB_C01 = 0.06                  # C01 Monómero residual sobre el límite: lote rechazado completo
PERDIDA_C03 = (0.00, 0.04)       # C03 Granulometría fuera de rango: fracción perdida

# Detenciones sin estacionalidad: (probabilidad después de cada lote, minutos mínimos, minutos máximos)
DETENCIONES = {
    "D01": (1.00, 50, 100),   # Limpieza y cambio entre lotes
    "D02": (0.15, 30, 150),   # Espera de liberación del laboratorio
    "D03": (0.05, 30, 180),   # Falla mecánica
}

# Estacionalidad de invierno
MESES_INVIERNO = [5, 6, 7, 8]

# D04 Falta de materia prima: más frecuente en invierno por cierres del puerto (marejadas)
PROB_D04_INVIERNO = 0.10
PROB_D04_RESTO = 0.03
MINUTOS_D04 = (60, 300)

# D08 Episodios críticos de contaminación (PPDA): días con restricción de operación
DIAS_EPISODIO = 15
MINUTOS_D08 = (240, 480)

rng = np.random.default_rng(SEMILLA)

# Sorteo de los días de episodio crítico (los mismos para toda la planta)
dias_de_invierno = pd.date_range("2026-05-01", "2026-08-31", freq="D").date
dias_episodio = set(rng.choice(dias_de_invierno, size=DIAS_EPISODIO, replace=False))


def registrar(detenciones, reactor, causa, reloj, minutos):
    """Agrega una detención a la lista y devuelve el reloj avanzado."""
    fin = reloj + timedelta(minutes=minutos)
    detenciones.append({"maquina": reactor, "causa": causa, "inicio": reloj, "fin": fin})
    return fin


def simular_reactor(reactor):
    """Simula un reactor durante todo el período y devuelve sus lotes y detenciones."""
    reloj = INICIO
    lotes = []
    detenciones = []
    numero = 0
    parada_realizada = False
    dias_restringidos = set()

    while reloj < FIN:
        # Parada anual: comienza al terminar el lote en curso
        if not parada_realizada and reloj >= INICIO_PARADA:
            reloj = reloj + timedelta(days=DIAS_PARADA)
            parada_realizada = True

        # Episodio crítico (D08): una restricción por reactor en cada día de episodio
        dia = reloj.date()
        if dia in dias_episodio and dia not in dias_restringidos:
            minutos = int(rng.integers(MINUTOS_D08[0], MINUTOS_D08[1] + 1))
            reloj = registrar(detenciones, reactor, "D08", reloj, minutos)
            dias_restringidos.add(dia)

        # Reacción del lote: duración ideal + variación normal + posible R04
        minutos_reaccion = HORAS_REACCION * 60 + int(rng.integers(VARIACION_REACCION[0], VARIACION_REACCION[1] + 1))
        r04 = rng.random() < PROB_R04
        if r04:
            minutos_reaccion = minutos_reaccion + int(rng.integers(MINUTOS_R04[0], MINUTOS_R04[1] + 1))

        numero = numero + 1
        inicio = reloj
        reloj = reloj + timedelta(minutes=minutos_reaccion)

        # Calidad del lote: rechazo completo (C01) o pérdida parcial en el tamizado (C03)
        if rng.random() < PROB_C01:
            toneladas_buenas = 0.0
            causa_calidad = "C01"
        else:
            perdida = rng.uniform(PERDIDA_C03[0], PERDIDA_C03[1])
            toneladas_buenas = round(TONELADAS_POR_LOTE * (1 - perdida), 2)
            if perdida > 0.01:
                causa_calidad = "C03"
            else:
                causa_calidad = ""

        lotes.append({"reactor": reactor, "lote": numero, "inicio": inicio, "fin": reloj,
                      "horas_reaccion": round(minutos_reaccion / 60, 2), "r04": r04,
                      "toneladas": TONELADAS_POR_LOTE, "toneladas_buenas": toneladas_buenas,
                      "causa_calidad": causa_calidad})

        # Detenciones sin estacionalidad (D01, D02, D03)
        for causa, (probabilidad, minimo, maximo) in DETENCIONES.items():
            if rng.random() < probabilidad:
                minutos = int(rng.integers(minimo, maximo + 1))
                reloj = registrar(detenciones, reactor, causa, reloj, minutos)

        # Falta de materia prima (D04): depende de la estación
        if reloj.month in MESES_INVIERNO:
            probabilidad_d04 = PROB_D04_INVIERNO
        else:
            probabilidad_d04 = PROB_D04_RESTO
        if rng.random() < probabilidad_d04:
            minutos = int(rng.integers(MINUTOS_D04[0], MINUTOS_D04[1] + 1))
            reloj = registrar(detenciones, reactor, "D04", reloj, minutos)

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
df_lotes["fecha"] = df_lotes["fin"].dt.date

# ===== Guardar =====
df_lotes.to_csv("data/lotes_L1_2026.csv", index=False)
df_det.to_csv("data/detenciones_L1_2026.csv", index=False)

# ===== Validación del modelo: OEE =====
horas_parada = DIAS_PARADA * 24
horas_planificadas = ((FIN - INICIO).total_seconds() / 3600 - horas_parada) * len(REACTORES)
horas_detenidas = df_det["minutos"].sum() / 60
horas_operativas = horas_planificadas - horas_detenidas
velocidad_ideal = TONELADAS_POR_LOTE / HORAS_REACCION   # t/h por reactor

toneladas = df_lotes["toneladas"].sum()
toneladas_buenas = df_lotes["toneladas_buenas"].sum()

disponibilidad = horas_operativas / horas_planificadas
rendimiento = toneladas / (velocidad_ideal * horas_operativas)
calidad = toneladas_buenas / toneladas
oee = disponibilidad * rendimiento * calidad
verificacion = toneladas_buenas / (velocidad_ideal * horas_planificadas)

print("Lotes completados:", len(df_lotes), "| Toneladas producidas:", round(toneladas), "| Toneladas buenas:", round(toneladas_buenas))
print("Disponibilidad:", round(disponibilidad * 100, 1), "%")
print("Rendimiento:   ", round(rendimiento * 100, 1), "%")
print("Calidad:       ", round(calidad * 100, 1), "%")
print("OEE:           ", round(oee * 100, 1), "%  | Verificación:", round(verificacion * 100, 1), "%")
print("--- Horas detenidas por causa ---")
print((df_det.groupby("causa")["minutos"].sum() / 60).round(1))