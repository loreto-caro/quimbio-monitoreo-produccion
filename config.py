"""
Parámetros de la planta y metas de gestión de la Línea 1 de QuimBío Minería.

Es la única fuente de estos valores: el simulador y el dashboard los importan desde aquí.
Fuente: docs/ficha_empresa.md (secciones 4, 5 y 7).
"""
from datetime import datetime

# ===== Período de análisis =====
INICIO = datetime(2026, 1, 1, 0, 0)
FIN = datetime(2027, 1, 1, 0, 0)

# ===== Línea 1: cuello de botella (reactores de polimerización) =====
REACTORES = ["QBM-L1-R01", "QBM-L1-R02"]
HORAS_REACCION = 7                                       # duración ideal de un lote
TONELADAS_POR_LOTE = 8
VELOCIDAD_IDEAL = TONELADAS_POR_LOTE / HORAS_REACCION    # t/h por reactor

# ===== Parada anual programada (mantención mayor de verano) =====
INICIO_PARADA = datetime(2026, 2, 1, 8, 0)
DIAS_PARADA = 14

# ===== Horas-reactor planificadas del período =====
HORAS_PERIODO = (FIN - INICIO).total_seconds() / 3600
HORAS_PLANIFICADAS = (HORAS_PERIODO - DIAS_PARADA * 24) * len(REACTORES)

# ===== Metas de gestión (ficha, sección 7) =====
META = {"OEE": 62, "Disponibilidad": 80, "Rendimiento": 85, "Calidad": 92}
ALERTA_OEE = 50