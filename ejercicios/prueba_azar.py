import numpy as np

# Generador de números aleatorios con "semilla" 42
rng = np.random.default_rng(42)

causas = ["D01", "D02", "D03", "D04"]

print("Una causa al azar:", rng.choice(causas))
print("10 causas, todas igual de probables:", rng.choice(causas, size=10))
print("10 causas, con D01 más probable:", rng.choice(causas, size=10, p=[0.6, 0.15, 0.15, 0.10]))
print("5 duraciones entre 30 y 180 minutos:", rng.integers(30, 181, size=5))