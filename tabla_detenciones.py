# Tabla de detenciones de la Línea 1: una lista de diccionarios
detenciones = [
    {"turno": "Día",   "maquina": "QBM-L1-R01",   "causa": "D01", "minutos": 60},
    {"turno": "Día",   "maquina": "QBM-L1-SEC01", "causa": "D03", "minutos": 45},
    {"turno": "Noche", "maquina": "QBM-L1-R02",   "causa": "D01", "minutos": 180},
    {"turno": "Noche", "maquina": "QBM-L1-R01",   "causa": "D02", "minutos": 30},
    {"turno": "Día",   "maquina": "QBM-L1-R02",   "causa": "D01", "minutos": 90},
    {"turno": "Noche", "maquina": "QBM-L1-R01",   "causa": "D04", "minutos": 75},
]

print("--- Detenciones de la Línea 1 ---")
for registro in detenciones:
    print(registro["turno"], "|", registro["maquina"], "|", registro["causa"], "|", registro["minutos"], "min")

# Sumar minutos por causa (como una tabla dinámica)
minutos_por_causa = {}

for registro in detenciones:
    causa = registro["causa"]
    minutos = registro["minutos"]
    if causa in minutos_por_causa:
        minutos_por_causa[causa] = minutos_por_causa[causa] + minutos
    else:
        minutos_por_causa[causa] = minutos

print("--- Minutos por causa ---")
for causa in minutos_por_causa:
    print(causa, ":", minutos_por_causa[causa], "min")

# Pareto: ordenar de mayor a menor y calcular porcentajes
total = sum(minutos_por_causa.values())
causas_ordenadas = sorted(minutos_por_causa, key=minutos_por_causa.get, reverse=True)

acumulado = 0
print("--- Pareto de detenciones L1 ---")
for causa in causas_ordenadas:
    minutos = minutos_por_causa[causa]
    porcentaje = minutos / total * 100
    acumulado = acumulado + porcentaje
    print(causa, "|", minutos, "min |", round(porcentaje, 1), "% | acumulado:", round(acumulado, 1), "%")