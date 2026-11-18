import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 1000  # cantidad de detenciones a inventar

# Cada columna se genera con sus propias reglas
fechas = pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 365, size=n), unit="D")
turnos = rng.choice(["Día", "Noche"], size=n)
maquinas = rng.choice(
    ["QBM-L1-R01", "QBM-L1-R02", "QBM-L1-SEC01", "QBM-L1-MOL01", "QBM-L1-ENV01"],
    size=n,
    p=[0.30, 0.30, 0.15, 0.15, 0.10],
)
causas = rng.choice(["D01", "D02", "D03", "D04"], size=n, p=[0.50, 0.20, 0.20, 0.10])
minutos = rng.integers(15, 181, size=n)

# Armar la tabla, ordenarla por fecha y guardarla
df = pd.DataFrame({
    "fecha": fechas,
    "turno": turnos,
    "maquina": maquinas,
    "causa": causas,
    "minutos": minutos,
})
df = df.sort_values("fecha")
df.to_csv("detenciones_L1_2026.csv", index=False)

print(df.head(10))
print("Total de registros:", len(df))
print("Archivo guardado: detenciones_L1_2026.csv")