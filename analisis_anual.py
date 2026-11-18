import pandas as pd

# Leer los datos guardados
df = pd.read_csv("detenciones_L1_2026.csv")
print("Registros cargados:", len(df))

# Disponibilidad del año
horas_planificadas = 8424  # ficha, sección 5
horas_detenidas = df["minutos"].sum() / 60
disponibilidad = (horas_planificadas - horas_detenidas) / horas_planificadas * 100

print("Horas detenidas en 2026:", round(horas_detenidas, 1))
print("Disponibilidad L1 2026:", round(disponibilidad, 1), "%  (meta: 80%)")

# Pareto anual de causas
pareto = df.groupby("causa")["minutos"].sum().sort_values(ascending=False).to_frame()
pareto["horas"] = (pareto["minutos"] / 60).round(1)
pareto["porcentaje"] = (pareto["minutos"] / pareto["minutos"].sum() * 100).round(1)
pareto["acumulado"] = pareto["porcentaje"].cumsum().round(1)

print("--- Pareto anual de detenciones L1 ---")
print(pareto)