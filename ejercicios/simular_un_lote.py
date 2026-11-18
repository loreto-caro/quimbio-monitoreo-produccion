from datetime import datetime, timedelta
import numpy as np

rng = np.random.default_rng(42)

# El "reloj" de la simulación: 1 de enero de 2026 a las 08:00
reloj = datetime(2026, 1, 1, 8, 0)
print("Inicio de la simulación:", reloj)

# Etapa 1: reacción del lote (7 horas, según la ficha)
horas_reaccion = 7
inicio_lote = reloj
reloj = reloj + timedelta(hours=horas_reaccion)
print("Lote producido desde", inicio_lote, "hasta", reloj)

# Etapa 2: limpieza entre lotes (D01), entre 50 y 120 minutos
minutos_limpieza = int(rng.integers(50, 121))
inicio_limpieza = reloj
reloj = reloj + timedelta(minutes=minutos_limpieza)
print("Limpieza D01 desde", inicio_limpieza, "hasta", reloj, "-", minutos_limpieza, "min")

print("El siguiente lote puede comenzar:", reloj)