import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 1000

reactores = ["QBM-L1-R01", "QBM-L1-R02"]
todas = reactores + ["QBM-L1-SEC01", "QBM-L1-MOL01", "QBM-L1-ENV01"]

# Reglas de cada causa (ficha, sección 6)
reglas = {
    "D01": {"maquinas": reactores, "min": 60, "max": 180},   # limpieza entre lotes
    "D02": {"maquinas": reactores, "min": 30, "max": 120},   # espera de laboratorio
    "D03": {"maquinas": todas,     "min": 20, "max": 240},   # falla mecánica
    "D04": {"maquinas": reactores, "min": 30, "max": 150},   # falta de materia prima
}
probabilidades = {"D01": 0.40, "D02": 0.20, "D03": 0.25, "D04": 0.15}

# Crear las detenciones una por una
registros = []
for i in range(n):
    causa = rng.choice(list(probabilidades.keys()), p=list(probabilidades.values()))
    regla = reglas[causa]
    registro = {
        "fecha": pd.Timestamp("2026-01-01") + pd.Timedelta(days=int(rng.integers(0, 365))),
        "turno": rng.choice(["Día", "Noche"]),
        "maquina": rng.choice(regla["maquinas"]),
        "causa": causa,
        "minutos": int(rng.integers(regla["min"], regla["max"] + 1)),
    }
    registros.append(registro)

# Armar la tabla y guardarla (reemplaza la versión 1)
df = pd.DataFrame(registros).sort_values("fecha")
df.to_csv("detenciones_L1_2026.csv", index=False)

print(df.head(10))
print("Total de registros:", len(df))
print("Archivo actualizado: detenciones_L1_2026.csv (versión 2)")