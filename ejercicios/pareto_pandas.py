import pandas as pd

# La misma tabla de detenciones de la Línea 1
detenciones = [
    {"turno": "Día",   "maquina": "QBM-L1-R01",   "causa": "D01", "minutos": 60},
    {"turno": "Día",   "maquina": "QBM-L1-SEC01", "causa": "D03", "minutos": 45},
    {"turno": "Noche", "maquina": "QBM-L1-R02",   "causa": "D01", "minutos": 180},
    {"turno": "Noche", "maquina": "QBM-L1-R01",   "causa": "D02", "minutos": 30},
    {"turno": "Día",   "maquina": "QBM-L1-R02",   "causa": "D01", "minutos": 90},
    {"turno": "Noche", "maquina": "QBM-L1-R01",   "causa": "D04", "minutos": 75},
]

# Convertir la lista en una tabla de pandas
df = pd.DataFrame(detenciones)
print(df)

# Sumar minutos por causa y ordenar de mayor a menor
por_causa = df.groupby("causa")["minutos"].sum().sort_values(ascending=False)
print("--- Minutos por causa ---")
print(por_causa)

# Pareto completo: porcentaje y acumulado
pareto = por_causa.to_frame()
pareto["porcentaje"] = (pareto["minutos"] / pareto["minutos"].sum() * 100).round(1)
pareto["acumulado"] = pareto["porcentaje"].cumsum().round(1)

print("--- Pareto de detenciones L1 ---")
print(pareto)