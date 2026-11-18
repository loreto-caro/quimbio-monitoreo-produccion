from datetime import datetime, timedelta
import numpy as np

rng = np.random.default_rng(42)

inicio_simulacion = datetime(2026, 1, 1, 8, 0)
fin_simulacion = inicio_simulacion + timedelta(days=1)

reloj = inicio_simulacion
numero_lote = 0

while reloj < fin_simulacion:
    # Etapa 1: reacción del lote
    numero_lote = numero_lote + 1
    inicio_lote = reloj
    reloj = reloj + timedelta(hours=7)
    print("Lote", numero_lote, ":", inicio_lote.strftime("%d/%m %H:%M"), "→", reloj.strftime("%d/%m %H:%M"))

    # Etapa 2: limpieza entre lotes (D01)
    minutos_limpieza = int(rng.integers(50, 121))
    reloj = reloj + timedelta(minutes=minutos_limpieza)
    print("   Limpieza D01:", minutos_limpieza, "min")

print("Lotes iniciados en 24 horas:", numero_lote)