nombre = "Loreto"
proyecto = "Sistema de Monitoreo y Control"

meta = 100
produccion = 120

print("Hola", nombre)
print("Hoy comienza:", proyecto)
print("¿Se cumplió la meta?", produccion >= meta)
meta = 100
produccion = 85
if produccion >= meta:
    print("🟢 Meta cumplida")
elif produccion >= 80:
    print("🟡 Alerta: cerca de la meta")
else:
    print("🔴 Bajo la meta")