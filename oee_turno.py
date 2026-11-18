# ===== OEE de un turno - Línea 1 (QuimBío Minería) =====

# Datos del turno día
tiempo_planificado = 720    # minutos (12 horas)
detencion_d01 = 180          # minutos: limpieza entre lotes
detencion_d03 = 45          # minutos: falla mecánica
produccion_real = 20.0      # toneladas producidas
rechazo = 2.0               # toneladas rechazadas (C01)
velocidad_ideal = 2.286     # t/h del cuello de botella (reactores)

# Cálculos intermedios
tiempo_operativo = tiempo_planificado - detencion_d01 - detencion_d03
horas_operativas = tiempo_operativo / 60
toneladas_buenas = produccion_real - rechazo

# Los 3 factores del OEE
disponibilidad = tiempo_operativo / tiempo_planificado
rendimiento = produccion_real / (velocidad_ideal * horas_operativas)
calidad = toneladas_buenas / produccion_real
oee = disponibilidad * rendimiento * calidad

# Mostrar resultados en porcentaje, con 1 decimal
print("Disponibilidad:", round(disponibilidad * 100, 1), "%")
print("Rendimiento:", round(rendimiento * 100, 1), "%")
print("Calidad:", round(calidad * 100, 1), "%")
print("OEE:", round(oee * 100, 1), "%")

# Metas de la Línea 1 (ficha, sección 7)
meta_oee = 62
alerta_oee = 50
oee_porcentaje = oee * 100

# Primero validar, después evaluar
if rendimiento > 1:
    print("⚠️ ERROR EN LOS DATOS: el rendimiento supera el 100%.")
    print("   Revisa la producción real o los minutos de detención.")
else:
    if oee_porcentaje >= meta_oee:
        print("🟢 L1 sobre la meta")
    elif oee_porcentaje >= alerta_oee:
        print("🟡 L1 en alerta")
    else:
        print("🔴 L1 crítica")