# Minutos de detención registrados en 6 turnos de la Línea 1
detenciones = [60, 45, 180, 30, 90, 75]

print("Detenciones:", detenciones)
print("Cantidad de registros:", len(detenciones))
print("Total de minutos:", sum(detenciones))
print("Detención más larga:", max(detenciones))
print("Primer registro:", detenciones[0])

print("--- Revisión turno por turno ---")
for minutos in detenciones:
    if minutos > 60:
        print(minutos, "min → ⚠️ detención larga")
    else:
        print(minutos, "min → normal")

# Resumen de detenciones largas
cantidad_largas = 0
minutos_largos = 0

for minutos in detenciones:
    if minutos > 60:
        cantidad_largas = cantidad_largas + 1
        minutos_largos = minutos_largos + minutos

print("--- Resumen ---")
print("Detenciones largas:", cantidad_largas, "de", len(detenciones))
print("Minutos perdidos en ellas:", minutos_largos, "de", sum(detenciones))
porcentaje = minutos_largos / sum(detenciones) * 100
print("Porcentaje del tiempo perdido:", round(porcentaje, 1), "%")